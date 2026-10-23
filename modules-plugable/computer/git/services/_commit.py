#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""computer/git/services/_commit.py — `commit`: commit the named paths alone, in a tree other tasks share.

The tree is built in a private index, the commit object written with `hash-object`, the branch moved
with `update-ref` against the commit expected, and the shared index updated for the committed paths
in one write. Hooks do not run.
"""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from . import _tasks as git_tasks
from ._index import PrivateIndex, index_entries, index_from, index_input, tree_entry
from ._lock import LOCK_NOTE, lock_deadline, locks_free, once, patiently, shared_locks, stopped
from ._run import in_repo, plumb, repository_flag, repository_root
from ._staged import refuse_staged, renames_lost, staged_moves, upstream_holding

def cmd_commit(repository: Path, paths: list[Path], prepared: list[str], leave_out: list[Path], fold: int, message_file: Path, *, tasks: list[str], no_task: bool) -> None:
    """Commit the named paths alone, without the shared index and without porcelain, citing TASKS (`git_tasks`)."""
    root = repository_root(repository)
    if fold < 0:
        sys.exit('error: --fold counts commits and cannot be negative')
    if not paths and (not prepared) and (not fold):
        sys.exit('error: name a path, an --as, or a --fold; there is nothing to commit')
    if leave_out and (not fold):
        sys.exit('error: --leave-out only means something inside a --fold')
    head = plumb(['rev-parse', 'HEAD'], root)
    parent = plumb(['rev-parse', f'HEAD~{fold}'], root) if fold else head
    if fold:
        if plumb(['rev-list', '--min-parents=2', f'{parent}..{head}'], root):
            sys.exit(f'error: the last {fold} commits include a merge; this does not fold merges')
        oldest = plumb(['rev-parse', f'HEAD~{fold - 1}'], root)
        upstream = upstream_holding(oldest, root)
        if upstream:
            sys.exit(f'error: {oldest[:12]} is already on {upstream[:12]} upstream; folding it would rewrite published history')
    message = message_file.read_bytes().decode('utf-8').replace('\r\n', '\n').strip()
    if not message:
        sys.exit(f'error: {message_file} is empty; a commit needs a message')
    cited = git_tasks.checked(message, tasks, no_task, parent, head, root)
    named: dict[str, Path | None] = {in_repo(p, root): None for p in paths}
    for pair in prepared:
        target, separator, source = pair.partition('=')
        if not separator or not target or (not source):
            sys.exit(f'error: --as takes PATH=FILE, not {pair!r}')
        source_path = Path(source).expanduser().resolve()
        if not source_path.is_file():
            sys.exit(f'error: --as source is not a file: {source}')
        named[in_repo(Path(target), root)] = source_path
    left = [in_repo(p, root) for p in leave_out]
    prepared_for = {path: source for path, source in named.items() if source is not None}
    moved = staged_moves(list(named), root, prepared=prepared_for)
    refuse_staged([path for path in [*named, *left] if path not in moved], root, 'Nothing was committed.')
    with PrivateIndex(root) as private:
        plumb(['read-tree', head], root, env=private)
        if left:
            plumb(['update-index', '-z', '--index-info'], root, env=private, data=index_input(parent, left, root, private))
        for path, source in named.items():
            if source is not None:
                sha = plumb(['hash-object', '-w', '--path', path, str(source)], root)
                entry = index_entries([path], root)[path] if path in moved else tree_entry(head, path, root)
                mode = entry.split()[0] if entry else '100644'
                plumb(['update-index', '--add', '--cacheinfo', f'{mode},{sha},{path}'], root, env=private)
            elif (root / path).exists():
                plumb(['add', '--', path], root, env=private)
            else:
                plumb(['update-index', '--force-remove', '--', path], root, env=private)
        tree = plumb(['write-tree'], root, env=private)
    if tree == plumb(['rev-parse', f'{parent}^{{tree}}'], root):
        sys.exit('error: the result is the tree the parent already has; nothing to commit')
    lost = renames_lost(moved, parent, tree, root)
    if lost:
        sys.exit("error: with the working tree's edit in it, git no longer sees " + ', '.join(lost) + " as a rename, so its history would not follow. An edit rides with a move only while the file stays above git's rename threshold; this one pushes it below, so the move keeps a commit of its own: commit the move alone with --as DESTINATION=FILE holding the blob the move staged, and fold the edit into the task's commit after it. Nothing was committed.")
    message = git_tasks.with_trailers(message, cited, root)
    body = f"tree {tree}\nparent {parent}\nauthor {plumb(['var', 'GIT_AUTHOR_IDENT'], root)}\ncommitter {plumb(['var', 'GIT_COMMITTER_IDENT'], root)}\n\n{message}\n"
    made = plumb(['hash-object', '-t', 'commit', '-w', '--stdin'], root, data=body.encode('utf-8'))
    unmoved = f'the commit object {made} was written, but HEAD was not moved: it is still {head}, and the shared index and the working tree are as they were (git gc drops the unreferenced object).'
    deadline = lock_deadline()
    lock = locks_free(shared_locks(root), 'moving HEAD', deadline)
    if lock is not None:
        stopped(unmoved, f'Nothing to undo. {once(lock).capitalize()}, rerun the same command.', lock=lock)
    moved, lock = patiently(['update-ref', '-m', f'modules-plugable/computer/git/services/_host_git_cli.py commit (fold {fold})', 'HEAD', made, head], root, deadline)
    if moved.returncode != 0:
        stopped(unmoved, f'Nothing to undo. {once(lock).capitalize()}, rerun the same command.', moved, lock)
    index_from(made, head, [*named, *left], root, f'HEAD moved from {head} to the commit {made}', deadline)
    print(made)
    print(plumb(['diff', '--stat', parent, made], root), file=sys.stderr)
    replaced = f'; it replaces {fold} commit(s), recoverable from git reflog as {head[:12]}' if fold else ''
    print(f'committed {made[:12]} on {parent[:12]}{replaced}.\nThe shared index was updated for the committed paths only; whatever else was staged is still staged.', file=sys.stderr)

def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_commit = sub.add_parser('commit', help="commit only the named paths; the shared index keeps others' staging", description=f'Commit only the paths you name, as they are in the working tree, for a\nworking tree other tasks share: plain `git commit` takes everything\nstaged, theirs included, and so does any rewrite of it your runtime makes.\nThe commits a --fold replaces stay reachable through `git reflog`.\n\nEvery commit names the tasks it carries out, each with --task-id, or\nsays with --no-task that it carries out none; one that does neither is\nrefused. The ids are read back with\n`git log --format=%(trailers:key={git_tasks.TRAILER},valueonly)`.\n\n{LOCK_NOTE}', formatter_class=argparse.RawDescriptionHelpFormatter)
    repository_flag(p_commit)
    p_commit.add_argument('paths', nargs='*', type=Path, help='paths to commit as they are in the working tree, relative to the repository or absolute')
    p_commit.add_argument('-F', '--message-file', required=True, type=Path, help='the commit message, read from a file (write it with a file tool)')
    p_commit.add_argument('--as', dest='prepared', action='append', default=[], metavar='PATH=FILE', help="commit FILE's content as PATH: your hunk in a file others also edit, or a staged move's destination as the move staged it once the file has been edited")
    p_commit.add_argument('--fold', type=int, default=0, metavar='N', help='replace the last N unpushed commits with this one')
    p_commit.add_argument('--leave-out', action='append', default=[], type=Path, metavar='PATH', help='inside a --fold, keep PATH as the new parent has it; its change stays unstaged')
    p_commit.add_argument(git_tasks.TASK_FLAG, dest='tasks', action='append', default=[], metavar='ID', help=f"a task this commit carries out, by its id; once for each. Each is looked up as `memar git show-task-records` looks it up, in its folder and then on the project's records branch, and refused when neither holds it; each is written into the message as a `{git_tasks.TRAILER}: ID` trailer, after those of the commits a --fold replaces, which are kept. The message itself names no task")
    p_commit.add_argument(git_tasks.NO_TASK_FLAG, action='store_true', help=f'this commit carries out no task: the task opened none, as committing, staging, a rename, or one edit done in place. Without it, a commit that cites no task is refused; never with {git_tasks.TASK_FLAG}')
    p_commit.set_defaults(run=lambda a: cmd_commit(a.repository, a.paths, a.prepared, a.leave_out, a.fold, a.message_file, tasks=a.tasks, no_task=a.no_task))

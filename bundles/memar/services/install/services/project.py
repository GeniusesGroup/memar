#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/install/services/project.py — the project layer of `memar install`: Memar put into a project as https://agents.md/ instructions.

Named for the surface it writes into, the project, rather than for the agents
file it writes there: the other two layers of `memar install` are named for
theirs, the machine and the agent apps.

Writes one thing for agents: the `## Memar` section of the project's AGENTS.md,
which says to load the Memar skill and where `memar` comes from when it is
missing. AGENTS.md is sent with every prompt, so the section is the whole of
what a task needs before the skill and points at no file in between: a file
that only names the next file costs every task a tool call and says nothing.
The Memar repository's section names its own skill file, which it holds.

An install of an earlier Memar wrote `.agents/memar/README.md` as that file in
between; an install moves it to the trash, since nothing but an install wrote it. It
writes no preferences file: what a project says to Memar's tools is a `memar:`
block in the project's own manifest, which no agent reads and no install writes
(`project_preferences`). A `.agents/memar/preferences.md` left by an earlier
install is not read any more, and an install says so and leaves it.

Every module has a `temp` folder for what the work makes and no record needs
(`modules-plugable/computer/filesystem/services/fs_memar.py`'s `TEMP_FOLDER`), every task included, so a project under
git is given a `.gitignore` line that ignores a folder of that name at any
depth, added once when no line there already does, with the file's own lines
and line endings kept.

Installing is declaring that the project follows Memar, so the registry
(`project_registry`) learns it in the same run, under the project's folder
name, which a person changes later with `memar project add --alias`. A project
already registered, under any name, is left as it is: that is not an error, and
it is not given a second name. A name another project holds is reported with
the holder, and nothing is renamed, neither the holder nor this project; the
install goes on, and `memar project add NAME PATH` registers it under a name
that is free. A dry run says what it would register and writes no registry.

It places no script and no Python file in the project: the bootstrap for the
machine is fetched from the Memar repository at the point of use, and a copy per
repository is unmaintainable — every change here would have to be re-copied into
every project by hand.

Where Memar lives on this machine is one thing, and this file asks rather than
decides: `machine/env_location.py` is the one module that reads the location
variable, and `modules-plugable/computer/filesystem/services/fs_memar_repository.py` holds the test of what a Memar
repository is — which is what gives the Memar repository the section that names
its own skill rather than the one written for a project that has to fetch Memar first.

It writes into the project it is told, never the one the process happens to be
in: the folder is given (`memar install --project-path PATH`, or `--project NAME`), and a subfolder
of a project is fine — this walks up to the version-control root. Given none,
it writes nothing and says how to name one. It never installs anything
else: the machine is settled before this runs, and the section it writes says
where to read what to run when it is not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
PUBLISH_BRANCH = _m_fs_memar.PUBLISH_BRANCH
PUBLISHED_REPOSITORY = _m_fs_memar.PUBLISHED_REPOSITORY
SCRIPTS_RELATIVE = _m_fs_memar.SCRIPTS_RELATIVE
LAUNCHER_RELATIVE = _m_fs_memar.LAUNCHER_RELATIVE
SKILL_RELATIVE = _m_fs_memar.SKILL_RELATIVE
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
_m_fs_memar_repository = import_module('modules-plugable.computer.filesystem.services.fs_memar_repository')
is_memar_repository = _m_fs_memar_repository.is_memar_repository
_m_fs_trash = import_module('modules-plugable.computer.filesystem.services.fs_trash')
soft_delete = _m_fs_trash.soft_delete
import contextlib
import re
import sys
from pathlib import Path
from machine.env_location import VARIABLE, recorded_value
from modules.process.project.services.preferences import BLOCK_KEY, PREFERENCES_RELATIVE
from modules.process.project.services.registry import add_project, ensure_memar_entry, normalized, path_key, read_entries
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath
SCRIPTS_RAW = f'https://raw.githubusercontent.com/{PUBLISHED_REPOSITORY}/{PUBLISH_BRANCH}/{SCRIPTS_RELATIVE.as_posix()}'
WINDOWS_BOOTSTRAP = f'powershell -ExecutionPolicy Bypass -Command "& ([scriptblock]::Create((irm {SCRIPTS_RAW}/install.ps1)))"'
POSIX_BOOTSTRAP = f"""sh -c 'c=$(curl -fsSL {SCRIPTS_RAW}/install.sh); test -n "$c" && exec sh -c "$c" install.sh'"""
INSTALL_BOOTSTRAP = f'`{SCRIPTS_RELATIVE.as_posix()}/install.sh` or `{SCRIPTS_RELATIVE.as_posix()}/install.ps1` ({SCRIPTS_RAW}/)'
OBSOLETE_README = Path('.agents') / 'memar' / 'README.md'
OBSOLETE_PREFERENCES = OBSOLETE_README.with_name('preferences.md')
MEMAR_HEADING = '## Memar'
AGENTS_H1 = '# Repository instructions'
AGENTS_SECTION_BODY = f'Before any other work in a task, load and follow the Memar skill: `memar content resolve-path {SKILL_RELATIVE.as_posix()}/SKILL.md` prints its file. Where `memar` is not on PATH, install Memar with {INSTALL_BOOTSTRAP}, or run `memar install --help`.'
MEMAR_SECTION_BODY = f'Before any other work in a task, load and follow [`{SKILL_RELATIVE.as_posix()}/SKILL.md`]({SKILL_RELATIVE.as_posix()}/SKILL.md).'
HEADING_RE = re.compile('(?m)^## Memar[ \\t]*$')
NEXT_HEADING_RE = re.compile('(?m)^#{1,2}[ \\t]+\\S')
GITIGNORE = '.gitignore'
TEMP_IGNORE_LINE = f'{TEMP_FOLDER}/'
TEMP_IGNORED_BY = {TEMP_FOLDER, TEMP_IGNORE_LINE, f'**/{TEMP_FOLDER}', f'**/{TEMP_IGNORE_LINE}'}
VCS_MARKERS = ('.git', '.hg', '.svn', '.fossil', '.bzr', '_darcs', '.pijul')

def _has_vcs_marker(path: Path) -> bool:
    return any(((path / name).exists() for name in VCS_MARKERS))

def _vcs_root(start: Path) -> Path | None:
    for candidate in [start, *start.parents]:
        if _has_vcs_marker(candidate):
            return candidate
    return None

def resolve_project_dir(given: Path) -> Path:
    given = given.resolve()
    if given == Path.home().resolve() or given.parent == given:
        sys.exit(f'error: {given} is not a project directory; name the version-controlled project you want Memar in')
    root = _vcs_root(given)
    if root is not None:
        if root != given:
            print(f'using repository root {root}', file=sys.stderr)
        return root
    print(f'warning: no VCS metadata under {given}; installing into this directory', file=sys.stderr)
    return given

def memar_section_markdown(*, memar: bool=False) -> str:
    return f'{MEMAR_HEADING}\n{(MEMAR_SECTION_BODY if memar else AGENTS_SECTION_BODY)}\n'

def upsert_memar_section(content: str, *, memar: bool=False) -> str:
    section = memar_section_markdown(memar=memar)
    match = HEADING_RE.search(content)
    if match is None:
        stripped = content.rstrip()
        if stripped:
            return stripped + '\n\n' + section
        return f'{AGENTS_H1}\n\n{section}'
    start = match.start()
    rest = content[match.end():]
    next_heading = NEXT_HEADING_RE.search(rest)
    if next_heading is None:
        prefix = content[:start].rstrip()
        if prefix:
            return prefix + '\n\n' + section
        return section
    end = match.end() + next_heading.start()
    prefix = content[:start].rstrip()
    suffix = content[end:].lstrip('\n')
    middle = section
    if prefix:
        middle = prefix + '\n\n' + section
    if suffix:
        return middle.rstrip() + '\n\n' + suffix
    return middle

def write_text(path: Path, text: str, *, dry_run: bool) -> None:
    if not text.endswith('\n'):
        text += '\n'
    if dry_run:
        print(f'dry-run: write {path}')
        print(text, end='' if text.endswith('\n') else '\n')
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')
    print(f'wrote {path}')

def ignore_temp(target: Path, *, dry_run: bool=False) -> None:
    """Add TEMP_IGNORE_LINE to TARGET's .gitignore unless a line there already ignores `temp` at every depth; only under git.

    TODO (owner, 2026-10-15): git only for now; a project under another VCS gets no ignore file written. Write that VCS's
    own ignore file (for example .hgignore) when a project of Memar's uses one. A `temp` folder's content must never reach
    version control, in the root or in any module.
    """
    if not (target / '.git').exists():
        return
    path = target / GITIGNORE
    text = ''
    if path.is_file():
        with open(path, encoding='utf-8', newline='') as file:
            text = file.read()
    if any((line.strip() in TEMP_IGNORED_BY for line in text.splitlines())):
        return
    ending = '\r\n' if '\r\n' in text else '\n'
    if text and (not text.endswith(('\n', '\r'))):
        text += ending
    write_text(path, text + TEMP_IGNORE_LINE + ending, dry_run=dry_run)

def register_project(target: Path, *, dry_run: bool=False) -> None:
    """Make Memar know TARGET, the project root, under its folder name; see the module docstring for the cases."""
    name = target.name
    if dry_run:
        print(f'dry-run: register the project {name} at {target}')
        return
    ensure_memar_entry()
    entries = read_entries()
    mine = path_key(target)
    for entry in entries:
        if path_key(entry.path) == mine:
            print(f'the project is already registered as {entry.names[0]}; `memar project add --alias` gives it another name')
            return
    for entry in entries:
        if normalized(name) in {normalized(each) for each in entry.names}:
            print(f'the project was not registered: the name {name} is already the project {entry.names[0]} at {entry.path}; register it under a free name with `memar project add NAME {target}`', file=sys.stderr)
            return
    try:
        add_project(name, target)
    except SystemExit as refused:
        print(f'the project was not registered: {refused.code}', file=sys.stderr)
        return
    print(f'registered the project {name} at {target}; `memar project add --alias` gives it another name')

def remove_obsolete(target: Path, *, dry_run: bool=False) -> None:
    """Remove the README an earlier install wrote into TARGET, and name the preferences file it no longer reads."""
    readme = target / OBSOLETE_README
    if readme.is_file():
        if dry_run:
            print(f'dry-run: remove {readme}')
        else:
            soft_delete(readme)
            print(f'moved {readme} to the trash: AGENTS.md now says what it said')
            with contextlib.suppress(OSError):
                readme.parent.rmdir()
    preferences = target / OBSOLETE_PREFERENCES
    if preferences.is_file():
        print(f'{preferences} is not read any more: write what its front matter sets as a `{BLOCK_KEY}:` block in {target / PREFERENCES_RELATIVE}, and anything written for agents in AGENTS.md, then delete it', file=sys.stderr)

def into_project(project: Path | None=None, *, dry_run: bool=False) -> None:
    """Put Memar into PROJECT, a folder the caller named; the folder the process is in is never read."""
    if project is None:
        print(f'no project was named, so Memar was not put into one; run `memar install {ProjectName.FLAG} {ProjectName.METAVAR}` or `memar install {ProjectPath.FLAG} {ProjectPath.METAVAR}` to name it', file=sys.stderr)
        return
    target = resolve_project_dir(project)
    agents = target / 'AGENTS.md'
    memar = is_memar_repository(target)
    if agents.is_file():
        updated = upsert_memar_section(agents.read_text(encoding='utf-8'), memar=memar)
    else:
        updated = upsert_memar_section('', memar=memar)
    write_text(agents, updated, dry_run=dry_run)
    remove_obsolete(target, dry_run=dry_run)
    ignore_temp(target, dry_run=dry_run)
    register_project(target, dry_run=dry_run)
    if not dry_run:
        recorded = recorded_value()
        if not recorded:
            print(f'{VARIABLE} is not set, so Memar is not on this machine yet; the bootstrap this project now points at installs it', file=sys.stderr)
        else:
            print(f'{VARIABLE} is set to {recorded}')

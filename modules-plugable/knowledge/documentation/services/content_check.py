#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/documentation/services/content_check.py — `memar content check`: what is wrong with a text file, reported before it is inherited.

Two sets of rules, separated by what they hold for. The encoding and newline
rules hold for every text file in every project, because a shell damages a file
the same way whatever the file is for. Memar's written-surface rules — no blank
line under a heading, no run of blank lines, a link that resolves to a file and
a heading — are Memar's own conventions and apply only inside a Memar
repository, which is asked of `modules-plugable/computer/filesystem/services/fs_memar_repository.py` rather than
assumed.

Given a folder it also prints the undischarged propagations its ledgers hold,
apart from the problems and not counted among them: a `Pending` entry is the
correct content of the changelog that holds it, and a gate that is always red
is not a gate. A link that points up the layers of the written content is a
warning for the same kind of reason: it is a debt, repaid when its text is
upgraded, and never a defect a link is deleted to clear.

The bytes of a file are judged in `modules/knowledge/text/services/text_check.py`,
the links and anchors of a Markdown document in `links` of the Markdown module, and
a normative-references list's entries in `normative_references_check`; this file
holds the Memar rules that remain, the folder walk, and the report: it composes the
domains' parts and decides none of them.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar_repository = plugable_load('computer.filesystem.services.fs_memar_repository')
enclosing_repository = _m_fs_memar_repository.enclosing_repository
import argparse
import re
from pathlib import Path
from modules.knowledge.text.services.corpus import is_generated
_m_links = import_module('modules-plugable.computer.codec.markdown.services.links')
anchor_problems = _m_links.anchor_problems
link_problems = _m_links.link_problems
upward_link_warnings = _m_links.upward_link_warnings
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
without_code = _m_markdown.without_code
_m_owed = import_module('modules-plugable.knowledge.documentation.services.owed')
owed_hints = _m_owed.owed_hints
_m_propagation = import_module('modules-plugable.knowledge.documentation.services.propagation')
undischarged_propagations = _m_propagation.undischarged_propagations
_m_questions_lint = import_module('modules-plugable.knowledge.documentation.services.questions_lint')
entry_warnings = _m_questions_lint.entry_warnings
from modules.knowledge.content.services.reference import content_root
from modules.knowledge.text.services.file_text import plain_path
from modules.knowledge.text.services.text_check import file_problems
_m_normative_references_check = import_module('modules-plugable.knowledge.documentation.services.normative_references_check')
is_declared = _m_normative_references_check.is_declared
list_drops = _m_normative_references_check.list_drops
list_problems = _m_normative_references_check.list_problems
list_warnings = _m_normative_references_check.list_warnings
CHECKED_SUFFIXES = ('.md', '.kh', '.py', '.ts', '.json', '.yaml', '.yml', '.txt', '.ps1', '.sh', '.bat', '.cmd')
def describe(verbs):
    parser = verbs.add_parser('check', help='report encoding, newline, and written-surface problems in text files; a folder also reports undischarged propagations', description="Report what is wrong with text files: a UTF-8 BOM, invalid UTF-8, a U+FFFD replacement character, mixed or CRLF line endings, a missing final newline, and the fingerprints of mojibake; and for Markdown, two blank lines in a row, a blank line between a heading and its body, an anchor with no matching heading, a relative link, or a root-relative one (/docs/...) resolved as `memar content resolve-path` resolves it, whose file or heading does not exist; and for a normative-references list in modules/knowledge/content/rules/normative_references/, or in a folder the `normative_references` preference of the project it lies in names, a word that names no kind, an entry whose link names no Markdown file of the repository or is root-relative, a missing review mark or one that differs from its section's hash now, a drop that drops nothing or has no reason, and a project's drop of an every-act section, which is refused; the summary line counts the passages of Memar a project's lists drop. A relative link that points up the citation layers, an Open Questions entry missing a field, a file named like a list outside the declared places, and one passage twice in a list, are printed apart as warnings; given a folder it also reports undischarged propagations. Neither is counted as a problem.", formatter_class=argparse.HelpFormatter)
    parser.add_argument('files', nargs='+', help='files or folders (any path)')
    parser.add_argument('-v', '--verbose', action='store_true', help='also print clean files')
    parser.add_argument('--memar-rules', dest='memar_rules', action='store_true', default=None, help="apply Memar's Markdown conventions; the default asks whether the folder is a Memar repository")
    parser.add_argument('--no-memar-rules', dest='memar_rules', action='store_false', help='apply only the rules that hold for any text file')
    return run

def run(args: argparse.Namespace) -> None:
    cmd_check(args, content_root())

def check_file(path: Path, link_cache: dict | None=None, memar_rules: bool=True, *, root: Path) -> list[str]:
    """Report what is wrong with a text file. Empty list means clean.

    `root` is the checkout a root-relative link (`/docs/...`) resolves under,
    the one `memar content resolve-path` resolves against.

    `memar_rules` decides whether the Markdown rules are applied at all. They are
    Memar's own conventions — no blank line under a heading, linear load-bearing
    logic, a relative link that resolves — and a file in a project that has not
    adopted Memar is not a Memar document, so a missing blank line there is not a
    defect and reporting it tells the owner their repository is wrong for a
    reason they never agreed to. The encoding and newline rules are different:
    they hold for every text file in every project, because a shell damages a
    file the same way whatever the file is for. So the two sets are separated by
    a flag rather than by a list, and the caller decides by asking
    `modules-plugable/computer/filesystem/services/fs_memar_repository.py` whether the folder is a Memar repository.
    """
    cache: dict = {} if link_cache is None else link_cache
    problems, text = file_problems(path)
    if text is None:
        return problems
    if path.suffix == '.md' and memar_rules:
        if re.search('\\n\\s*\\n\\s*\\n', text):
            match = re.search('\\n\\s*\\n\\s*\\n', text)
            problems.append(f'line {text[:match.start()].count(chr(10)) + 1}: two or more blank lines in a row')
        blank_after = re.search('(?m)^#{1,6} .*\\n[ \\t]*\\n(?=[ \\t]*\\n|[ \\t]*\\S)', text)
        if blank_after:
            rest = text[blank_after.end():].lstrip('\n \t')
            if not rest.startswith('#'):
                problems.append(f'line {text[:blank_after.start()].count(chr(10)) + 1}: blank line between a heading and its body')
        visible = without_code(text)
        problems.extend(anchor_problems(visible, text))
        problems.extend(link_problems(path, visible, cache, root))
    if path.suffix == '.md':
        problems.extend(list_problems(path, root))
    return problems

def upward_warnings(path: Path, link_cache: dict | None=None) -> list[str]:
    """Every link in a Markdown document that points up the citation layers.

    A warning and not a problem (Documentation -> Citation Direction): an
    upward link is a debt, and a link is never deleted to comply.
    """
    if path.suffix != '.md':
        return []
    try:
        text = path.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return []
    cache: dict = {} if link_cache is None else link_cache
    return upward_link_warnings(path, without_code(text), cache)

def checkable_files(folder: Path) -> list[Path]:
    """Every checked file a walk of `folder` should look at.

    A walk is how the tool chooses for itself, so it chooses only what the
    project owns. An installed dependency tree is not this project's work, and a
    report that raises it on every run is a report about the tool, not the tree.
    """
    return [path for path in sorted(folder.rglob('*')) if path.is_file() and path.suffix in CHECKED_SUFFIXES and (not is_generated(path.relative_to(folder).parts[:-1]))]

def cmd_check(args: argparse.Namespace, root: Path) -> None:
    files: list[Path] = []
    directories: list[Path] = []
    for ref in args.files:
        resolved = plain_path(ref)
        if resolved.is_dir():
            directories.append(resolved)
            files.extend(checkable_files(resolved))
        else:
            files.append(resolved)
    total = 0
    link_cache: dict = {}
    memar_rules = args.memar_rules
    if memar_rules is None:
        memar_rules = enclosing_repository(directories[0] if directories else files[0]) is not None
    for path in files:
        problems = check_file(path, link_cache, memar_rules, root=root)
        total += len(problems)
        try:
            shown = path.relative_to(root)
        except ValueError:
            shown = path
        if not problems:
            if args.verbose:
                print(f'ok    {shown}')
        else:
            print(f'{shown}:')
            for problem in problems:
                print(f'  - {problem}')
    outstanding: list[tuple[Path, int, str]] = []
    if directories:
        outstanding = undischarged_propagations(files)
    if outstanding:
        print('\nundischarged propagations:')
        for _, _, report in outstanding:
            print(f'  - {report}')
    warnings: list[str] = []
    if memar_rules:
        for path in files:
            try:
                shown = path.relative_to(root)
            except ValueError:
                shown = path
            if path.name.endswith('.handoff.md'):
                warnings.extend((f"{shown}:{text.removeprefix('line ')}" for text in entry_warnings(path)))
            warnings.extend((f"{shown}:{text.removeprefix('line ')}" for text in upward_warnings(path, link_cache)))
            if path.suffix == '.md':
                warnings.extend((f'{shown}: {text}' for text in list_warnings(path, root)))
    else:
        for path in files:
            if path.suffix == '.md' and is_declared(path, root):
                warnings.extend((f'{path}: {text}' for text in list_warnings(path, root)))
    if warnings:
        print('\nwarnings (not counted as problems):')
        for warning in warnings:
            print(f'  - {warning}')
    if directories and memar_rules:
        hints = owed_hints(files)
        if hints:
            print('\nowed marks on one side only (hints, not counted as problems):')
            for hint in hints:
                print(f'  - {hint}')
    dropped = sum((list_drops(path, root) for path in files if path.suffix == '.md'))
    print(f"\nchecked {len(files)} file{('s' if len(files) != 1 else '')}, {total} problem{('s' if total != 1 else '')}" + (f", {len(outstanding)} undischarged propagation{('s' if len(outstanding) != 1 else '')}" if outstanding else '') + (f", {len(warnings)} warning{('s' if len(warnings) != 1 else '')}" if warnings else '') + (f", {dropped} passage{('s' if dropped != 1 else '')} of Memar dropped by this project's lists" if dropped else ''))
    if not memar_rules:
        print("not a Memar repository, so Memar's Markdown conventions were not applied: encoding, newlines, and decoding damage only")
    if total:
        raise SystemExit(1)

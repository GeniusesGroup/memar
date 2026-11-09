#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_repository = import_module('bundles.memar.services.location.repository')
enclosing_repository = _m_repository.enclosing_repository
import argparse
import re
from pathlib import Path
from modules.knowledge.text.services.corpus import is_generated
_m_links = import_module('modules-plugable.computer.codec.markdown.services.links')
anchor_problems = _m_links.anchor_problems
link_problems = _m_links.link_problems
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
without_code = _m_markdown.without_code
_m_owed = import_module('modules-plugable.knowledge.documentation.services.owed')
owed_hints = _m_owed.owed_hints
from modules.knowledge.content.services.reference import content_root
from modules.knowledge.text.services.file_text import plain_path
from modules.knowledge.text.services.text_check import file_problems
_m_normative_references_check = import_module('modules-plugable.knowledge.documentation.services.normative_references_check')
is_declared = _m_normative_references_check.is_declared
list_drops = _m_normative_references_check.list_drops
list_problems = _m_normative_references_check.list_problems
list_warnings = _m_normative_references_check.list_warnings
_m_temp_duplicate = import_module('modules-plugable.knowledge.documentation.services.temp_duplicate')
temp_duplicate_problems = _m_temp_duplicate.temp_duplicate_problems
open_questions_problems = import_module('modules-plugable.knowledge.documentation.services.open_questions').open_questions_problems
denial_findings = import_module('modules-plugable.knowledge.documentation.services.denial').denial_findings
restated_field_problems = import_module('modules-plugable.knowledge.documentation.services.restated_fields').restated_field_problems
foreign_domain_hints = import_module('modules-plugable.knowledge.documentation.services.foreign_domain').foreign_domain_hints
HINTS_KEY = 'document-hints'
CHECKED_SUFFIXES = ('.md', '.kh', '.py', '.ts', '.json', '.yaml', '.yml', '.txt', '.ps1', '.sh', '.bat', '.cmd')
def describe(verbs):
    parser = verbs.add_parser('check', help='report encoding, newline, and written-surface problems in text files', description="Report what is wrong with text files: a UTF-8 BOM, invalid UTF-8, a U+FFFD replacement character, mixed or CRLF line endings, a missing final newline, and the fingerprints of mojibake; and for Markdown, two blank lines in a row, a blank line between a heading and its body, a blank line after the closing front-matter fence, an anchor with no matching heading, a relative link, or a root-relative one (/docs/...) resolved as `memar content resolve-path` resolves it, whose file or heading does not exist, a section of Open, Unresolved or Review Questions or of questions for the owner, a heading or a sentence whose subject holds or knows nothing (the body states what a thing holds), and a table whose first column restates at least three names a `.kh` file of the document's own module declares; and for a normative-references list in modules/knowledge/content/rules/normative_references/, or in a folder the `normative_references` preference of the project it lies in names, a word that names no kind, an entry whose link names no Markdown file of the repository or is root-relative, a missing review mark or one that differs from its section's hash now, a drop that drops nothing or has no reason, and a project's drop of an every-act section, which is refused; the summary line counts the passages of Memar a project's lists drop. A file named like a list outside the declared places, and one passage twice in a list, are printed apart as warnings; a weaker denial (has no, is not a, owns no, carries no), any denial in a document under a rules folder, and a link to the main document or folder of a module the document's module does not import in its `.kh` files or whose imports cannot be read (not judged in bundles/ or under a widgets folder) are printed apart as hints; None of these is counted as a problem.", formatter_class=argparse.HelpFormatter)
    parser.add_argument('files', nargs='+', help='files or folders (any path)')
    parser.add_argument('-v', '--verbose', action='store_true', help='also print clean files')
    parser.add_argument('--memar-rules', dest='memar_rules', action='store_true', default=None, help="apply Memar's Markdown conventions; the default asks whether the folder is a Memar repository")
    parser.add_argument('--no-memar-rules', dest='memar_rules', action='store_false', help='apply only the rules that hold for any text file')
    return run

def run(args: argparse.Namespace) -> None:
    cmd_check(args, content_root())

def check_file(path: Path, link_cache: dict | None=None, memar_rules: bool=True, *, root: Path) -> list[str]:
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
        if text.startswith('---\n'):
            fm_end = text.find('\n---\n', 4)
            if fm_end >= 0:
                after_fm = fm_end + len('\n---\n')
                if after_fm < len(text) and text[after_fm] == '\n':
                    problems.append(f'line {text[:after_fm].count(chr(10)) + 1}: blank line after the closing front-matter fence')
        visible = without_code(text)
        problems.extend(anchor_problems(visible, text))
        problems.extend(link_problems(path, visible, cache, root))
        problems.extend(open_questions_problems(visible))
        denial_problems, denial_hints = denial_findings(visible, path)
        problems.extend(denial_problems)
        problems.extend(restated_field_problems(path, text, cache, root))
        cache[(HINTS_KEY, str(path))] = denial_hints + foreign_domain_hints(path, visible, cache, root)
    if path.suffix == '.md':
        problems.extend(list_problems(path, root))
    if memar_rules:
        problems.extend(temp_duplicate_problems(path))
    return problems

def document_hints(path: Path, link_cache: dict, root: Path) -> list[str]:
    if path.suffix != '.md':
        return []
    kept = link_cache.get((HINTS_KEY, str(path)))
    if kept is not None:
        return kept
    try:
        visible = without_code(path.read_text(encoding='utf-8'))
    except (OSError, UnicodeDecodeError):
        return []
    return denial_findings(visible, path)[1] + foreign_domain_hints(path, visible, link_cache, root)

def checkable_files(folder: Path) -> list[Path]:
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
    warnings: list[str] = []
    if memar_rules:
        for path in files:
            try:
                shown = path.relative_to(root)
            except ValueError:
                shown = path
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
    if memar_rules:
        document_rule_hints: list[str] = []
        for path in files:
            try:
                shown = path.relative_to(root)
            except ValueError:
                shown = path
            document_rule_hints.extend((f'{shown}: {text}' for text in document_hints(path, link_cache, root)))
        if document_rule_hints:
            print('\nhints (not counted as problems):')
            for hint in document_rule_hints:
                print(f'  - {hint}')
    dropped =sum((list_drops(path, root) for path in files if path.suffix == '.md'))
    print(f"\nchecked {len(files)} file{('s' if len(files) != 1 else '')}, {total} problem{('s' if total != 1 else '')}" + (f", {len(warnings)} warning{('s' if len(warnings) != 1 else '')}" if warnings else '') + (f", {dropped} passage{('s' if dropped != 1 else '')} of Memar dropped by this project's lists" if dropped else ''))
    if not memar_rules:
        print("not a Memar repository, so Memar's Markdown conventions were not applied: encoding, newlines, and decoding damage only")
    if total:
        raise SystemExit(1)

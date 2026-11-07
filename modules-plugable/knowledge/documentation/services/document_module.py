#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import os
import re
from pathlib import Path
MODULE_LAYERS = ('modules', 'modules-plugable', 'bundles')
NOT_A_MODULE_PARENT = 'rules'
IMPORT_LINE = re.compile('^\\s*(?:tp|vr)\\s+\\w+\\s+in\\s+"([^"]+)"', re.MULTILINE)
DECLARATION_LINE = re.compile('^\\s*(?:tp|vr)\\s+(\\w+)\\s+(?!in\\b)(\\w+)(.*)$')
MEMBER_LINE = re.compile('^\\s+(\\w+)(?:\\s+[\\w.\\[\\]]+)?\\s*$')
PARAMETER = re.compile('(\\w+)\\s+[\\w.\\[\\]]+\\s*(?=[,)])')
NOT_NAMES = frozenset(('self',))


def _is_module(folder: Path) -> bool:
    return folder.parent.name != NOT_A_MODULE_PARENT and (folder / f'{folder.name}.md').is_file()


def module_of(path: Path, root: Path, cache: dict) -> Path | None:
    key = ('document-module', str(path.parent))
    if key not in cache:
        cache[key] = _module_of(path.parent, root)
    return cache[key]


def _module_of(folder: Path, root: Path) -> Path | None:
    try:
        parts = folder.relative_to(root).parts
    except ValueError:
        return None
    if not parts or parts[0] not in MODULE_LAYERS:
        return None
    for depth in range(len(parts), 1, -1):
        candidate = root.joinpath(*parts[:depth])
        if _is_module(candidate):
            return candidate
    return None


def khayyam_files(module: Path, cache: dict) -> list[Path]:
    key = ('document-module-khayyam', str(module))
    if key not in cache:
        found: list[Path] = []
        for folder, subfolders, files in os.walk(module):
            here = Path(folder)
            subfolders[:] = sorted((name for name in subfolders if not name.startswith(('.', '__')) and not _is_module(here / name)))
            found.extend((here / name for name in sorted(files) if name.endswith('.kh')))
        cache[key] = found
    return cache[key]


def _khayyam_text(path: Path, cache: dict) -> str:
    key = ('document-module-text', str(path))
    if key not in cache:
        try:
            cache[key] = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeDecodeError):
            cache[key] = ''
    return cache[key]


def _without_comments(text: str) -> str:
    return re.sub('//[^\\n]*', '', re.sub('(?s)/\\*.*?\\*/', '', text))


def declared_names(module: Path, root: Path, cache: dict) -> dict[str, Path]:
    key = ('document-module-names', str(module))
    if key not in cache:
        names: dict[str, Path] = {}
        for path in khayyam_files(module, cache):
            depth = 0
            for line in _without_comments(_khayyam_text(path, cache)).splitlines():
                declared = DECLARATION_LINE.match(line)
                if declared and depth == 0:
                    names.setdefault(declared.group(1).lower(), path)
                    for parameter in PARAMETER.findall(declared.group(3)):
                        names.setdefault(parameter.lower(), path)
                elif depth > 0:
                    member = MEMBER_LINE.match(line)
                    if member:
                        names.setdefault(member.group(1).lower(), path)
                depth += line.count('{') - line.count('}')
        for word in NOT_NAMES:
            names.pop(word, None)
        cache[key] = names
    return cache[key]


def imported_modules(module: Path, root: Path, cache: dict) -> set[Path] | None:
    key = ('document-module-imports', str(module))
    if key not in cache:
        files = khayyam_files(module, cache)
        if not files:
            cache[key] = None
        else:
            imported: set[Path] = set()
            for path in files:
                for target in IMPORT_LINE.findall(_khayyam_text(path, cache)):
                    other = module_of(root / target, root, cache)
                    if other is not None and other != module:
                        imported.add(other)
            cache[key] = imported
    return cache[key]

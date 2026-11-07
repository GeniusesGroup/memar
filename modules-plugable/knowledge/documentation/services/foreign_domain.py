#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import os
from importlib import import_module
from pathlib import Path
_m_document_module = import_module('modules-plugable.knowledge.documentation.services.document_module')
_m_links = import_module('modules-plugable.computer.codec.markdown.services.links')
RULE = 'modules-plugable/knowledge/documentation/rules/document-names-only-its-own-domain/document-names-only-its-own-domain.md'
NOT_JUDGED_LAYER = 'bundles'
NOT_JUDGED_FOLDER = 'widgets'


def _normal(path: Path) -> Path:
    return Path(os.path.normpath(path))


def _related(one: Path, other: Path) -> bool:
    return one == other or one in other.parents or other in one.parents


def _concept_module(target: Path, root: Path, cache: dict) -> Path | None:
    if target.is_dir():
        target = target / f'{target.name}.md'
    if target.suffix.lower() != '.md' or not target.is_file():
        return None
    module = _m_document_module.module_of(target, root, cache)
    if module is None or target.parent != module or target.name not in (f'{module.name}.md', 'README.md'):
        return None
    return module


def foreign_domain_hints(path: Path, visible: str, cache: dict, root: Path) -> list[str]:
    root = _normal(root)
    path = _normal(path)
    module = _m_document_module.module_of(path, root, cache)
    if module is None or module.relative_to(root).parts[0] == NOT_JUDGED_LAYER or NOT_JUDGED_FOLDER in path.relative_to(root).parts:
        return []
    hints: list[str] = []
    for line, _, file_part, _ in _m_links.file_links(visible):
        other = _concept_module(_normal(_m_links.link_target(path, file_part, root)), root, cache)
        if other is None or _related(other, module):
            continue
        imports = _m_document_module.imported_modules(module, root, cache)
        shown = other.relative_to(root).as_posix()
        own = module.relative_to(root).as_posix()
        if imports is None:
            hints.append(f'line {line}: links the concept of {shown}, and the imports of {own} cannot be read because it declares no Khayyam; a document names only the concepts of its module and of the modules it imports ({RULE})')
        elif not any((other == imported or other in imported.parents for imported in imports)):
            hints.append(f'line {line}: links the concept of {shown}, which {own} does not import; a document names only the concepts of its module and of the modules it imports, so the import is declared first or the sentence moves to the module that composes both ({RULE})')
    return hints

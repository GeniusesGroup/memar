#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""labels that take a given label — the query DocumentKind/Status bags used to hard-code.

A caller asks for every `Label_*` whose definition takes a kind (e.g. `Label_Status`,
`Label_DocumentKind`), either among a known set of types or by walking a project's
`labels/` folders ([declarations](declarations.py)). There is no second vocabulary
class that re-lists those words.
"""
from __future__ import annotations
import hashlib
import importlib.util
from pathlib import Path
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.services.declarations import declaring_files

def load_types(paths: list[Path]) -> tuple[type, ...]:
    """The DeclaredLabel subclasses the files at PATHS define, one file each, in path order."""
    found: list[type] = []
    for path in paths:
        name = '_memar_label_type_' + hashlib.sha1(str(path).encode('utf-8')).hexdigest()
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for attr in vars(module).values():
            if isinstance(attr, type) and issubclass(attr, DeclaredLabel) and attr is not DeclaredLabel and attr.__name__.startswith('Label_'):
                found.append(attr)
                break
    return tuple(found)

def declared_types(project: Path) -> tuple[type, ...]:
    """Every Label_* DeclaredLabel PROJECT declares, file by file in path order."""
    return load_types(declaring_files(project)) if project.is_dir() else ()

def taking(kind: type, *, among: tuple[type, ...] | None=None, project: Path | None=None) -> tuple[type, ...]:
    """The DeclaredLabel types that take KIND: from AMONG when given, else from PROJECT's declarations."""
    pool = among if among is not None else declared_types(project) if project is not None else ()
    return tuple(member for member in pool if kind in getattr(member, 'takes', ()))

def whose_kinds_include(members: tuple[type, ...], word: str) -> tuple[type, ...]:
    """MEMBERS whose `kinds` field lists WORD (a document-kind word a Status-kind label may apply to)."""
    wanted = word if isinstance(word, str) else getattr(word, 'word', str(word))
    return tuple(member for member in members if wanted in getattr(member, 'kinds', ()))

def read(members: tuple[type, ...], text: str):
    """The member whose key matches TEXT (any case, stripped); None when none does."""
    wanted = text.strip().lower()
    return next((member for member in members if member.key == wanted), None)

def keys(members: tuple[type, ...]) -> tuple[str, ...]:
    return tuple(member.key for member in members)

def listing(members: tuple[type, ...]) -> str:
    words = [member.word for member in members]
    return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else (words[0] if words else '')

def definitions(members: tuple[type, ...]):
    return tuple(member.definition() for member in members)

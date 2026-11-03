#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import hashlib
import importlib
import importlib.util
import pkgutil
from pathlib import Path
from modules.knowledge.label.primitive.label import Label, LabelDefinition

_REGISTRY: list[type] = []
_ENSURED_PACKAGES: set[str] = set()

class DeclaredLabel:
    title = ''
    id = ''
    labels: tuple[type, ...] = ()
    safe = ''
    report_ending: str | None = None
    carried = True

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls is DeclaredLabel:
            return
        if not cls.__name__.startswith('Label_'):
            raise TypeError(f'{cls.__name__} must be named Label_<Word>')
        if not cls.__dict__.get('title'):
            raise TypeError(f'{cls.__name__} declares no title')
        cls.key = cls.title.lower()
        cls.as_label = Label(cls.title, cls.id) if cls.id else Label(cls.title, '')
        cls.label = cls.as_label
        if cls not in _REGISTRY:
            _REGISTRY.append(cls)

    @classmethod
    def definition(cls) -> LabelDefinition:
        return LabelDefinition(
            cls.as_label,
            tuple(held.as_label for held in cls.labels),
        )

    @classmethod
    def Domain(cls) -> str:
        return 'Label'

    @classmethod
    def Summary(cls) -> str:
        text = (cls.Overview() or cls.title).strip()
        if not text:
            return cls.title
        end = text.find('.')
        return text[: end + 1] if end >= 0 else text

    @classmethod
    def Overview(cls) -> str:
        return ''

    @classmethod
    def ExpiryDate(cls) -> str:
        return ''

    @classmethod
    def ExpireInFavorOf(cls) -> tuple[type, ...]:
        return ()

    @classmethod
    def UserActionNote(cls) -> str:
        return ''

    @classmethod
    def DevActionNote(cls) -> str:
        return (
            'Declare Label_<Word>(DeclaredLabel) with labels=(KindType, …) as DeclaredLabel types. '
            'Ask having(kind) or the kind\'s members()/statuses(); text is title and Details, never a string cache. '
            'The in-memory registry is process-local until a graph of label edges replaces it.'
        )

    @classmethod
    def all_declared(cls) -> tuple[type, ...]:
        return tuple(_REGISTRY)

    @classmethod
    def of(cls, label: Label) -> type | None:
        return next((member for member in reversed(_REGISTRY) if member.id == label.id), None)

    @classmethod
    def having(cls, kind: type) -> tuple[type, ...]:
        return tuple(member for member in _REGISTRY if kind in getattr(member, 'labels', ()))

    @classmethod
    def ensure_under(cls, package_name: str) -> None:
        if package_name in _ENSURED_PACKAGES:
            return
        package = importlib.import_module(package_name)
        paths = getattr(package, '__path__', None)
        if paths is None:
            _ENSURED_PACKAGES.add(package_name)
            return
        for module in pkgutil.walk_packages(paths, package.__name__ + '.'):
            leaf = module.name.rsplit('.', 1)[-1]
            if leaf.startswith('_'):
                continue
            if '.labels.' in module.name:
                importlib.import_module(module.name)
        _ENSURED_PACKAGES.add(package_name)

    @classmethod
    def import_path(cls, path: Path) -> type:
        name = '_memar_labels_' + hashlib.sha1(str(path).encode('utf-8')).hexdigest()
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        found = [
            attr for attr in vars(module).values()
            if (
                isinstance(attr, type)
                and issubclass(attr, DeclaredLabel)
                and attr is not DeclaredLabel
                and attr.__name__.startswith('Label_')
                and attr.__module__ == module.__name__
            )
        ]
        if len(found) != 1:
            raise TypeError(f'{path}: one Label_<Word> per file; found {len(found)}')
        return found[0]

    @classmethod
    def read_among(cls, members: tuple[type, ...], text: str):
        wanted = text.strip().lower()
        return next((member for member in members if member.key == wanted), None)

    @classmethod
    def keys_of(cls, members: tuple[type, ...]) -> tuple[str, ...]:
        return tuple(member.key for member in members)

    @classmethod
    def listing_of(cls, members: tuple[type, ...]) -> str:
        titles = [member.title for member in members]
        return f"{', '.join(titles[:-1])}, or {titles[-1]}" if len(titles) > 1 else (titles[0] if titles else '')

    @classmethod
    def definitions_of(cls, members: tuple[type, ...]):
        return tuple(member.definition() for member in members)

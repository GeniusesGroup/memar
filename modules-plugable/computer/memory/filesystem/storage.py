#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import time
from pathlib import Path
from typing import Iterator

class URI_Path(str):

    def summary(self) -> str:
        return 'A URI path'

class Storage_File:

    def __init__(self, path: Path) -> None:
        self._path = Path(path)

    def host_path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.is_file()

    def get_file_data(self) -> bytes:
        return self._path.read_bytes()

    def replace_bytes(self, data: bytes) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self._path.with_name(self._path.name + '.tmp-' + os.urandom(4).hex())
        temporary.write_bytes(data)
        last: OSError | None = None
        for _ in range(20):
            try:
                if os.name == 'nt' and self._path.exists():
                    try:
                        self._path.unlink()
                    except OSError as error:
                        last = error
                        time.sleep(0.01)
                        continue
                os.replace(str(temporary), str(self._path))
                return
            except OSError as error:
                last = error
                time.sleep(0.01)
        if temporary.exists():
            try:
                temporary.unlink()
            except OSError:
                pass
        raise last if last is not None else OSError('replace_bytes failed')

    def delete(self) -> None:
        if self._path.is_file():
            self._path.unlink()

    def summary(self) -> str:
        return 'A file on the host filesystem'

class Storage_Directory:

    def __init__(self, path: Path) -> None:
        self._path = Path(path)

    def host_path(self) -> Path:
        return self._path

    def ensure(self) -> 'Storage_Directory':
        self._path.mkdir(parents=True, exist_ok=True)
        return self

    def directory(self, name: str) -> 'Storage_Directory':
        return Storage_Directory(self._path / name)

    def file(self, name: str) -> Storage_File:
        return Storage_File(self._path / name)

    def get_file_by_path(self, uri_path: URI_Path) -> Storage_File:
        relative = str(uri_path).replace('\\', '/').lstrip('/')
        return Storage_File(self._path.joinpath(*relative.split('/')) if relative else self._path)

    def iter_files(self) -> Iterator[tuple[URI_Path, Storage_File]]:
        root = self._path
        if not root.is_dir():
            return
        for folder, _folders, names in os.walk(root):
            for name in names:
                path = Path(folder) / name
                relative = path.relative_to(root).as_posix()
                yield (URI_Path(relative), Storage_File(path))

    def summary(self) -> str:
        return 'A directory on the host filesystem'

def directory_at(path: Path | str) -> Storage_Directory:
    return Storage_Directory(Path(path))

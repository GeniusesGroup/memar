#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""editor_extension.py — the editor extensions this checkout ships, put where the editor reads them.

A Khayyam extension without Memar on the machine resolves nothing: it has no
location to read the documentation tree from. So installing the extension is
part of installing Memar, not a separate errand to remember afterwards.

It is copied out of the checkout the installer just settled on — the Memar that
was installed brings its own extension — and the folder name it lands under is
read from that extension's own manifest, so nothing here names an extension or
a version. A second run moves the installed folder to the trash and writes the
checkout's extension in its place, because the folder was the installer's own
copy and a change in the checkout has to reach the editor: skipping an existing
folder left a stale client running while the checkout held the new one, and the
editor showed the old behaviour with the new code on disk. The old folder goes
to the trash rather than being deleted, so a local edit can be taken back. So
the editor is brought to the checkout, every run.

Between runs the checkout keeps changing and the editor keeps the copy it was
given — a refactor once left the installed client calling a server that had
moved on. `stale_extensions` is how that is noticed: it asks, of each extension
this checkout ships, whether the editor's folder is missing or no longer what
copying would write, and `memar update` is what asks it.

When extensions reach a marketplace this step changes shape, not purpose. A
marketplace install reaches the network and writes into somebody's editor, so it
has to be asked for; copying a folder the installer already put on the machine
is a different kind of act, and that is the whole of the difference.
"""
from __future__ import annotations

import json
import shutil
from collections.abc import Collection
from pathlib import Path

from machine.console import fail, note
from machine.fs_copy_excluded import NEVER_COPIED
from machine.fs_copy import differs
from machine.fs_trash import soft_delete

# Editor extensions this repository ships, found by listing this folder rather
# than by name: a new extension is a new folder here and nothing else to change.
EXTENSIONS_RELATIVE = Path(".agents") / "vscode" / "extensions"
MANIFEST_NAME = "package.json"


def editor_extensions_dir() -> Path:
    """Where this platform's editor keeps the extensions it has installed."""
    return Path.home() / ".vscode" / "extensions"


def extension_folder_name(manifest: Path) -> str:
    """The name the editor expects a folder to have, read from the manifest.

    <publisher>.<name>-<version> is the editor's own form and the marketplace's.
    A manifest without those fields names no installable extension, which is said
    rather than guessed around.
    """
    try:
        fields = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        fail(f"{manifest} cannot be read as an extension manifest ({error})")
    try:
        publisher = str(fields["publisher"]).lower().replace(".", "")
        name = str(fields["name"]).lower()
        version = str(fields["version"])
    except KeyError as missing:
        fail(f"{manifest} declares no {missing}, so it names no installable extension")
    return f"{publisher}.{name}-{version}"


def shipped_extensions(source_root: Path) -> list[tuple[Path, str]]:
    """Each extension folder under SOURCE_ROOT that has a manifest, with the folder name it installs under."""
    shipped: list[tuple[Path, str]] = []
    for source in sorted(source_root.iterdir()):
        manifest = source / MANIFEST_NAME
        if manifest.is_file():
            shipped.append((source, extension_folder_name(manifest)))
    return shipped


def stale_extensions(checkout: Path) -> list[Path]:
    """Where an extension CHECKOUT ships is missing from the editor or differs from the checkout's.

    Empty when the checkout ships none or this machine has no editor, the two
    cases `install_extensions` skips; a folder that cannot be read counts as
    stale, since refreshing it is what would settle it.
    """
    source_root = checkout / EXTENSIONS_RELATIVE
    installed = editor_extensions_dir()
    if not source_root.is_dir() or not installed.is_dir():
        return []
    stale: list[Path] = []
    for source, name in shipped_extensions(source_root):
        target = installed / name
        try:
            if not target.is_dir() or differs(source, target, NEVER_COPIED):
                stale.append(target)
        except OSError:
            stale.append(target)
    return stale


def install_extensions(checkout: Path, only: Collection[Path] | None = None) -> None:
    """Put the editor extensions this checkout ships into the editor; with ONLY, those landing there.

    The copy already there is the installer's own, so it is moved to the trash
    and the checkout's copy is written in its place: a change in the checkout
    that does not reach the editor is a change that is not installed, and a
    local edit in the old folder can be taken back from the trash. That is the
    whole of the reason, and the reason the step is repeated on every run
    instead of only on the first. ONLY is what `stale_extensions` returned, so
    a refresh moves nothing that is current.
    """
    source_root = checkout / EXTENSIONS_RELATIVE
    if not source_root.is_dir():
        note(f"no editor extension to install: {source_root} is not there")
        return
    installed = editor_extensions_dir()
    if not installed.is_dir():
        # Writing into a folder no editor reads leaves litter, not an extension.
        note(f"no editor on this machine: {installed} is not there, so skipped")
        return
    for source, name in shipped_extensions(source_root):
        target = installed / name
        if only is not None and target not in only:
            continue
        first_time = not target.is_dir()
        if not first_time:
            soft_delete(target)
        shutil.copytree(source, target, ignore=NEVER_COPIED)
        verb = "installed" if first_time else "refreshed"
        note(f"{name} {verb} at {target}")
        note(f"from {source}")
        note("reload the editor window to apply it")

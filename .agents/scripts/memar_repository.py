#!/usr/bin/env python3
"""What a Memar repository is.

The one definition of the question, and the one place the words of a refusal
about it are written. Every other file in this folder — and every shell that
installs Memar — asks here instead of carrying its own copy of the test, which
is the only way two of them cannot come to disagree.
"""
from __future__ import annotations

from pathlib import Path

SKILL_MARKER = Path(".agents") / "skills" / "memar" / "SKILL.md"


def is_memar_repository(path: Path) -> bool:
    """A Memar repository: the entry document, the docs tree, and the skill."""
    return (
        (path / "README.md").is_file()
        and (path / "docs").is_dir()
        and (path / SKILL_MARKER).is_file()
    )


def not_a_repository(path: Path) -> str:
    """Why PATH is not a Memar repository, in the words every refusal uses."""
    return (
        f"{path} is not a Memar repository (no README.md, docs/, and "
        f"{SKILL_MARKER.as_posix()})"
    )

"""Comments of Go and Khayyam text, which share the `//` and `/* */` forms: where every
comment is, what it says, what is left once they are blanked, and which comment
documents which declaration. Every consumer of a doc comment reads it from here, so
a trailing comment documents the line it trails and never the one below it."""

import re
from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class CommentBlock:
    start: int
    end: int
    lines: tuple[str, ...]
    trailing: bool = False


def comment_is_trailing(source: str, start: int) -> bool:
    """True when only whitespace precedes the comment on its first line."""
    beginning = source.rfind("\n", 0, start) + 1
    return bool(source[beginning:start].strip())


def extract_comment_blocks(source: str) -> list[CommentBlock]:
    """Collect every comment in `source` with the line range it covers.

    Runs of adjacent `//` lines form one block so a doc comment keeps its
    line structure; `/* ... */` blocks keep theirs, minus the markers. A
    comment that trails code is a block of its own, never the head of the doc
    comment on the lines below it. Every other token, including string and
    rune literals, is left alone.
    """
    blocks: list[CommentBlock] = []
    index = 0
    line = 1
    length = len(source)
    pending: list[str] | None = None
    pending_start = 0
    pending_trailing = False

    def continues_comment(position: int) -> bool:
        return re.match(r"[ \t]*//", source[position:position + 4]) is not None

    while index < length:
        character = source[index]
        if character == "\n":
            if pending is not None and (pending_trailing or not continues_comment(index + 1)):
                blocks.append(
                    CommentBlock(pending_start, line, tuple(pending), pending_trailing)
                )
                pending = None
            line += 1
            index += 1
            continue
        if character in " \t\r\f\v":
            index += 1
            continue
        if source.startswith("//", index):
            end = source.find("\n", index)
            if end < 0:
                end = length
            if pending is None:
                pending = []
                pending_start = line
                pending_trailing = comment_is_trailing(source, index)
            pending.append(source[index + 2 : end])
            index = end
            continue
        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end < 0:
                end = length - 2
            raw = source[index : end + 2]
            if pending is not None:
                blocks.append(
                    CommentBlock(pending_start, line, tuple(pending), pending_trailing)
                )
                pending = None
            start_line = line
            line += raw.count("\n")
            blocks.append(
                CommentBlock(
                    start_line,
                    line,
                    tuple(raw[2:-2].split("\n")),
                    comment_is_trailing(source, index),
                )
            )
            index = end + 2
            continue
        if character in {'"', "'", "`"}:
            if pending is not None:
                blocks.append(
                    CommentBlock(pending_start, line, tuple(pending), pending_trailing)
                )
                pending = None
            quote = character
            index += 1
            while index < length:
                if quote != "`" and source[index] == "\\":
                    index += 2
                    continue
                if source[index] == quote:
                    index += 1
                    break
                if source[index] == "\n":
                    line += 1
                index += 1
            continue
        if pending is not None:
            blocks.append(CommentBlock(pending_start, line, tuple(pending), pending_trailing))
            pending = None
        index += 1
    if pending is not None:
        blocks.append(CommentBlock(pending_start, line, tuple(pending), pending_trailing))
    return blocks


def strip_comments(source: str) -> str:
    """Blank out every comment, keeping line structure, for text scanning."""
    result = list(source)
    index = 0
    line = 1
    length = len(source)
    while index < length:
        character = source[index]
        if character == "\n":
            line += 1
            index += 1
            continue
        if source.startswith("//", index):
            end = source.find("\n", index)
            if end < 0:
                end = length
            for position in range(index, end):
                result[position] = " "
            index = end
            continue
        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end < 0:
                end = length - 2
            for position in range(index, end + 2):
                if result[position] != "\n":
                    result[position] = " "
            index = end + 2
            continue
        if character in {'"', "'", "`"}:
            quote = character
            index += 1
            while index < length:
                if quote != "`" and source[index] == "\\":
                    index += 2
                    continue
                if source[index] == quote:
                    index += 1
                    break
                index += 1
            continue
        index += 1
    return "".join(result)


def render_comment(lines: Sequence[str]) -> list[str]:
    """Render a Go comment block as Khayyam `//` lines, structure preserved."""
    rendered: list[str] = []
    for text in lines:
        value = text.rstrip()
        if value.startswith("*"):
            value = value[1:]
            if value.startswith(" "):
                value = value[1:]
        rendered.append(f"//{value}" if value else "//")
    return rendered


class CommentIndex:
    """Hands out the comment block that directly precedes a declaration line,
    and the comment that trails it on the same line."""

    def __init__(self, blocks: Sequence[CommentBlock]) -> None:
        self.blocks = list(blocks)
        self._by_end: dict[int, list[str]] = {}
        self._trailing: set[int] = set()
        self._trailing_on: dict[int, CommentBlock] = {}
        for block in self.blocks:
            self._by_end[block.end] = list(block.lines)
            if block.trailing:
                self._trailing.add(block.end)
                self._trailing_on[block.start] = block
        self.claimed: set[int] = set()

    def documenting(self, line: int) -> list[str]:
        """The doc comment above `line` followed by the comment trailing it."""
        return self.before(line) + self.on(line)

    def on(self, line: int) -> list[str]:
        block = self._trailing_on.get(line)
        if block is None or block.end in self.claimed:
            return []
        self.claimed.add(block.end)
        return list(block.lines)

    def before(self, line: int) -> list[str]:
        lines = self._by_end.get(line - 1)
        if not lines or (line - 1) in self.claimed:
            return []
        if (line - 1) in self._trailing:
            # A comment that shares its line with code trails that code; it
            # never documents what comes next.
            return []
        self.claimed.add(line - 1)
        return list(lines)

    def floating(self) -> list[CommentBlock]:
        return [block for block in self.blocks if block.end not in self.claimed]


def comment_lines(source: str) -> list[str]:
    """The non-empty text lines of every comment in `source`."""
    return [
        line.strip()
        for block in extract_comment_blocks(source)
        for line in block.lines
        if line.strip()
    ]

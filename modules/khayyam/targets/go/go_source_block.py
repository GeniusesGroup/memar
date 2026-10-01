"""The verbatim Go source a ported Khayyam file keeps at its end, the residue marker
that says so, and the licence line a ported file opens with.

A block carries a sha256 of the bytes it was made from, so what it holds can be
checked rather than trusted. A file that holds one is never re-rendered without it.
The block and the licence are the two things `transfer` puts in a destination that
`reemit` must keep."""

import re
import hashlib


CORPUS_LICENSE = "/* For license and copyright information please see the LEGAL file in the code repository */"
CORPUS_LICENSE_TEXT = "For license and copyright information"


GO_MIGRATE = "TODO(go-migrate)"
SOURCE_BLOCK_HEAD = f"// {GO_MIGRATE}: full original Go source follows"
SOURCE_BLOCK_BEGIN = re.compile(r"^// --- go-source: (.+) sha256:([0-9a-f]{64}) ---$")
RESIDUE_MARKER = re.compile(
    r"^// TODO\(go-migrate\): residue from (.+); full original source is at end of file$"
)


def residue_marker(label: str) -> str:
    return f"// {GO_MIGRATE}: residue from {label}; full original source is at end of file"


def go_source_lines(raw: bytes) -> list[str]:
    """The lines of a Go file, line endings removed."""
    lines = raw.decode("utf-8", errors="replace").split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    return [line[:-1] if line.endswith("\r") else line for line in lines]


def comment_out(text: str) -> str:
    return f"// {text}" if text else "//"


def comment_text(line: str) -> str:
    """The words of a comment line, without its `//` markers or indentation,
    so a quoted Go doc comment matches the same words kept as a Khayyam comment."""
    text = line.strip()
    while text.startswith("//"):
        text = text[2:].strip()
    return text


def render_source_block(label: str, raw: bytes) -> list[str]:
    digest = hashlib.sha256(raw).hexdigest()
    return [
        SOURCE_BLOCK_HEAD,
        f"// --- go-source: {label} sha256:{digest} ---",
        *(comment_out(line) for line in go_source_lines(raw)),
        f"// --- end go-source: {label} ---",
    ]


def source_blocks(text: str) -> list[tuple[str, str, int, int]]:
    """(label, sha256, first, last) of every go-source block in `text`, as
    indexes into its lines; `first` is the head line when the block has one."""
    lines = text.split("\n")
    blocks: list[tuple[str, str, int, int]] = []
    index = 0
    while index < len(lines):
        match = SOURCE_BLOCK_BEGIN.match(lines[index])
        if match:
            label, digest = match.group(1), match.group(2)
            closing = f"// --- end go-source: {label} ---"
            end = index + 1
            while end < len(lines) and lines[end] != closing:
                end += 1
            if end < len(lines):
                first = index - 1 if index and lines[index - 1] == SOURCE_BLOCK_HEAD else index
                blocks.append((label, digest, first, end))
                index = end + 1
                continue
        index += 1
    return blocks


def verify_source_block(text: str, label: str, raw: bytes) -> str | None:
    """None when `text` carries `raw` under `label` faithfully, apart from the
    comment prefix and the line ending; otherwise what is wrong."""
    digest = hashlib.sha256(raw).hexdigest()
    lines = text.split("\n")
    blocks = source_blocks(text)
    for found, found_digest, first, last in blocks:
        if found != label or found_digest != digest:
            continue
        header = first + 1 if lines[first] == SOURCE_BLOCK_HEAD else first
        body: list[str] = []
        for line in lines[header + 1 : last]:
            if line == "//":
                body.append("")
            elif line.startswith("// "):
                body.append(line[3:])
            else:
                return f"block line {line[:40]!r} is not a commented source line"
        for newline in ("\n", "\r\n"):
            joined = newline.join(body)
            for candidate in (joined + newline if body else joined, joined):
                if hashlib.sha256(candidate.encode("utf-8")).hexdigest() == digest:
                    return None
        return "the block text does not hash to its sha256"
    held = ", ".join(f"{found} {found_digest[:12]}" for found, found_digest, _, _ in blocks)
    return f"no block for {label} sha256:{digest[:12]}" + (f" (holds {held})" if held else "")


def preserve_transfer_text(existing: str, rendered: str) -> str:
    """Keep what `transfer` put in a file `reemit` re-renders: the residue
    markers on top and the go-source blocks at the end. The residue itself is
    not carried, so a file that holds some is guarded, never overwritten."""
    lines = existing.split("\n")
    markers: list[str] = []
    for line in lines:
        if not RESIDUE_MARKER.match(line):
            break
        markers.append(line)
    blocks = [lines[first : last + 1] for _, _, first, last in source_blocks(existing)]
    if not markers and not blocks:
        return rendered
    present = set(rendered.split("\n"))
    head = [line for line in markers if line not in present]
    result = "\n".join([*head, rendered.rstrip("\n")])
    for block in blocks:
        header = next(line for line in block if SOURCE_BLOCK_BEGIN.match(line))
        if header not in present:
            result += "\n\n" + "\n".join(block)
    return result + "\n"

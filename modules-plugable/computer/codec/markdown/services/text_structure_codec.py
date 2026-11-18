#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import re
from importlib import import_module
_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
_span = import_module('modules.knowledge.text.primitive.text_span')
_link = import_module('modules.knowledge.text.primitive.text_link')
_item = import_module('modules.knowledge.text.primitive.text_item')
_section = import_module('modules.knowledge.text.primitive.text_section')
_errors = import_module('modules.knowledge.text.errors.structure')
without_code = _markdown.without_code
Text_Span = _span.Text_Span
Text_Link = _link.Text_Link
Text_Item_Editable = _item.Text_Item_Editable
Text_Section_Editable = _section.Text_Section_Editable
Text_Error_Structure_Malformed = _errors.Text_Error_Structure_Malformed
Text_Error_Structure_NotEncodable = _errors.Text_Error_Structure_NotEncodable
Text_Error_Structure_Foreign = _errors.Text_Error_Structure_Foreign
FENCE = re.compile('^( {0,3})(`{3,}|~{3,})')
HEADING = re.compile('^(#{1,6})[ \\t]+(.*?)[ \\t]*$')
BULLET = re.compile('^([ \\t]*)([-*+]|\\d{1,9}[.)])([ \\t]+)(.*)$')
NAME = re.compile('^(?:\\*\\*)?([A-Za-z][^:\\[\\]`()/\\n]*?)(?::\\*\\*|\\*\\*:|:)(?:[ \\t]+(.*))?$')
LINK = re.compile('(?<!!)\\[([^\\]\\n]+)\\]\\(([^)\\s]+)\\)')
LINE_END = re.compile(b'\\r\\n|\\n|\\r')
TRAILING_END = re.compile(b'(?:\\r\\n|\\n|\\r)?$')
DEEPEST = 6


class _Error(Exception):
    def __init__(self, error: Exception) -> None:
        self.error = error


def _width(blanks: str) -> int:
    return len(blanks.replace('\t', '    '))


def _split_links(raw: str) -> tuple[str, list]:
    visible = without_code(raw)
    plain = ''
    links = []
    cursor = 0
    for match in LINK.finditer(visible):
        plain += raw[cursor:match.start()]
        start = len(plain)
        plain += raw[match.start(1):match.end(1)]
        links.append((Text_Link(raw[match.start(2):match.end(2)]), start, len(plain)))
        cursor = match.end()
    return plain + raw[cursor:], links


def _decode(raw: bytes) -> Text_Section_Editable:
    root = Text_Section_Editable(0, '', False)
    root._s, root._e, root._h = (0, len(raw), 0)
    sections = [root]
    items: list = []
    leaf = None
    fence = None
    blank = False
    offset = 0

    def touch(end: int) -> None:
        for each in sections:
            each._e = end
        for _, each in items:
            each._e = end
        if leaf is not None:
            leaf._e = end

    def new_item(prefix: str, name: str, named: bool, text: str, start: int, end: int) -> Text_Item_Editable:
        item = Text_Item_Editable(name, named, '')
        item._s, item._e, item._h = (start, end, end)
        item._prefix = prefix
        item._raw = text
        return item

    for line in raw.splitlines(keepends=True):
        start = offset
        offset += len(line)
        end = offset
        text = line.rstrip(b'\r\n').decode('utf-8')
        if fence is not None:
            marker, size, item, standalone = fence
            if standalone:
                item._raw += '\n' + text
            else:
                item._raw += '\n' + text.strip()
            item._e = end
            if re.match('^ {0,3}' + re.escape(marker) + '{' + str(size) + ',}[ \\t]*$', text):
                fence = None
            touch(end)
            continue
        if not text.strip():
            blank = True
            leaf = None
            continue
        was_blank = blank
        blank = False
        heading = HEADING.match(text)
        if heading:
            level = len(heading.group(1))
            while sections[-1].GetSectionLevel() >= level:
                sections.pop()
            section = Text_Section_Editable(level, heading.group(2), True)
            section._s, section._e, section._h = (start, end, end)
            sections[-1].AppendSection(section)
            sections.append(section)
            items = []
            leaf = None
            touch(end)
            continue
        opening = FENCE.match(text)
        if opening:
            marker = opening.group(2)[0]
            size = len(opening.group(2))
            if items and (not was_blank or _width(re.match('^[ \\t]*', text).group()) > items[-1][0]):
                owner = items[-1][1]
                owner._raw += '\n' + text.strip()
                owner._h = end
                fence = (marker, size, owner, False)
            else:
                items = []
                item = new_item('', '', False, text, start, end)
                sections[-1].AppendItem(item)
                leaf = item
                fence = (marker, size, item, True)
            touch(end)
            continue
        bullet = BULLET.match(text)
        if bullet:
            indent = _width(bullet.group(1))
            while items and items[-1][0] >= indent:
                items.pop()
            content = bullet.group(4)
            named = NAME.match(content)
            if named:
                item = new_item(text[:bullet.end(3)], named.group(1), True, named.group(2) or '', start, end)
            else:
                item = new_item(text[:bullet.end(3)], '', False, content, start, end)
            (items[-1][1] if items else sections[-1]).AppendItem(item)
            items.append((indent, item))
            leaf = None
            touch(end)
            continue
        if items and (not was_blank or _width(re.match('^[ \\t]*', text).group()) > items[-1][0]):
            owner = items[-1][1]
            owner._raw += '\n' + text.strip()
            owner._h = end
            touch(end)
            continue
        items = []
        if leaf is not None:
            leaf._raw += '\n' + text
        else:
            leaf = new_item('', '', False, text, start, end)
            sections[-1].AppendItem(leaf)
        touch(end)
    if fence is not None:
        raise _Error(Text_Error_Structure_Malformed())
    root._e = len(raw)
    _finish(root)
    return root


def _finish(node) -> None:
    node._span = Text_Span(node._s, node._e, True)
    if isinstance(node, Text_Item_Editable):
        if node._prefix == '' and node._raw.startswith(('```', '~~~')):
            node._value = node._raw
        else:
            node._value, node._links = _split_links(node._raw)
    for child in _children(node):
        _finish(child)


def _children(node) -> list:
    if isinstance(node, Text_Section_Editable):
        return list(node._items) + list(node._sections)
    return list(node._items)


def _kind(node) -> str:
    return 's' if isinstance(node, Text_Section_Editable) else 'i'


def _same(node, ref) -> bool:
    if _kind(node) == 's':
        return (node.GetSectionLevel(), node.GetTitle()) == (ref.GetSectionLevel(), ref.GetTitle())
    return (node.GetItemName(), node.GetValue(), node._links) == (ref.GetItemName(), ref.GetValue(), ref._links)


def _value_text(item) -> str:
    value = item.GetValue()
    cursor = 0
    text = ''
    for link, start, end in sorted(item._links, key=lambda each: each[1]):
        locator = link.GetLocator()
        if start < cursor or start >= end or end > len(value) or not locator or re.search('[\\s)]', locator):
            raise _Error(Text_Error_Structure_NotEncodable())
        text += value[cursor:start] + '[' + value[start:end] + '](' + locator + ')'
        cursor = end
    return text + value[cursor:]


def _validate(node, parent_level: int) -> None:
    if _kind(node) == 's':
        title, titled = node.GetTitle()
        level = node.GetSectionLevel()
        if level <= parent_level or level > DEEPEST or (titled and '\n' in title):
            raise _Error(Text_Error_Structure_NotEncodable())
        for child in node._items:
            _validate(child, level)
        for child in node._sections:
            _validate(child, level)
        return
    name, named = node.GetItemName()
    if named and (not name.strip() or name != name.strip() or re.search('[:\\n\\r]', name)):
        raise _Error(Text_Error_Structure_NotEncodable())
    _value_text(node)
    for child in node._items:
        _validate(child, parent_level)


class _Writing:

    def __init__(self, before: bytes, root) -> None:
        self.before = before
        found = LINE_END.search(before)
        self.eol = found.group() if found else b'\n'
        self.ref = _decode(before)
        self.by_span: dict = {}
        self.parent: dict = {}
        self._index(self.ref)
        self.root = root

    def _index(self, ref) -> None:
        self.by_span[(_kind(ref), ref._s, ref._e)] = ref
        for child in _children(ref):
            self.parent[id(child)] = ref
            self._index(child)

    def check_foreign(self, node, top: bool) -> None:
        span = node.GetSpan()
        if top and (not span.IsDecoded() or (span.GetStart(), span.GetEnd()) != (0, len(self.before)) or node.GetSectionLevel() != 0):
            raise _Error(Text_Error_Structure_Foreign())
        if span.IsDecoded() and (_kind(node), span.GetStart(), span.GetEnd()) not in self.by_span:
            raise _Error(Text_Error_Structure_Foreign())
        for child in _children(node):
            self.check_foreign(child, False)

    def lines(self, item, prefix: str) -> list:
        name, named = item.GetItemName()
        parts = _value_text(item).split('\n')
        first = (name + ':' + (' ' + parts[0] if parts[0] else '')) if named else parts[0]
        pad = ' ' * len(prefix) if prefix.strip() else ''
        return [(prefix + first).encode('utf-8')] + [(pad + each).encode('utf-8') for each in parts[1:]]

    def anew(self, node, indent: str) -> bytes:
        eol = self.eol
        if _kind(node) == 's':
            title, titled = node.GetTitle()
            out = b'#' * node.GetSectionLevel() + b' ' + title.encode('utf-8') + eol
            if node._items or node._sections:
                out += eol
            for child in node._items:
                out += self.anew(child, '')
            for child in node._sections:
                if not out.endswith(eol + eol):
                    out += eol
                out += self.anew(child, '')
            return out
        marker = getattr(node, '_prefix', '- ').lstrip()
        prefix = indent + marker if marker else ''
        out = eol.join(self.lines(node, prefix)) + eol
        for child in node._items:
            out += self.anew(child, ' ' * len(prefix) if prefix else indent)
        return out

    def head(self, node, ref, indent: str) -> bytes:
        original = self.before[ref._s:ref._h]
        end = TRAILING_END.search(original).group()
        if _kind(node) == 's':
            return b'#' * node.GetSectionLevel() + b' ' + node.GetTitle()[0].encode('utf-8') + end
        return self.eol.join(self.lines(node, ref._prefix)) + end

    def emit(self, node, ref, indent: str) -> bytes:
        before = self.before
        out = before[ref._s:ref._h]
        if not _same(node, ref):
            out = self.head(node, ref, indent)
        prefix = getattr(ref, '_prefix', '')
        child_indent = ' ' * len(prefix) if prefix.strip() else indent
        gaps: dict = {}
        previous = ref._h
        for position, each in enumerate(_children(ref)):
            gaps[id(each)] = (position, before[previous:each._s])
            previous = each._e
        tail = before[previous:ref._e]
        kept = -1
        for child in _children(node):
            found = self.by_span.get((_kind(child), child.GetSpan().GetStart(), child.GetSpan().GetEnd())) if child.GetSpan().IsDecoded() else None
            if found is not None and self.parent.get(id(found)) is ref and gaps[id(found)][0] > kept:
                kept = gaps[id(found)][0]
                out += gaps[id(found)][1] + self.emit(child, found, child_indent)
                continue
            if out and not out.endswith((b'\n', b'\r')):
                out += self.eol
            if _kind(child) == 's' and out and not out.endswith(self.eol + self.eol):
                out += self.eol
            out += self.anew(child, child_indent)
        return out + tail


class Text_Structure_Codec:

    def DecodeStructure(self, encoded: str):
        try:
            return _decode(encoded.encode('utf-8')), None
        except _Error as failure:
            return None, failure.error

    def EncodeStructure(self, before: str, root):
        try:
            writing = _Writing(before.encode('utf-8'), root)
            writing.check_foreign(root, True)
            _validate(root, -1)
            return writing.emit(root, writing.ref, '').decode('utf-8'), None
        except _Error as failure:
            return '', failure.error

#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path[0:0] = [str(TOP), str(TOP / 'bundles' / 'memar'), str(TOP / 'bundles' / 'memar' / 'services')]
BUDGET_SECONDS = 5
TIER = 'unit'
_codec = import_module('modules-plugable.computer.codec.markdown.services.text_structure_codec')
_nodes = import_module('modules.knowledge.text.primitive.text_nodes')
_link = import_module('modules.knowledge.text.primitive.text_link')
_errors = import_module('modules.knowledge.text.errors.structure')
Codec = _codec.Text_Structure_Codec
Nodes = _nodes.Text_Nodes
Link = _link.Text_Link
Malformed = _errors.Text_Error_Structure_Malformed
NotEncodable = _errors.Text_Error_Structure_NotEncodable
Foreign = _errors.Text_Error_Structure_Foreign

FENCE = '```\n## not a heading\n- not: a field\n```\n'
LEDGER = (
    '# Module Changelog\n'
    '\n'
    'Some prose before the first section.\n'
    '\n'
    '## Changelog\n'
    '\n'
    '### 1. First record\n'
    '- Date: 2026-10-30\n'
    '- Contributors:\n'
    '  - [Claude Sonnet 5.5](../../CONTRIBUTORS.md#claude-sonnet-55) proposed\n'
    '  - [Omid](../../CONTRIBUTORS.md#omid) approved\n'
    '- Summary: kept `[not](a#link)` as it is\n'
    '\n'
    + FENCE +
    '\n'
    '### 2. Second record\n'
    '- Date: 2026-10-31\n'
    '- Contributors: [Claude](../../CONTRIBUTORS.md#claude) proposed\n'
)


def decode(text: str):
    root, err = Codec().DecodeStructure(text)
    assert err is None, err
    return root


def encode(before: str, root) -> str:
    out, err = Codec().EncodeStructure(before, root)
    assert err is None, err
    return out


def section(root, *path: int):
    for position in path:
        root = root.GetEditableSectionAt(position)
    return root


class Decode(unittest.TestCase):

    def test_the_root_is_level_zero_and_the_first_heading_is_its_section(self) -> None:
        root = decode(LEDGER)
        self.assertEqual(root.GetSectionLevel(), 0)
        self.assertEqual(root.GetTitle()[1], False)
        self.assertEqual(root.GetItemCount(), 0)
        self.assertEqual(root.GetOccupiedLength(), 1)
        top = section(root, 0)
        self.assertEqual(top.GetTitle(), ('Module Changelog', True))
        self.assertEqual(top.GetItemAt(0).GetValue(), 'Some prose before the first section.')

    def test_text_before_any_heading_is_items_of_the_root(self) -> None:
        root = decode('front matter\n\nprose\n\n## A\n')
        self.assertEqual(root.GetItemCount(), 2)
        self.assertEqual(root.GetItemAt(0).GetItemName()[1], False)
        self.assertEqual(root.GetItemAt(0).GetValue(), 'front matter')
        self.assertEqual(root.GetItemAt(1).GetValue(), 'prose')

    def test_sections_nest_by_level_and_a_skipped_level_is_kept(self) -> None:
        root = decode('## A\n#### B\n## C\n')
        self.assertEqual(root.GetOccupiedLength(), 2)
        a = section(root, 0)
        self.assertEqual(a.GetOccupiedLength(), 1)
        self.assertEqual(section(a, 0).GetSectionLevel(), 4)
        self.assertEqual(section(root, 1).GetTitle(), ('C', True))

    def test_a_record_reads_as_fields_with_sub_items_and_links(self) -> None:
        record = section(decode(LEDGER), 0, 0, 0)
        self.assertEqual(record.GetTitle(), ('1. First record', True))
        self.assertEqual(record.GetItemAt(0).GetItemName(), ('Date', True))
        self.assertEqual(record.GetItemAt(0).GetValue(), '2026-10-30')
        contributors = record.GetItemAt(1)
        self.assertEqual(contributors.GetItemName(), ('Contributors', True))
        self.assertEqual(contributors.GetValue(), '')
        self.assertEqual(contributors.GetItemCount(), 2)
        claude = contributors.GetItemAt(0)
        self.assertEqual(claude.GetValue(), 'Claude Sonnet 5.5 proposed')
        link, start, end = claude.GetLinkAt(0)
        self.assertEqual(link.GetLocator(), '../../CONTRIBUTORS.md#claude-sonnet-55')
        self.assertEqual(claude.GetValue()[start:end], 'Claude Sonnet 5.5')
        self.assertEqual(claude.GetItemName()[1], False)

    def test_a_field_with_its_value_on_the_line_holds_the_link_in_its_value(self) -> None:
        contributors = section(decode(LEDGER), 0, 0, 1).GetItemAt(1)
        self.assertEqual(contributors.GetValue(), 'Claude proposed')
        self.assertEqual(contributors.GetLinkCount(), 1)
        self.assertEqual(contributors.GetItemCount(), 0)

    def test_a_link_inside_a_code_span_is_not_a_link(self) -> None:
        summary = section(decode(LEDGER), 0, 0, 0).GetItemAt(2)
        self.assertEqual(summary.GetLinkCount(), 0)
        self.assertEqual(summary.GetValue(), 'kept `[not](a#link)` as it is')

    def test_a_code_fence_is_one_item_and_its_lines_are_no_headings_or_fields(self) -> None:
        record = section(decode(LEDGER), 0, 0, 0)
        self.assertEqual(record.GetOccupiedLength(), 0)
        fence = record.GetItemAt(3)
        self.assertEqual(fence.GetItemName()[1], False)
        self.assertEqual(fence.GetValue(), FENCE.rstrip('\n'))

    def test_lf_and_crlf_decode_alike(self) -> None:
        a = section(decode(LEDGER), 0, 0, 0).GetItemAt(1)
        b = section(decode(LEDGER.replace('\n', '\r\n')), 0, 0, 0).GetItemAt(1)
        self.assertEqual((a.GetItemName(), a.GetItemCount(), a.GetItemAt(1).GetValue()), (b.GetItemName(), b.GetItemCount(), b.GetItemAt(1).GetValue()))

    def test_spans_are_in_bytes_and_the_root_covers_all(self) -> None:
        text = '## Ä\n- a: ü\n'
        root = decode(text)
        size = len(text.encode('utf-8'))
        self.assertEqual((root.GetSpan().GetStart(), root.GetSpan().GetEnd()), (0, size))
        self.assertTrue(root.GetSpan().IsDecoded())
        item = section(root, 0).GetItemAt(0)
        self.assertEqual((item.GetSpan().GetStart(), item.GetSpan().GetEnd()), (len('## Ä\n'.encode()), size))

    def test_an_unclosed_fence_is_malformed(self) -> None:
        root, err = Codec().DecodeStructure('## A\n```\ncode\n')
        self.assertIsInstance(err, Malformed)


class Keeping(unittest.TestCase):

    def test_nothing_changed_gives_the_same_bytes(self) -> None:
        for text in (LEDGER, LEDGER.replace('\n', '\r\n'), LEDGER.rstrip('\n'), '', '\n\n## A\n\n\n'):
            self.assertEqual(encode(text, decode(text)), text)

    def test_a_changed_node_changes_only_its_own_bytes(self) -> None:
        root = decode(LEDGER)
        section(root, 0, 0, 1).GetEditableItemAt(0).SetValue('2027-01-01')
        self.assertEqual(encode(LEDGER, root), LEDGER.replace('- Date: 2026-10-31', '- Date: 2027-01-01'))

    def test_line_endings_are_kept_when_a_node_changes(self) -> None:
        before = LEDGER.replace('\n', '\r\n')
        root = decode(before)
        section(root, 0, 0, 1).GetEditableItemAt(0).SetValue('2027-01-01')
        out = encode(before, root)
        self.assertEqual(out, before.replace('- Date: 2026-10-31', '- Date: 2027-01-01'))
        self.assertEqual(out.count('\n'), out.count('\r\n'))

    def test_a_node_made_after_decoding_is_written_in_the_line_ending_of_before(self) -> None:
        before = '## A\r\n- x: 1\r\n'
        root = decode(before)
        section(root, 0).AppendItem(Nodes().MakeItem('y', True, '2'))
        self.assertEqual(encode(before, root), '## A\r\n- x: 1\r\n- y: 2\r\n')

    def test_a_code_fence_is_kept_byte_for_byte_when_its_neighbours_change(self) -> None:
        root = decode(LEDGER)
        section(root, 0, 0, 0).GetEditableItemAt(0).SetValue('2027-01-01')
        out = encode(LEDGER, root)
        self.assertIn(FENCE, out)
        self.assertEqual(out.replace('2027-01-01', '2026-10-30'), LEDGER)

    def test_a_changed_sub_item_does_not_rewrite_its_ancestors(self) -> None:
        root = decode(LEDGER)
        contributors = section(root, 0, 0, 0).GetEditableItemAt(1)
        contributors.GetEditableItemAt(1).SetItemName('Role')
        self.assertEqual(encode(LEDGER, root), LEDGER.replace('  - [Omid](../../CONTRIBUTORS.md#omid) approved', '  - Role: [Omid](../../CONTRIBUTORS.md#omid) approved'))

    def test_an_inserted_item_is_written_where_it_was_put_and_the_rest_is_kept(self) -> None:
        root = decode(LEDGER)
        contributors = section(root, 0, 0, 0).GetEditableItemAt(1)
        new = Nodes().MakeItem('', False, 'Reviewer approved')
        self.assertIsNone(new.AppendLink(Link('../../CONTRIBUTORS.md#reviewer'), 0, 8))
        contributors.AppendItem(new)
        out = encode(LEDGER, root)
        self.assertEqual(out, LEDGER.replace('approved\n- Summary', 'approved\n  - [Reviewer](../../CONTRIBUTORS.md#reviewer) approved\n- Summary'))
        item = section(decode(out), 0, 0, 0).GetItemAt(1).GetItemAt(2)
        self.assertEqual(item.GetValue(), 'Reviewer approved')
        self.assertEqual(item.GetLinkAt(0)[0].GetLocator(), '../../CONTRIBUTORS.md#reviewer')

    def test_a_removed_section_takes_its_bytes_and_the_gap_before_it(self) -> None:
        root = decode(LEDGER)
        self.assertIsNone(section(root, 0, 0).RemoveSection(1))
        self.assertEqual(encode(LEDGER, root), LEDGER[:LEDGER.index('\n### 2.')])

    def test_a_removed_item_leaves_its_neighbours_intact(self) -> None:
        root = decode(LEDGER)
        self.assertIsNone(section(root, 0, 0, 0).RemoveItem(2))
        self.assertEqual(encode(LEDGER, root), LEDGER.replace('- Summary: kept `[not](a#link)` as it is\n', ''))

    def test_a_moved_node_is_rewritten_and_the_others_keep_their_bytes(self) -> None:
        before = '## A\n- x: 1\n- y:   2\n- z: 3\n'
        root = decode(before)
        a = section(root, 0)
        first = a.GetItemAt(0)
        self.assertIsNone(a.RemoveItem(0))
        a.AppendItem(first)
        self.assertEqual(encode(before, root), '## A\n- y:   2\n- z: 3\n- x: 1\n')

    def test_a_moved_node_is_written_anew_from_its_content(self) -> None:
        before = '## A\n- x:    1\n- y: 2\n'
        root = decode(before)
        a = section(root, 0)
        first = a.GetItemAt(0)
        a.RemoveItem(0)
        a.AppendItem(first)
        self.assertEqual(encode(before, root), '## A\n- y: 2\n- x: 1\n')

    def test_a_moved_node_keeps_its_own_marker(self) -> None:
        before = '## A\n* x: 1\n* y: 2\n'
        root = decode(before)
        a = section(root, 0)
        first = a.GetItemAt(0)
        a.RemoveItem(0)
        a.AppendItem(first)
        self.assertEqual(encode(before, root), '## A\n* y: 2\n* x: 1\n')

    def test_a_changed_node_keeps_its_marker_and_indent(self) -> None:
        before = '## A\n* x: 1\n  * sub\n'
        root = decode(before)
        section(root, 0).GetEditableItemAt(0).SetValue('2')
        self.assertEqual(encode(before, root), '## A\n* x: 2\n  * sub\n')

    def test_a_new_section_is_written_with_its_heading_and_items(self) -> None:
        before = '## A\n- x: 1\n'
        root = decode(before)
        nodes = Nodes()
        b = nodes.MakeSection(2, 'B', True)
        b.AppendItem(nodes.MakeItem('k', True, 'v'))
        root.AppendSection(b)
        self.assertEqual(encode(before, root), '## A\n- x: 1\n\n## B\n\n- k: v\n')

    def test_a_changed_title_rewrites_only_the_heading_line(self) -> None:
        root = decode(LEDGER)
        section(root, 0, 0, 1).SetTitle('2. Renamed')
        self.assertEqual(encode(LEDGER, root), LEDGER.replace('### 2. Second record', '### 2. Renamed'))

    def test_a_text_without_a_final_newline_stays_so_when_its_last_node_changes(self) -> None:
        before = '## A\n- x: 1'
        root = decode(before)
        section(root, 0).GetEditableItemAt(0).SetValue('2')
        self.assertEqual(encode(before, root), '## A\n- x: 2')

    def test_a_link_in_a_changed_item_is_written_back_as_a_link(self) -> None:
        before = '## A\n- w: [Name](a.md#b) role\n'
        root = decode(before)
        section(root, 0).GetEditableItemAt(0).SetItemName('v')
        self.assertEqual(encode(before, root), '## A\n- v: [Name](a.md#b) role\n')


class Refusals(unittest.TestCase):

    def test_a_root_not_decoded_from_before_is_foreign(self) -> None:
        root = decode('## A\n- x: 1\n')
        out, err = Codec().EncodeStructure('## A\n', root)
        self.assertIsInstance(err, Foreign)

    def test_a_made_root_is_foreign(self) -> None:
        out, err = Codec().EncodeStructure('', Nodes().MakeSection(0, '', False))
        self.assertIsInstance(err, Foreign)

    def test_a_child_not_of_a_greater_level_is_not_encodable(self) -> None:
        root = decode('## A\n')
        section(root, 0).AppendSection(Nodes().MakeSection(2, 'same', True))
        out, err = Codec().EncodeStructure('## A\n', root)
        self.assertIsInstance(err, NotEncodable)

    def test_a_name_with_a_colon_or_a_line_break_is_not_encodable(self) -> None:
        for name in ('a:b', 'a\nb', ''):
            root = decode('## A\n')
            section(root, 0).AppendItem(Nodes().MakeItem(name, True, 'v'))
            out, err = Codec().EncodeStructure('## A\n', root)
            self.assertIsInstance(err, NotEncodable, name)

    def test_a_level_above_six_is_not_encodable(self) -> None:
        root = decode('')
        root.AppendSection(Nodes().MakeSection(7, 'deep', True))
        out, err = Codec().EncodeStructure('', root)
        self.assertIsInstance(err, NotEncodable)


if __name__ == '__main__':
    unittest.main()

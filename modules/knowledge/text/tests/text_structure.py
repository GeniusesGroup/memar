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
_nodes = import_module('modules.knowledge.text.primitive.text_nodes')
_link = import_module('modules.knowledge.text.primitive.text_link')
_errors = import_module('modules.knowledge.text.errors.structure')
Text_Nodes = _nodes.Text_Nodes
Text_Link = _link.Text_Link
Position = _errors.Text_Error_Structure_Position


class MadeNodes(unittest.TestCase):

    def setUp(self) -> None:
        self.nodes = Text_Nodes()

    def test_a_made_item_holds_its_name_value_and_no_links_or_sub_items(self) -> None:
        item = self.nodes.MakeItem('Contributors', True, 'x')
        self.assertEqual(item.GetItemName(), ('Contributors', True))
        self.assertEqual(item.GetValue(), 'x')
        self.assertEqual(item.GetLinkCount(), 0)
        self.assertEqual(item.GetItemCount(), 0)

    def test_a_made_node_has_no_span(self) -> None:
        self.assertFalse(self.nodes.MakeItem('', False, 'v').GetSpan().IsDecoded())
        self.assertFalse(self.nodes.MakeSection(2, 'T', True).GetSpan().IsDecoded())

    def test_a_made_section_holds_its_level_and_title(self) -> None:
        section = self.nodes.MakeSection(3, 'Title', True)
        self.assertEqual(section.GetLevel(), 3)
        self.assertEqual(section.GetTitle(), ('Title', True))
        self.assertEqual(section.GetItemCount(), 0)
        self.assertEqual(section.GetSectionCount(), 0)


class ItemMutators(unittest.TestCase):

    def setUp(self) -> None:
        self.nodes = Text_Nodes()
        self.item = self.nodes.MakeItem('A', True, 'hello world')

    def test_names_can_be_set_and_cleared(self) -> None:
        self.item.SetItemName('B')
        self.assertEqual(self.item.GetItemName(), ('B', True))
        self.item.ClearItemName()
        self.assertEqual(self.item.GetItemName()[1], False)

    def test_a_link_is_kept_with_its_start_and_end(self) -> None:
        link = Text_Link('x.md#a')
        self.assertIsNone(self.item.AppendLink(link, 0, 5))
        self.assertEqual(self.item.GetLinkAt(0), (link, 0, 5))

    def test_a_link_beyond_the_value_is_refused_and_nothing_changes(self) -> None:
        self.assertIsInstance(self.item.AppendLink(Text_Link('x'), 0, 99), Position)
        self.assertIsInstance(self.item.AppendLink(Text_Link('x'), 5, 2), Position)
        self.assertEqual(self.item.GetLinkCount(), 0)

    def test_setting_the_value_clears_the_links(self) -> None:
        self.item.AppendLink(Text_Link('x'), 0, 5)
        self.item.SetValue('other')
        self.assertEqual(self.item.GetLinkCount(), 0)

    def test_removing_a_link_out_of_range_is_refused(self) -> None:
        self.assertIsInstance(self.item.RemoveLink(0), Position)


class RunsOfItems(unittest.TestCase):

    def setUp(self) -> None:
        self.nodes = Text_Nodes()
        self.section = self.nodes.MakeSection(1, 'S', True)
        self.a = self.nodes.MakeItem('', False, 'a')
        self.b = self.nodes.MakeItem('', False, 'b')
        self.c = self.nodes.MakeItem('', False, 'c')

    def values(self) -> list[str]:
        return [self.section.GetItemAt(i).GetValue() for i in range(self.section.GetItemCount())]

    def test_append_insert_replace_and_remove(self) -> None:
        self.section.AppendItem(self.a)
        self.section.AppendItem(self.c)
        self.assertIsNone(self.section.InsertItem(1, self.b))
        self.assertEqual(self.values(), ['a', 'b', 'c'])
        self.assertIsNone(self.section.ReplaceItem(0, self.nodes.MakeItem('', False, 'z')))
        self.assertIsNone(self.section.RemoveItem(2))
        self.assertEqual(self.values(), ['z', 'b'])

    def test_insert_accepts_the_count_and_replace_and_remove_do_not(self) -> None:
        self.section.AppendItem(self.a)
        self.assertIsNone(self.section.InsertItem(1, self.b))
        self.assertIsInstance(self.section.InsertItem(3, self.c), Position)
        self.assertIsInstance(self.section.ReplaceItem(2, self.c), Position)
        self.assertIsInstance(self.section.RemoveItem(2), Position)
        self.assertEqual(self.values(), ['a', 'b'])

    def test_the_item_reached_for_editing_is_the_item_observed(self) -> None:
        self.section.AppendItem(self.a)
        self.assertIs(self.section.GetEditableItemAt(0), self.section.GetItemAt(0))

    def test_sub_sections_follow_the_same_positions(self) -> None:
        child = self.nodes.MakeSection(2, 'C', True)
        self.section.AppendSection(child)
        self.assertIsInstance(self.section.InsertSection(2, child), Position)
        self.assertIsInstance(self.section.RemoveSection(1), Position)
        self.assertIs(self.section.GetEditableSectionAt(0), self.section.GetSectionAt(0))
        self.assertIsNone(self.section.RemoveSection(0))
        self.assertEqual(self.section.GetSectionCount(), 0)

    def test_the_title_can_be_set(self) -> None:
        self.section.SetTitle('New')
        self.assertEqual(self.section.GetTitle(), ('New', True))


if __name__ == '__main__':
    unittest.main()

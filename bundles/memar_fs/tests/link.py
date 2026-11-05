#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle, errors

def link(*args, **keywords):
    return bundle('services.link').link(*args, **keywords)

class LinkMakesADirectoryLink(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'target'
        self.target.mkdir()
        (self.target / 'inside.md').write_text('inside\n', encoding='utf-8', newline='\n')
        self.place = self.root / 'place'

    def test_the_link_leads_to_the_target(self) -> None:
        link(self.place, self.target)
        self.assertTrue(self.place.is_dir())
        self.assertEqual(self.place.resolve(), self.target.resolve())
        self.assertEqual((self.place / 'inside.md').read_text(encoding='utf-8'), 'inside\n')

    def test_the_parent_folders_of_the_link_are_made(self) -> None:
        deep = self.root / 'a' / 'b' / 'place'
        link(deep, self.target)
        self.assertEqual(deep.resolve(), self.target.resolve())

    def test_a_link_that_already_resolves_to_the_target_is_left_as_it_is(self) -> None:
        link(self.place, self.target)
        link(self.place, self.target)
        self.assertEqual(self.place.resolve(), self.target.resolve())
        link(self.place, self.target, replace=True)
        self.assertEqual(self.place.resolve(), self.target.resolve())

    def test_something_else_at_the_place_is_replaced_when_asked_and_goes_to_the_recycle_bin(self) -> None:
        self.place.mkdir()
        (self.place / 'old.md').write_text('old\n', encoding='utf-8', newline='\n')
        link(self.place, self.target, replace=True)
        self.assertEqual(self.place.resolve(), self.target.resolve())
        self.assertFalse((self.target / 'old.md').exists())

class LinkRefuses(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'target'
        self.target.mkdir()
        self.place = self.root / 'place'

    def test_a_target_that_is_not_a_folder_is_refused(self) -> None:
        plain = self.root / 'plain.md'
        plain.write_text('x\n', encoding='utf-8', newline='\n')
        for target in (plain, self.root / 'absent'):
            with self.subTest(target=target.name):
                with self.assertRaises(errors().NotAFolder):
                    link(self.place, target)
                self.assertFalse(self.place.exists())

    def test_something_else_at_the_place_is_refused_unless_replacing_is_asked_for(self) -> None:
        self.place.mkdir()
        (self.place / 'kept.md').write_text('kept\n', encoding='utf-8', newline='\n')
        with self.assertRaises(errors().LinkExists):
            link(self.place, self.target)
        self.assertEqual((self.place / 'kept.md').read_text(encoding='utf-8'), 'kept\n')
        self.assertNotEqual(self.place.resolve(), self.target.resolve())
if __name__ == '__main__':
    unittest.main(verbosity=2)

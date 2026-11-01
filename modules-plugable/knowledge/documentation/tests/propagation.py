#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
propagation = import_module('modules-plugable.knowledge.documentation.services.propagation')
Content = import_module('modules.management.timeline.services.timeline_files').Content


def changelog(number: int, items: str, kind: str = 'changelog') -> Content:
    return Content(number, {'kind': kind}, f'### A change\n- Propagates to:\n{items}\n#### What changed\nx\n')


class OpenPropagations(unittest.TestCase):

    def test_a_pending_item_is_open_with_its_task_content_line_and_text(self) -> None:
        found = propagation.open_propagations([('T-1', changelog(3, '  - modeling.md: Pending - reference this.'))])
        self.assertEqual(found, [('T-1', 3, 3, 'modeling.md: Pending - reference this.')])

    def test_a_wrapped_continuation_line_is_not_a_second_item(self) -> None:
        found = propagation.open_propagations([('T-1', changelog(1, '  - [m.md](./m.md): Pending - reference\n    this instead.'))])
        self.assertEqual(len(found), 1, found)

    def test_a_state_written_as_a_phrase_is_still_pending(self) -> None:
        found = propagation.open_propagations([('T-1', changelog(1, '  - p.md: Pending deletion - superseded.'))])
        self.assertEqual(len(found), 1, found)

    def test_a_state_word_later_in_the_description_is_not_the_state(self) -> None:
        self.assertEqual(propagation.open_propagations([('T-1', changelog(1, '  - m.md: Done - it was Pending until now.'))]), [])

    def test_done_and_rejected_are_not_open(self) -> None:
        items = '  - a.md: Done - landed\n  - b.md: Rejected - not wanted\n  - c.md: Pending - owed'
        found = propagation.open_propagations([('T-1', changelog(1, items))])
        self.assertEqual([entry[3].split(':')[0] for entry in found], ['c.md'])

    def test_a_line_outside_the_propagates_to_field_is_not_an_item(self) -> None:
        body = '### A change\n- Type: x\n  - m.md: Pending - not in the field\n'
        self.assertEqual(propagation.open_propagations([('T-1', Content(1, {'kind': 'changelog'}, body))]), [])

    def test_only_contents_of_kind_changelog_are_read(self) -> None:
        self.assertEqual(propagation.open_propagations([('T-1', changelog(1, '  - m.md: Pending - owed', 'report'))]), [])

    def test_a_later_content_naming_the_item_done_closes_it(self) -> None:
        first = ('T-1', changelog(1, '  - m.md: Pending - owed'))
        later = ('T-2', changelog(4, '  - m.md: Done - landed'))
        self.assertEqual(propagation.open_propagations([first, later]), [])

    def test_a_later_content_naming_the_item_rejected_closes_it(self) -> None:
        first = ('T-1', changelog(1, '  - m.md: Pending - owed'))
        later = ('T-1', changelog(2, '  - m.md: Rejected - not wanted'))
        self.assertEqual(propagation.open_propagations([first, later]), [])

    def test_a_later_pending_reopens_a_closed_item(self) -> None:
        contents = [('T-1', changelog(1, '  - m.md: Done - landed')), ('T-1', changelog(2, '  - m.md: Pending - again'))]
        self.assertEqual([entry[1] for entry in propagation.open_propagations(contents)], [2])

    def test_closing_one_item_leaves_the_others_open(self) -> None:
        first = ('T-1', changelog(1, '  - a.md: Pending - owed\n  - b.md: Pending - owed'))
        later = ('T-1', changelog(2, '  - a.md: Done - landed'))
        found = propagation.open_propagations([first, later])
        self.assertEqual([(entry[1], entry[3].split(':')[0]) for entry in found], [(1, 'b.md')])

    def test_code_in_a_body_is_not_read(self) -> None:
        body = '### A change\n```\n- Propagates to:\n  - m.md: Pending - shown\n```\n'
        self.assertEqual(propagation.open_propagations([('T-1', Content(1, {'kind': 'changelog'}, body))]), [])

    def test_the_states_are_those_of_the_propagation_state_catalog(self) -> None:
        self.assertEqual(propagation.STATES, ('Pending', 'Done', 'Rejected'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

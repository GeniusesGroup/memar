#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for printing a text too long for one tool output in ordered parts.

    python bundles/memar/services/machine/tests/console_parts.py

The subject is `machine/console_parts.py`, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
What `memar ai get-task-init-context` and `memar content get-act-context` print through it is
pinned beside them, in `modules-plugable/management/task/tests/start.py` and
`modules-plugable/ai/tests/task_context.py`.

What is pinned, and what each pin is for:

  Whole          A text that fits is printed as it is, with no closing line.
  Bound          Every printed part, its closing line included, is at most
                 the bound; the bound is declared once, below the runtime's
                 cut, and the default is the one the help offers.
  Preferred      With no flag the project's preference is the bound, and
                 with neither the declared one; the flag outranks the
                 preference; a closing line names the bound only when the
                 flag gave it, since the next run reads the same preference.
  TextId         Every part's closing line says "part N of M of text H", H
                 a short hash of the whole unparted text: the same in every
                 part of one text, another for a changed text.
  Joined         The parts, each without its closing line, joined in order,
                 are the text itself, and no body holds a closing line.
  Cuts           A part ends at a passage's end while passages fit; a passage
                 longer than a part is cut at its headings, then at its
                 paragraphs; a paragraph is never cut, and one longer than a
                 part is a part of its own; nothing inside a fence is a cut.
  Closing        Each part but the last ends with the exact command for the
                 next and says to run it now and to read every part before
                 acting; the last says it is the last.
  Stateless      The same inputs print the same parts.
  Refusal        A part that is not there, or a bound too small to hold a
                 closing line, is refused, saying why.
  CommandLine    The flags every parted command takes, and the command a
                 closing line names: the bound only when it is not the
                 default, and the part.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import argparse
import contextlib
import io
import re
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True
import machine.console_parts as console_parts
from machine.console_parts import CLOSING_MARK, MOST_CHARACTERS, TEXT_ID_LENGTH, add_part_arguments, bound, cut, part_text, print_part, text_id
RUNTIME_CUT = 30000

def command(number: int) -> str:
    return f'memar demo --part {number}'

def paragraph(word: str, size: int) -> str:
    """A paragraph of about SIZE characters, ending its line."""
    return ' '.join([word] * max(1, size // (len(word) + 1))) + '\n'

def passage(title: str, *paragraphs: str) -> str:
    return f'--- {title} ---\n' + '\n'.join(paragraphs) + '\n'

def every_part(passages: list[str], most: int) -> list[str]:
    printed = [part_text(passages, 1, most, command)]
    while CLOSING_MARK in printed[-1] and (not is_last(printed[-1])):
        printed.append(part_text(passages, len(printed) + 1, most, command))
    return printed

def is_last(part: str) -> bool:
    return closing(part).startswith(f'{CLOSING_MARK} part') and 'the last' in closing(part)

def closing(part: str) -> str:
    return part[part.rindex(CLOSING_MARK):] if CLOSING_MARK in part else ''

def body(part: str) -> str:
    return part[:part.rindex(CLOSING_MARK)] if CLOSING_MARK in part else part
SMALL = 600
PASSAGES = [passage(f'p{index}', paragraph(f'w{index}', 120), paragraph(f'v{index}', 90)) for index in range(12)]

class Whole(unittest.TestCase):

    def test_a_text_that_fits_is_printed_as_it_is(self) -> None:
        passages = PASSAGES[:2]
        self.assertEqual(part_text(passages, 1, SMALL, command), ''.join(passages))
        self.assertEqual(cut(passages, SMALL), [''.join(passages)])

class Bound(unittest.TestCase):

    def test_every_part_is_at_most_the_bound(self) -> None:
        parts = every_part(PASSAGES, SMALL)
        self.assertGreater(len(parts), 2)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertLessEqual(len(part), SMALL)

    def test_the_default_bound_is_below_the_runtimes_cut(self) -> None:
        self.assertEqual(MOST_CHARACTERS, 24000)
        self.assertLess(MOST_CHARACTERS, RUNTIME_CUT)

class Preferred(unittest.TestCase):

    def test_with_no_flag_and_no_preference_the_bound_is_the_declared_one(self) -> None:
        self.assertEqual(bound(None, None), MOST_CHARACTERS)

    def test_a_preference_changes_the_bound(self) -> None:
        self.assertEqual(bound(None, SMALL), SMALL)

    def test_the_flag_outranks_the_preference(self) -> None:
        self.assertEqual(bound(SMALL, 9000), SMALL)

    def test_a_bound_that_is_not_a_positive_number_is_refused(self) -> None:
        for given, preferred in ((0, None), (None, -5)):
            with self.subTest(given=given, preferred=preferred), self.assertRaises(SystemExit) as refused:
                bound(given, preferred)
            self.assertIn('--most-characters', str(refused.exception.code))

    def test_under_a_preference_parts_keep_to_it_and_name_no_bound(self) -> None:
        parser = argparse.ArgumentParser()
        add_part_arguments(parser, "the demo's preference")
        printed = []
        number = 1
        while True:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                print_part(PASSAGES, parser.parse_args(['--part', str(number)]), ['memar', 'demo'], SMALL)
            printed.append(out.getvalue())
            if is_last(printed[-1]):
                break
            number += 1
        self.assertGreater(len(printed), 2)
        for part in printed:
            self.assertLessEqual(len(part), SMALL)
        self.assertIn('`memar demo --part 2`', closing(printed[0]))
ID_LINE = re.compile(f'^{re.escape(CLOSING_MARK)} part (\\d+) of (\\d+) of text ([0-9a-f]+)[ ,]', re.MULTILINE)

def named(part: str) -> tuple[int, int, str]:
    found = ID_LINE.search(closing(part))
    assert found, f'no part line in {closing(part)!r}'
    return (int(found.group(1)), int(found.group(2)), found.group(3))

class TextId(unittest.TestCase):

    def test_every_part_says_part_n_of_m_of_one_text(self) -> None:
        parts = every_part(PASSAGES, SMALL)
        whole = text_id(''.join(PASSAGES))
        self.assertEqual(len(whole), TEXT_ID_LENGTH)
        for number, part in enumerate(parts, 1):
            with self.subTest(part=number):
                self.assertEqual(named(part), (number, len(parts), whole))
                self.assertTrue(closing(part).startswith(f'{CLOSING_MARK} part {number} of {len(parts)} of text {whole}'))

    def test_a_changed_text_names_another_id_in_every_part(self) -> None:
        changed = [PASSAGES[0].replace('w0', 'x0', 1), *PASSAGES[1:]]
        before = {named(part)[2] for part in every_part(PASSAGES, SMALL)}
        after = {named(part)[2] for part in every_part(changed, SMALL)}
        self.assertEqual(len(before), 1)
        self.assertEqual(len(after), 1)
        self.assertNotEqual(before, after)

    def test_the_id_is_the_texts_alone_not_the_bounds(self) -> None:
        self.assertEqual({named(part)[2] for part in every_part(PASSAGES, SMALL)}, {named(part)[2] for part in every_part(PASSAGES, SMALL * 2)})

class Joined(unittest.TestCase):

    def test_the_parts_joined_are_the_text(self) -> None:
        self.assertEqual(''.join((body(part) for part in every_part(PASSAGES, SMALL))), ''.join(PASSAGES))

    def test_no_body_holds_a_closing_line(self) -> None:
        for part in every_part(PASSAGES, SMALL):
            self.assertNotIn(CLOSING_MARK, body(part))
            self.assertEqual(closing(part).count('\n'), 1)

    def test_the_cut_bodies_joined_are_the_text(self) -> None:
        self.assertEqual(''.join(cut(PASSAGES, SMALL)), ''.join(PASSAGES))

class Cuts(unittest.TestCase):

    def test_while_passages_fit_a_part_ends_at_a_passages_end(self) -> None:
        ends = set()
        position = 0
        for one in PASSAGES:
            position += len(one)
            ends.add(position)
        position = 0
        for one in cut(PASSAGES, SMALL)[:-1]:
            position += len(one)
            self.assertIn(position, ends)

    def test_a_passage_longer_than_a_part_is_cut_at_its_headings(self) -> None:
        sections = [f'## S{index}\n' + paragraph(f's{index}', 100) + '\n' + paragraph(f't{index}', 100) for index in range(8)]
        long = '--- long ---\n' + '\n'.join(sections)
        parts = cut([PASSAGES[0], long, PASSAGES[1]], SMALL)
        inside = [one for one in parts if '## S' in one]
        self.assertGreater(len(inside), 1)
        for one in parts[1:]:
            if one.startswith('## ') or one.startswith('--- '):
                continue
            self.fail(f'a part begins inside a section, not at a heading: {one[:40]!r}')

    def test_a_passage_with_no_heading_is_cut_at_its_paragraphs(self) -> None:
        long = '--- long ---\n' + '\n'.join((paragraph(f'q{index}', 150) for index in range(12)))
        parts = cut([long], SMALL)
        self.assertGreater(len(parts), 1)
        text = long
        position = 0
        for one in parts[:-1]:
            position += len(one)
            self.assertEqual(text[position - 2:position], '\n\n', f'cut not after a blank line at {position}')

    def test_a_paragraph_is_never_cut_and_one_longer_than_a_part_is_a_part_of_its_own(self) -> None:
        huge = paragraph('huge', SMALL * 2)
        long = '--- long ---\n' + paragraph('a', 100) + '\n' + huge + '\n' + paragraph('b', 100)
        parts = cut([long], SMALL)
        self.assertTrue(any((one.strip() == huge.strip() for one in parts)), 'the long paragraph was cut or shared')
        self.assertEqual(''.join(parts), long)

    def test_nothing_inside_a_fence_is_a_cut(self) -> None:
        fenced = '```\n' + '\n'.join((f'# not a heading {index}\n\n' + paragraph(f'c{index}', 60) for index in range(10))) + '```\n'
        long = '--- long ---\n' + paragraph('a', 100) + '\n' + fenced + '\n' + paragraph('b', 100)
        parts = cut([long], SMALL)
        self.assertTrue(any((fenced in one for one in parts)), 'the fence was cut')

class Closing(unittest.TestCase):

    def test_each_part_but_the_last_names_the_next_command_to_run_now(self) -> None:
        parts = every_part(PASSAGES, SMALL)
        for number, part in enumerate(parts[:-1], 1):
            with self.subTest(part=number):
                line = closing(part)
                self.assertIn(f'`{command(number + 1)}`', line)
                self.assertIn(f'part {number} of {len(parts)}', line)
                self.assertIn('now', line)
                self.assertIn('every part', line)
                self.assertTrue(part.endswith('\n'))

    def test_the_last_part_says_it_is_the_last(self) -> None:
        parts = every_part(PASSAGES, SMALL)
        self.assertIn(f'part {len(parts)} of {len(parts)}', closing(parts[-1]))
        self.assertIn('the last', closing(parts[-1]))
        self.assertNotIn('--part', closing(parts[-1]))

class Stateless(unittest.TestCase):

    def test_the_same_inputs_print_the_same_parts(self) -> None:
        self.assertEqual(every_part(PASSAGES, SMALL), every_part(list(PASSAGES), SMALL))

class Refusal(unittest.TestCase):

    def test_a_part_that_is_not_there_is_refused_naming_how_many_there_are(self) -> None:
        count = len(every_part(PASSAGES, SMALL))
        for number in (0, count + 1):
            with self.subTest(number=number), self.assertRaises(SystemExit) as refused:
                part_text(PASSAGES, number, SMALL, command)
            self.assertIn(f'{count} parts', str(refused.exception.code))

    def test_a_bound_too_small_for_a_closing_line_is_refused(self) -> None:
        with self.assertRaises(SystemExit) as refused:
            part_text(PASSAGES, 1, 40, command)
        self.assertIn('--most-characters', str(refused.exception.code))

class CommandLine(unittest.TestCase):

    def parse(self, *words: str) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        add_part_arguments(parser, "the demo's preference")
        return parser.parse_args(words)

    def printed(self, args: argparse.Namespace, passages: list[str]) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            print_part(passages, args, ['memar', 'demo', '--kind', 'x'], None)
        return out.getvalue()

    def test_the_defaults_are_the_first_part_and_no_bound_given(self) -> None:
        args = self.parse()
        self.assertEqual((args.part, args.most_characters), (1, None))

    def test_the_closing_line_names_the_bound_only_when_the_flag_gave_it(self) -> None:
        many = PASSAGES * 60
        default = self.printed(self.parse(), many)
        self.assertIn('`memar demo --kind x --part 2`', closing(default))
        given = self.printed(self.parse('--most-characters', str(SMALL), '--part', '2'), PASSAGES)
        self.assertIn(f'`memar demo --kind x --most-characters {SMALL} --part 3`', closing(given))

    def test_print_part_prints_the_part_as_part_text_gives_it(self) -> None:
        args = self.parse('--most-characters', str(SMALL), '--part', '2')
        expected = part_text(PASSAGES, 2, SMALL, console_parts.next_command(['memar', 'demo', '--kind', 'x'], SMALL))
        self.assertEqual(self.printed(args, PASSAGES), expected)
if __name__ == '__main__':
    unittest.main(verbosity=2)

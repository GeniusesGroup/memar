#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the bytes of a text file judged, in `modules/knowledge/text/services/text_check.py`.

    python modules/knowledge/text/tests/text_check.py

The subject is the text domain's half of `memar content check`: what holds for
every text file in every project whatever the file is for, the encoding and the
newlines. The Markdown conventions are the documentation module's and are not
tested here. Named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md), in the
`tests/` folder of the shelf that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

What is pinned: a clean file has no problem and its text is returned; a BOM, bytes that are
not UTF-8, a replacement character, mixed line endings, a missing final newline and a mojibake
fingerprint are each reported; a file that is not UTF-8 returns no text, so nothing more is judged of it.
"""
from __future__ import annotations
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path[0:0] = [str(TOP), str(TOP / 'bundles' / 'memar'), str(TOP / 'bundles' / 'memar' / 'services')]
from modules.knowledge.text.services.text_check import file_problems


class FileProblems(unittest.TestCase):

    def judged(self, raw: bytes, name: str = 'file.txt'):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / name
            path.write_bytes(raw)
            return file_problems(path)

    def test_a_clean_file_has_no_problem_and_returns_its_text(self) -> None:
        self.assertEqual(self.judged(b'one\ntwo\n'), ([], 'one\ntwo\n'))

    def test_a_bom_is_reported_and_the_text_is_returned_without_it(self) -> None:
        problems, text = self.judged(b'\xef\xbb\xbfone\n')
        self.assertEqual(text, 'one\n')
        self.assertEqual(len(problems), 1)
        self.assertIn('BOM', problems[0])

    def test_bytes_that_are_not_utf8_return_no_text(self) -> None:
        problems, text = self.judged(b'\xff\xfe\n')
        self.assertIsNone(text)
        self.assertIn('not valid UTF-8', problems[0])

    def test_mixed_line_endings_are_reported_with_their_counts(self) -> None:
        problems, _text = self.judged(b'one\r\ntwo\nthree\n')
        self.assertEqual(len(problems), 1)
        self.assertIn('1 CRLF and 2 LF', problems[0])

    def test_a_missing_final_newline_is_reported(self) -> None:
        self.assertEqual(self.judged(b'one')[0], ['no newline at end of file'])

    def test_a_replacement_character_is_reported_with_its_line(self) -> None:
        problems, _text = self.judged('one\ntw\ufffd\n'.encode('utf-8'))
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith('line 2: U+FFFD'))

    def test_a_mojibake_fingerprint_is_a_hint_in_the_problems(self) -> None:
        raw = ('caf' + '\u00e2\u20ac' + '\n').encode('utf-8')
        problems, _text = self.judged(raw)
        self.assertEqual(len(problems), 1)
        self.assertTrue(problems[0].startswith('likely mojibake'))

    def test_an_empty_file_is_reported(self) -> None:
        self.assertEqual(self.judged(b'')[0], ['file is empty'])

    def test_a_readme_that_is_only_a_link_stand_in_has_no_problem_and_no_text(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / 'target.md').write_text('# Target\n', encoding='utf-8')
            readme = Path(folder) / 'README.md'
            readme.write_bytes(b'target.md')
            self.assertEqual(file_problems(readme), ([], None))


if __name__ == '__main__':
    unittest.main(verbosity=2)

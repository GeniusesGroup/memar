#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the byte check of a text, `modules/knowledge/text/services/text_bytes_check.py`.

    python modules/knowledge/text/tests/text_bytes_check.py

The subject is `Text_Check` (`services/text-check/text-check.kh`) and its refusals in `errors/bytes.kh`: the
first fault of the bytes of a text that holds for every text is a refusal of its own.
"""
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
check = import_module('modules.knowledge.text.services.text_bytes_check')
errors = import_module('modules.knowledge.text.errors.bytes')
structure = import_module('modules.knowledge.text.errors.structure')


class Check(unittest.TestCase):

    def test_a_clean_text_passes(self) -> None:
        check.check_text('one\ntwo\n')
        check.check_text('one\r\ntwo\r\n')

    def test_a_byte_order_mark_is_refused(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_Bom):
            check.check_text('﻿one\n')

    def test_a_replacement_character_is_refused(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_Replacement):
            check.check_text('a � b\n')

    def test_the_marks_of_mojibake_are_refused(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_Mojibake):
            check.check_text('itâ€™s\n')

    def test_mixed_line_endings_are_refused(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_MixedEndings):
            check.check_text('one\r\ntwo\n')

    def test_a_missing_final_newline_is_refused(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_NoFinalNewline):
            check.check_text('one')

    def test_bytes_that_are_not_utf8_are_refused_on_decoding(self) -> None:
        with self.assertRaises(errors.Text_Error_Bytes_NotUtf8):
            check.decode_text(b'\xff\xfe\x00')

    def test_bytes_are_decoded_without_dropping_a_mark(self) -> None:
        self.assertEqual(check.decode_text(b'\xef\xbb\xbfx\n'), '﻿x\n')
        self.assertEqual(check.decode_text('a\n'.encode('utf-8')), 'a\n')


class Substance(unittest.TestCase):

    def test_a_text_with_a_line_that_is_no_heading_passes(self) -> None:
        check.check_substance('# Plan\n\nBody\n')
        check.check_substance('x\n')

    def test_a_text_of_only_headings_and_blank_lines_is_refused(self) -> None:
        for text in ('', '\n', '\n\n  \n', '# Plan\n', '# Plan\n\n## Part\n  ### Deep\n'):
            with self.assertRaises(structure.Text_Error_Structure_Empty):
                check.check_substance(text)


if __name__ == '__main__':
    unittest.main()

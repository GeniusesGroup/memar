#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
BUDGET_SECONDS = 60
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
for _folder in (TOP, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
mark_module = import_module('modules-plugable.computer.codec.string.utf8.services.utf8_byte_order_mark')
codec_module = import_module('modules-plugable.computer.codec.string.utf8.services.utf8_codec')
utf8_errors = import_module('modules-plugable.computer.codec.string.utf8.errors.errors')
text_errors = import_module('modules.knowledge.text.errors.edit')
MARK = b'\xef\xbb\xbf'


class ByteOrderMark(unittest.TestCase):

    def setUp(self) -> None:
        self.mark = mark_module.UTF8_ByteOrderMark()

    def test_bytes_that_begin_with_the_mark_have_it(self) -> None:
        self.assertTrue(self.mark.detect(MARK + b'# A\n'))
        self.assertTrue(self.mark.detect(MARK))

    def test_bytes_that_do_not_begin_with_the_mark_do_not(self) -> None:
        self.assertFalse(self.mark.detect(b'# A\n'))
        self.assertFalse(self.mark.detect(b''))
        self.assertFalse(self.mark.detect(b'a' + MARK))

    def test_strip_answers_the_rest_and_whether_the_mark_was_there(self) -> None:
        self.assertEqual(self.mark.strip(MARK + b'# A\n'), (b'# A\n', True))
        self.assertEqual(self.mark.strip(b'# A\n'), (b'# A\n', False))
        self.assertEqual(self.mark.strip(b''), (b'', False))

    def test_only_a_leading_mark_is_one(self) -> None:
        self.assertEqual(self.mark.strip(b'a' + MARK + b'b'), (b'a' + MARK + b'b', False))

    def test_only_one_leading_mark_is_stripped(self) -> None:
        self.assertEqual(self.mark.strip(MARK + MARK + b'x'), (MARK + b'x', True))


class Decode(unittest.TestCase):

    def setUp(self) -> None:
        self.codec = codec_module.UTF8_Codec()

    def test_valid_bytes_are_decoded_and_no_mark_is_reported(self) -> None:
        self.assertEqual(self.codec.decode('# Ünï\n'.encode('utf-8')), ('# Ünï\n', False))

    def test_a_leading_mark_is_removed_and_reported(self) -> None:
        self.assertEqual(self.codec.decode(MARK + b'# A\n'), ('# A\n', True))

    def test_bytes_that_are_not_valid_are_refused_and_never_replaced(self) -> None:
        with self.assertRaises(utf8_errors.UTF8_Error_NotUtf8):
            self.codec.decode(b'caf\xe9\n')

    def test_the_refusal_is_the_text_domains(self) -> None:
        self.assertTrue(issubclass(utf8_errors.UTF8_Error_NotUtf8, text_errors.Text_Error_Edit_NotUtf8))
        self.assertTrue(issubclass(utf8_errors.UTF8_Error_NotUtf8, text_errors.Text_Error_Edit_Refusal))


class DecodeBare(unittest.TestCase):

    def setUp(self) -> None:
        self.codec = codec_module.UTF8_Codec()

    def test_a_leading_mark_stays_as_the_character_u_feff(self) -> None:
        self.assertEqual(self.codec.decode_bare(MARK + b'# A\n'), '﻿# A\n')

    def test_valid_bytes_are_decoded(self) -> None:
        self.assertEqual(self.codec.decode_bare('ü\n'.encode('utf-8')), 'ü\n')

    def test_bytes_that_are_not_valid_are_a_refusal(self) -> None:
        with self.assertRaises(utf8_errors.UTF8_Error_NotUtf8) as refused:
            self.codec.decode_bare(b'caf\xe9')
        self.assertIsInstance(refused.exception, text_errors.Text_Error_Edit_Refusal)


class DecodeNamed(unittest.TestCase):

    def setUp(self) -> None:
        self.codec = codec_module.UTF8_Codec()

    def test_a_leading_mark_stays_as_the_character_u_feff(self) -> None:
        self.assertEqual(self.codec.decode_named(MARK + b'x'), '﻿x')

    def test_valid_bytes_are_decoded(self) -> None:
        self.assertEqual(self.codec.decode_named('# Ünï'.encode('utf-8')), '# Ünï')

    def test_bytes_that_are_not_valid_are_a_failure_and_not_a_refusal(self) -> None:
        with self.assertRaises(utf8_errors.UTF8_Error_NamedTextNotUtf8) as failed:
            self.codec.decode_named(b'caf\xe9')
        self.assertIsInstance(failed.exception, text_errors.Text_Error_Edit_NamedTextNotUtf8)
        self.assertNotIsInstance(failed.exception, text_errors.Text_Error_Edit_Refusal)


class Encode(unittest.TestCase):

    def setUp(self) -> None:
        self.codec = codec_module.UTF8_Codec()

    def test_a_text_is_encoded_without_a_mark(self) -> None:
        data = self.codec.encode('# Ünï\n')
        self.assertEqual(data, '# Ünï\n'.encode('utf-8'))
        self.assertFalse(data.startswith(MARK))

    def test_a_text_decoded_and_encoded_again_is_the_same_text(self) -> None:
        text, _ = self.codec.decode(MARK + 'ü\n'.encode('utf-8'))
        self.assertEqual(self.codec.encode(text), 'ü\n'.encode('utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

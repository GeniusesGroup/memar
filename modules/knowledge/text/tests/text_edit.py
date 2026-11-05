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
edit_module = import_module('modules.knowledge.text.services.text_edit')
rule_module = import_module('modules.knowledge.text.services.text_line_ending_rule')
errors = import_module('modules.knowledge.text.errors.edit')
MARK = b'\xef\xbb\xbf'


class LineEnding:

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def get_sequence(self) -> str:
        return self.sequence


class Choice:

    def __init__(self, line_ending=None) -> None:
        self.line_ending = line_ending

    def is_given(self) -> bool:
        return self.line_ending is not None

    def get_line_ending(self):
        return self.line_ending


NO_CHOICE = Choice()
LF = Choice(LineEnding('\n'))
CRLF = Choice(LineEnding('\r\n'))


class Limits:

    def get_wait_seconds(self) -> float:
        return 1.0

    def get_stale_seconds(self) -> float:
        return 1.0

    def get_poll_seconds(self) -> float:
        return 0.05


class Store:

    def __init__(self, data, log: list | None = None, name: str = 'store') -> None:
        self.data = data
        self.log = [] if log is None else log
        self.name = name
        self.version = 0
        self.read_fails = False
        self.write_fails = False

    def exists(self) -> bool:
        return self.data is not None

    def get_bytes(self) -> bytes:
        self.log.append(f'{self.name}.get_bytes')
        if self.read_fails:
            raise errors.Text_Error_Edit_ReadFailed('cannot read')
        return self.data

    def replace_bytes(self, data: bytes) -> None:
        self.log.append(f'{self.name}.replace_bytes')
        if self.write_fails:
            raise errors.Text_Error_Edit_WriteFailed('cannot write')
        self.data = data
        self.version += 1

    def get_stamp(self):
        return (self.data, self.version)


class Codec:

    def decode(self, data: bytes):
        had = data.startswith(MARK)
        return (self.decode_bare(data[len(MARK):] if had else data), had)

    def decode_bare(self, data: bytes) -> str:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as error:
            raise errors.Text_Error_Edit_NotUtf8(str(error)) from None

    def decode_named(self, data: bytes) -> str:
        try:
            return data.decode('utf-8')
        except UnicodeDecodeError as error:
            raise errors.Text_Error_Edit_NamedTextNotUtf8(str(error)) from None

    def encode(self, text: str) -> bytes:
        return text.encode('utf-8')


class Held:

    def __init__(self, log: list) -> None:
        self.log = log

    def release(self) -> None:
        self.log.append('release')


class Lock:

    def __init__(self, log: list, fails=None) -> None:
        self.log = log
        self.fails = fails
        self.taken = []

    def take(self, store, writer, summary, limits):
        self.log.append('take')
        self.taken.append((store, writer, summary, limits))
        if self.fails is not None:
            raise self.fails('lock')
        return Held(self.log)


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.log: list = []
        self.service = edit_module.Text_Edit()
        self.rule = rule_module.Text_LineEnding_Rule()
        self.codec = Codec()
        self.limits = Limits()
        self.lock = Lock(self.log)

    def store(self, data) -> Store:
        return Store(data, self.log)

    def replace(self, store, old, new, every=False, choice=NO_CHOICE, lock=None):
        return self.service.replace(store, old, new, every, choice, self.rule, self.codec, lock or self.lock, self.limits, 'writer-1')

    def write(self, store, text, choice=NO_CHOICE, create=False, lock=None):
        return self.service.write(store, text, choice, create, self.rule, self.codec, lock or self.lock, self.limits, 'writer-1')

    def write_from(self, store, source, choice=NO_CHOICE, create=False, lock=None):
        return self.service.write_from(store, source, choice, create, self.rule, self.codec, lock or self.lock, self.limits, 'writer-1')


class ReplaceReplacesExactText(Fixture):

    def test_a_unique_text_is_replaced_and_one_replacement_is_answered(self) -> None:
        store = self.store(b'# Notes\n\nBody\n')
        replacements, had_mark = self.replace(store, '# Notes', '# Renamed')
        self.assertEqual(replacements, 1)
        self.assertFalse(had_mark)
        self.assertEqual(store.data, b'# Renamed\n\nBody\n')

    def test_an_empty_replacement_is_allowed(self) -> None:
        store = self.store(b'# Notes\n\nBody\n')
        self.assertEqual(self.replace(store, '\nBody', '')[0], 1)
        self.assertEqual(store.data, b'# Notes\n\n')

    def test_every_replaces_each_occurrence_and_answers_how_many(self) -> None:
        store = self.store(b'a b a b a\n')
        self.assertEqual(self.replace(store, 'a', 'z', every=True)[0], 3)
        self.assertEqual(store.data, b'z b z b z\n')

    def test_a_byte_order_mark_is_removed_and_reported(self) -> None:
        store = self.store(MARK + b'# Notes\n')
        replacements, had_mark = self.replace(store, '# Notes', '# Renamed')
        self.assertEqual((replacements, had_mark), (1, True))
        self.assertEqual(store.data, b'# Renamed\n')

    def test_the_line_ending_of_the_held_text_is_kept_without_a_choice(self) -> None:
        store = self.store(b'# Notes\r\n\r\nBody\r\n')
        self.replace(store, 'Body', 'Text')
        self.assertEqual(store.data, b'# Notes\r\n\r\nText\r\n')

    def test_the_line_ending_asked_for_is_the_one_written(self) -> None:
        store = self.store(b'# Notes\n\nBody\n')
        self.replace(store, 'Body', 'Text', choice=CRLF)
        self.assertEqual(store.data, b'# Notes\r\n\r\nText\r\n')
        self.replace(store, 'Text', 'Back', choice=LF)
        self.assertEqual(store.data, b'# Notes\n\nBack\n')

    def test_a_final_newline_is_guaranteed(self) -> None:
        store = self.store(b'# Notes\nBody')
        self.replace(store, 'Body', 'Text')
        self.assertEqual(store.data, b'# Notes\nText\n')

    def test_the_read_the_match_and_the_write_happen_under_the_lock_and_it_is_released(self) -> None:
        store = self.store(b'# Notes\n')
        self.replace(store, '# Notes', '# Renamed')
        self.assertEqual(self.log, ['take', 'store.get_bytes', 'store.replace_bytes', 'release'])
        taken_store, writer, summary, limits = self.lock.taken[0]
        self.assertIs(taken_store, store)
        self.assertEqual(writer, 'writer-1')
        self.assertIs(limits, self.limits)
        self.assertTrue(summary)


class ReplaceRefuses(Fixture):

    def refused(self, refusal, data, old, new, **keywords) -> None:
        store = self.store(data)
        with self.assertRaises(refusal):
            self.replace(store, old, new, **keywords)
        self.assertEqual(store.data, data)
        self.assertNotIn('store.replace_bytes', self.log)
        self.assertEqual(self.log.count('take'), self.log.count('release'))

    def test_an_absent_match_is_refused_and_nothing_is_written(self) -> None:
        self.refused(errors.Text_Error_Edit_MatchAbsent, b'# Notes\n', '# Absent', 'x')

    def test_an_ambiguous_match_is_refused_unless_every_is_asked_for(self) -> None:
        self.refused(errors.Text_Error_Edit_MatchAmbiguous, b'a a\n', 'a', 'z')

    def test_an_empty_text_to_replace_is_refused(self) -> None:
        self.refused(errors.Text_Error_Edit_OldEmpty, b'# Notes\n', '', 'x')

    def test_a_held_text_that_is_not_valid_is_refused(self) -> None:
        self.refused(errors.Text_Error_Edit_NotUtf8, b'caf\xe9\n', 'caf', 'x')

    def test_a_text_that_is_not_held_is_refused(self) -> None:
        store = self.store(None)
        with self.assertRaises(errors.Text_Error_Edit_TextAbsent):
            self.replace(store, 'a', 'b')
        self.assertFalse(store.exists())

    def test_a_refusal_is_a_refusal_and_a_failure_is_not(self) -> None:
        for refusal in (errors.Text_Error_Edit_MatchAbsent, errors.Text_Error_Edit_MatchAmbiguous, errors.Text_Error_Edit_OldEmpty, errors.Text_Error_Edit_EmptyText, errors.Text_Error_Edit_CreateNotAsked, errors.Text_Error_Edit_TextAbsent, errors.Text_Error_Edit_NotUtf8):
            self.assertTrue(issubclass(refusal, errors.Text_Error_Edit_Refusal))
        for failure in (errors.Text_Error_Edit_ReadFailed, errors.Text_Error_Edit_WriteFailed, errors.Text_Error_Edit_Locked, errors.Text_Error_Edit_LockUnwritable, errors.Text_Error_Edit_ChangedWhileWaiting, errors.Text_Error_Edit_NamedTextNotUtf8):
            self.assertFalse(issubclass(failure, errors.Text_Error_Edit_Refusal))


class ReplaceFails(Fixture):

    def test_a_read_that_fails_is_a_failure_and_the_lock_is_released(self) -> None:
        store = self.store(b'# Notes\n')
        store.read_fails = True
        with self.assertRaises(errors.Text_Error_Edit_ReadFailed):
            self.replace(store, '# Notes', 'x')
        self.assertEqual(self.log, ['take', 'store.get_bytes', 'release'])

    def test_a_write_that_fails_is_a_failure_and_the_lock_is_released(self) -> None:
        store = self.store(b'# Notes\n')
        store.write_fails = True
        with self.assertRaises(errors.Text_Error_Edit_WriteFailed):
            self.replace(store, '# Notes', 'x')
        self.assertEqual(self.log[-1], 'release')
        self.assertEqual(store.data, b'# Notes\n')

    def test_a_lock_that_fails_stops_the_edit_before_the_text_is_read(self) -> None:
        for failure in (errors.Text_Error_Edit_Locked, errors.Text_Error_Edit_LockUnwritable, errors.Text_Error_Edit_ChangedWhileWaiting):
            with self.subTest(failure=failure.__name__):
                self.log.clear()
                store = self.store(b'# Notes\n')
                with self.assertRaises(failure):
                    self.replace(store, '# Notes', 'x', lock=Lock(self.log, failure))
                self.assertEqual(self.log, ['take'])
                self.assertEqual(store.data, b'# Notes\n')


class WritePutsAWholeText(Fixture):

    def test_a_text_is_written_as_utf8_without_a_mark_and_the_size_is_answered(self) -> None:
        store = self.store(b'# Notes\n')
        size, had_mark = self.write(store, '# Ünï\n')
        self.assertEqual(store.data, '# Ünï\n'.encode('utf-8'))
        self.assertEqual(size, len(store.data))
        self.assertFalse(had_mark)

    def test_a_final_newline_is_added(self) -> None:
        store = self.store(b'# Notes\n')
        self.write(store, '# A')
        self.assertEqual(store.data, b'# A\n')

    def test_a_text_that_is_not_held_needs_create_and_gets_lf(self) -> None:
        store = self.store(None)
        self.write(store, '# A\n\nB\n', create=True)
        self.assertEqual(store.data, b'# A\n\nB\n')

    def test_a_byte_order_mark_in_the_held_text_is_removed_and_reported(self) -> None:
        store = self.store(MARK + b'# Notes\n')
        _, had_mark = self.write(store, '# New\n')
        self.assertTrue(had_mark)
        self.assertEqual(store.data, b'# New\n')

    def test_the_line_ending_asked_for_is_written_and_the_held_texts_own_is_kept_otherwise(self) -> None:
        store = self.store(b'# Notes\n')
        self.write(store, '# A\n\nB\n', choice=CRLF)
        self.assertEqual(store.data, b'# A\r\n\r\nB\r\n')
        self.write(store, '# A\n\nB\n', choice=LF)
        self.assertEqual(store.data, b'# A\n\nB\n')
        store.data = b'# Old\r\n'
        self.write(store, '# A\n\nB\n')
        self.assertEqual(store.data, b'# A\r\n\r\nB\r\n')

    def test_the_write_is_taken_under_the_lock_and_it_is_released(self) -> None:
        store = self.store(b'# Notes\n')
        self.write(store, '# Later\n')
        self.assertEqual(self.log[0], 'take')
        self.assertEqual(self.log[-1], 'release')
        self.assertIn('store.replace_bytes', self.log)


class WriteRefuses(Fixture):

    def test_a_text_that_is_not_held_is_not_created_unless_asked_for(self) -> None:
        store = self.store(None)
        with self.assertRaises(errors.Text_Error_Edit_CreateNotAsked):
            self.write(store, 'x\n')
        self.assertFalse(store.exists())

    def test_an_empty_or_blank_text_is_refused_and_the_held_text_is_kept(self) -> None:
        for text in ('', '  \n\t\n'):
            with self.subTest(text=text):
                store = self.store(b'# Notes\n')
                with self.assertRaises(errors.Text_Error_Edit_EmptyText):
                    self.write(store, text)
                self.assertEqual(store.data, b'# Notes\n')

    def test_a_held_text_that_is_not_valid_is_refused(self) -> None:
        store = self.store(b'caf\xe9\n')
        with self.assertRaises(errors.Text_Error_Edit_NotUtf8):
            self.write(store, '# New\n')
        self.assertEqual(store.data, b'caf\xe9\n')
        self.assertEqual(self.log.count('take'), self.log.count('release'))

    def test_a_blank_text_is_refused_even_when_creating(self) -> None:
        store = self.store(None)
        with self.assertRaises(errors.Text_Error_Edit_EmptyText):
            self.write(store, ' \n', create=True)
        self.assertFalse(store.exists())


class WriteFails(Fixture):

    def test_a_write_that_fails_is_a_failure_and_not_a_refusal(self) -> None:
        store = self.store(None)
        store.write_fails = True
        with self.assertRaises(errors.Text_Error_Edit_WriteFailed) as failed:
            self.write(store, 'x\n', create=True)
        self.assertNotIsInstance(failed.exception, errors.Text_Error_Edit_Refusal)
        self.assertEqual(self.log[-1], 'release')

    def test_a_lock_that_fails_stops_the_write_before_anything_is_written(self) -> None:
        for failure in (errors.Text_Error_Edit_Locked, errors.Text_Error_Edit_LockUnwritable, errors.Text_Error_Edit_ChangedWhileWaiting):
            with self.subTest(failure=failure.__name__):
                store = self.store(b'# Notes\n')
                with self.assertRaises(failure):
                    self.write(store, '# New\n', lock=Lock([], failure))
                self.assertEqual(store.data, b'# Notes\n')


class WriteFromPutsTheTextOfASource(Fixture):

    def test_the_text_of_the_source_is_written(self) -> None:
        store = self.store(b'# Notes\n')
        source = Store('# From disk ü\n'.encode('utf-8'), self.log, 'source')
        size, _ = self.write_from(store, source)
        self.assertEqual(store.data, '# From disk ü\n'.encode('utf-8'))
        self.assertEqual(size, len(store.data))

    def test_a_leading_mark_in_the_source_stays_as_the_character_u_feff(self) -> None:
        store = self.store(b'# Notes\n')
        source = Store(MARK + b'# Marked\n', self.log, 'source')
        self.write_from(store, source)
        self.assertEqual(store.data, MARK + b'# Marked\n')

    def test_a_source_that_is_not_valid_is_a_refusal_and_nothing_is_written(self) -> None:
        store = self.store(b'# Notes\n')
        source = Store(b'caf\xe9\n', self.log, 'source')
        with self.assertRaises(errors.Text_Error_Edit_NotUtf8):
            self.write_from(store, source)
        self.assertEqual(store.data, b'# Notes\n')

    def test_a_source_that_cannot_be_read_is_a_failure(self) -> None:
        store = self.store(b'# Notes\n')
        source = Store(b'x\n', self.log, 'source')
        source.read_fails = True
        with self.assertRaises(errors.Text_Error_Edit_ReadFailed):
            self.write_from(store, source)
        self.assertEqual(store.data, b'# Notes\n')

    def test_the_refusals_of_a_write_hold_for_a_write_from(self) -> None:
        store = self.store(None)
        with self.assertRaises(errors.Text_Error_Edit_CreateNotAsked):
            self.write_from(store, Store(b'x\n', self.log, 'source'))
        with self.assertRaises(errors.Text_Error_Edit_EmptyText):
            self.write_from(self.store(b'# Notes\n'), Store(b' \n', self.log, 'source'))


if __name__ == '__main__':
    unittest.main(verbosity=2)

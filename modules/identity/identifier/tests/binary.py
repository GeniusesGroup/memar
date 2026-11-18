# For license and copyright information please see the LEGAL file in the code repository

import io
import unittest
from unittest.mock import Mock

from modules.identity.identifier.value import IdentifierValue
from modules.identity.identifier.tests.value import time_view
from modules.identity.identifier.tests.time_coordinate import REFERENCE
from modules.identity.identifier.errors.already_initialized import Identifier_Error_AlreadyInitialized
from modules.identity.identifier.errors.not_initialized import Identifier_Error_NotInitialized
from modules.identity.identifier.errors.not_decodable import Identifier_Error_NotDecodable
from modules.identity.identifier.errors.buffer_failure import Identifier_Error_BufferFailure

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier binary retained-value codec"
CONTRACT = "modules/identity/identifier/protocol/identifier.codec.binary.eng.kh"


class BinaryExpectations(unittest.TestCase):
    def make(self, view=time_view):
        mint = Mock(side_effect=AssertionError("decode minted"))
        self.addCleanup(mint.assert_not_called)
        return IdentifierValue(mint, view, REFERENCE)

    def test_exact_network_order_and_framing(self):
        number = 0x01020304050607081112131415161718
        value = self.make()
        source = io.BytesIO(b"pre" + bytes.fromhex("01020304050607081112131415161718") + b"tail")
        source.seek(3)
        value.decode(source)
        self.assertEqual(source.read(), b"tail")
        self.assertEqual(value.read_value(), number)
        target = io.BytesIO(b"head")
        target.seek(4)
        value.encode(target)
        self.assertEqual(target.getvalue(), b"head" + number.to_bytes(16, "big"))

    def test_boundaries_preserve_every_bit(self):
        for number in (0, 1, (1 << 64) - 1, 1 << 64, (1 << 127), (1 << 128) - 1):
            with self.subTest(number=number):
                value = self.make()
                value.decode(io.BytesIO(number.to_bytes(16, "big")))
                target = io.BytesIO()
                value.encode(target)
                self.assertEqual(target.getvalue(), number.to_bytes(16, "big"))
                self.assertFalse(value.is_empty())

    def test_empty_encode_and_filled_decode_refuse_before_io(self):
        value = self.make()
        target = Mock()
        with self.assertRaises(Identifier_Error_NotInitialized):
            value.encode(target)
        target.write.assert_not_called()
        value.load(0)
        source = Mock()
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.decode(source)
        source.read.assert_not_called()
        self.assertEqual(value.read_value(), 0)

    def test_length_and_media_type_do_not_issue(self):
        value = self.make()
        self.assertEqual(value.get_serialization_length(), 16)
        self.assertEqual(value.get_media_type(), "application/octet-stream")
        self.assertTrue(value.is_empty())

    def test_short_reads_accumulate_only_remaining_bytes(self):
        source = Mock()
        source.read.side_effect = [b"abc", b"defgh", b"ijklmnop"]
        value = self.make()
        value.decode(source)
        self.assertEqual(value.read_value().to_bytes(16, "big"), b"abcdefghijklmnop")
        self.assertEqual([call.args for call in source.read.call_args_list], [(16,), (13,), (8,)])

    def test_incomplete_or_malformed_reads_leave_empty(self):
        for result in (b"", None, "x", bytearray(16), bytes(17), 4):
            with self.subTest(result=result):
                source = Mock()
                source.read.side_effect = [b"a", result]
                value = self.make()
                with self.assertRaises(Identifier_Error_NotDecodable):
                    value.decode(source)
                self.assertTrue(value.is_empty())
                value.decode(io.BytesIO(bytes(16)))
                self.assertEqual(value.read_value(), 0)

    def test_all_truncations_refuse(self):
        for length in range(16):
            with self.subTest(length=length):
                value = self.make()
                with self.assertRaises(Identifier_Error_NotDecodable):
                    value.decode(io.BytesIO(bytes(length)))
                self.assertTrue(value.is_empty())

    def test_short_writes_retry_unacknowledged_suffix(self):
        value = self.make()
        value.load(int.from_bytes(b"abcdefghijklmnop", "big"))
        target = Mock()
        target.write.side_effect = [3, 5, 8]
        value.encode(target)
        self.assertEqual([call.args for call in target.write.call_args_list],
                         [(b"abcdefghijklmnop",), (b"defghijklmnop",), (b"ijklmnop",)])

    def test_bad_write_progress_refuses_without_identity_change(self):
        for progress in (None, 0, -1, 17, True, 1.0, "1"):
            with self.subTest(progress=progress):
                value = self.make()
                value.load(7)
                target = Mock()
                target.write.return_value = progress
                with self.assertRaises(Identifier_Error_BufferFailure):
                    value.encode(target)
                self.assertEqual(target.write.call_count, 1)
                self.assertEqual(value.read_value(), 7)

    def test_buffer_failures_propagate_and_do_not_publish(self):
        refusal = OSError("binding refused")
        source = Mock()
        source.read.side_effect = [b"x", refusal]
        value = self.make()
        with self.assertRaises(OSError) as caught:
            value.decode(source)
        self.assertIs(caught.exception, refusal)
        self.assertTrue(value.is_empty())
        value.load(8)
        target = Mock()
        target.write.side_effect = [2, refusal]
        with self.assertRaises(OSError) as caught:
            value.encode(target)
        self.assertIs(caught.exception, refusal)
        self.assertEqual(value.read_value(), 8)

    def test_time_view_failure_publishes_nothing(self):
        refusal = OSError("time view refused")
        value = self.make(Mock(side_effect=refusal))
        with self.assertRaises(OSError) as caught:
            value.decode(io.BytesIO(bytes(16)))
        self.assertIs(caught.exception, refusal)
        self.assertTrue(value.is_empty())


if __name__ == "__main__":
    unittest.main()

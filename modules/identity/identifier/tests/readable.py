# For license and copyright information please see the LEGAL file in the code repository

import io
import random
import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import Mock

from modules.identity.identifier.readable import encode_readable, decode_readable
from modules.identity.identifier.value import IdentifierValue
from modules.computer.codec.string.errors.not_supported import Stringer_Error_NotSupported
from modules.identity.identifier.errors.invalid_value import Identifier_Error_InvalidValue
from modules.identity.identifier.tests.value import time_view
from modules.identity.identifier.tests.time_coordinate import REFERENCE
from modules.identity.identifier.errors.already_initialized import Identifier_Error_AlreadyInitialized
from modules.identity.identifier.errors.not_initialized import Identifier_Error_NotInitialized
from modules.identity.identifier.errors.not_decodable import Identifier_Error_NotDecodable
from modules.identity.identifier.errors.value import Identifier_Error_InvalidBytes

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier optional reversible readable profile"
CONTRACT = "modules/identity/identifier/protocol/identifier.eng.kh"
ZERO = "19700101-T000000.000000000Z-0000000000000000"


class ReadableExpectations(unittest.TestCase):
    def make(self, view=time_view, **bindings):
        mint = Mock(side_effect=AssertionError("parse minted"))
        self.addCleanup(mint.assert_not_called)
        return IdentifierValue(mint, view, REFERENCE, **bindings)

    def test_epoch_and_maximum_fixed_vectors(self):
        for raw, text in (
            (bytes(16), ZERO),
            (((1 << 128) - 1).to_bytes(16, "big"), "25540721-T233433.709551615Z-FFFFFFFFFFFFFFFF"),
            (((1 << 64) | 0x17BA988ED5072891).to_bytes(16, "big"), "19700101-T000000.000000001Z-17BA988ED5072891"),
            ((946684800000000000 << 64).to_bytes(16, "big"), "20000101-T000000.000000000Z-0000000000000000"),
        ):
            with self.subTest(text=text):
                self.assertEqual(encode_readable(raw), text)
                self.assertEqual(decode_readable(text), raw)

    def test_full_range_roundtrips_without_float_or_microsecond_loss(self):
        source = random.Random(42)
        numbers = [source.getrandbits(128) for _ in range(2000)]
        numbers += [(coordinate << 64) | tail for coordinate in (0, 1, 999999999, 1000000000, (1 << 64) - 1)
                    for tail in (0, 1, (1 << 64) - 1)]
        for number in numbers:
            with self.subTest(number=number):
                raw = number.to_bytes(16, "big")
                text = encode_readable(raw)
                self.assertEqual(len(text), 44)
                self.assertTrue(text.isascii())
                self.assertEqual(decode_readable(text), raw)

    def test_valid_leap_date_and_nanosecond_carry_boundary(self):
        before = decode_readable("20000229-T235959.999999999Z-0123456789ABCDEF")
        after = decode_readable("20000301-T000000.000000000Z-0123456789ABCDEF")
        self.assertEqual((int.from_bytes(after, "big") >> 64) - (int.from_bytes(before, "big") >> 64), 1)

    def test_invalid_forms_are_not_guessed_or_normalized(self):
        bad = [
            "", ZERO + "\n", " " + ZERO, ZERO.lower(), ZERO.replace("T", "t"),
            ZERO.replace("Z", "+0000"), ZERO.replace(".000000000", ".000000"),
            ZERO[:-1], ZERO + "0", ZERO.replace("1970", "۱۹۷۰"),
            "19700101-T000000.000000000Z-abcdef0123456789",
            "19700101-T000000.000000000Z-000000000000000G",
            "20261115-T124949Z-5000", "00000000-0000-0000-0000-000000000000",
            "19691231-T235959.999999999Z-0000000000000000",
            "25540721-T233433.709551616Z-0000000000000000",
            "99991231-T235959.999999999Z-0000000000000000",
            "21000229-T000000.000000000Z-0000000000000000",
            "20230229-T000000.000000000Z-0000000000000000",
            "20000431-T000000.000000000Z-0000000000000000",
            "20001301-T000000.000000000Z-0000000000000000",
            "20000100-T000000.000000000Z-0000000000000000",
            "20000101-T240000.000000000Z-0000000000000000",
            "20000101-T006000.000000000Z-0000000000000000",
            "20161231-T235960.000000000Z-0000000000000000",
            None, bytes(44), 0, True,
        ]
        for text in bad:
            with self.subTest(text=text):
                with self.assertRaises(Identifier_Error_NotDecodable):
                    decode_readable(text)

    def test_encoder_requires_complete_immutable_identity(self):
        for raw in (b"", bytes(15), bytes(17), bytearray(16), 0, None, ZERO):
            with self.subTest(raw=raw):
                with self.assertRaises(Identifier_Error_InvalidBytes):
                    encode_readable(raw)

    def test_empty_observation_and_one_shot_parse(self):
        value = self.make()
        with self.assertRaises(Identifier_Error_NotInitialized):
            value.to_string()
        value.from_string(ZERO)
        self.assertFalse(value.is_empty())
        self.assertEqual(value.read_value(), 0)
        self.assertEqual(value.to_string(), ZERO)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.from_string(None)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.generate()

    def test_parse_failure_preserves_empty_for_retry(self):
        value = self.make()
        with self.assertRaises(Identifier_Error_NotDecodable):
            value.from_string("bad")
        self.assertTrue(value.is_empty())
        value.from_string(ZERO)
        self.assertEqual(value.to_string(), ZERO)

    def test_binary_and_readable_share_one_retained_value(self):
        value = self.make()
        text = "20261117-T124949.123456789Z-17BA988ED5072891"
        value.from_string(text)
        target = io.BytesIO()
        value.encode(target)
        self.assertEqual(target.getvalue(), decode_readable(text))
        restored = self.make()
        restored.decode(io.BytesIO(target.getvalue()))
        self.assertEqual(restored.to_string(), text)
        self.assertTrue(value.equivalence(restored))

    def test_time_view_failure_leaves_empty(self):
        refusal = OSError("view refused")
        value = self.make(Mock(side_effect=refusal))
        with self.assertRaises(OSError) as caught:
            value.from_string(ZERO)
        self.assertIs(caught.exception, refusal)
        self.assertTrue(value.is_empty())

    def test_concurrent_parses_publish_one_value(self):
        value = self.make()
        barrier = Barrier(8)

        def parse(index):
            barrier.wait(timeout=5)
            text = ZERO[:-16] + format(index, "016X")
            try:
                value.from_string(text)
                return index
            except Identifier_Error_AlreadyInitialized:
                return None

        with ThreadPoolExecutor(max_workers=8) as pool:
            outcomes = list(pool.map(parse, range(8)))
        winners = [item for item in outcomes if item is not None]
        self.assertEqual(len(winners), 1)
        self.assertEqual(value.get_discriminator(), winners[0])


class BoundConversionExpectations(unittest.TestCase):
    make = ReadableExpectations.make

    def test_disabled_directions_preserve_state_and_precedence(self):
        value = self.make(string_encoder=None, string_decoder=None)
        with self.assertRaises(Identifier_Error_NotInitialized):
            value.to_string()
        with self.assertRaises(Stringer_Error_NotSupported):
            value.from_string(None)
        self.assertTrue(value.is_empty())
        value.load(0)
        for _ in range(2):
            with self.assertRaises(Stringer_Error_NotSupported):
                value.to_string()
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.from_string(None)
        self.assertEqual(value.read_value(), 0)

    def test_each_direction_can_be_supported_independently(self):
        encode_only = self.make(string_decoder=None)
        encode_only.load(0)
        self.assertEqual(encode_only.to_string(), ZERO)
        decode_only = self.make(string_encoder=None)
        decode_only.from_string(ZERO)
        self.assertEqual(decode_only.read_value(), 0)
        with self.assertRaises(Stringer_Error_NotSupported):
            decode_only.to_string()

    def test_custom_pair_reuses_one_identifier_and_all_bits(self):
        encode = Mock(side_effect=lambda raw: raw.hex())
        decode = Mock(side_effect=lambda text: bytes.fromhex(text))
        number = (1 << 128) - 1
        value = self.make(string_encoder=encode, string_decoder=decode)
        value.from_string("f" * 32)
        self.assertEqual(value.read_value(), number)
        self.assertEqual(value.to_string(), "f" * 32)
        encode.assert_called_once_with(number.to_bytes(16, "big"))
        decode.assert_called_once_with("f" * 32)
        default = self.make()
        default.load(number)
        self.assertTrue(default.equivalence(value))

    def test_invalid_conversion_configuration_refuses(self):
        for name in ("string_encoder", "string_decoder"):
            for binding in (False, 0, "", bytes(16), object()):
                with self.subTest(name=name, binding=binding):
                    with self.assertRaises(Identifier_Error_InvalidValue):
                        self.make(**{name: binding})

    def test_supported_decoder_rejects_nonstring_before_callback(self):
        decode = Mock()
        value = self.make(string_decoder=decode)
        for source in (None, 0, True, bytes(16), bytearray(16)):
            with self.subTest(source=source):
                with self.assertRaises(Identifier_Error_NotDecodable):
                    value.from_string(source)
                self.assertTrue(value.is_empty())
        decode.assert_not_called()

    def test_bad_callback_results_never_publish_or_change_identity(self):
        for result in (None, 0, True, "x", bytes(15), bytes(17), bytearray(16)):
            with self.subTest(result=result):
                decode = Mock(return_value=result)
                value = self.make(string_decoder=decode)
                with self.assertRaises(Identifier_Error_InvalidValue):
                    value.from_string("valid for this binding")
                self.assertTrue(value.is_empty())
        for result in (None, 0, True, bytes(16), bytearray(16)):
            with self.subTest(result=result):
                value = self.make(string_encoder=Mock(return_value=result))
                value.load(5)
                with self.assertRaises(Identifier_Error_InvalidValue):
                    value.to_string()
                self.assertEqual(value.read_value(), 5)

    def test_callback_refusals_propagate_and_keep_retained_state(self):
        refusal = Stringer_Error_NotSupported()
        value = self.make(string_encoder=Mock(side_effect=refusal), string_decoder=Mock(side_effect=refusal))
        with self.assertRaises(Stringer_Error_NotSupported) as caught:
            value.from_string("x")
        self.assertIs(caught.exception, refusal)
        self.assertTrue(value.is_empty())
        value.load(3)
        with self.assertRaises(Stringer_Error_NotSupported) as caught:
            value.to_string()
        self.assertIs(caught.exception, refusal)
        self.assertEqual(value.read_value(), 3)


if __name__ == "__main__":
    unittest.main()

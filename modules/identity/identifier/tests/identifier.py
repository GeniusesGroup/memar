# For license and copyright information please see the LEGAL file in the code repository

import unittest
from modules.identity.identifier.identifier import complete_bytes
from modules.identity.identifier.errors.value import Identifier_Error_InvalidBytes

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier complete immutable host-byte admission"
CONTRACT = "modules/identity/identifier/protocol/identifier.eng.kh"


class CompleteBytes(unittest.TestCase):
    def test_all_complete_bit_patterns_remain_unchanged(self):
        for value in (bytes(16), bytes(range(16)), bytes([255]) * 16):
            self.assertEqual(complete_bytes(value), value)

    def test_incomplete_and_overlong_values_are_refused(self):
        for size in (0, 1, 8, 15, 17, 32):
            with self.subTest(size=size):
                with self.assertRaises(Identifier_Error_InvalidBytes):
                    complete_bytes(bytes(size))

    def test_nonbyte_and_mutable_representations_are_refused(self):
        for value in (None, True, 0, 1 << 127, "0" * 32, bytearray(16), memoryview(bytes(16)), list(range(16))):
            with self.subTest(value=value):
                with self.assertRaises(Identifier_Error_InvalidBytes):
                    complete_bytes(value)


if __name__ == "__main__":
    unittest.main()

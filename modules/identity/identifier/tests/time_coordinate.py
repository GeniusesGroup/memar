# For license and copyright information please see the LEGAL file in the code repository

import unittest
from modules.identity.identifier.time_coordinate import coordinate_from_time, generate_from_time
from modules.identity.identifier.generator import CandidateGenerator
from modules.identity.identifier.errors.generation import Identifier_Error_InvalidGeneratorInput
from modules.time.errors.exact_parts import Time_Error_ExactPartsUnavailable

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier exact shared-time coordinate adapter"
CONTRACT = "modules/identity/identifier/protocol/identifier.eng.kh"
MAXIMUM = (1 << 64) - 1
REFERENCE = object()


class Parts:
    def __init__(self, value):
        self.value = value
        self.seen_reference = None

    def parts_in_epoch(self, reference):
        self.seen_reference = reference
        return self.value


class TimeCoordinate(unittest.TestCase):
    def test_exact_parts_are_requested_in_the_trusted_reference(self):
        source = Parts((2, 3, None))
        self.assertEqual(coordinate_from_time(source, REFERENCE), 2000000003)
        self.assertIs(source.seen_reference, REFERENCE)

    def test_unsigned_carrier_boundaries_are_exact(self):
        seconds, remainder = divmod(MAXIMUM, 1000000000)
        self.assertEqual(coordinate_from_time(Parts((0, 0, None)), REFERENCE), 0)
        self.assertEqual(coordinate_from_time(Parts((seconds, remainder, None)), REFERENCE), MAXIMUM)
        for pair in ((-1, 0), (-1, 999999999), (seconds, remainder + 1), (MAXIMUM, 0)):
            with self.subTest(pair=pair):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    coordinate_from_time(Parts((*pair, None)), REFERENCE)

    def test_noncanonical_or_inexact_parts_are_refused_without_rounding(self):
        for pair in ((0, -1), (0, 1000000000), (True, 0), (0, True), (1.0, 0), (0, 0.5), ("1", 0)):
            with self.subTest(pair=pair):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    coordinate_from_time(Parts((*pair, None)), REFERENCE)

    def test_malformed_host_bindings_are_refused(self):
        for value in (None, (), (1,), (1, 2), (1, 2, None, 4), (0, 0, "bad error")):
            with self.subTest(value=value):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    coordinate_from_time(Parts(value), REFERENCE)
        for source in (None, object(), type("MissingMethod", (), {"parts_in_epoch": 1})()):
            with self.subTest(source=source):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    coordinate_from_time(source, REFERENCE)

    def test_owner_refusal_propagates_before_parts_are_interpreted(self):
        refusal = Time_Error_ExactPartsUnavailable()
        with self.assertRaises(Time_Error_ExactPartsUnavailable) as caught:
            coordinate_from_time(Parts((None, None, refusal)), REFERENCE)
        self.assertIs(caught.exception, refusal)

    def test_conversion_failure_consumes_no_generator_reservation(self):
        generator = CandidateGenerator(max_rollback_ticks=3, max_per_tick=4, entropy=lambda size: bytes(range(32)), session=lambda: 1)
        first = generate_from_time(generator, Parts((0, 10, None)), REFERENCE)
        self.assertEqual(first >> 64, 10)
        refusal = Time_Error_ExactPartsUnavailable()
        with self.assertRaises(Time_Error_ExactPartsUnavailable):
            generate_from_time(generator, Parts((None, None, refusal)), REFERENCE)
        with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
            generate_from_time(generator, Parts((0, -1, None)), REFERENCE)
        self.assertEqual(generator.generate(10), first + 1)


if __name__ == "__main__":
    unittest.main()

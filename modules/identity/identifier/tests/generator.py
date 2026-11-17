# For license and copyright information please see the LEGAL file in the code repository

import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import MagicMock, Mock, patch

from modules.identity.identifier.generator import CandidateGenerator
from modules.identity.identifier.errors.generation import (
    Identifier_Error_InvalidGeneratorInput,
    Identifier_Error_EntropyUnavailable,
    Identifier_Error_ClockRollback,
    Identifier_Error_GenerationExhausted,
    Identifier_Error_GeneratorSessionUnverified,
)

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier private issuance kernel"
CONTRACT = "modules/identity/identifier/protocol/identifier.eng.kh"
VECTOR_SOURCE = "Node.js crypto HMAC-SHA256, independently evaluated canonical transcript"
MAXIMUM = (1 << 64) - 1
KEY = bytes(range(32))
SOURCE = bytes.fromhex("00112233445566778899aabbccddeeff")
VECTORS = (
    (b"", 0, 0xEF360333FF189B52),
    (b"", 1, 0xEF360333FF189B52),
    (b"", 0x0102030405060708, 0xEF360333FF189B52),
    (SOURCE, 0, 0x17BA988ED5072891),
    (SOURCE, 1, 0x17BA988ED5072891),
    (SOURCE, 0x0102030405060708, 0x17BA988ED5072891),
)


class GeneratorExpectations(unittest.TestCase):
    def make(self, **overrides):
        arguments = dict(max_rollback_ticks=3, max_per_tick=4096, entropy=lambda size: KEY, session=lambda: 1)
        arguments.update(overrides)
        return CandidateGenerator(**arguments)

    def test_independent_transcript_vectors(self):
        for source, tick, tail in VECTORS:
            with self.subTest(source=source, tick=tick):
                self.assertEqual(self.make(source=source).generate(tick), (tick << 64) | tail)

    def test_same_tick_increments_and_later_tick_reuses_anchor(self):
        generator = self.make()
        first = generator.generate(0)
        self.assertEqual(generator.generate(0), first + 1)
        later = generator.generate(1)
        self.assertEqual(later, (1 << 64) | VECTORS[1][2])
        self.assertGreater(later, first + 1)

    def test_bounded_rollback_retains_creation_count(self):
        generator = self.make()
        first = generator.generate(10)
        self.assertEqual(generator.generate(7), first + 1)
        self.assertEqual(generator.generate(9), first + 2)
        with self.assertRaises(Identifier_Error_ClockRollback):
            generator.generate(6)
        self.assertEqual(generator.generate(10), first + 3)

    def test_zero_rollback_bound(self):
        generator = self.make(max_rollback_ticks=0)
        first = generator.generate(10)
        with self.assertRaises(Identifier_Error_ClockRollback):
            generator.generate(9)
        self.assertEqual(generator.generate(10), first + 1)

    def test_invalid_time_consumes_no_reservation(self):
        generator = self.make()
        first = generator.generate(10)
        for bad in (-1, 1 << 64, True, None, 1.0, "1"):
            with self.subTest(value=bad):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    generator.generate(bad)
        self.assertEqual(generator.generate(10), first + 1)

    def test_timestamp_maximum_is_representable_without_wrap(self):
        generator = self.make()
        value = generator.generate(MAXIMUM)
        self.assertEqual(value >> 64, MAXIMUM)
        self.assertLess(value, 1 << 128)
        with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
            generator.generate(MAXIMUM + 1)
        self.assertEqual(generator.generate(MAXIMUM), value + 1)

    def test_invalid_configuration_is_refused(self):
        for bad in (-1, 1 << 64, True, None, 1.0):
            with self.subTest(rollback=bad):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    self.make(max_rollback_ticks=bad)
        for bad in (-1, 0, 1 << 64, True, None, 1.0):
            with self.subTest(cap=bad):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    self.make(max_per_tick=bad)
        for bad in (b"x", bytes(15), bytes(17), bytearray(16), None, 1):
            with self.subTest(source=bad):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    self.make(source=bad)
        for adapter in ("entropy", "session"):
            with self.subTest(adapter=adapter):
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    self.make(**{adapter: None})

    def test_entropy_is_fresh_once_per_lifetime(self):
        entropy = Mock(return_value=KEY)
        generator = self.make(entropy=entropy)
        generator.generate(0)
        generator.generate(0)
        generator.generate(1)
        entropy.assert_called_once_with(32)

    def test_entropy_failure_has_no_fallback(self):
        for result in (b"", bytes(31), bytes(33), bytearray(32), None):
            with self.subTest(result=result):
                with self.assertRaises(Identifier_Error_EntropyUnavailable):
                    self.make(entropy=lambda size: result)
        entropy = Mock(side_effect=OSError("fixture unavailable"))
        with self.assertRaises(Identifier_Error_EntropyUnavailable):
            self.make(entropy=entropy)

    def test_tail_exhaustion_refuses_without_artificial_time(self):
        with patch("modules.identity.identifier.generator.hmac.digest", return_value=bytes([255]) * 32):
            generator = self.make()
            first = generator.generate(10)
            self.assertEqual(first, (10 << 64) | MAXIMUM)
            for tick in (10, 9, 10):
                with self.assertRaises(Identifier_Error_GenerationExhausted):
                    generator.generate(tick)
            later = generator.generate(11)
            self.assertEqual(later, (11 << 64) | MAXIMUM)

    def test_held_tick_uses_counter_even_when_hash_adapter_would_fail(self):
        generator = self.make()
        first = generator.generate(10)
        with patch("modules.identity.identifier.generator.hmac.digest", side_effect=AssertionError("unexpected reseed")):
            self.assertEqual(generator.generate(10), first + 1)
            self.assertEqual(generator.generate(8), first + 2)
            self.assertEqual(generator.generate(11), (11 << 64) | (first & MAXIMUM))

    def test_bucket_cap_accumulates_rollback_and_resets_only_on_later_time(self):
        generator = self.make(max_per_tick=3)
        first = generator.generate(10)
        self.assertEqual(generator.generate(7), first + 1)
        self.assertEqual(generator.generate(10), first + 2)
        for tick in (8, 10):
            with self.assertRaises(Identifier_Error_GenerationExhausted):
                generator.generate(tick)
        later = generator.generate(11)
        self.assertEqual(later & MAXIMUM, first & MAXIMUM)
        self.assertEqual(generator.generate(8), later + 1)
        self.assertEqual(generator.generate(11), later + 2)
        with self.assertRaises(Identifier_Error_GenerationExhausted):
            generator.generate(11)

    def test_cap_one_and_maximum_cap_are_valid(self):
        generator = self.make(max_per_tick=1)
        first = generator.generate(0)
        with self.assertRaises(Identifier_Error_GenerationExhausted):
            generator.generate(0)
        self.assertEqual(generator.generate(1), (1 << 64) | first)
        self.assertGreaterEqual(self.make(max_per_tick=MAXIMUM).generate(0), 0)

    def test_anchor_is_derived_once_for_whole_lifetime(self):
        with patch("modules.identity.identifier.generator.hmac.digest", return_value=bytes(32)) as digest:
            generator = self.make()
            for tick in (0, 1, 2, 1, 3):
                generator.generate(tick)
            digest.assert_called_once()

    def test_runway_exhaustion_recurs_after_later_time(self):
        near_end = (MAXIMUM - 1).to_bytes(8, "big") + bytes(24)
        with patch("modules.identity.identifier.generator.hmac.digest", return_value=near_end):
            generator = self.make()
        for tick in (10, 11):
            self.assertEqual(generator.generate(tick), (tick << 64) | (MAXIMUM - 1))
            self.assertEqual(generator.generate(tick), (tick << 64) | MAXIMUM)
            with self.assertRaises(Identifier_Error_GenerationExhausted):
                generator.generate(tick)

    def test_session_change_during_entropy_acquisition_refuses_construction(self):
        session = Mock(return_value=1)

        def changed(size):
            session.return_value = 2
            return KEY

        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            self.make(session=session, entropy=changed)

    def test_concurrent_reservations_are_unique_and_contiguous(self):
        generator = self.make()
        first = generator.generate(123)
        with ThreadPoolExecutor(max_workers=16) as pool:
            results = list(pool.map(generator.generate, [123] * 1000))
        self.assertEqual(sorted(results), list(range(first + 1, first + 1001)))

    def test_changed_session_is_permanently_invalid(self):
        session = Mock(return_value=1)
        generator = self.make(session=session)
        generator.generate(0)
        session.return_value = 2
        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            generator.generate(1)
        session.return_value = 1
        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            generator.generate(2)

    def test_unreadable_or_invalid_session_is_permanently_invalid(self):
        for failure in (OSError("fixture session failed"), 0, -1, True, None, "1"):
            with self.subTest(failure=failure):
                session = Mock(return_value=1)
                generator = self.make(session=session)
                if isinstance(failure, Exception):
                    session.side_effect = failure
                else:
                    session.return_value = failure
                with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
                    generator.generate(0)
                session.side_effect = None
                session.return_value = 1
                with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
                    generator.generate(0)

    def test_session_must_be_valid_at_construction(self):
        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            self.make(session=lambda: 0)
        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            self.make(session=Mock(side_effect=OSError("fixture session failed")))

    def test_session_change_under_lock_and_before_commit_is_refused(self):
        for readings in ((1, 2), (1, 1, 2)):
            with self.subTest(readings=readings):
                session = Mock(return_value=1)
                generator = self.make(session=session)
                session.side_effect = readings
                with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
                    generator.generate(0)
                session.side_effect = None
                session.return_value = 1
                with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
                    generator.generate(0)

    def test_session_refusal_precedes_attempt_to_acquire_copied_lock(self):
        unacquirable = MagicMock()
        unacquirable.__enter__.side_effect = AssertionError("copied lock was entered")
        session = Mock(return_value=1)
        with patch("modules.identity.identifier.generator.Lock", return_value=unacquirable):
            generator = self.make(session=session)
        session.return_value = 2
        with self.assertRaises(Identifier_Error_GeneratorSessionUnverified):
            generator.generate(0)
        unacquirable.__enter__.assert_not_called()

    def test_complete_cloned_inputs_are_not_claimed_unique(self):
        first = self.make(source=SOURCE)
        cloned = self.make(source=SOURCE)
        for tick in (100, 100, 99, 101):
            self.assertEqual(first.generate(tick), cloned.generate(tick))

    def test_restart_has_no_cross_lifetime_monotonicity_promise(self):
        first = self.make()
        old = first.generate(1)
        restarted = self.make(entropy=lambda size: bytes(reversed(KEY)))
        new = restarted.generate(0)
        self.assertLess(new, old)


if __name__ == "__main__":
    unittest.main()

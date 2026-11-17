# For license and copyright information please see the LEGAL file in the code repository

import unittest
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import Mock

from modules.identity.identifier.value import IdentifierValue
from modules.identity.identifier.generator import CandidateGenerator
from modules.identity.identifier.tests.time_coordinate import Parts, REFERENCE
from modules.identity.identifier.time_coordinate import coordinate_from_time
from modules.identity.identifier.errors.already_initialized import Identifier_Error_AlreadyInitialized
from modules.identity.identifier.errors.not_initialized import Identifier_Error_NotInitialized
from modules.identity.identifier.errors.invalid_value import Identifier_Error_InvalidValue
from modules.identity.identifier.errors.generation import Identifier_Error_ClockRollback, Identifier_Error_InvalidGeneratorInput
from modules.time.errors.exact_parts import Time_Error_ExactPartsUnavailable

BUDGET_SECONDS = 30
TIER = "unit"
COST = {"subprocesses": 0, "writes_files": False, "clock_waits": False}
SUBJECT = "Identifier one-shot native value publication"
CONTRACT = "modules/identity/identifier/protocol/identifier.eng.kh"
MAXIMUM = (1 << 128) - 1


def time_view(coordinate):
    seconds, remainder = divmod(coordinate, 1000000000)
    return Parts((seconds, remainder, None))


class IdentifierValueExpectations(unittest.TestCase):
    def make(self, mint=None, view=time_view):
        return IdentifierValue(Mock(return_value=(10 << 64) | 7) if mint is None else mint, view, REFERENCE)

    def test_empty_observations_and_equality_refuse(self):
        value = self.make()
        self.assertTrue(value.is_empty())
        for observe in (value.read_value, value.get_issuance_time, lambda: value.equivalence(value)):
            with self.assertRaises(Identifier_Error_NotInitialized):
                observe()

    def test_generation_publishes_complete_value_once(self):
        mint = Mock(return_value=(10 << 64) | 7)
        value = self.make(mint)
        value.generate()
        self.assertFalse(value.is_empty())
        self.assertEqual(value.read_value(), (10 << 64) | 7)
        self.assertEqual(coordinate_from_time(value.get_issuance_time(), REFERENCE), 10)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.generate()
        mint.assert_called_once_with()
        self.assertEqual(value.read_value(), (10 << 64) | 7)

    def test_loaded_zero_is_initialized_and_never_mints(self):
        mint = Mock(side_effect=AssertionError("hydration minted a replacement"))
        value = self.make(mint)
        value.load(0)
        self.assertFalse(value.is_empty())
        self.assertEqual(value.read_value(), 0)
        self.assertEqual(coordinate_from_time(value.get_issuance_time(), REFERENCE), 0)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.load(1)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.generate()
        mint.assert_not_called()

    def test_failed_issuer_preserves_empty_and_retry(self):
        refusal = Identifier_Error_ClockRollback()
        mint = Mock(side_effect=[refusal, 5])
        value = self.make(mint)
        with self.assertRaises(Identifier_Error_ClockRollback) as caught:
            value.generate()
        self.assertIs(caught.exception, refusal)
        self.assertTrue(value.is_empty())
        value.generate()
        self.assertEqual(value.read_value(), 5)

    def test_invalid_internal_values_do_not_publish(self):
        for candidate in (-1, 1 << 128, True, None, 1.0, "1", bytes(16)):
            with self.subTest(candidate=candidate):
                value = self.make(Mock(return_value=candidate))
                with self.assertRaises(Identifier_Error_InvalidValue):
                    value.generate()
                self.assertTrue(value.is_empty())
                with self.assertRaises(Identifier_Error_InvalidValue):
                    value.load(candidate)
                self.assertTrue(value.is_empty())

    def test_time_view_must_match_the_published_coordinate(self):
        for view in (lambda count: None, lambda count: time_view(count + 1)):
            with self.subTest(view=view):
                value = self.make(view=view)
                with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                    value.generate()
                self.assertTrue(value.is_empty())

    def test_invalid_bindings_are_refused(self):
        for mint, view in ((None, time_view), (lambda: 1, None)):
            with self.assertRaises(Identifier_Error_InvalidGeneratorInput):
                IdentifierValue(mint, view, REFERENCE)

    def test_maximum_loaded_value_is_preserved(self):
        value = self.make()
        value.load(MAXIMUM)
        self.assertEqual(value.read_value(), MAXIMUM)

    def test_failed_time_binding_preserves_empty_without_reusing_issuance(self):
        state = CandidateGenerator(max_rollback_ticks=3, max_per_tick=8, entropy=lambda size: bytes(range(32)), session=lambda: 1)
        first = state.generate(10)
        views = Mock(side_effect=[Time_Error_ExactPartsUnavailable(), time_view(10)])
        value = self.make(lambda: state.generate(10), views)
        with self.assertRaises(Time_Error_ExactPartsUnavailable):
            value.generate()
        self.assertTrue(value.is_empty())
        value.generate()
        self.assertEqual(value.read_value(), first + 2)

    def test_distinct_values_share_existing_issuer_lifetime(self):
        state = CandidateGenerator(max_rollback_ticks=3, max_per_tick=8, entropy=lambda size: bytes(range(32)), session=lambda: 1)
        left = self.make(lambda: state.generate(10))
        right = self.make(lambda: state.generate(10))
        left.generate()
        right.generate()
        self.assertEqual(right.read_value(), left.read_value() + 1)

    def test_retained_rollback_coordinate_is_observed_not_raw_clock(self):
        state = CandidateGenerator(max_rollback_ticks=3, max_per_tick=8, entropy=lambda size: bytes(range(32)), session=lambda: 1)
        state.generate(10)
        value = self.make(lambda: state.generate(8))
        value.generate()
        self.assertEqual(coordinate_from_time(value.get_issuance_time(), REFERENCE), 10)

    def test_equality_compares_complete_initialized_values(self):
        left, same, other = self.make(), self.make(), self.make()
        left.load(1)
        same.load(1)
        other.load(2)
        self.assertTrue(left.equivalence(same))
        self.assertFalse(left.equivalence(other))
        with self.assertRaises(Identifier_Error_NotInitialized):
            left.equivalence(self.make())

    def test_concurrent_initialization_publishes_exactly_once(self):
        mint = Mock(return_value=1)
        value = self.make(mint)
        start = Barrier(16)

        def initialize(_):
            start.wait(timeout=5)
            try:
                value.generate()
                return True
            except Identifier_Error_AlreadyInitialized:
                return False

        with ThreadPoolExecutor(max_workers=16) as pool:
            outcomes = list(pool.map(initialize, range(16)))
        self.assertEqual(outcomes.count(True), 1)
        mint.assert_called_once_with()
        self.assertEqual(value.read_value(), 1)

    def test_filled_receiver_refuses_before_other_binding_work(self):
        value = self.make()
        value.load(3)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.load(-1)
        self.assertEqual(value.read_value(), 3)

    def test_empty_discriminator_refuses_without_issuing(self):
        mint = Mock(return_value=1)
        value = self.make(mint)
        with self.assertRaises(Identifier_Error_NotInitialized):
            value.get_discriminator()
        mint.assert_not_called()
        self.assertTrue(value.is_empty())

    def test_component_observations_reconstruct_boundary_identities(self):
        maximum = (1 << 64) - 1
        for coordinate in (0, 1, maximum):
            for discriminator in (0, 1, maximum):
                with self.subTest(coordinate=coordinate, discriminator=discriminator):
                    mint = Mock(side_effect=AssertionError("observation minted"))
                    value = self.make(mint)
                    complete = (coordinate << 64) | discriminator
                    value.load(complete)
                    observed_time = coordinate_from_time(value.get_issuance_time(), REFERENCE)
                    self.assertEqual(value.get_discriminator(), discriminator)
                    self.assertEqual((observed_time << 64) | value.get_discriminator(), complete)
                    self.assertEqual(value.read_value(), complete)
                    mint.assert_not_called()

    def test_discriminator_alone_does_not_establish_equality(self):
        left, right = self.make(), self.make()
        left.load((1 << 64) | 7)
        right.load((2 << 64) | 7)
        self.assertEqual(left.get_discriminator(), right.get_discriminator())
        self.assertFalse(left.equivalence(right))

    def test_generated_component_observations_are_stable(self):
        mint = Mock(return_value=(10 << 64) | 19)
        value = self.make(mint)
        value.generate()
        for _ in range(3):
            self.assertEqual(value.get_discriminator(), 19)
            self.assertEqual(coordinate_from_time(value.get_issuance_time(), REFERENCE), 10)
        with self.assertRaises(Identifier_Error_AlreadyInitialized):
            value.generate()
        self.assertEqual(value.get_discriminator(), 19)
        mint.assert_called_once_with()


    def test_order_refuses_empty_operands_and_invalid_values(self):
        empty = self.make()
        filled = self.make()
        filled.load(0)
        for left, right in ((empty, empty), (empty, filled), (filled, empty)):
            with self.assertRaises(Identifier_Error_NotInitialized):
                left.precedes(right)
        with self.assertRaises(Identifier_Error_InvalidValue):
            filled.precedes(0)

    def test_order_is_strict_and_total_at_both_component_boundaries(self):
        numbers = (0, 1, (1 << 64) - 1, 1 << 64, (1 << 64) + 1, MAXIMUM)
        values = []
        for number in numbers:
            value = self.make()
            value.load(number)
            values.append(value)
        for i, left in enumerate(values):
            for j, right in enumerate(values):
                with self.subTest(left=numbers[i], right=numbers[j]):
                    self.assertEqual(left.precedes(right), i < j)
                    self.assertEqual(right.precedes(left), j < i)
                    self.assertEqual(left.equivalence(right), i == j)

    def test_order_observation_does_not_issue_or_change_identity(self):
        mint = Mock(side_effect=AssertionError("comparison minted"))
        left, right = self.make(mint), self.make(mint)
        left.load((4 << 64) | 9)
        right.load((5 << 64) | 1)
        for _ in range(3):
            self.assertTrue(left.precedes(right))
            self.assertFalse(right.precedes(left))
        self.assertEqual(left.read_value(), (4 << 64) | 9)
        self.assertEqual(right.read_value(), (5 << 64) | 1)
        mint.assert_not_called()


if __name__ == "__main__":
    unittest.main()

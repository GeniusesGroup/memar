#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the label types in `primitive/label.py`.

    python modules/knowledge/documentation/tests/label.py

The subject is the `Labels` field of a documentation record: a list of labels,
each a word with the identifier of the label it names, defined once, its
definition taking labels of its own, with no limit on how many a record takes.
Named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md), in the
`tests/` folder of the module that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

Nothing here writes.

What is pinned, and what each pin is for:

  Identifiers  A new identifier is a UUID version 7: its version nibble is 7,
               its variant is RFC 4122's, and identifiers made later sort
               later, as a task id does.
  OneLabel     A label is a word and an identifier, written `word(id)`; the
               identifier, not the word, is what two labels are the same by.
  Definitions  A label is defined once; its definition takes labels (the kinds
               it is a member of) and carries its meaning and its end of life;
               a registry holds the declared definitions, lists them by kind,
               and reads a refined word as its declaration writes it.
  Kinds        A kind is a label other labels take, with the rule that makes a
               word of it valid; a closed kind lists its words, a free kind
               returns, for a word not yet defined, the definition that would
               declare it.
  ManyLabels   A record takes as many labels as it needs, in the order
               written, none twice; adding and removing one changes nothing else.
  TheBlock     The field is a block of `- word(id)` lines, read back from the
               lines of that block.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import re
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = TESTS.parents[3]
SCRIPTS = TOP / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
from modules.knowledge.documentation.primitive.label import Label, LabelDefinition, LabelKind, LabelProblem, LabelRegistry, Labels, new_id
UUID7 = re.compile('^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

def lower_word(text: str) -> str:
    word = '-'.join(text.lower().split())
    if not word:
        raise LabelProblem('a word is not empty')
    return word

def small_or_large(text: str) -> str:
    if text.strip() not in ('small', 'large'):
        raise LabelProblem('a size is small or large')
    return text.strip()
COLOR = LabelKind(Label('Color', new_id()), 'a colour', 'a test', lower_word)
SIZE_LABEL = Label('Size', new_id())
SIZE = LabelKind(SIZE_LABEL, 'a size', 'a test', small_or_large, tuple((LabelDefinition(Label(word, new_id()), (SIZE_LABEL,)) for word in ('small', 'large'))))
A, B, C = (Label('a', new_id()), Label('b', new_id()), Label('c', new_id()))

class Identifiers(unittest.TestCase):

    def test_a_new_identifier_is_a_uuid_version_7(self) -> None:
        self.assertRegex(new_id(), UUID7)

    def test_identifiers_made_later_sort_later(self) -> None:
        import time
        first = new_id()
        time.sleep(0.005)
        self.assertLess(first, new_id())

class OneLabel(unittest.TestCase):

    def test_a_label_is_written_word_and_identifier(self) -> None:
        self.assertEqual(str(Label('design', '01a14a04-6531-73d5-8eeb-6e37ddce016d')), 'design(01a14a04-6531-73d5-8eeb-6e37ddce016d)')

    def test_a_written_label_is_read_back_bare_or_as_a_block_line(self) -> None:
        label = Label('memar scripts', '01a14a04-6531-73d5-8eeb-6e37ddce016d')
        self.assertEqual(Label.read(str(label)), label)
        self.assertEqual(Label.read(f'  - {label}  '), label)

    def test_text_without_a_word_and_an_identifier_is_no_label(self) -> None:
        for text in ('', 'design', 'design()', '(01a14a04-6531-73d5-8eeb-6e37ddce016d)', 'TaskKind: design', 'design(not-an-id)'):
            with self.subTest(text=text):
                self.assertIsNone(Label.read(text))

    def test_the_same_word_with_two_identifiers_is_two_labels(self) -> None:
        self.assertNotEqual(Label('design', new_id()), Label('design', new_id()))

class Definitions(unittest.TestCase):

    def test_a_definition_takes_labels(self) -> None:
        definition = LabelDefinition(A, (B, C))
        self.assertTrue(definition.is_a(B))
        self.assertFalse(definition.is_a(Label('z', new_id())))

    def test_a_definition_carries_its_meaning_and_its_end_of_life(self) -> None:
        live = LabelDefinition(A, (B,), 'what a means')
        self.assertEqual((live.meaning, live.ended, live.replaced_by), ('what a means', '', ()))
        ended = LabelDefinition(A, (B,), 'what a meant', '2026-10-23', (C,))
        self.assertEqual((ended.ended, ended.replaced_by), ('2026-10-23', (C,)))

    def test_the_registry_holds_declared_definitions_and_lists_them_by_kind(self) -> None:
        declared = (LabelDefinition(Label('red', new_id()), (COLOR.label,), 'a red'), LabelDefinition(Label('blue', new_id()), (COLOR.label,), 'a blue'))
        registry = LabelRegistry([SIZE, COLOR], declared)
        self.assertEqual(registry.definitions('Color'), declared)
        self.assertEqual(registry.resolve('Color=red'), (declared[0].label, None))

    def test_a_refined_word_is_read_as_its_declaration_writes_it(self) -> None:
        red = LabelDefinition(Label('red', new_id()), (COLOR.label,), 'a red')
        registry = LabelRegistry([COLOR], (red,))
        self.assertEqual(registry.words(Labels((Label('rouge', red.label.id),)), 'Color'), ('red',))

class Kinds(unittest.TestCase):

    def test_a_free_kind_defines_a_word_by_its_rule_with_a_new_identifier(self) -> None:
        definition = COLOR.define('Dark  Red')
        self.assertEqual(definition.label.word, 'dark-red')
        self.assertRegex(definition.label.id, UUID7)
        self.assertTrue(definition.is_a(COLOR.label))

    def test_a_word_the_rule_refuses_is_refused_with_the_kinds_words(self) -> None:
        with self.assertRaises(LabelProblem) as refused:
            SIZE.define('medium')
        self.assertIn('small or large', str(refused.exception))

    def test_the_registry_resolves_a_closed_word_to_its_label_and_defines_nothing(self) -> None:
        label, fresh = LabelRegistry([SIZE, COLOR]).resolve('Size=small')
        self.assertEqual(label.word, 'small')
        self.assertIsNone(fresh)

    def test_the_registry_defines_a_free_word_once_and_knows_it_after(self) -> None:
        registry = LabelRegistry([SIZE, COLOR])
        label, fresh = registry.resolve('Color=Dark Red')
        self.assertIsNotNone(fresh)
        registry.add(fresh)
        again, fresh_again = registry.resolve('Color=dark-red')
        self.assertEqual((again, fresh_again), (label, None))

    def test_the_same_word_of_two_kinds_is_two_labels(self) -> None:
        registry = LabelRegistry([SIZE, COLOR])
        color, fresh = registry.resolve('Color=small')
        registry.add(fresh)
        size, _ = registry.resolve('Size=small')
        self.assertNotEqual(color.id, size.id)

    def test_a_kind_nobody_declared_or_a_text_without_a_word_is_refused(self) -> None:
        registry = LabelRegistry([SIZE, COLOR])
        with self.assertRaises(LabelProblem) as unknown:
            registry.resolve('Weight=heavy')
        self.assertIn('Size, Color', str(unknown.exception))
        for text in ('small', 'Size=', '=small'):
            with self.subTest(text=text):
                with self.assertRaises(LabelProblem):
                    registry.resolve(text)

    def test_words_of_a_kind_are_those_whose_definition_takes_it(self) -> None:
        registry = LabelRegistry([SIZE, COLOR])
        dark, fresh = registry.resolve('Color=dark')
        registry.add(fresh)
        small, _ = registry.resolve('Size=small')
        self.assertEqual(registry.words(Labels((dark, small)), 'Color'), ('dark',))
        self.assertEqual(registry.words(Labels((dark, small)), 'Size'), ('small',))

class ManyLabels(unittest.TestCase):

    def test_a_record_takes_several_labels_in_the_order_written(self) -> None:
        labels = Labels().with_label(A).with_label(B).with_label(C)
        self.assertEqual([label.word for label in labels], ['a', 'b', 'c'])
        self.assertEqual(len(labels), 3)

    def test_a_label_is_never_twice_by_identifier(self) -> None:
        once = Labels().with_label(A)
        self.assertEqual(once.with_label(A), once)
        self.assertEqual(once.with_label(Label('renamed', A.id)), once)

    def test_removing_one_changes_nothing_else(self) -> None:
        labels = Labels((A, B, C))
        self.assertEqual(labels.without(A), Labels((B, C)))
        self.assertEqual(labels.without(Label('absent', new_id())), labels)

    def test_no_labels_is_falsy(self) -> None:
        self.assertFalse(Labels())

class TheBlock(unittest.TestCase):

    def test_the_block_is_one_line_a_label(self) -> None:
        self.assertEqual(Labels((A, B)).lines(), [f'  - {A}', f'  - {B}'])

    def test_the_value_a_front_matter_reader_gives_is_read_back(self) -> None:
        self.assertEqual(Labels.read(f'{A}\n{B}'), Labels((A, B)))

    def test_a_line_that_is_no_label_is_kept_out_of_the_reading(self) -> None:
        self.assertEqual(Labels.read(f'{A}\n\nnonsense\nTaskKind: design'), Labels((A,)))

    def test_an_empty_value_reads_as_no_labels(self) -> None:
        self.assertEqual(Labels.read(''), Labels())
if __name__ == '__main__':
    unittest.main(verbosity=2)

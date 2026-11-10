# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True

BUDGET_SECONDS = 30

field_mod = import_module('modules.computer.capsule.field')
Field = field_mod.Field
Fields = field_mod.Fields
FieldBag = field_mod.FieldBag
LimitToUseBy = field_mod.LimitToUseBy
ImmediateComposer = field_mod.ImmediateComposer
Unrestricted = field_mod.Unrestricted


class CapsuleField(unittest.TestCase):

    def test_field_exposes_title_value_type_authorization(self) -> None:
        f = Field(title='task-id', value_type='TaskID', authorization=Unrestricted())
        self.assertEqual(f.get_title(), 'task-id')
        self.assertEqual(f.value_type(), 'TaskID')
        self.assertIsInstance(f.authorization(), Unrestricted)

    def test_authorization_policies(self) -> None:
        limited = Field(
            title='b',
            value_type='T',
            authorization=LimitToUseBy(allowed_types=('TcpSocket',)),
        )
        self.assertEqual(limited.authorization().allowed_types(), ('TcpSocket',))
        nested = Field(title='timer', value_type='Timer', authorization=ImmediateComposer())
        self.assertIsInstance(nested.authorization(), ImmediateComposer)

    def test_no_hidden_private_cardinality_or_lexical_default_api(self) -> None:
        names = set(field_mod.__dict__)
        for refused in ('Hidden', 'Private', 'One', 'Optional', 'Many', 'Some', 'FieldExclusion'):
            self.assertNotIn(refused, names)
        f = Field(title='a', value_type='T')
        self.assertFalse(hasattr(f, 'default_form'))
        self.assertFalse(hasattr(f, 'choice_forms'))
        self.assertFalse(hasattr(f, 'cardinality'))

    def test_fields_collection_returns_named_type_not_list_api_as_domain(self) -> None:
        bag = FieldBag()
        a = Field(title='a', value_type='T')
        b = Field(title='b', value_type='T')
        bag.add(a)
        bag.add(b)
        fields = bag.get_fields()
        self.assertIsInstance(fields, Fields)
        self.assertEqual(fields.get_occupied_length(), 2)
        self.assertIs(fields.get_element(0), a)
        self.assertIs(fields.get_element(1), b)

    def test_module_has_no_argparse(self) -> None:
        text = Path(field_mod.__file__).read_text(encoding='utf-8')
        self.assertNotIn('argparse', text)
        self.assertNotIn('add_argument', text)


if __name__ == '__main__':
    unittest.main()

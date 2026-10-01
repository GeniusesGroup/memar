"""Tests for khayyam_source: python -m unittest test_khayyam_source"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True

from failures import SourceFailure
from khayyam_source import parse_khayyam_source


class VariableInclusion(unittest.TestCase):
    """`vr {name} in "{path}"` -- the Variable Inclusion form of `docs/khayyam/khayyam.md`,
    Import Mechanism (`in`), and of `docs/khayyam/variable.md`, Variable Scope and
    Visibility: a file-level variable included from another file, addressed by the
    URI that names the file. The name names a variable, not a type, and the address
    is that URI rather than a type reference."""

    def refuse(self, source: str) -> str:
        with self.assertRaises(SourceFailure) as caught:
            parse_khayyam_source("page.kh", source)
        return str(caught.exception)

    def test_a_variable_inclusion_is_read_as_the_inclusion_it_is(self):
        # The line as this repository writes it: the address is the URI a rule
        # states (`modules/khayyam/rules/import-address/`), the path of the file
        # the name is declared in, and `modules/lib/process/command/path.kh`
        # declares `vr cwd String`. `in` is a keyword and `main.kh` writes no
        # other token between it and the quoted address.
        declarations = parse_khayyam_source(
            "page.kh", 'vr cwd in "modules/lib/process/command/path.kh"\n'
        )
        self.assertEqual(len(declarations), 1)
        inclusion = declarations[0]
        self.assertEqual(inclusion.kind, "vr-in")
        self.assertEqual(inclusion.name, "cwd")
        self.assertEqual(inclusion.line, 1)
        self.assertEqual(inclusion.composition, ["modules/lib/process/command/path.kh"])
        # Not read as the typed variable it is not: `in` is a keyword, so a
        # reader that took it for a type reference would have refused the line.
        self.assertNotEqual(inclusion.kind, "vr")

    def test_reading_goes_on_after_a_variable_inclusion(self):
        # An inclusion is a declaration, so the file is not read as though it
        # ended there: the typed variable after it is still a typed variable.
        declarations = parse_khayyam_source(
            "page.kh",
            'vr cwd in "modules/lib/process/command/path.kh"\n'
            "vr ed String\n"
            "tp Page ab\n",
        )
        self.assertEqual(
            [(entry.kind, entry.name, entry.composition) for entry in declarations],
            [
                ("vr-in", "cwd", ["modules/lib/process/command/path.kh"]),
                ("vr", "ed", ["String"]),
                ("ab", "Page", []),
            ],
        )

    def test_the_address_is_a_uri_and_not_a_plain_value(self):
        # The language states the address as a URI and leaves what a URI may
        # look like to the resolver, so a bare name is not one and the reader
        # says so where the address stands -- the same refusal a type inclusion
        # gets, at its own line.
        self.assertEqual(
            self.refuse("vr MaxTimeout in bare\n"), "page.kh:1: import path must be a string"
        )
        self.assertEqual(
            self.refuse("vr MaxTimeout in\n"), "page.kh:1: import path must be a string"
        )
        self.assertEqual(
            self.refuse('vr MaxTimeout in a.b\n'), "page.kh:1: import path must be a string"
        )
        # A name is a name and not a keyword: `in` names the inclusion, and the
        # frontend refuses a keyword in a name's place as `keyword-as-identifier`.
        self.assertEqual(
            self.refuse('vr in "modules/a/b.kh"\n'), "page.kh:1: expected a name"
        )
        # A declaration occupies one line and the line's break ends it
        # (`docs/khayyam/khayyam.md`, Declaration separator), so nothing may
        # follow the address on that line.
        self.assertEqual(
            self.refuse('vr cwd in "modules/lib/process/command/path.kh" extra\n'),
            "page.kh:1: expected a declaration separator, got 'extra'",
        )


if __name__ == "__main__":
    unittest.main()

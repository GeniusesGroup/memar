"""Tests for names: python -m unittest test_names"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True

import names as names


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


from khayyam_source import khayyam_uri


class Addresses(unittest.TestCase):
    def test_in_uri_is_repository_relative(self):
        self.assertEqual(
            khayyam_uri("modules/codec/string/protocol/string.kh"),
            "modules/codec/string/protocol/string.kh",
        )

    def test_corpus_roots_map_to_archive_roots(self):
        cases = {
            "modules": "modules",
            "modules/app/protocol": "modules/app/protocol",
            "modules/gui/services/x": "modules/gui/services/x",
            "modulesx/y": "modulesx/y",
            "libgo/net/http/protocol": "lib/net/http/protocol",
            "libgo/time/timer/protocol": "time/timer/protocol",
            "libgo": "lib",
            "storage/block/protocol": "memory/block/protocol",
            "storage/memory/reference/mutable": "memory/reference/mutable",
            "storage/memory/protocol/address": "memory/address/protocol/address",
            "storage/memory/pointer": "memory/address/pointer",
            "storage": "memory",
            "codec/string/protocol": "codec/string/protocol",
            "libgoose": "libgoose",
        }
        for corpus, archive in cases.items():
            self.assertEqual(names.normalize_module(corpus), archive, corpus)

    def test_corpus_root_packages_stay_beside_the_modules_folder(self):
        for root in ("codec", "computer", "crypto", "identifier", "math", "memory", "net", "process", "time"):
            self.assertEqual(names.normalize_module(f"{root}/x/protocol"), f"{root}/x/protocol", root)

    def test_the_corpus_modules_folder_is_never_stripped(self):
        for corpus in ("modules", "modules/app", "modules/error/protocol", "modules/init-cmd"):
            self.assertTrue(names.normalize_module(corpus).startswith("modules"), corpus)
            self.assertEqual(names.normalize_module(corpus), corpus)

    def test_archive_files_drop_only_the_archive_root(self):
        cases = {
            "modules": "",
            "modules/gui/protocol": "gui/protocol",
            "modules/modules/app/protocol": "modules/app/protocol",
            "docs": "docs",
        }
        for relative, module in cases.items():
            self.assertEqual(names.archive_module(relative), module, relative)

    def test_the_modules_folder_does_not_qualify_names(self):
        self.assertEqual(names.module_identity("modules/module/protocol"), ["module"])
        self.assertEqual(names.module_identity("modules"), [])
        self.assertEqual(names.module_identity("codec/string/protocol"), ["string", "codec"])


class Naming(unittest.TestCase):
    """The name predicates every mode shares."""

    def test_a_field_name_starts_with_field(self):
        self.assertEqual(names.split_field_name("URI_Field_Scheme"), ("URI", "Scheme"))
        self.assertEqual(names.split_field_name("Field_URI_Scheme"), ("", "URI_Scheme"))
        self.assertIsNone(names.split_field_name("URI_Scheme"))
        self.assertEqual(names.field_name("Scheme"), "Observer_Scheme")
        self.assertEqual(names.field_name("Scheme", "URI"), "Observer_URI_Scheme")

    def test_a_qualifier_goes_after_field(self):
        self.assertEqual(names.qualify_name("URI", "Observer_Scheme"), "Observer_URI_Scheme")
        self.assertEqual(names.qualify_name("UTF8", "Stringer"), "UTF8_Stringer")

    def test_repeats_matches_whole_words(self):
        self.assertTrue(names.repeats("Block", "BlockNumber"))
        self.assertFalse(names.repeats("Block", "Blocking"))
        self.assertFalse(names.repeats("URI", "Scheme"))

    def test_a_field_holds_its_concept_or_its_singular(self):
        self.assertTrue(names.field_holds_its_concept("Scheme", ["URI_Scheme"]))
        self.assertTrue(names.field_holds_its_concept("Lengths", ["Syllab_Length"]))
        self.assertFalse(names.field_holds_its_concept("Access", ["Time"]))

    def test_a_field_accessor_is_named_for_the_value_it_returns(self):
        self.assertEqual(names.field_accessor_options("URI_Field_Scheme", "Scheme")[:2], ["Scheme", "URIScheme"])
        self.assertIn("SocketStatus", names.field_accessor_options("Observer_SocketStatus", "Status"))
        self.assertEqual(names.field_accessor_options("URI", "Scheme"), ["Scheme"])

    def test_a_field_qualified_after_field_is_qualified_by_its_module(self):
        self.assertTrue(names.qualified_by_module("Observer_Scheme", "Observer_URI_Scheme", "net/uri"))

if __name__ == "__main__":
    unittest.main()

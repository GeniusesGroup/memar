"""Tests for corpus_port: python -m unittest test_corpus_port"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path
from corpus_port import CorpusPort
from go_source_block import CORPUS_LICENSE

LICENSE = CORPUS_LICENSE


class Reemit(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        base = Path(self.directory.name)
        self.go = base / "go"
        self.memar = base / "memar"
        write(self.go, "go.mod", "module memar\n")
        write(
            self.go,
            "codec/string/protocol/string.go",
            "package string_p\n\ntype String interface{}\n",
        )
        write(
            self.go,
            "x/protocol/thing.go",
            "package x_p\n"
            "\n"
            "// Thing is a thing.\n"
            "type Thing interface {\n"
            "\tName() string // It must be unique\n"
            "}\n"
            "\n"
            "type Noted interface{}\n"
            "\n"
            "const Limit = 3\n",
        )
        self.string = write(
            self.memar, "modules/codec/string/protocol/string.kh", f"{LICENSE}\n\ntp String ab\n"
        )
        self.thing = write(
            self.memar,
            "modules/x/protocol/thing.kh",
            f"{LICENSE}\n"
            "\n"
            'tp String in "modules/codec/string/protocol/string.kh"\n'
            "\n"
            "// Thing is a thing.\n"
            "tp Thing ab\n"
            "tp Thing_Name mt (self Thing) () (result0 String)\n",
        )
        self.orphan = write(
            self.memar,
            "modules/x/protocol/orphan.kh",
            f"{LICENSE}\n\n// Orphan has no Go source.\ntp Orphan ab\n",
        )
        self.capsule = write(
            self.memar, "modules/x/protocol/capsule.kh", f"{LICENSE}\n\ntp Capsule cp {{\n}}\n"
        )
        self.noted = write(
            self.memar,
            "modules/x/protocol/noted.kh",
            f"{LICENSE}\n\n// recovered by hand from the Go source\ntp Noted ab\n",
        )
        self.originals = {
            path: path.read_text(encoding="utf-8")
            for path in (self.string, self.thing, self.orphan, self.capsule, self.noted)
        }

    def tearDown(self):
        self.directory.cleanup()

    def run_port(self, write: bool) -> dict:
        return CorpusPort(self.go, self.memar).run(write=write)

    def test_dry_run_writes_nothing(self):
        self.run_port(write=False)
        for path, text in self.originals.items():
            self.assertEqual(path.read_text(encoding="utf-8"), text, path)

    def test_rewrites_what_the_corpus_carries(self):
        summary = self.run_port(write=True)
        self.assertEqual(summary["written"], 1)
        text = self.thing.read_text(encoding="utf-8")
        self.assertIn('tp String in "modules/codec/string/protocol/string.kh"', text)
        self.assertIn("// Thing is a thing.\ntp Thing ab", text)
        self.assertIn("// It must be unique\ntp Name mt (self Thing) () (result0 String)", text)

    def test_guards_files_the_corpus_cannot_reproduce(self):
        summary = self.run_port(write=True)
        guarded = set(summary["guarded_files"])
        self.assertEqual(
            guarded,
            {
                "modules/x/protocol/orphan.kh",
                "modules/x/protocol/capsule.kh",
                "modules/x/protocol/noted.kh",
            },
        )
        for path in (self.orphan, self.capsule, self.noted):
            self.assertEqual(path.read_text(encoding="utf-8"), self.originals[path], path)

    def test_only_narrows_writing_not_placement(self):
        summary = CorpusPort(self.go, self.memar, only=["x/protocol/thing.kh"]).run(write=True)
        self.assertEqual(summary["targets"], 1)
        text = self.thing.read_text(encoding="utf-8")
        self.assertNotIn("tp Noted ab", text)
        self.assertNotIn("tp String ab", text)
        for path in (self.string, self.orphan, self.capsule, self.noted):
            self.assertEqual(path.read_text(encoding="utf-8"), self.originals[path], path)

    def test_reports_constants_it_cannot_port(self):
        summary = self.run_port(write=False)
        self.assertIn(
            "x/protocol/thing.go: const Limit", summary["constants_and_variables_not_ported"]
        )


class TypeOwnedInstantiations(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.memar = self.root / "memar"
        write(self.root, "go.mod", "module memar\n")
        write(
            self.root,
            "math/logic/protocol/equivalence.go",
            "package logic_p\n\ntype Equivalence[T any] interface {\n\tEquivalence(with T) bool\n}\n",
        )
        write(
            self.root,
            "codec/string/protocol/character.go",
            "package string_p\n\nimport logic_p \"memar/math/logic/protocol\"\n\n"
            "type Character interface {\n\tlogic_p.Equivalence[Character]\n}\n",
        )
        write(
            self.memar,
            "modules/math/logic/protocol/equivalence.kh",
            f"{LICENSE}\n\ntp Logic_Equivalence ab\n",
        )
        write(
            self.memar,
            "modules/codec/string/protocol/character.kh",
            f"{LICENSE}\n\ntp Character ab {{\n    Logic_Equivalence\n}}\n",
        )

    @property
    def memar_modules(self) -> Path:
        return self.memar / "modules"

    def tearDown(self):
        self.temp.cleanup()

    def test_single_type_argument_instantiations_live_in_the_owner_module(self):
        port = CorpusPort(self.root, self.memar)
        port.prepare()
        instantiations = list(port.instantiation_index.values())
        self.assertEqual(len(instantiations), 1)
        instantiation = instantiations[0]
        self.assertTrue(instantiation.type_owned)
        self.assertEqual(
            instantiation.home,
            "modules/codec/string/protocol/character.kh",
        )
        self.assertEqual(instantiation.decl.output_file, "modules/math/logic/protocol/equivalence.kh")

if __name__ == "__main__":
    unittest.main()

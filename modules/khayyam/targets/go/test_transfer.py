"""Tests for transfer: python -m unittest test_transfer"""

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
import shutil

from go_source_block import (
    CORPUS_LICENSE,
    RESIDUE_MARKER,
    SOURCE_BLOCK_HEAD,
    preserve_transfer_text,
    render_source_block,
    residue_marker,
    verify_source_block,
)
from transfer import GoTransfer, insertion_hazards, transfer_items

LICENSE = CORPUS_LICENSE


THING_GO = (
    "package x_p\n"
    "\n"
    "// Thing is a thing.\n"
    "type Thing interface {\n"
    "\tName() string // It must be unique\n"
    "\tRaw() []byte\n"
    "\tAny(value any)\n"
    "}\n"
    "\n"
    "// GUI is the default Thing.\n"
    "var GUI Thing\n"
    "\n"
    "var Count = 3\n"
    "\n"
    "const Limit = 3\n"
    "\n"
    "const (\n"
    "\tA Kind = iota\n"
    "\tB\n"
    ")\n"
    "\n"
    "type Kind uint8\n"
    "\n"
    "type Pair struct {\n"
    "\ta int\n"
    "}\n"
    "\n"
    "func (p *Pair) Sum() int {\n"
    "\treturn p.a\n"
    "}\n"
)


class Placement(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        base = Path(self.directory.name)
        self.go = base / "memar-go"
        self.memar = base / "memar"
        write(self.go, "go.mod", "module memar\n")
        write(self.go, "modules/app/protocol/domain.go", "package app_p\n")
        write(self.go, "modules/const.go", "package modules\n")
        write(self.go, "math/boolean/boolean.go", "package boolean\n")
        write(self.go, "libgo/net/http/http.go", "package http\n")
        write(self.go, "libgo/time/timer/timer.go", "package timer\n")
        self.memar.mkdir()

    def tearDown(self):
        self.directory.cleanup()

    def placed(self) -> dict[str, tuple[str, str]]:
        items = transfer_items(self.go, self.memar / "modules", self.memar, self.go, recursive=True)
        return {item.relative: (item.dest_relative, item.module) for item in items}

    def test_recursive_transfer_keeps_the_modules_folder(self):
        placed = self.placed()
        self.assertEqual(placed["modules/app/protocol/domain.go"], ("modules/modules/app/protocol/domain.kh", "modules/app/protocol"))
        self.assertEqual(placed["modules/const.go"], ("modules/modules/const.kh", "modules"))

    def test_recursive_transfer_keeps_root_packages_at_the_archive_root(self):
        placed = self.placed()
        self.assertEqual(placed["math/boolean/boolean.go"], ("modules/math/boolean/boolean.kh", "math/boolean"))
        self.assertEqual(placed["libgo/net/http/http.go"], ("modules/lib/net/http/http.kh", "lib/net/http"))
        self.assertEqual(placed["libgo/time/timer/timer.go"], ("modules/time/timer/timer.kh", "time/timer"))

    def test_a_go_file_under_the_archive_takes_the_archive_module(self):
        path = write(self.memar, "modules/gui/protocol/scroll.go", "package gui_p\n")
        items = transfer_items(path, self.memar / "modules/gui/protocol/scroll.kh", self.memar, self.go, recursive=False)
        self.assertEqual(items[0].module, "gui/protocol")
        self.assertEqual(items[0].dest_relative, "modules/gui/protocol/scroll.kh")


def todo_blocks(text: str) -> int:
    return sum(
        1
        for line in text.splitlines()
        if line.startswith("// TODO(go-migrate):")
        and not RESIDUE_MARKER.match(line)
        and line != SOURCE_BLOCK_HEAD
    )


class Transfer(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        base = Path(self.directory.name)
        self.go = base / "memar-go"
        self.memar = base / "memar"
        write(self.go, "go.mod", "module memar\n")
        write(self.go, "codec/string/protocol/string.go", "package string_p\n\ntype String interface{}\n")
        self.thing_go = write(self.go, "x/protocol/thing.go", THING_GO)
        self.clean_go = write(
            self.go, "y/protocol/clean.go", "package y_p\n\ntype Clean interface {\n\tLabel() string\n}\n"
        )
        write(self.memar, "modules/codec/string/protocol/string.kh", f"{LICENSE}\n\ntp String ab\n")
        self.thing = self.memar / "modules/x/protocol/thing.kh"
        self.clean = self.memar / "modules/y/protocol/clean.kh"

    def tearDown(self):
        self.directory.cleanup()

    def transfer(self, source: Path, dest: Path, write: bool, frontend: bool = False, cls=GoTransfer):
        items = transfer_items(source, dest, self.memar, self.go, recursive=False)
        port = cls(items, self.memar, self.go, frontend=frontend)
        return port, port.run(write=write)

    def test_dry_run_writes_nothing_and_makes_no_directory(self):
        _, summary = self.transfer(self.thing_go, self.thing, write=False)
        self.assertEqual(summary["files"], {"created": 1})
        self.assertFalse(self.thing.exists())
        self.assertFalse((self.memar / "modules/x").exists())

    def test_write_creates_a_missing_destination(self):
        _, summary = self.transfer(self.thing_go, self.thing, write=True)
        self.assertEqual(summary["files"], {"created": 1})
        text = self.thing.read_text(encoding="utf-8")
        self.assertIn('tp String in "modules/codec/string/protocol/string.kh"', text)
        self.assertIn("// Thing is a thing.\ntp Thing ab", text)
        self.assertIn("// It must be unique\ntp Name mt (self Thing) () (result0 String)", text)
        self.assertNotIn('"memar/', text)

    def test_var_with_a_resolvable_type_becomes_vr_with_a_binding_todo(self):
        self.transfer(self.thing_go, self.thing, write=True)
        text = self.thing.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"// GUI is the default Thing\.\n// TODO\(go-migrate\): Khayyam has no assignment operator[^\n]*\n"
            r"// var GUI Thing\nvr GUI Thing\n",
        )

    def test_constants_iota_and_initialized_vars_are_residue_with_their_text(self):
        self.transfer(self.thing_go, self.thing, write=True)
        text = self.thing.read_text(encoding="utf-8")
        body = text.split(SOURCE_BLOCK_HEAD)[0]
        self.assertRegex(body, r"// TODO\(go-migrate\): const:[^\n]*\n// const Limit = 3\n")
        self.assertRegex(body, r"// TODO\(go-migrate\): const:[^\n]*iota[^\n]*\n// \tA Kind = iota\n")
        self.assertRegex(body, r"// TODO\(go-migrate\): const:[^\n]*iota[^\n]*\n// \tB\n")
        self.assertRegex(body, r"// TODO\(go-migrate\): var with an initial value[^\n]*\n// var Count = 3\n")

    def test_methods_with_bytes_or_any_are_residue_not_dropped(self):
        self.transfer(self.thing_go, self.thing, write=True)
        body = self.thing.read_text(encoding="utf-8").split(SOURCE_BLOCK_HEAD)[0]
        self.assertRegex(body, r"// TODO\(go-migrate\): method not portable: Go slice[^\n]*\n// \tRaw\(\) \[\]byte\n")
        self.assertRegex(body, r"// TODO\(go-migrate\): method not portable: Go 'any'[^\n]*\n// \tAny\(value any\)\n")

    def test_first_line_marks_residue_and_only_residue(self):
        self.transfer(self.thing_go, self.thing, write=True)
        self.transfer(self.clean_go, self.clean, write=True)
        self.assertEqual(
            self.thing.read_text(encoding="utf-8").splitlines()[0],
            "// TODO(go-migrate): residue from memar-go/x/protocol/thing.go; full original source is at end of file",
        )
        clean = self.clean.read_text(encoding="utf-8")
        self.assertEqual(clean.splitlines()[0], LICENSE)
        self.assertIn("tp Label mt (self Clean) () (result0 String)", clean)

    def test_residue_count_matches_todo_blocks(self):
        _, summary = self.transfer(self.thing_go, self.thing, write=True)
        text = self.thing.read_text(encoding="utf-8")
        self.assertEqual(summary["constructs"]["residue"], todo_blocks(text))
        self.assertEqual(summary["todo_blocks_added"], todo_blocks(text))

    def test_full_source_block_is_faithful_even_for_crlf(self):
        raw = THING_GO.replace("\n", "\r\n").encode("utf-8") + "// Â§ Ú©Ø¯\r\n".encode("utf-8")
        self.thing_go.write_bytes(raw)
        self.transfer(self.thing_go, self.thing, write=True)
        text = self.thing.read_text(encoding="utf-8")
        self.assertIsNone(verify_source_block(text, "memar-go/x/protocol/thing.go", raw))
        self.assertIn("// // Â§ Ú©Ø¯\n", text)
        self.assertIsNotNone(verify_source_block(text.replace("// \tB\n", "// \tC\n"), "memar-go/x/protocol/thing.go", raw))

    def test_rerun_is_unchanged(self):
        self.transfer(self.thing_go, self.thing, write=True)
        first = self.thing.read_text(encoding="utf-8")
        _, summary = self.transfer(self.thing_go, self.thing, write=True)
        self.assertEqual(summary["files"], {"unchanged": 1})
        self.assertEqual(self.thing.read_text(encoding="utf-8"), first)

    def test_existing_destination_only_gains_lines(self):
        original = (
            f"{LICENSE}\n"
            "\n"
            'tp String in "modules/codec/string/protocol/string.kh"\n'
            "\n"
            "// recovered by hand from the Go source\n"
            "tp Thing ab\n"
            "tp Name mt (self Thing) () (result0 String)\n"
            "tp Holder cp {\n"
            "}\n"
        )
        write(self.memar, "modules/x/protocol/thing.kh", original)
        _, summary = self.transfer(self.thing_go, self.thing, write=True)
        self.assertEqual(summary["files"], {"appended": 1})
        text = self.thing.read_text(encoding="utf-8")
        self.assertEqual(insertion_hazards(original, text), [])
        self.assertEqual(text.count("tp Thing ab"), 1)
        self.assertEqual(text.count("mt (self Thing) () (result0 String)"), 1)
        self.assertIn("tp Holder cp {", text)
        self.assertIsNone(verify_source_block(text, "memar-go/x/protocol/thing.go", THING_GO.encode()))

    def test_residue_a_hand_port_already_quotes_is_not_repeated(self):
        original = (
            "// TODO(go-migrate): manual port from x/protocol/thing.go; search TODO(go-migrate) in this file\n"
            f"{LICENSE}\n"
            "\n"
            "tp Thing ab\n"
            "// TODO(go-migrate): slice result has no Khayyam form yet. Original Go:\n"
            "// \tRaw() []byte\n"
        )
        write(self.memar, "modules/x/protocol/thing.kh", original)
        port, _ = self.transfer(self.thing_go, self.thing, write=True)
        raw = [entry for entry in port.entries if entry.construct == "method Thing.Raw"]
        self.assertEqual([entry.state for entry in raw], ["present"])
        body = self.thing.read_text(encoding="utf-8").split(SOURCE_BLOCK_HEAD)[0]
        self.assertEqual(body.count("// \tRaw() []byte"), 1)
        self.assertIn("// \tAny(value any)", body)

    def test_source_only_adds_just_the_block_and_marker_to_a_hand_port(self):
        original = (
            f"{LICENSE}\n"
            "\n"
            "tp Thing ab\n"
            "// TODO(go-migrate): the method name is undecided. Original Go:\n"
            "// \tName() string\n"
            "tp Thing_Name_2 mt (self Thing) () (result0 String)\n"
        )
        write(self.memar, "modules/x/protocol/thing.kh", original)
        items = transfer_items(self.thing_go, self.thing, self.memar, self.go, recursive=False)
        summary = GoTransfer(items, self.memar, self.go, frontend=False, source_only=True).run(write=True)
        self.assertEqual(summary["files"], {"appended": 1})
        text = self.thing.read_text(encoding="utf-8")
        head, block = text.split(SOURCE_BLOCK_HEAD)
        self.assertEqual(head, residue_marker("memar-go/x/protocol/thing.go") + "\n" + original + "\n")
        self.assertIsNone(verify_source_block(text, "memar-go/x/protocol/thing.go", THING_GO.encode()))

    def test_a_result_that_would_lose_content_is_not_written(self):
        original = f"{LICENSE}\n\n// kept by hand\ntp Thing ab\n"
        write(self.memar, "modules/x/protocol/thing.kh", original)

        class Thinner(GoTransfer):
            def render(self, item, current):
                return f"{LICENSE}\n\ntp Other ab\n", []

        _, summary = self.transfer(self.thing_go, self.thing, write=True, cls=Thinner)
        self.assertEqual(summary["files"], {"guarded": 1})
        self.assertIn("target-would-lose-content", summary["file_states"]["modules/x/protocol/thing.kh"])
        self.assertEqual(self.thing.read_text(encoding="utf-8"), original)

    def test_reemit_keeps_transfer_markers_and_source_blocks(self):
        marker = residue_marker("memar-go/x/protocol/thing.go")
        block = render_source_block("memar-go/x/protocol/thing.go", b"package x_p\n")
        existing = "\n".join([marker, LICENSE, "", "tp Thing ab", "", *block]) + "\n"
        kept = preserve_transfer_text(existing, f"{LICENSE}\n\ntp Thing ab\n")
        self.assertEqual(kept, existing)

    @unittest.skipUnless(shutil.which("node"), "node is not on PATH")
    def test_created_files_pass_the_khayyam_frontend(self):
        port, summary = self.transfer(self.thing_go, self.thing, write=True, frontend=True)
        self.assertEqual(summary["files"], {"created": 1})
        self.assertEqual(port.outcomes["modules/x/protocol/thing.kh"]["outcome"], "accept")

    @unittest.skipUnless(shutil.which("node"), "node is not on PATH")
    def test_an_untouched_importer_whose_outcome_moves_is_reported(self):
        write(
            self.memar,
            "modules/z/protocol/user.kh",
            f'{LICENSE}\n\ntp Thing in "modules/x/protocol/thing.kh"\n\ntp User ab {{\n    Thing\n}}\n',
        )
        _, summary = self.transfer(self.thing_go, self.thing, write=False, frontend=True)
        change = summary["dependents_changed"]["modules/z/protocol/user.kh"]
        self.assertEqual(change["before"]["reason"], "unresolved-import")
        self.assertEqual(change["after"]["outcome"], "accept")

if __name__ == "__main__":
    unittest.main()

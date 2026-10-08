"""Tests for tidy: python -m unittest test_tidy"""

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
from go_source_block import CORPUS_LICENSE
from tidy import TIDY_RULES, run_tidy, tidy_text

LICENSE = CORPUS_LICENSE


def go_block(*go_lines: str) -> str:
    return "\n".join(["// TODO(go-migrate):", "/*", *go_lines, "*/", ""])


GO_LICENSE = "/* For license and copyright information please see the LEGAL file in the code repository * /"


class Tidy(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write(self.root, "modules/t/protocol/time.kh", f"{LICENSE}\n\ntp Time ab\n")
        write(
            self.root,
            "modules/t/timer/protocol/timer-status.kh",
            f"{LICENSE}\n\ntp Timer_Status ab\n",
        )

    def tearDown(self):
        self.temp.cleanup()

    def tidy(self, text: str, relative: str = "modules/t/timer/protocol/timer.kh", rules=TIDY_RULES):
        return tidy_text(text, relative, self.root, rules)

    def assertIdempotent(self, text: str, relative: str = "modules/t/timer/protocol/timer.kh", rules=TIDY_RULES):
        once, _ = self.tidy(text, relative, rules)
        twice, report = self.tidy(once, relative, rules)
        self.assertEqual(once, twice)
        return once

    # method-separation

    def test_methods_are_separated_by_one_blank_line_in_a_commented_file(self):
        text = (
            f"{LICENSE}\n\n// Timer is a timer.\ntp Timer ab\n"
            "tp Start mt (self Timer) () ()\n// Stop stops it.\ntp Stop mt (self Timer) () ()\n"
        )
        out, report = self.tidy(text, rules=("method-separation",))
        self.assertEqual(
            out,
            f"{LICENSE}\n\n// Timer is a timer.\ntp Timer ab\n"
            "tp Start mt (self Timer) () ()\n\n// Stop stops it.\ntp Stop mt (self Timer) () ()\n",
        )
        self.assertEqual(report.blank_lines, 1)
        self.assertIdempotent(text, rules=("method-separation",))

    def test_separation_never_doubles_a_blank_line(self):
        text = f"{LICENSE}\n\n// T.\ntp T ab\ntp A mt (self T) () ()\n\ntp B mt (self T) () ()\n"
        out, report = self.tidy(text, rules=("method-separation",))
        self.assertEqual(out, text)
        self.assertEqual(report.blank_lines, 0)

    def test_a_file_whose_only_comments_are_license_and_marker_is_not_separated(self):
        text = (
            f"{LICENSE}\n\ntp T ab\ntp A mt (self T) () ()\ntp B mt (self T) () ()\n\n"
            + go_block("package t", "", "type Other interface {", "\tC()", "\tD()", "}")
        )
        out, report = self.tidy(text, rules=("method-separation",))
        self.assertEqual(out, text)

    def test_separation_never_touches_the_go_block(self):
        go = go_block("package t", "", "// Other is kept.", "type Other interface {", "\tC()", "\tD()", "}")
        text = f"{LICENSE}\n\n// T.\ntp T ab\ntp A mt (self T) () ()\ntp B mt (self T) () ()\n\n" + go
        out, _ = self.tidy(text, rules=("method-separation",))
        self.assertTrue(out.endswith(go))

    # go-clue-residue

    def test_a_go_method_is_removed_only_when_its_khayyam_method_exists(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Start mt (self Timer) () ()\n\n"
            + go_block(GO_LICENSE, "", "package timer_p", "", "type Timer interface {", "\tStart()", "\tStop()", "}")
        )
        out, report = self.tidy(text, rules=("go-clue-residue",))
        self.assertIn("tp Start mt (self Timer) () ()", out)
        self.assertNotIn("\tStart()", out)
        self.assertIn("\tStop()", out)
        self.assertNotIn("LEGAL file in the code repository * /", out)
        self.assertEqual(report.licenses_removed, 1)
        self.assertEqual(len(report.members_removed), 1)
        self.assertEqual(report.blocks_shrunk, 1)
        self.assertIdempotent(text, rules=("go-clue-residue",))

    def test_an_owner_prefixed_khayyam_method_represents_the_go_method(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Timer_Start mt (self Timer) () ()\n\n"
            + go_block("package timer_p", "", "type Timer interface {", "\tStart()", "\tStop()", "}")
        )
        out, _ = self.tidy(text, rules=("go-clue-residue",))
        self.assertNotIn("\tStart()", out)
        self.assertIn("\tStop()", out)

    def test_a_method_with_another_arity_is_not_represented(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Start mt (self Timer) () ()\n\n"
            + go_block("package timer_p", "", "type Timer interface {", "\tStart(d int)", "}")
        )
        out, report = self.tidy(text, rules=("go-clue-residue",))
        self.assertIn("\tStart(d int)", out)
        self.assertEqual(report.members_removed, [])

    def test_a_go_comment_not_carried_in_khayyam_keeps_its_declaration(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Start mt (self Timer) () ()\n\n"
            + go_block("package timer_p", "", "type Timer interface {", "\tStart() // begins counting", "}")
        )
        out, _ = self.tidy(text, rules=("go-clue-residue",))
        self.assertIn("\tStart() // begins counting", out)

    def test_a_fully_represented_block_and_its_marker_are_removed(self):
        head = f"{LICENSE}\n\ntp Timer ab\n// Start begins.\ntp Start mt (self Timer) () ()\n"
        text = head + "\n" + go_block(
            GO_LICENSE, "", "package timer_p", "", "type Timer interface {", "\t// Start begins.", "\tStart()", "}"
        )
        out, report = self.tidy(text, rules=("go-clue-residue",))
        self.assertEqual(out, head)
        self.assertNotIn("TODO(go-migrate)", out)
        self.assertEqual(report.blocks_removed, 1)
        self.assertEqual(len(report.types_removed), 1)

    def test_a_multi_line_raw_string_does_not_shift_the_removed_line(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Start mt (self Timer) () ()\n\n"
            + go_block(
                "package timer_p",
                "",
                "var Detail = `first",
                "second",
                "third`",
                "",
                "type Timer interface {",
                "\tStart()",
                "\tStop()",
                "}",
            )
        )
        out, _ = self.tidy(text, rules=("go-clue-residue",))
        self.assertIn("type Timer interface {\n\tStop()\n}", out)
        self.assertIn("var Detail = `first\nsecond\nthird`", out)

    def test_a_go_function_with_a_body_is_never_removed(self):
        text = (
            f"{LICENSE}\n\ntp Timer ab\ntp Start mt (self Timer) () ()\n\n"
            + go_block("package timer_p", "", "func (t *Timer) Start() {", "\tt.run()", "}")
        )
        out, _ = self.tidy(text, rules=("go-clue-residue",))
        self.assertIn("func (t *Timer) Start() {", out)

    # commented-generic-bindings

    TIMER_GO = (
        "package timer_p",
        "",
        "import (",
        '\ttime_p "memar/t/protocol"',
        ")",
        "",
        "type Timer[TIME time_p.Time, ST TimerStatus] interface {",
        "\tWhen() TIME",
        "\t// Status reports the status.",
        "\tStatus() ST",
        "}",
    )

    def test_bound_generic_methods_become_khayyam_methods_with_qualified_types(self):
        text = f"{LICENSE}\n\n// Timer is a timer.\ntp Timer ab\n\n" + go_block(*self.TIMER_GO)
        out, report = self.tidy(text)
        self.assertIn('tp Time in "modules/t/protocol/time.kh"', out)
        self.assertIn('tp Timer_Status in "modules/t/timer/protocol/timer-status.kh"', out)
        self.assertIn("tp When mt (self Timer) () (t Time)\n\n// Status reports the status.\n", out)
        self.assertIn("// Status reports the status.\ntp Status mt (self Timer) () (s Timer_Status)", out)
        self.assertEqual(len(report.methods_realized), 2)
        self.assertEqual(report.unresolved, [])
        self.assertIdempotent(text)

    def test_an_unresolvable_binding_is_left_and_reported(self):
        go = list(self.TIMER_GO)
        go[6] = "type Timer[TIME time_p.Time, ST Missing] interface {"
        text = f"{LICENSE}\n\n// Timer is a timer.\ntp Timer ab\n\n" + go_block(*go)
        out, report = self.tidy(text)
        self.assertIn("\tStatus() ST", out)
        self.assertNotIn("tp Status mt", out)
        self.assertNotIn("Missing mt", out)
        self.assertEqual(len(report.unresolved), 1)
        self.assertEqual(report.unresolved[0]["method"], "Status")
        self.assertEqual(report.unresolved[0]["binding"], "ST Missing")

    def test_an_open_type_parameter_is_not_a_binding(self):
        text = (
            f"{LICENSE}\n\ntp Box ab\n\n"
            + go_block("package t", "", "type Box[E any] interface {", "\tGet() E", "}")
        )
        out, report = self.tidy(text)
        self.assertIn("\tGet() E", out)
        self.assertEqual(report.methods_realized, [])
        self.assertEqual(report.unresolved, [])
        self.assertEqual(len(report.open_parameters), 1)

    # result-parameter-names

    def test_synthetic_names_take_the_first_letter_of_their_type(self):
        text = f"{LICENSE}\n\ntp T ab\ntp A mt (self T) (arg0 Timer_Status) (result0 Time, result1 Error)\n"
        out, report = self.tidy(text, rules=("result-parameter-names",))
        self.assertIn("tp A mt (self T) (s Timer_Status) (t Time, e Error)", out)
        self.assertEqual(len(report.renames), 3)
        self.assertIdempotent(text, rules=("result-parameter-names",))

    def test_a_colliding_name_takes_two_letters_then_a_number(self):
        text = f"{LICENSE}\n\ntp T ab\ntp A mt (self T) (s String) (result0 Status, result1 Status, result2 Status)\n"
        out, _ = self.tidy(text, rules=("result-parameter-names",))
        self.assertIn("(s String) (st Status, st1 Status, st2 Status)", out)

    def test_author_chosen_names_are_kept(self):
        text = f"{LICENSE}\n\ntp T ab\ntp A mt (self T) (with Bool) (ok Bool)\n"
        out, report = self.tidy(text, rules=("result-parameter-names",))
        self.assertEqual(out, text)
        self.assertEqual(report.renames, [])

    def test_run_tidy_preserves_crlf_and_a_second_run_changes_nothing(self):
        path = write(
            self.root,
            "modules/t/timer/protocol/timer.kh",
            f"{LICENSE}\n\n// Timer is a timer.\ntp Timer ab\n\n" + go_block(*self.TIMER_GO),
        )
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        first = run_tidy(self.root, write=True)
        self.assertIn("modules/t/timer/protocol/timer.kh", first["changed"])
        self.assertNotIn(b"\n", path.read_bytes().replace(b"\r\n", b""))
        second = run_tidy(self.root, write=True)
        self.assertEqual(second["changed"], [])

if __name__ == "__main__":
    unittest.main()

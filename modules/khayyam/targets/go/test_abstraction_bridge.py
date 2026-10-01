"""Tests for abstraction_bridge: python -m unittest test_abstraction_bridge"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True

import abstraction_bridge as bridge
from go_source_block import CORPUS_LICENSE


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


THE_PAGE = (
    "package p\n"
    "\n"
    "// Page is a page.\n"
    "type Page interface {\n"
    "\tPath() string // To route page by path\n"
    "\tDepth() int\n"
    "}\n"
    "\n"
    "// Count is a struct.\n"
    "type Count struct{ n int }\n"
    "\n"
    "func (c Count) Add(other Count) Count { return c }\n"
    "\n"
    "// Holder references a non-interface.\n"
    "type Holder interface {\n"
    "\tOwn() Count\n"
    "}\n"
    "\n"
    "type Marker interface{}\n"
    "\n"
    "type Composite interface {\n"
    "\tPage\n"
    "\tMarker\n"
    "}\n"
)


class Refusals(unittest.TestCase):
    """One refusal surface for both directions: the messages, without the path
    of the temporary corpus they name, which is not what is being pinned."""

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.base = Path(self.directory.name)

    def tearDown(self):
        self.directory.cleanup()

    def reasons(self, call) -> list[str]:
        try:
            call()
        except bridge.BridgeFailure as failure:
            messages = failure.messages
        except bridge.SourceFailure as failure:
            messages = [str(failure)]
        else:
            return []
        return [message.replace(str(self.base) + "\\", "").replace(str(self.base) + "/", "") for message in messages]

    def go(self, text: str, mode: int, only: str | None = None) -> str:
        return self.reasons(
            lambda: bridge.convert_go_to_khayyam([str(write(self.base, "input.go", text))], mode, only)
        )

    def kh(self, text: str) -> str:
        return self.reasons(lambda: bridge.convert_khayyam_to_go([str(write(self.base, "page.kh", text))]))


class GoToKhayyam(Refusals):
    """Mode 1 promotes a referenced non-interface; mode 2 refuses it."""

    def emit(self, text: str, only: str | None = None) -> str:
        return bridge.convert_go_to_khayyam([str(write(self.base, "input.go", text))], 1, only)

    def test_promoting_writes_the_imports_the_abstractions_and_their_methods(self):
        self.assertEqual(
            self.emit(THE_PAGE),
            'tp String in "memar/codec/string/protocol"\n'
            'tp S64 in "memar/math/integer"\n'
            "tp Page ab\n"
            "tp Path mt (self Page) () (result0 String)\n"
            "tp Depth mt (self Page) () (result0 S64)\n"
            "tp Holder ab\n"
            "tp Own mt (self Holder) () (result0 Count)\n"
            "tp Marker ab\n"
            "tp Composite ab {\n"
            "    Page\n"
            "    Marker\n"
            "}\n"
            "tp Count ab\n"
            "tp Add mt (self Count) (other Count) (result0 Count)\n",
        )

    def test_promotion_declares_the_promoted_type_after_the_interfaces_and_its_own_methods(self):
        lines = self.emit(THE_PAGE).splitlines()
        self.assertGreater(lines.index("tp Count ab"), lines.index("tp Composite ab {"))
        self.assertEqual(
            lines[lines.index("tp Count ab") + 1], "tp Add mt (self Count) (other Count) (result0 Count)"
        )

    def test_a_go_type_only_a_method_names_promotes_to_a_name_of_its_own(self):
        self.assertEqual(
            self.emit("package p\n\ntype H interface {\n\tOwn() Absent\n}\n"),
            "tp H ab\ntp Own mt (self H) () (result0 Absent)\ntp Absent ab\n",
        )

    def test_a_type_with_no_khayyam_form_at_all_becomes_a_numbered_empty_interface(self):
        self.assertEqual(
            self.emit("package p\n\ntype H interface {\n\tAny(value any)\n}\n"),
            "tp EmptyInterface1 ab\n"
            "tp H ab\n"
            "tp Any mt (self H) (value EmptyInterface1) ()\n",
        )
        self.assertIn(
            "tp EmptyInterface2 ab",
            self.emit("package p\n\ntype H interface {\n\tOne(a any)\n\tTwo(b any)\n}\n"),
        )

    def test_only_narrows_to_one_interface_and_to_one_method(self):
        self.assertEqual(
            self.emit(THE_PAGE, "Page"),
            'tp String in "memar/codec/string/protocol"\n'
            'tp S64 in "memar/math/integer"\n'
            "tp Page ab\n"
            "tp Path mt (self Page) () (result0 String)\n"
            "tp Depth mt (self Page) () (result0 S64)\n",
        )
        self.assertEqual(
            self.emit(THE_PAGE, "Page.Path"),
            'tp String in "memar/codec/string/protocol"\n'
            "tp Page ab\n"
            "tp Path mt (self Page) () (result0 String)\n",
        )

    def test_only_naming_what_the_corpus_does_not_have_is_refused(self):
        self.assertEqual(self.go(THE_PAGE, 1, "Page.Nope"), ["input.go:4: selected method 'Nope' is not in interface 'Page'"])
        self.assertEqual(self.go(THE_PAGE, 1, "Absent"), ["selected interface 'Absent' was not found"])

    def test_a_go_type_with_no_khayyam_form_is_refused_in_both_modes_and_never_guessed_at(self):
        source = "package p\n\ntype P interface {\n\tRender() []string\n}\n"
        for mode in (1, 2):
            self.assertEqual(
                self.go(source, mode),
                ["input.go:4: method Render of interface P has unmappable slice type '[] string'"],
                mode,
            )

    def test_a_generic_interface_is_refused_whole_and_its_generic_method_is_not_reported_separately(self):
        self.assertEqual(
            self.go("package p\n\ntype G[T any] interface {\n\tGet() T\n}\n", 1),
            ["input.go:3: generic interface 'G' is unmappable"],
        )
        self.assertEqual(
            self.go("package p\n\ntype P interface {\n\tGet[T any]() T\n}\n", 1),
            ["input.go:3: generic interface 'P' is unmappable"],
        )

    def test_mode_1_promotes_the_non_interface_and_mode_2_refuses_it_naming_that_reason(self):
        self.assertIn(
            "tp Count ab\ntp Add mt (self Count) (other Count) (result0 Count)", self.emit(THE_PAGE)
        )
        self.assertEqual(
            self.go(THE_PAGE, 2),
            [
                "input.go: method Own of interface Holder cannot reference 'Count' from a Khayyam "
                "abstraction: it is a non-interface type and mode 2 forbids promotion"
            ],
        )

    def test_mode_2_names_the_other_reason_when_it_cannot_establish_the_kind_either(self):
        self.assertEqual(
            self.go("package p\n\ntype H interface {\n\tOwn() Absent\n}\n", 2),
            [
                "input.go: method Own of interface H cannot reference 'Absent' from a Khayyam "
                "abstraction: its interface kind cannot be established and mode 2 forbids promotion"
            ],
        )

    def test_mode_2_answers_with_the_same_text_it_has_no_reason_to_refuse(self):
        source = "package p\n\n// S is an interface.\ntype S interface {\n\tName() string\n}\n"
        self.assertEqual(
            self.go(source, 2),
            [],
        )
        self.assertEqual(
            self.emit(source),
            'tp String in "memar/codec/string/protocol"\n'
            "tp S ab\n"
            "tp Name mt (self S) () (result0 String)\n",
        )

    def test_a_path_that_does_not_exist_is_refused_by_name(self):
        with self.assertRaises(bridge.BridgeFailure) as caught:
            bridge.convert_go_to_khayyam([str(self.base / "absent.go")], 1)
        self.assertEqual(
            caught.exception.messages, [f"input path does not exist: {self.base / 'absent.go'}"]
        )


class KhayyamToGo(Refusals):
    """The inverse direction emits Go interfaces and refuses what has no Go form."""

    def emit(self, text: str) -> str:
        return bridge.convert_khayyam_to_go([str(write(self.base, "page.kh", text))])

    def test_a_file_that_opens_the_way_every_khayyam_file_in_this_repository_opens_is_read(self):
        # A licence comment, the blank line under it, and a blank line between
        # declarations. `docs/khayyam/khayyam.md` puts a declaration on a line and
        # lets the line's break end it, so a line holding nothing holds no
        # declaration -- whether it opens the file, closes it, or sits between two.
        self.assertEqual(
            self.emit(f"{CORPUS_LICENSE}\n\ntp Page ab\n\ntp Path mt (self Page) () ()\n"),
            "package generated\n\ntype Page interface {\n\tPath()\n}\n",
        )

    def test_a_blank_line_is_no_declaration_wherever_it_falls(self):
        self.assertEqual(
            self.emit("\n\n// only a comment, then a declaration\ntp Page ab\n\n\ntp Path mt (self Page) () ()\n\n"),
            "package generated\n\ntype Page interface {\n\tPath()\n}\n",
        )

    def test_a_byte_order_mark_is_refused_by_name_wherever_the_encoding_puts_it(self):
        # A mark is not text the grammar has a form for, so it is neither read
        # past nor deleted: the reader says what it is and the owner removes it.
        self.assertEqual(
            self.kh("\ufefftp Page ab\n"),
            ["page.kh:1: a byte-order mark is not valid Khayyam"],
        )
        # Past the first character a mark is ordinary text, and the ordinary
        # refusal is the answer there, at the line it sits on -- this reader is
        # not a general scrubber.
        self.assertEqual(self.kh("\n\ufefftp Page ab\n"), ["page.kh:2: expected tp or vr"])

    def test_an_abstraction_with_methods_and_primitive_inclusions_becomes_a_go_interface(self):
        self.assertEqual(
            self.emit(
                'tp String in "memar/codec/string/protocol"\n'
                "tp Page ab\n"
                "tp Path mt (self Page) () (s String)\n"
                "tp Depth mt (self Page) () (d S64)\n"
            ),
            "package generated\n"
            "\n"
            "type Page interface {\n"
            "\tPath() (s string)\n"
            "\tDepth() (d int64)\n"
            "}\n",
        )

    def test_a_composition_of_another_abstraction_is_written_as_an_embedded_interface(self):
        self.assertEqual(
            self.emit("tp Base ab\ntp Derived ab {\n    Base\n}\n"),
            "package generated\n\ntype Base interface {\n}\n\ntype Derived interface {\n\tBase\n}\n",
        )

    def test_an_inclusion_that_is_not_a_primitive_becomes_an_import_and_a_qualified_name(self):
        self.assertEqual(
            self.emit('tp N in "memar/a/b"\ntp Page ab\ntp Path mt (self Page) () (n N)\n'),
            'package generated\n\nimport b "memar/a/b"\n\ntype Page interface {\n\tPath() (n b.N)\n}\n',
        )

    def test_an_abstraction_with_no_method_and_no_composition_is_still_written(self):
        self.assertEqual(self.emit("tp Page ab\n"), "package generated\n\ntype Page interface {\n}\n")

    def test_a_capsule_and_a_value_declaration_have_no_go_interface_form(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Count cp {\n\tn int\n}\n"),
            ["page.kh:2: cp declaration 'Count' has no Go interface form"],
        )
        self.assertEqual(
            self.kh("vr Page String\ntp Page ab\n"),
            ["page.kh:1: vr declaration 'Page' has no Go interface form"],
        )
        # `vr {name} in "{path}"` is an inclusion, and the inclusion is not what
        # would give it a Go form here -- the value it names is. A file-level
        # variable is a module-level constant, singleton or shared configuration
        # value (`docs/khayyam/variable.md`, Variable Scope and Visibility), and
        # this direction emits Go interfaces and refuses what has none (this
        # module's own docstring). A type inclusion earns its Go `import`
        # because an emitted signature references the name it introduces; no
        # signature references a variable, so the import a `vr-in` would want is
        # an import nothing uses, which Go will not compile. The answer is the
        # refusal its typed neighbour gets, naming it -- `vr-in` being what the
        # frontend's own realization calls this declaration
        # (`modules/khayyam/core/src/sr.ts` and `parse.ts`) -- and not a silent
        # drop of a declaration that was read.
        self.assertEqual(
            self.kh('vr MaxTimeout in "modules/time/timeout.kh"\ntp Page ab\n'),
            ["page.kh:1: vr-in declaration 'MaxTimeout' has no Go interface form"],
        )

    def test_a_primitive_is_not_an_interface_and_cannot_be_composed(self):
        self.assertEqual(
            self.kh('tp String in "memar/codec/string/protocol"\ntp Page ab {\n    String\n}\n'),
            [
                "page.kh:2: composition of interface Page composes primitive 'String', "
                "which has no Go interface form"
            ],
        )

    def test_an_unknown_type_and_a_qualified_type_without_an_inclusion_have_no_go_form(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) () (s Mystery)\n"),
            ["page.kh:2: method Path references unknown type 'Mystery', which has no Go interface form"],
        )
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) () (s a.Mystery)\n"),
            [
                "page.kh:2: method Path references qualified type 'a.Mystery' without a resolvable "
                "Khayyam import, which has no Go interface form"
            ],
        )

    def test_a_method_owner_is_exactly_one_parameter_named_self_holding_a_local_abstraction(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (other Page) () ()\n"),
            ["page.kh:2: method 'Path' must have exactly one owner named self"],
        )
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page, second Page) () ()\n"),
            ["page.kh:2: method 'Path' must have exactly one owner named self"],
        )
        self.assertEqual(
            self.kh('tp String in "memar/codec/string/protocol"\ntp Path mt (self String) () ()\n'),
            [
                "page.kh:2: method 'Path' owner 'String' is not a local abstraction",
                "input contains no Khayyam abstraction",
            ],
        )

    def test_a_method_with_a_body_is_refused_because_a_go_interface_method_has_none(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) () () {\n\treturn 1\n}\n"),
            ["page.kh:2: method 'Path' has a body and no body-less Go interface form"],
        )

    def test_an_empty_body_is_the_body_less_method_the_language_has_and_is_written(self):
        # `docs/khayyam/method.md`, Body-less Methods (FFI and Contracts): "A method
        # can be defined without a body (`{}`)"; the same file's Method Structure
        # writes it as `tp {name} mt (self {owner}) (...) (...) { }`, and
        # `docs/khayyam/khayyam.md` lists it among the syntax rules. A body holding
        # nothing is that form, so it is admitted -- and it is the body-less Go
        # interface method it is written as, not a refusal.
        for text in (
            "tp Page ab\ntp Path mt (self Page) () () {}\n",
            "tp Page ab\ntp Path mt (self Page) () () { }\n",
            "tp Page ab\ntp Path mt (self Page) () () {\n}\n",
        ):
            self.assertEqual(
                self.emit(text),
                "package generated\n\ntype Page interface {\n\tPath()\n}\n",
                text,
            )
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) () () {\n\treturn 1\n}\n"),
            ["page.kh:2: method 'Path' has a body and no body-less Go interface form"],
        )

    def test_a_repeated_method_name_on_one_interface_and_a_repeated_parameter_are_refused(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) () ()\ntp Path mt (self Page) (s String) ()\n"),
            ["page.kh:3: interface 'Page' repeats method 'Path'"],
        )
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) (s String, s String) ()\n"),
            ["page.kh:2: method Path repeats parameter 's'"],
        )

    def test_input_that_holds_no_abstraction_at_all_is_refused(self):
        self.assertEqual(self.kh('tp N in "memar/a/b"\n'), ["input contains no Khayyam abstraction"])

    def test_a_semicolon_an_unsupported_subtype_and_an_inclusion_path_that_is_not_a_string_are_refused(self):
        self.assertEqual(
            self.kh("tp Page ab;\ntp Path mt (self Page) () ()\n"),
            ["page.kh:1: semicolons are not valid Khayyam"],
        )
        self.assertEqual(self.kh("tp Page zz\n"), ["page.kh:1: unsupported subtype 'zz'"])
        self.assertEqual(
            self.kh("tp Page ab\ntp String in bare\n"), ["page.kh:2: import path must be a string"]
        )

    def test_a_parameter_named_with_a_khayyam_keyword_is_refused(self):
        self.assertEqual(
            self.kh("tp Page ab\ntp Path mt (self Page) (ab String) ()\n"),
            ["page.kh:2: expected a name"],
        )

if __name__ == "__main__":
    unittest.main()

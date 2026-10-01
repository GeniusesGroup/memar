"""Tests for renames: python -m unittest test_renames"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True

import renames as renames


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path
import shutil

from go_source_block import CORPUS_LICENSE


from names import qualified_by_module


def go_block(*go_lines: str) -> str:
    return "\n".join(["// TODO(go-migrate):", "/*", *go_lines, "*/", ""])

GO_LICENSE = "/* For license and copyright information please see the LEGAL file in the code repository * /"

LICENSE = CORPUS_LICENSE


class FieldNames(unittest.TestCase):
    SCHEME = (
        f"{LICENSE}\n\ntp URI_Field_Scheme ab\n"
        "tp URI_Field_Scheme_Scheme mt (self URI_Field_Scheme) () (s URI_Scheme)\ntp URI_Scheme ab\n"
    )
    URI_PATH = (
        f"{LICENSE}\n\ntp URI_Field_Path ab\n"
        "tp URI_Field_Path_Path mt (self URI_Field_Path) () (p URI_Path)\ntp URI_Path ab\n"
    )
    PARSED = (
        f'{LICENSE}\n\ntp URI_Field_Path in "modules/net/uri/protocol/path.kh"\n'
        'tp URI_Field_Scheme in "modules/net/uri/protocol/scheme.kh"\n\n'
        "tp URI_Field_Parsed ab {\n    URI_Field_Scheme\n    URI_Field_Path\n}\n\n"
        + go_block("package uri_p", "", "type URI_Field_Scheme interface {", "\tScheme() string", "}")
    )


    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write(self.root, "modules/net/uri/protocol/scheme.kh", self.SCHEME)
        write(self.root, "modules/net/uri/protocol/path.kh", self.URI_PATH)
        write(self.root, "modules/net/uri/protocol/parsed.kh", self.PARSED)
        write(self.root, "modules/memory/file/protocol/path.kh", f"{LICENSE}\n\ntp File_Path ab\n")

    def tearDown(self):
        self.temp.cleanup()


    def texts(self) -> dict[str, str]:
        return {
            path.relative_to(self.root).as_posix(): path.read_text(encoding="utf-8")
            for path in self.root.rglob("*.kh")
        }


    def test_the_scheme_field_takes_the_short_names(self):
        plan = renames.observer_names_plan(self.texts())
        self.assertEqual(plan["abstractions"]["URI_Field_Scheme"], "Observer_Scheme")
        self.assertEqual(plan["methods"]["URI_Field_Scheme_Scheme"], "Scheme")

    def test_a_concept_another_module_claims_keeps_its_qualifier(self):
        plan = renames.observer_names_plan(self.texts())
        self.assertEqual(plan["abstractions"]["URI_Field_Path"], "Observer_URI_Path")
        self.assertEqual(plan["methods"]["URI_Field_Path_Path"], "Path")

    def test_twins_qualification_cannot_separate_are_skipped(self):
        write(self.root, "modules/identifier/record/protocol/uuid.kh", f"{LICENSE}\n\ntp Record_Field_RecordUUID ab\n")
        write(self.root, "modules/memory/record/protocol/uuid.kh", f"{LICENSE}\n\ntp Storage_Field_RecordUUID ab\n")
        plan = renames.observer_names_plan(self.texts())
        self.assertNotIn("Record_Field_RecordUUID", plan["abstractions"])
        self.assertNotIn("Storage_Field_RecordUUID", plan["abstractions"])
        self.assertIn("Record_Field_RecordUUID", plan["skipped"])
        self.assertIn("Storage_Field_RecordUUID", plan["skipped"])

    def test_a_method_named_as_its_value_is_skipped_and_its_owner_part_follows(self):
        write(
            self.root,
            "modules/memory/block/protocol/number.kh",
            f"{LICENSE}\n\ntp Block_Field_BlockNumber ab\n"
            "tp Block_Field_BlockNumber_BlockNumber mt (self Block_Field_BlockNumber) () (n BlockNumber)\n"
            "tp BlockNumber ab\n",
        )
        plan = renames.observer_names_plan(self.texts())
        self.assertEqual(plan["abstractions"]["Block_Field_BlockNumber"], "Observer_BlockNumber")
        self.assertIn("Block_Field_BlockNumber_BlockNumber", plan["skipped"])
        self.assertEqual(plan["methods"]["Block_Field_BlockNumber_BlockNumber"], "Observer_BlockNumber_BlockNumber")

    def test_run_renames_imports_leaves_go_blocks_and_a_second_run_changes_nothing(self):
        parsed = self.root / "modules/net/uri/protocol/parsed.kh"
        parsed.write_bytes(parsed.read_bytes().replace(b"\n", b"\r\n"))
        first = renames.run_observer_names(self.root, write=True, frontend=False)
        self.assertIn("modules/net/uri/protocol/parsed.kh", first["files_changed"])
        text = parsed.read_bytes().decode("utf-8")
        self.assertNotIn("\n", text.replace("\r\n", ""))
        self.assertIn('tp Observer_Scheme in "modules/net/uri/protocol/scheme.kh"', text)
        self.assertIn("    Observer_Scheme\r\n    Observer_URI_Path\r\n", text)
        self.assertIn("type URI_Field_Scheme interface {", text)
        scheme = (self.root / "modules/net/uri/protocol/scheme.kh").read_text(encoding="utf-8")
        self.assertIn("tp Observer_Scheme ab\ntp Scheme mt (self Observer_Scheme) () (s URI_Scheme)\n", scheme)
        second = renames.run_observer_names(self.root, write=True, frontend=False)
        self.assertEqual(second["files_changed"], [])


    @unittest.skipUnless(shutil.which("node"), "node is not on PATH")
    def test_renamed_files_pass_the_khayyam_frontend(self):
        summary = renames.run_observer_names(self.root, write=False)
        self.assertEqual(summary["frontend"]["newly_refused"], {})
        self.assertEqual(summary["frontend"]["after"]["refuse"], 0)


class BareNames(unittest.TestCase):
    DETAIL = (
        f"{LICENSE}\n\ntp String in \"modules/codec/string/protocol/string.kh\"\n\n"
        "tp Computer_Detail ab {\n    Datatype_Quiddity\n}\n"
        "tp Computer_Detail_Domain mt (self Computer_Detail) () (s String)\n"
        "tp Datatype_Quiddity ab\n"
        "tp Datatype_Quiddity_Name mt (self Datatype_Quiddity) () (s String)\n"
    )
    DATA_TYPE = (
        f'{LICENSE}\n\ntp Computer_Detail in "modules/computer/datatype/protocol/detail.kh"\n\n'
        "tp Computer_DataType ab {\n    Computer_Detail\n}\n"
    )
    TIME = f"{LICENSE}\n\ntp Time ab\n"
    TIMER = (
        f'{LICENSE}\n\ntp Time in "modules/time/protocol/time.kh"\n\n'
        "tp Timer ab\ntp Timer_Time mt (self Timer) () (t Time)\n"
    )

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def texts(self) -> dict[str, str]:
        return {
            path.relative_to(self.root).as_posix(): path.read_text(encoding="utf-8")
            for path in self.root.rglob("*.kh")
        }

    def test_a_unique_module_prefix_is_stripped(self):
        write(self.root, "modules/computer/datatype/protocol/detail.kh", self.DETAIL)
        plan = renames.bare_names_plan(self.texts())
        self.assertEqual(plan["abstractions"]["Datatype_Quiddity"], "Quiddity")
        self.assertEqual(plan["methods"]["Computer_Detail_Domain"], "Domain")
        self.assertEqual(plan["methods"]["Datatype_Quiddity_Name"], "Name")

    def test_a_collision_with_an_existing_declaration_is_skipped(self):
        write(self.root, "modules/time/protocol/time.kh", self.TIME)
        write(self.root, "modules/time/timer/protocol/timer.kh", self.TIMER)
        plan = renames.bare_names_plan(self.texts())
        self.assertNotIn("Timer_Time", plan["methods"])
        self.assertIn("Timer_Time", plan["skipped"])

    def test_run_rewrites_imports_and_is_idempotent(self):
        write(self.root, "modules/computer/datatype/protocol/detail.kh", self.DETAIL)
        write(self.root, "modules/computer/datatype/protocol/data-type.kh", self.DATA_TYPE)
        first = renames.run_bare_names(self.root, write=True, frontend=False)
        self.assertIn("modules/computer/datatype/protocol/detail.kh", first["files_changed"])
        data_type = (self.root / "modules/computer/datatype/protocol/data-type.kh").read_text(encoding="utf-8")
        self.assertIn('tp Detail in "modules/computer/datatype/protocol/detail.kh"', data_type)
        self.assertIn("    Detail\n", data_type)
        detail = (self.root / "modules/computer/datatype/protocol/detail.kh").read_text(encoding="utf-8")
        self.assertIn("tp Detail ab {\n    Quiddity\n}", detail)
        self.assertIn("tp Domain mt (self Detail) () (s String)", detail)
        second = renames.run_bare_names(self.root, write=True, frontend=False)
        self.assertEqual(second["files_changed"], [])

    def test_record_storage_uuid_pair_and_counters_are_skipped(self):
        write(self.root, "modules/identifier/record/protocol/uuid.kh", f"{LICENSE}\n\ntp Record_Observer_RecordUUID ab\n")
        write(self.root, "modules/memory/record/protocol/uuid.kh", f"{LICENSE}\n\ntp Storage_Observer_RecordUUID ab\n")
        write(
            self.root,
            "modules/gui/protocol/element.kh",
            f"{LICENSE}\n\ntp GUI_Element ab\ntp GUI_Element_Type_2 mt (self GUI_Element) () (t GUI_Element_Type)\n"
            "tp GUI_Element_Type ab\n",
        )
        plan = renames.bare_names_plan(self.texts())
        self.assertIn("Record_Observer_RecordUUID", plan["skipped"])
        self.assertIn("Storage_Observer_RecordUUID", plan["skipped"])
        self.assertIn("GUI_Element_Type_2", plan["skipped"])

if __name__ == "__main__":
    unittest.main()

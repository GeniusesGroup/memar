"""Tests for go_source: python -m unittest test_go_source"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.dont_write_bytecode = True

import go_source as go


def write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


class Comments(unittest.TestCase):
    def test_trailing_comment_documents_its_own_line_only(self):
        source = go.parse_go_source(
            "page.go",
            "package p\n"
            "\n"
            "type Page interface {\n"
            "\tPath() string // To route page by path\n"
            "\t// Robots names the crawler policy\n"
            "\tRobots() string\n"
            "}\n",
        )
        entries = {entry.name: entry.doc for entry in source.interfaces[0].entries}
        self.assertEqual(entries["Path"], [" To route page by path"])
        self.assertEqual(entries["Robots"], [" Robots names the crawler policy"])

    def test_trailing_comment_on_a_method_line(self):
        source = go.parse_go_source(
            "navigator.go",
            "package p\n"
            "\n"
            "type Navigator struct{}\n"
            "\n"
            "func (n *Navigator) ActivatePage(url string) {} // Navigate(url string)\n",
        )
        self.assertEqual(source.methods[0].doc, [" Navigate(url string)"])


class Constants(unittest.TestCase):
    def test_top_level_constants_and_variables_are_named(self):
        tokens = go.lex_source(
            "package p\n"
            "var GUI Application\n"
            "const (\n"
            "\tA Kind = iota\n"
            "\t// B is second\n"
            "\tB\n"
            "\tC, D = 3, 4\n"
            ")\n"
            "func f() { const local = 1 }\n",
            True,
        )
        self.assertEqual(go.top_level_value_names(tokens, "var"), ["GUI"])
        self.assertEqual(go.top_level_value_names(tokens, "const"), ["A", "B", "C", "D"])

if __name__ == "__main__":
    unittest.main()

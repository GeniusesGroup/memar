#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that no module of the scripts imports a module that imports it back.

    python .agents/scripts/tests/module_graph.py

A module here is a folder under `modules/`, `modules-plugable/`, or `bundles/`
that holds Python of its own: a file named by its folder, or files in its
`services/` folder. What it
imports of another module — by the dotted path of that module's files — is an
edge, and a cycle of edges is a pair of modules neither of which can be understood,
moved or converted to Khayyam without the other
([Modeling Practice → The Modeling Workflow](../../../docs/modeling.practice.md#the-modeling-workflow)).
The types below the modules (`machine/`, `host/`) are not modules and
are not edges: they are what the modules share so that none has to import another for it.

What is pinned:

  NoCycle   The graph of the modules has no strongly connected set of more than one.
  Finds     The check sees a cycle when one is written into a scratch tree.
"""
from __future__ import annotations

import ast
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
TOP = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

ROOTS = ("modules", "modules-plugable", "bundles")
SKIPPED = {"tests", "temp", "node_modules", "__pycache__", "primitive", "protocol", "errors", "docs", "rules"}


def module_folders(top: Path) -> dict[str, Path]:
    """Each module's dotted path, with its folder."""
    found: dict[str, Path] = {}
    for root in ROOTS:
        base = top / root
        if not base.is_dir():
            continue
        stack = [base]
        while stack:
            folder = stack.pop()
            own = folder / f"{folder.name}.py"
            shelf = folder / "services"
            if folder != base and (own.is_file() or (shelf.is_dir() and any(shelf.glob("*.py")))):
                found[".".join(folder.relative_to(top).parts)] = folder
            stack.extend(child for child in folder.iterdir() if child.is_dir() and child.name not in SKIPPED | {"services"})
    return found


def edges(top: Path) -> dict[str, set[str]]:
    modules = module_folders(top)
    names = sorted(modules, key=len, reverse=True)
    graph: dict[str, set[str]] = {name: set() for name in modules}
    for name, folder in modules.items():
        files = [*folder.glob("*.py"), *(folder / "services").glob("*.py")]
        for path in files:
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                targets = []
                if isinstance(node, ast.ImportFrom) and node.module:
                    targets = [node.module]
                elif isinstance(node, ast.Import):
                    targets = [alias.name for alias in node.names]
                for target in targets:
                    owner = next((each for each in names if target == each or target.startswith(each + ".")), None)
                    if owner and owner != name:
                        graph[name].add(owner)
    return graph


def cycles(graph: dict[str, set[str]]) -> list[list[str]]:
    """The strongly connected sets of more than one module."""
    index: dict[str, int] = {}
    low: dict[str, int] = {}
    stack: list[str] = []
    on: set[str] = set()
    found: list[list[str]] = []
    counter = [0]

    def visit(node: str) -> None:
        index[node] = low[node] = counter[0]
        counter[0] += 1
        stack.append(node)
        on.add(node)
        for other in sorted(graph.get(node, ())):
            if other not in index:
                visit(other)
                low[node] = min(low[node], low[other])
            elif other in on:
                low[node] = min(low[node], index[other])
        if low[node] == index[node]:
            members = []
            while True:
                other = stack.pop()
                on.discard(other)
                members.append(other)
                if other == node:
                    break
            if len(members) > 1:
                found.append(sorted(members))

    for node in sorted(graph):
        if node not in index:
            visit(node)
    return found


class NoCycle(unittest.TestCase):
    def test_no_module_imports_a_module_that_imports_it_back(self) -> None:
        self.assertEqual(cycles(edges(TOP)), [], "break each set by moving what both need below them")


class Finds(unittest.TestCase):
    def test_a_cycle_written_into_a_scratch_tree_is_found(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            top = Path(folder)
            for mine, other in (("one", "two"), ("two", "one")):
                shelf = top / "modules" / mine / "services"
                shelf.mkdir(parents=True)
                (shelf / "a.py").write_text(f"from modules.{other}.services.a import x\n", encoding="utf-8")
            self.assertEqual(cycles(edges(top)), [["modules.one", "modules.two"]])


if __name__ == "__main__":
    unittest.main()

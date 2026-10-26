#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that no module of the scripts imports a module that imports it back, nor a kernel module an optional one.

    python bundles/memar/tests/module_graph.py

A module here is a folder at any depth under `modules/`, `modules-plugable/`, or `bundles/`
that holds Python of its own: a file named by its folder, or files in its
`services/` or `primitive/` folder. What it
imports of another module — by the dotted path of that module's files, in an
`import` statement or as the string given to `import_module` — is an
edge, and a cycle of edges is a pair of modules neither of which can be understood,
moved or converted to Khayyam without the other
([Modeling Practice → The Modeling Workflow](../../../docs/modeling.practice.md#the-modeling-workflow)).
An edge from a kernel module, under `modules/`, to one under `modules-plugable/`
or `bundles/` runs against the direction of
[Placement → The rule](../../../modules/knowledge/modularity/rules/placement/placement.md#the-rule)
and is a back edge ([Kernel Neutrality → How a check runs](../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#how-a-check-runs)),
unless `ALLOWED` names it with the owner's date and the condition that ends it.
The types below the modules (`machine/`) are not modules and
are not edges: they are what the modules share so that none has to import another for it.

What is pinned:

  NoCycle      The graph of the modules has no strongly connected set of more than one.
  Finds        The check sees a cycle when one is written into a scratch tree.
  NoBackEdge   No kernel module imports a pluggable module or a bundle that `ALLOWED` does not name,
               and every allowance still names an edge the graph has.
  FindsBack    The check sees a back edge, by `import` and by `import_module`, written into a scratch tree.
  Nested       A module nested under categories, holding only `primitive/` code, is named and its edges are checked.
  Mirrored     A pluggable module stands at the path of a kernel module or of a category, and `UNMIRRORED` names no path
               that now stands right; the check sees a stray one written into a scratch tree.
"""
from __future__ import annotations

from importlib import import_module

_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
role_folders = _m_fs_memar.role_folders
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import ast
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
TOP = SCRIPTS.parent.parent
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True
ROOTS = ('modules', 'modules-plugable', 'bundles')
SKIPPED = {'services', *role_folders(), 'node_modules', '__pycache__'}
KERNEL = 'modules'
OPTIONAL = ('modules-plugable', 'bundles')
ALLOWED = {}
CODE_FOLDERS = ('services', 'primitive')
# Pluggable modules whose path matches no kernel module or category yet, each with the condition that ends it; the check
# names a path that is listed and now stands right. Found by this check on 2026-10-26 (task 20261025-T160939Z-23124),
# not allowed by the owner: they stand inside the pluggable module `knowledge/documentation`, which the move tasks of the
# category rule place; each leaves this list when its move lands.
UNMIRRORED = {path: 'placed by the move tasks of the category rule' for path in ('knowledge/documentation/changelog', 'knowledge/documentation/comparison', 'knowledge/documentation/explanation', 'knowledge/documentation/handoff', 'knowledge/documentation/practice', 'knowledge/documentation/research')}

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
            own = folder / f'{folder.name}.py'
            if folder != base and (own.is_file() or any((any((folder / code).glob('*.py')) for code in CODE_FOLDERS if (folder / code).is_dir()))):
                found['.'.join(folder.relative_to(top).parts)] = folder
            stack.extend((child for child in folder.iterdir() if child.is_dir() and child.name not in SKIPPED | set(CODE_FOLDERS)))
    return found

def unmirrored(top: Path) -> list[str]:
    """The pluggable modules whose path, or whose parent's, is no folder under `modules/`: a pluggable module stands at
    `modules-plugable/` + the path of the kernel module it attaches to + its own name, or in a category the kernel side has."""
    kernel = top / KERNEL
    found = []
    for name, folder in module_folders(top).items():
        relative = folder.relative_to(top / OPTIONAL[0]) if name.split('.')[0] == OPTIONAL[0] else None
        if relative is not None and not (kernel / relative).is_dir() and not (kernel / relative.parent).is_dir():
            found.append(relative.as_posix())
    return sorted(found)

def is_import_module(node: ast.AST) -> bool:
    """A call of `import_module` or `importlib.import_module` whose first argument is a literal string."""
    if not isinstance(node, ast.Call) or not node.args:
        return False
    called = node.func
    name = called.id if isinstance(called, ast.Name) else called.attr if isinstance(called, ast.Attribute) else None
    first = node.args[0]
    return name == 'import_module' and isinstance(first, ast.Constant) and isinstance(first.value, str)

def back_edges(graph: dict[str, set[str]]) -> list[tuple[str, str]]:
    """The edges from a kernel module to a pluggable module or a bundle."""
    return sorted(((source, target) for source, targets in graph.items() if source.split('.')[0] == KERNEL for target in targets if target.split('.')[0] in OPTIONAL))

def edges(top: Path) -> dict[str, set[str]]:
    modules = module_folders(top)
    names = sorted(modules, key=len, reverse=True)
    graph: dict[str, set[str]] = {name: set() for name in modules}
    for name, folder in modules.items():
        files = [*folder.glob('*.py'), *(path for code in CODE_FOLDERS for path in (folder / code).glob('*.py'))]
        for path in files:
            for node in ast.walk(ast.parse(path.read_text(encoding='utf-8'))):
                targets = []
                if isinstance(node, ast.ImportFrom) and node.module:
                    targets = [node.module]
                elif isinstance(node, ast.Import):
                    targets = [alias.name for alias in node.names]
                elif is_import_module(node):
                    targets = [node.args[0].value]
                for target in targets:
                    owner = next((each for each in names if target == each or target.startswith(each + '.')), None)
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
        self.assertEqual(cycles(edges(TOP)), [], 'break each set by moving what both need below them')

class Finds(unittest.TestCase):

    def test_a_cycle_written_into_a_scratch_tree_is_found(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            top = Path(folder)
            for mine, other in (('one', 'two'), ('two', 'one')):
                shelf = top / 'modules' / mine / 'services'
                shelf.mkdir(parents=True)
                (shelf / 'a.py').write_text(f'from modules.{other}.services.a import x\n', encoding='utf-8')
            self.assertEqual(cycles(edges(top)), [['modules.one', 'modules.two']])

class NoBackEdge(unittest.TestCase):

    def setUp(self) -> None:
        self.found = back_edges(edges(TOP))

    def test_no_kernel_module_imports_an_optional_one(self) -> None:
        self.assertEqual([edge for edge in self.found if edge not in ALLOWED], [], 'move what the kernel module needs into it or below the modules, or ask the owner for a dated allowance')

    def test_every_allowance_names_an_edge_the_graph_has(self) -> None:
        self.assertEqual([edge for edge in ALLOWED if edge not in self.found], [], 'drop the allowance whose edge is gone')

class FindsBack(unittest.TestCase):

    def test_a_back_edge_written_into_a_scratch_tree_is_found(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            top = Path(folder)
            for place in ('modules-plugable/cat/two', 'bundles/three'):
                shelf = top / place / 'services'
                shelf.mkdir(parents=True)
                (shelf / 'b.py').write_text('x = 1\n', encoding='utf-8')
            shelf = top / 'modules' / 'one' / 'services'
            shelf.mkdir(parents=True)
            (shelf / 'a.py').write_text('from importlib import import_module\ntwo = import_module("modules-plugable.cat.two.services.b")\nfrom bundles.three.services.b import x\n', encoding='utf-8')
            self.assertEqual(back_edges(edges(top)), [('modules.one', 'bundles.three'), ('modules.one', 'modules-plugable.cat.two')])
class Nested(unittest.TestCase):

    def test_a_module_nested_under_categories_with_only_primitive_code_is_named_and_checked(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            top = Path(folder)
            for mine, other in (('cat/sub/one', 'cat/two'), ('cat/two', 'cat/sub/one')):
                shelf = top / 'modules' / mine / 'primitive'
                shelf.mkdir(parents=True)
                (shelf / 'a.py').write_text('from modules.' + other.replace('/', '.') + '.primitive.a import x' + chr(10), encoding='utf-8')
            self.assertEqual(sorted(module_folders(top)), ['modules.cat.sub.one', 'modules.cat.two'])
            self.assertEqual(cycles(edges(top)), [['modules.cat.sub.one', 'modules.cat.two']])

class Mirrored(unittest.TestCase):

    def test_every_pluggable_path_stands_at_a_kernel_path_or_in_a_category(self) -> None:
        self.assertEqual([path for path in unmirrored(TOP) if path not in UNMIRRORED], [], 'move the module to the path of the kernel module it attaches to, or ask the owner for a dated allowance')

    def test_every_allowance_names_a_path_still_unmirrored(self) -> None:
        self.assertEqual([path for path in UNMIRRORED if path not in unmirrored(TOP)], [], 'drop the allowance whose path now stands right')

    def test_a_stray_pluggable_path_written_into_a_scratch_tree_is_found(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as folder:
            top = Path(folder)
            (top / 'modules' / 'cat' / 'kernel').mkdir(parents=True)
            for place in ('modules-plugable/cat/kernel/extra', 'modules-plugable/cat/kernel', 'modules-plugable/other/stray'):
                shelf = top / place / 'services'
                shelf.mkdir(parents=True)
                (shelf / 'a.py').write_text('x = 1' + chr(10), encoding='utf-8')
            self.assertEqual(unmirrored(top), ['other/stray'])
if __name__ == '__main__':
    unittest.main()

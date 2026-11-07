#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_copy_excluded = import_module('bundles.memar.services.machine.copy_excluded')
NEVER_COPIED_PATTERNS = _m_copy_excluded.NEVER_COPIED_PATTERNS
_m_repository = import_module('bundles.memar.services.location.repository')
memar_repository = _m_repository
enclosing_repository = _m_repository.enclosing_repository
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_check = import_module('modules-plugable.knowledge.documentation.services.content_check')
BUDGET_SECONDS = 60

class LinkFixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.cache: dict = {}

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def problems(self, path: Path) -> list[str]:
        return content_check.check_file(path, self.cache, root=self.root)

    def only_link_problems(self, path: Path) -> list[str]:
        return [p for p in self.problems(path) if 'does not exist' in p or 'names no heading' in p]

class LinkStandIn(LinkFixture):

    def test_a_readme_holding_only_its_siblings_name_is_clean(self) -> None:
        self.write('m/m.md', '# M\n')
        stand_in = self.root / 'm' / 'README.md'
        stand_in.write_bytes(b'm.md')
        self.assertEqual(self.problems(stand_in), [])

    def test_a_readme_naming_nothing_there_is_judged_as_text(self) -> None:
        self.write('m/m.md', '# M\n')
        stand_in = self.root / 'm' / 'README.md'
        stand_in.write_bytes(b'gone.md')
        self.assertIn('no newline at end of file', self.problems(stand_in))

    def test_another_file_with_the_same_content_is_judged_as_text(self) -> None:
        self.write('m/m.md', '# M\n')
        other = self.root / 'm' / 'notes.md'
        other.write_bytes(b'm.md')
        self.assertIn('no newline at end of file', self.problems(other))

class ReachableLink(LinkFixture):

    def test_sibling_link_is_not_reported(self) -> None:
        self.write('other.md', '# Other\n')
        path = self.write('base.md', '# Base\nSee [Other](./other.md).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_parent_and_grandparent_links_are_not_reported(self) -> None:
        self.write('deep/target.md', '# Target\n')
        path = self.write('deep/inner/base.md', '# Base\n[Up](../target.md) and [Out](../../deep/target.md).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_directory_target_is_not_reported(self) -> None:
        self.write('modules/math/one.kh', '')
        path = self.write('base.md', '# Base\n[Modules](./modules/math/).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_non_markdown_target_needs_no_anchor(self) -> None:
        self.write('code.kh', 'tp X\n')
        path = self.write('base.md', '# Base\n[Code](./code.kh#anything).\n')
        self.assertEqual(self.only_link_problems(path), [])

class MovedDocument(LinkFixture):

    def test_target_one_folder_short_is_reported(self) -> None:
        self.write('area/deeper/target.md', '# Target\n')
        path = self.write('area/base.md', '# Base\nSee [Target](./target.md).\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('./target.md does not exist', found[0])
        self.assertIn('line 2', found[0])

    def test_a_link_to_a_real_sibling_is_not_reported(self) -> None:
        self.write('area/deeper/target.md', '# Target\n')
        path = self.write('area/base.md', '# Base\nSee [Target](./deeper/target.md).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_contributors_link_out_of_a_subfolder_is_reported(self) -> None:
        self.write('CONTRIBUTORS.md', '# Contributors\n')
        path = self.write('modules/net/chapar/chapar.changelog.md', '# Log\n- [Owner](../../CONTRIBUTORS.md#owner)\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('../../CONTRIBUTORS.md does not exist', found[0])

    def test_the_same_link_from_the_right_depth_is_not_reported(self) -> None:
        self.write('CONTRIBUTORS.md', '# Contributors\n### Owner\n')
        path = self.write('modules/net/chapar/chapar.changelog.md', '# Log\n- [Owner](../../../CONTRIBUTORS.md#owner)\n')
        self.assertEqual(self.only_link_problems(path), [])

class NamedHeading(LinkFixture):

    def test_anchor_is_checked_in_the_named_document(self) -> None:
        self.write('target.md', '# Target\n## The Part\n')
        path = self.write('base.md', '# Base\n[Part](./target.md#the-part).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_anchor_absent_from_the_named_document_is_reported(self) -> None:
        self.write('target.md', '# Target\n## The Part\n')
        path = self.write('base.md', '# Base\n[Gone](./target.md#the-gone).\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('names no heading in ./target.md', found[0])

    def test_anchor_present_only_in_the_holding_document_is_reported(self) -> None:
        self.write('target.md', '# Target\n')
        path = self.write('base.md', '# Base\n## Elsewhere\n[X](./target.md#elsewhere).\n')
        self.assertEqual(len(self.only_link_problems(path)), 1)

    def test_existence_is_reported_before_the_anchor(self) -> None:
        path = self.write('base.md', '# Base\n[X](./gone.md#somewhere).\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('does not exist', found[0])

class SharedCacheAnswers(LinkFixture):

    def test_one_read_serves_every_link_to_that_document(self) -> None:
        target = self.write('target.md', '# Target\n## The Part\n')
        readers = [self.write(f'base{index}.md', f'# Base\n[A](./target.md#the-part)\n[B](./target.md#the-part)\n') for index in range(3)]
        for path in readers:
            self.assertEqual(self.only_link_problems(path), [])
        self.assertEqual(sum((1 for key in self.cache if key == str(target))), 1)

    def test_cache_is_keyed_by_the_file_not_by_the_link(self) -> None:
        self.write('one.md', '# One\n## Shared\n')
        self.write('two.md', '# Two\n')
        good = self.write('a.md', '# A\n[X](./one.md#shared).\n')
        bad = self.write('b.md', '# B\n[X](./two.md#shared).\n')
        self.assertEqual(self.only_link_problems(good), [])
        self.assertEqual(len(self.only_link_problems(bad)), 1)

    def test_a_second_run_reaches_the_same_answer(self) -> None:
        self.write('target.md', '# Target\n')
        path = self.write('base.md', '# Base\n[X](./target.md#gone).\n')
        first = self.only_link_problems(path)
        self.assertEqual(len(first), 1, first)
        self.assertEqual(first, self.only_link_problems(path))

class UnreadableTarget(LinkFixture):

    def test_invalid_utf8_target_is_not_reported_as_a_missing_heading(self) -> None:
        target = self.root / 'target.md'
        target.write_bytes(b'# Target\n## \xff\xfe not utf-8\n')
        path = self.write('base.md', '# Base\n[X](./target.md#anything).\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_missing_target_is_still_reported_when_the_read_would_fail(self) -> None:
        path = self.write('base.md', '# Base\n[X](./target.md#anything).\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('does not exist', found[0])

class CodeIsNotALink(LinkFixture):

    def test_link_shown_inside_a_code_span_is_not_a_link(self) -> None:
        path = self.write('base.md', '# Base\nWrite `[X](./gone.md)` and it resolves.\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_link_shown_inside_a_fence_is_not_a_link(self) -> None:
        path = self.write('base.md', '# Base\n```\n[X](./gone.md#gone)\n```\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_real_link_beside_a_shown_one_is_still_judged(self) -> None:
        path = self.write('base.md', '# Base\n`[X](./gone.md)` but [Y](./gone.md) is real.\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('./gone.md does not exist', found[0])

class ExternalIsNotJudged(LinkFixture):

    def test_links_with_a_scheme_are_left_alone(self) -> None:
        path = self.write('base.md', '# Base\n[A](https://example.invalid/x) [B](mailto:a@example.invalid) [C](//cdn.example.invalid/x)\n')
        self.assertEqual(self.only_link_problems(path), [])

class RootRelativeIsJudged(LinkFixture):

    def test_a_root_relative_link_to_a_heading_there_is_not_reported(self) -> None:
        self.write('docs/cognition.md', '# Cognition\n## Abstract\n')
        path = self.write('area/deep/base.md', '# Base\n[A](/docs/cognition.md#abstract)\n')
        self.assertEqual(self.only_link_problems(path), [])

    def test_a_root_relative_link_to_a_missing_anchor_is_reported(self) -> None:
        self.write('docs/cognition.md', '# Cognition\n## Abstract\n')
        path = self.write('area/base.md', '# Base\n[A](/docs/cognition.md#gone)\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('/docs/cognition.md#gone names no heading', found[0])
        self.assertIn('line 2', found[0])

    def test_a_root_relative_link_to_a_missing_file_is_reported(self) -> None:
        path = self.write('area/base.md', '# Base\n[A](/docs/gone.md)\n')
        found = self.only_link_problems(path)
        self.assertEqual(len(found), 1, found)
        self.assertIn('/docs/gone.md does not exist', found[0])

    def test_it_is_not_resolved_from_the_linking_folder(self) -> None:
        self.write('area/docs/x.md', '# X\n')
        path = self.write('area/base.md', '# Base\n[A](/docs/x.md)\n')
        self.assertEqual(len(self.only_link_problems(path)), 1)

class InPageAnchorStillJudged(LinkFixture):

    def test_in_page_anchor_is_reported_by_the_original_pass(self) -> None:
        path = self.write('base.md', '# Base\n## Real\n[X](#real)\n[Y](#gone)\n')
        found = [p for p in self.problems(path) if 'in-page anchor' in p]
        self.assertEqual(len(found), 1, found)
        self.assertIn('#gone', found[0])

    def test_both_passes_run_on_one_document(self) -> None:
        self.write('target.md', '# Target\n')
        path = self.write('base.md', '# Base\n## Real\n[X](#nowhere) and [Y](./target.md#gone)\n')
        found = self.problems(path)
        self.assertEqual(len(found), 2, found)
        self.assertTrue(any(('in-page anchor' in p for p in found)))
        self.assertTrue(any(('names no heading' in p for p in found)))

class RejectedInABodyIsNotJudged(LinkFixture):

    def test_the_facet_specification_carries_the_heading_and_is_clean(self) -> None:
        path = self.write('modules-plugable/knowledge/documentation/changelog/changelog.md', '# Documentation Changelog\n## Optional Sections\n#### Considered and not done\n- alternatives examined and rejected\n')
        self.assertEqual(self.problems(path), [])

    def test_a_body_naming_the_fields_home_is_clean(self) -> None:
        path = self.write('docs/cognition.md', "# Cognition\n## Rules\nA rejected alternative belongs in the changelog entry's `Considered and not done` section.\n")
        self.assertEqual(self.problems(path), [])

class WalkLooksOnlyAtWhatTheProjectOwns(LinkFixture):

    def install(self, relative: str, text: str='x') -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def walked(self) -> list[str]:
        return [p.relative_to(self.root).as_posix() for p in content_check.checkable_files(self.root)]

    def test_a_dependency_tree_is_not_walked(self) -> None:
        self.install('node_modules/dep/package.json', '{"name": "dep"}\n')
        self.install('notes.md', '# Notes\n')
        walked = self.walked()
        self.assertIn('notes.md', walked)
        self.assertFalse([p for p in walked if p.startswith('node_modules/')], walked)

    def test_a_generated_folder_is_not_walked(self) -> None:
        for name in ('__pycache__', '.DS_Store'):
            with self.subTest(name=name):
                self.install(f'{name}/thing.py', 'x = 1\n')
                walked = self.walked()
                self.assertFalse([p for p in walked if p.startswith(name)], walked)

    def test_a_file_inside_an_owned_folder_is_still_walked(self) -> None:
        self.install('src/deep/module.py', 'x = 1\n')
        self.assertIn('src/deep/module.py', self.walked())

    def test_a_named_file_is_checked_whatever_folder_it_is_in(self) -> None:
        path = self.install('node_modules/dep/broken.md', '# T\n\n\nbody\n')
        self.assertTrue(self.problems(path))

    def test_the_patterns_are_the_ones_the_folder_already_states(self) -> None:
        for pattern in ('__pycache__', '*.pyc', '.DS_Store', 'node_modules'):
            self.assertIn(pattern, NEVER_COPIED_PATTERNS)
        for pattern in NEVER_COPIED_PATTERNS:
            folder = pattern.replace('*', 'x')
            with self.subTest(pattern=pattern):
                self.install(f'{folder}/thing.py', 'x = 1\n')
                walked = self.walked()
                self.assertFalse([p for p in walked if p.startswith(f'{folder}/')], walked)

class RepositoryFixture(LinkFixture):

    def make_repo(self) -> Path:
        repo = self.root / 'Memar'
        repo.mkdir(parents=True, exist_ok=True)
        (repo / 'README.md').write_text('# Memar\n', encoding='utf-8', newline='\n')
        (repo / 'docs').mkdir(parents=True, exist_ok=True)
        skill = repo / '.agents' / 'skills' / 'memar' / 'SKILL.md'
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text('# Memar\n', encoding='utf-8', newline='\n')
        return repo

    def isolate(self) -> None:
        saved = memar_repository.is_memar_repository
        root = self.root.resolve()

        def isolated(path: Path) -> bool:
            try:
                Path(path).resolve().relative_to(root)
            except ValueError:
                return False
            return saved(path)
        memar_repository.is_memar_repository = isolated
        self.addCleanup(setattr, memar_repository, 'is_memar_repository', saved)

class MemarRulesAutoDetect(RepositoryFixture):

    def test_memar_conventions_apply_inside_and_not_outside(self) -> None:
        self.isolate()
        repo = self.make_repo()
        inside = repo / 'docs' / 'note.md'
        inside.parent.mkdir(parents=True, exist_ok=True)
        inside.write_text('# Base\n\nBody\n', encoding='utf-8', newline='\n')
        outside = self.root / 'plain' / 'note.md'
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_text('# Base\n\nBody\n', encoding='utf-8', newline='\n')
        self.assertIsNotNone(enclosing_repository(inside))
        self.assertIsNone(enclosing_repository(outside))
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))
        self.assertEqual(content_check.check_file(outside, {}, False, root=self.root), [])

    def test_an_explicit_flag_wins_over_the_folder(self) -> None:
        repo = self.make_repo()
        inside = repo / 'docs' / 'note.md'
        inside.parent.mkdir(parents=True, exist_ok=True)
        inside.write_text('# Base\n\nBody\n', encoding='utf-8', newline='\n')
        self.assertEqual(content_check.check_file(inside, {}, False, root=self.root), [])
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))

    def test_encoding_problems_report_whatever_the_folder_is(self) -> None:
        repo = self.make_repo()
        inside = repo / 'note.md'
        inside.write_text('# T\n', encoding='utf-8', newline='\n')
        inside.write_bytes(inside.read_bytes().rstrip(b'\n'))
        self.assertTrue(content_check.check_file(inside, {}, True, root=self.root))
        self.assertTrue(content_check.check_file(inside, {}, False, root=self.root))

class CitationDirection(RepositoryFixture):

    def setUp(self) -> None:
        super().setUp()
        self.repo = self.make_repo()

    def put(self, relative: str, text: str) -> Path:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def upward(self, path: Path) -> list[str]:
        return [w for w in content_check.upward_warnings(path, self.cache) if 'points up' in w]

    def test_an_upward_link_is_a_warning_and_not_a_problem(self) -> None:
        import argparse
        import contextlib
        import io
        self.targets()
        path = self.put('docs/process.md', '# T\nSee [X](../modules/process/error/error.md).\n')
        self.assertEqual(content_check.check_file(path, self.cache, True, root=self.repo), [])
        args = argparse.Namespace(files=[str(path)], verbose=False, memar_rules=True)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.repo)
            except SystemExit as stop:
                code = stop.code or 0
        self.assertEqual(code, 0)
        self.assertIn('warnings (not counted as problems)', out.getvalue())
        self.assertIn('points up', out.getvalue())
        self.assertIn('a debt', out.getvalue())
        self.assertIn('0 problems', out.getvalue())

    def targets(self) -> None:
        self.put('docs/system.md', '# System\n')
        self.put('modules/process/error/error.md', '# Error\n')
        self.put('docs/khayyam/khayyam.md', '# Khayyam\n')
        self.put('bundles/khayyam/khayyam.md', '# Toolchain\n')
        self.put('modules/process/error/README.md', '# Error\n')

    def test_each_upward_pair_is_reported(self) -> None:
        self.targets()
        cases = [('docs/process.md', '../modules/process/error/error.md'), ('docs/process.md', '../bundles/khayyam/khayyam.md'), ('docs/process.md', '../modules/process/error/'), ('docs/process.md', '../modules/'), ('docs/khayyam/flow.md', '../../modules/process/error/error.md'), ('docs/khayyam/flow.md', '../../bundles/khayyam/khayyam.md'), ('docs/khayyam/flow.md', '../../modules/process/error/README.md'), ('docs/comparisons/other.md', '../../modules/process/error/error.md'), ('docs/process.changelog.md', '../modules/process/error/error.md#error')]
        for source, link in cases:
            with self.subTest(source=source, link=link):
                path = self.put(source, f'# T\nSee [X]({link}).\n')
                found = self.upward(path)
                self.assertEqual(len(found), 1, found)
                self.assertIn('line 2', found[0])
                self.assertIn(link.partition('#')[0], found[0])

    def test_same_layer_and_downward_links_are_not_reported(self) -> None:
        self.targets()
        cases = [('docs/process.md', './system.md'), ('docs/process.md', './khayyam/khayyam.md'), ('docs/process.md', './khayyam/'), ('docs/khayyam/flow.md', '../system.md'), ('modules/process/flow/flow.md', '../error/error.md'), ('modules/process/flow/flow.md', '../../../docs/system.md'), ('modules/process/flow/flow.md', '../../../docs/khayyam/khayyam.md'), ('modules/process/flow/flow.md', '../error/README.md'), ('modules/process/flow/flow.md', '../../../bundles'), ('bundles/khayyam/rules.md', '../../docs/khayyam/khayyam.md'), ('modules/process/error/error.md', '../../../modules/process/error/error.md'), ('modules/process/error/error.md', '../../../bundles/khayyam/khayyam.md')]
        for source, link in cases:
            with self.subTest(source=source, link=link):
                path = self.put(source, f'# T\nSee [X]({link}).\n')
                self.assertEqual(self.upward(path), [])

    def test_a_path_in_a_code_span_is_not_reported(self) -> None:
        self.targets()
        path = self.put('docs/process.md', '# T\nRealized in `bundles/khayyam/khayyam.md`; shown as `[X](../bundles/khayyam/khayyam.md)`.\n')
        self.assertEqual(self.upward(path), [])

    def test_a_readme_may_point_into_its_own_folder_only(self) -> None:
        self.targets()
        inside = self.put('docs/README.md', '# Docs\n[System](./system.md) [Language](./khayyam/khayyam.md)\n')
        self.assertEqual(self.upward(inside), [])
        out = self.put('docs/khayyam/README.md', '# Khayyam\n[Error](../../modules/process/error/error.md)\n')
        self.assertEqual(len(self.upward(out)), 1)

    def test_files_outside_the_layers_are_not_judged(self) -> None:
        self.targets()
        self.put('CONTRIBUTORS.md', '# Contributors\n')
        root_readme = self.put('README.md', '# Memar\n[Code](./bundles/khayyam/khayyam.md)\n')
        self.assertEqual(self.upward(root_readme), [])
        skill = self.put('.agents/skills/memar/notes.md', '# N\n[E](../../../modules/process/error/error.md)\n')
        self.assertEqual(self.upward(skill), [])
        base = self.put('docs/process.md', '# T\n[C](../CONTRIBUTORS.md)\n')
        self.assertEqual(self.upward(base), [])

    def test_outside_a_memar_repository_nothing_is_layered(self) -> None:
        self.isolate()
        self.write('plain/docs/modules/error.md', '# Error\n')
        path = self.write('plain/docs/process.md', '# T\n[E](./modules/error.md)\n')
        self.assertEqual(self.upward(path), [])

class OwedMarkIsAHint(LinkFixture):

    def run_check(self, memar_rules: bool=True) -> tuple[str, int]:
        import argparse
        import contextlib
        import io
        args = argparse.Namespace(files=[str(self.root)], verbose=False, memar_rules=memar_rules)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return (out.getvalue(), code)

    def test_a_changelog_file_is_not_read_for_propagations(self) -> None:
        self.write('docs/a.changelog.md', '# Log\n- Propagates to:\n  - x.md: Pending - owed\n')
        out, code = self.run_check()
        self.assertNotIn('undischarged propagations', out)
        self.assertNotIn('x.md', out)
        self.assertEqual(code, 0)

    def test_an_id_on_both_sides_is_not_reported(self) -> None:
        self.write('a.md', '# A\nOwed: khayyam.js-backend-runs\n')
        self.write('t/a.test.ts', "test('owed:khayyam.js-backend-runs runs', { todo: true }, () => {});\n")
        out, code = self.run_check()
        self.assertNotIn('khayyam.js-backend-runs', out)
        self.assertNotIn('owed marks', out)
        self.assertEqual(code, 0)

    def test_a_document_only_id_is_a_hint_not_a_problem(self) -> None:
        self.write('a.md', '# A\nOwed: only.in-doc\n')
        out, code = self.run_check()
        self.assertIn('owed marks', out)
        self.assertIn('only.in-doc', out)
        self.assertIn('no pending Test', out)
        self.assertIn('0 problems', out)
        self.assertEqual(code, 0)

    def test_a_test_only_id_is_a_hint_not_a_problem(self) -> None:
        self.write('a.md', '# A\nNothing owed.\n')
        self.write('t/test_a.py', "class T:\n    def test_x(self):\n        'owed:only.in-test is pending'\n")
        out, code = self.run_check()
        self.assertIn('only.in-test', out)
        self.assertIn('no Owed line', out)
        self.assertIn('0 problems', out)
        self.assertEqual(code, 0)

    def test_an_id_quoted_inside_prose_is_ignored(self) -> None:
        self.write('a.md', '# A\nWrite `Owed: quoted.id` in the document, or say Owed: prose.id inline.\n```\nOwed: fenced.id\n```\n')
        out, _ = self.run_check()
        self.assertNotIn('quoted.id', out)
        self.assertNotIn('prose.id', out)
        self.assertNotIn('fenced.id', out)

    def test_a_path_is_not_an_id(self) -> None:
        self.write('a.md', '# A\nOwed: docs/x.md\nOwed: Has Space\n')
        out, _ = self.run_check()
        self.assertNotIn('owed marks', out)

    def test_no_memar_rules_skips_the_hint(self) -> None:
        self.write('a.md', '# A\nOwed: only.in-doc\n')
        out, code = self.run_check(memar_rules=False)
        self.assertNotIn('owed marks', out)
        self.assertEqual(code, 0)

class HandoffFilesAreNotJudgedByName(LinkFixture):
    ENTRY = '## Decisions\n### D?\n- **State**: x\n'

    def run_check(self, memar_rules: bool=True) -> tuple[str, int]:
        import argparse
        import contextlib
        import io
        args = argparse.Namespace(files=[str(self.root)], verbose=False, memar_rules=memar_rules)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return (out.getvalue(), code)

    def test_a_short_entry_in_a_handoff_file_gives_no_warning(self) -> None:
        self.write('a.handoff.md', '# A handoff\n\n' + self.ENTRY)
        out, code = self.run_check()
        self.assertNotIn('lacks', out)
        self.assertNotIn('warning', out)
        self.assertEqual(code, 0)

    def test_the_check_no_longer_names_the_entry_lint(self) -> None:
        self.assertFalse(hasattr(content_check, 'entry_warnings'))

    def test_an_open_questions_section_in_a_handoff_file_is_a_problem_as_in_any_document(self) -> None:
        self.write('a.handoff.md', '# A handoff\n## Open Questions\n### Q?\n- **State**: x\n')
        out, code = self.run_check()
        self.assertIn('Open Questions', out)
        self.assertEqual(code, 1)

class DocumentRulesInTheCheck(LinkFixture):

    def run_check(self, memar_rules: bool=True) -> tuple[str, int]:
        import argparse
        import contextlib
        import io
        args = argparse.Namespace(files=[str(self.root)], verbose=False, memar_rules=memar_rules)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return (out.getvalue(), code)

    def test_each_decided_breach_is_a_problem_of_the_file(self) -> None:
        self.write('modules/a/protocol/a.kh', 'tp Thing ab {\n}\n\ntp GetName mt (self Thing) () (name Thing)\n\ntp GetSize mt (self Thing) () (size Thing)\n')
        self.write('modules/c/c.md', '# C\n')
        self.write('modules/c/protocol/c.kh', 'tp C ab {\n}\n')
        path = self.write('modules/a/a.md', '# A\nA group holds no Topics.\nSee [C](../c/c.md).\n| Name | Meaning |\n|---|---|\n| GetName | x |\n| GetSize | y |\n| Thing | z |\n## Open Questions\n- Q?\n')
        found = self.problems(path)
        for mark in ('no-record-beside-a-document.md', 'documentation.md#written-surface', 'document-restates-no-code.md'):
            with self.subTest(mark=mark):
                self.assertEqual(len([p for p in found if mark in p]), 1, found)
        self.assertEqual([p for p in found if 'document-names-only-its-own-domain.md' in p], [])

    def test_check_file_keeps_the_hints_so_they_are_not_computed_again(self) -> None:
        self.write('modules/c/c.md', '# C\n')
        path = self.write('modules/d/d.md', '# D\nA plan is not a schedule.\nSee [C](../c/c.md).\n')
        cache: dict = {}
        content_check.check_file(path, cache, root=self.root)
        kept = cache[('document-hints', str(path))]
        self.assertEqual(len(kept), 2, kept)
        cache[('document-hints', str(path))] = ['kept']
        self.assertEqual(content_check.document_hints(path, cache, self.root), ['kept'])

    def test_hints_are_printed_apart_and_change_no_exit(self) -> None:
        self.write('modules/c/c.md', '# C\n')
        self.write('modules/d/d.md', '# D\nA plan is not a schedule.\nSee [C](../c/c.md).\n')
        out, code = self.run_check()
        self.assertIn('hints (not counted as problems)', out)
        self.assertIn('is not a', out)
        self.assertIn('modules/c', out.replace('\\', '/'))
        self.assertIn('0 problems', out)
        self.assertEqual(code, 0)

    def test_no_memar_rules_judges_none_of_them(self) -> None:
        self.write('modules/a/a.md', '# A\nA group holds no Topics.\n## Open Questions\nA plan is not a schedule.\n')
        out, code = self.run_check(memar_rules=False)
        self.assertNotIn('Open Questions', out)
        self.assertNotIn('hints', out)
        self.assertEqual(code, 0)

class TempHoldsNoContent(LinkFixture):
    FRONT = '---\nkind: plan\nauthor: memar\nplaced_at: 2026-11-01T06:08:50Z\ncontent: cccb33f5-d955-467e-bb6a-39cedd3e0d77\n---\n'
    BODY_ONE = '# One\nfirst body\n'
    BODY_TWO = '# Two\nsecond body\n'
    TASK = '.agents/tasks/20261101-T060801Z-24804'
    OTHER = '.agents/tasks/20261101-T070000Z-1'

    def run_check(self) -> tuple[str, int]:
        import argparse
        import contextlib
        import io
        args = argparse.Namespace(files=[str(self.root)], verbose=False, memar_rules=True)
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                content_check.cmd_check(args, self.root)
            except SystemExit as stop:
                code = stop.code or 0
        return (out.getvalue(), code)

    def task_with_two_contents(self, task: str=None) -> str:
        task = task or self.TASK
        self.write(f'{task}/content.00001.md', self.FRONT + self.BODY_ONE)
        self.write(f'{task}/content.00002.md', self.FRONT + self.BODY_TWO)
        return task

    def test_a_temp_file_equal_to_a_content_body_is_reported(self) -> None:
        task = self.task_with_two_contents()
        self.write(f'{task}/temp/draft.txt', self.BODY_TWO)
        out, code = self.run_check()
        self.assertIn('draft.txt', out)
        self.assertIn('content.00002.md', out)
        self.assertEqual(code, 1)

    def test_a_final_newline_is_ignored(self) -> None:
        task = self.task_with_two_contents()
        self.write(f'{task}/temp/draft.txt', self.BODY_ONE.rstrip('\n'))
        out, code = self.run_check()
        self.assertIn('draft.txt', out)
        self.assertIn('content.00001.md', out)
        self.assertEqual(code, 1)

    def test_a_temp_file_that_differs_is_not_reported(self) -> None:
        task = self.task_with_two_contents()
        self.write(f'{task}/temp/draft.txt', self.BODY_ONE + 'one more line\n')
        out, code = self.run_check()
        self.assertNotIn('draft.txt', out)
        self.assertEqual(code, 0)

    def test_a_temp_file_equal_to_a_content_of_another_task_is_not_reported(self) -> None:
        self.task_with_two_contents()
        other = self.task_with_two_contents(self.OTHER)
        self.write(f'{self.TASK}/temp/draft.txt', 'a body only the other task holds\n')
        self.write(f'{other}/content.00003.md', self.FRONT + 'a body only the other task holds\n')
        out, code = self.run_check()
        self.assertNotIn('draft.txt', out)
        self.assertEqual(code, 0)

    def test_a_task_with_no_temp_folder_is_not_reported(self) -> None:
        self.task_with_two_contents()
        out, code = self.run_check()
        self.assertNotIn('temp', out)
        self.assertEqual(code, 0)

if __name__ == '__main__':
    unittest.main(verbosity=2)

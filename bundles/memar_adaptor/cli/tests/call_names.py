#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from pathlib import Path
import argparse
import io
import contextlib
import sys
import unittest

TOP = Path(__file__).resolve().parents[4]
sys.path[:0] = [str(TOP), str(TOP / 'bundles/memar/services'), str(TOP / 'bundles/memar_adaptor/cli')]
sys.dont_write_bytecode = True
BUDGET_SECONDS = 20
from bundles.memar_adaptor.cli.call_names import flat_parser, LegacyDetails
from bundles.memar_adaptor.mcp.services import _tools
from bundles.memar_adaptor.cli import router
from modules.process.service.errors.call_name import CallNameCollision


def example():
    top = argparse.ArgumentParser(prog='memar')
    group = top.add_subparsers().add_parser('display-category')
    group.add_argument('--shared', default='old')
    group.set_defaults(_memar_run_0=lambda args: None)
    leaf = group.add_subparsers().add_parser('display-command', help='summary', description='overview')
    leaf.add_argument('thing')
    leaf.add_argument('--number', type=int, default=2)
    leaf.set_defaults(_memar_run_1=lambda args: print(args.thing, args.number, args.shared))
    leaf._memar_details = LegacyDetails('Actual Domain', 'Actual Name')
    return top


class FlatCalls(unittest.TestCase):
    def test_explicit_service_details_survive_a_display_category_change(self):
        from modules.process.service.primitive.declaration import declare
        from bundles.memar_adaptor.cli.derive import describer
        def work():
            return 'yes'
        top = argparse.ArgumentParser(prog='memar')
        shown = top.add_subparsers().add_parser('temporary-display-group')
        describer(declare(work, domain='Work', name='Do', summary='s'))(shown.add_subparsers())
        parser = flat_parser(top)
        self.assertEqual(_tools.tools(parser)[0].name, 'work_do')
        self.assertIsNotNone(parser.parse_args(['work_do']))

    def test_hidden_legacy_calls_are_not_advertised_in_root_help(self):
        top = argparse.ArgumentParser(prog='memar')
        top.add_subparsers().add_parser('private-worker', help=argparse.SUPPRESS)
        parser = flat_parser(top)
        self.assertNotIn('==SUPPRESS==', parser.format_help())
        self.assertNotIn('memar_private_worker', parser.format_help())
        self.assertIsNotNone(parser.parse_args(['memar_private_worker']))

    def test_rendered_help_uses_the_actual_flat_calls_without_rewriting_inputs(self):
        top = example()
        leaf = top._subparsers._group_actions[0].choices['display-category']._subparsers._group_actions[0].choices['display-command']
        leaf.description = 'Run `memar display-category display-command x`; ask `memar display-category --help`.'
        parser = flat_parser(top)
        helper = io.StringIO()
        with contextlib.redirect_stdout(helper), self.assertRaises(SystemExit):
            parser.parse_args(['actual_domain_actual_name', '--help'])
        self.assertIn('memar actual_domain_actual_name x', ' '.join(helper.getvalue().split()))
        self.assertIn('memar --help', ' '.join(helper.getvalue().split()))
        self.assertEqual(parser.parse_args(['actual_domain_actual_name', 'memar display-category']).thing,
                         'memar display-category')

    def test_details_override_display_groups_and_keep_arguments_and_parent_runs(self):
        parser = flat_parser(example())
        parsed = parser.parse_args(['actual_domain_actual_name', 'x', '--number', '3', '--shared', 'yes'])
        self.assertEqual(len(router.runs(parsed)), 2)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            router.apply(parsed)
        self.assertEqual(out.getvalue(), 'x 3 yes\n')

    def test_cli_and_mcp_use_exactly_the_same_name_and_call_words(self):
        parser = flat_parser(example())
        tool, = _tools.tools(parser)
        self.assertEqual(tool.name, 'actual_domain_actual_name')
        words, _ = _tools.argv(tool, {'thing': 'x', 'number': 3})
        self.assertEqual(words[0], tool.name)
        self.assertEqual(parser.parse_args(words).thing, 'x')

    def test_old_group_words_are_not_public_calls(self):
        parser = flat_parser(example())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            parser.parse_args(['display-category', 'display-command', 'x'])

    def test_duplicate_names_are_refused_without_overwriting(self):
        top = example()
        other = top._subparsers._group_actions[0].add_parser('another')
        other._memar_details = LegacyDetails('Actual Domain', 'Actual Name')
        with self.assertRaises(CallNameCollision):
            flat_parser(top)

    def test_mcp_exclusion_uses_the_legacy_origin_not_a_flat_prefix_guess(self):
        top = argparse.ArgumentParser(prog='memar')
        groups = top.add_subparsers()
        groups.add_parser('mcp').add_subparsers().add_parser('worker')
        groups.add_parser('task').add_subparsers().add_parser('mcp-report')
        tools = _tools.tools(flat_parser(top), left_out=('mcp',))
        self.assertEqual([t.name for t in tools], ['task_mcp_report'])


if __name__ == '__main__':
    unittest.main()

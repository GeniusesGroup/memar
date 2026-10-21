#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/update/update.py — `memar update`: whether what Memar installed is still current, and refreshing it.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar update --help` prints: it is addressed to whoever wants to
know whether Memar on this machine has fallen behind, and it says what is
checked and what `--apply` does. `SUMMARY` is its line in `memar --help`, and
it carries the daily background run as well, because that run reaches every
person who types `memar`, and `memar --help` is where such a person looks.
Everything from here down is addressed to whoever opens this file.

Installing Memar copies things out of the checkout — the skill into agent apps,
the editor extensions into the editor — and the checkout keeps changing after
the copy is made. A copy that has fallen behind fails quietly: an agent acts on
rules that are gone, an editor runs a client against a server that has moved
on.

This file declares the verb and dispatches, and nothing else. Each run is one
service on this shelf, which holds why it is built as it is: `update_check`
answers the run a person asks for, with or without --apply, and
`update_background` the daily run `update_daily` starts; `update_copies` is
how both ask the install layers about their copies and refresh them. They are
imported only when the verb runs, because every `memar` invocation imports
this file to learn what `update` accepts.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import argparse
from typing import Callable
from bundles.memar.services.update.services.copies import REFRESH
from bundles.memar.services.update.services.daily import BACKGROUND_FLAG, OPT_OUT_VARIABLE, UPDATE_VERB
SUMMARY = f'check that what Memar installed is current; refresh it. Once a day the first `memar` command runs `memar {UPDATE_VERB}` in the background, and the next one says so if it needs you; {OPT_OUT_VARIABLE}=1 stops it.'
DESCRIPTION = f"memar update — is what Memar installed still current?\n\n    memar update               check, and name each thing that is stale;\n                               writes nothing\n    memar update --apply       refresh what is stale\n    memar update --quiet       check, and print nothing when all is current\n\nWhat is checked:\n\n  - the copies of the Memar skill in the AI agent apps on this machine;\n  - the MCP server's registration in those apps (the command and args that start it);\n  - the editor extensions Memar installed into your editor;\n  - whether this machine's Memar checkout is behind the branch it tracks.\n\n`--apply` refreshes the first three. A command you run never changes the\ncheckout: when it is behind, the git command that brings it up to date is\nprinted, and running it is yours to decide, because the checkout may hold work\nof yours. Update the checkout first, then run `{REFRESH}`, and everything is on\nthe same version.\n\nOnce a day the first `memar` command runs this with --apply in the background,\nand fast-forwards a clean consumer checkout; the next one says so if it needs\nyou. {OPT_OUT_VARIABLE}=1 stops it.\n\nA project's own AGENTS.md is not checked; `memar install`, run in the\nproject, writes it again.\n\nThe exit status is 0 whenever the check could run, stale or not, and 1 when\nit could not, or when a refresh --apply asked for failed.\n"

def run(args: argparse.Namespace) -> int:
    from machine.env_location import resolve_root
    from bundles.memar.services.update.services.background import run_in_background
    from bundles.memar.services.update.services.check import check
    checkout = resolve_root()
    if args.background:
        return run_in_background(checkout, fetch=not args.offline)
    return check(checkout, apply=args.apply, quiet=args.quiet, fetch=not args.offline)

def describe(verbs) -> Callable[[argparse.Namespace], int]:
    parser = verbs.add_parser(UPDATE_VERB, help=SUMMARY, description=DESCRIPTION)
    parser.add_argument('--apply', action='store_true', help='refresh the skill copies, MCP registrations and editor extensions that are stale')
    parser.add_argument('--quiet', action='store_true', help='print nothing when everything is current')
    parser.add_argument('--offline', action='store_true', help='compare the checkout with what was fetched last, without fetching')
    parser.add_argument(BACKGROUND_FLAG, action='store_true', help='the daily run `memar` starts: --apply, a fast-forward of a consumer checkout, and one line left for the next `memar` command')
    return run

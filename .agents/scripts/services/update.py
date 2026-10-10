#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/update.py — `memar update`: whether what Memar installed is still current, and refreshing it.

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

from services.update_copies import REFRESH
from services.update_daily import BACKGROUND_FLAG, OPT_OUT_VARIABLE, UPDATE_VERB

SUMMARY = (
    f"check that what Memar installed is current; refresh it. Once a day the first "
    f"`memar` command runs `memar {UPDATE_VERB}` in the background, and the next one "
    f"says so if it needs you; {OPT_OUT_VARIABLE}=1 stops it."
)

DESCRIPTION = f"""memar update — is what Memar installed still current?

    memar update               check, and name each thing that is stale;
                               writes nothing
    memar update --apply       refresh what is stale
    memar update --quiet       check, and print nothing when all is current

What is checked:

  - the copies of the Memar skill in the AI agent apps on this machine;
  - the editor extensions Memar installed into your editor;
  - whether this machine's Memar checkout is behind the branch it tracks.

`--apply` refreshes the first two. A command you run never changes the
checkout: when it is behind, the git command that brings it up to date is
printed, and running it is yours to decide, because the checkout may hold work
of yours. Update the checkout first, then run `{REFRESH}`, and everything is on
the same version.

Once a day the first `memar` command runs this with --apply in the background,
and fast-forwards a clean consumer checkout; the next one says so if it needs
you. {OPT_OUT_VARIABLE}=1 stops it.

A project's own AGENTS.md is not checked; `memar install`, run in the
project, writes it again.

The exit status is 0 whenever the check could run, stale or not, and 1 when
it could not, or when a refresh --apply asked for failed.
"""


def run(args: argparse.Namespace) -> int:
    from machine.env_location import resolve_root
    from services.update_background import run_in_background
    from services.update_check import check

    checkout = resolve_root()
    if args.background:
        return run_in_background(checkout, fetch=not args.offline)
    return check(checkout, apply=args.apply, quiet=args.quiet, fetch=not args.offline)


def describe(verbs) -> Callable[[argparse.Namespace], int]:
    parser = verbs.add_parser(UPDATE_VERB, help=SUMMARY, description=DESCRIPTION)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="refresh the skill copies and editor extensions that are stale",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="print nothing when everything is current",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="compare the checkout with what was fetched last, without fetching",
    )
    parser.add_argument(
        BACKGROUND_FLAG,
        action="store_true",
        help="the daily run `memar` starts: --apply, a fast-forward of a consumer "
             "checkout, and one line left for the next `memar` command",
    )
    return run

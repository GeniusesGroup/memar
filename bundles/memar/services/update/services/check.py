#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/update/services/check.py — `memar update` as a person runs it: what is stale, and with --apply, refreshed.

The question is asked in one place, as one command, rather than as a warning
scattered into whichever verbs happen to run often: each scattered check is
another place to maintain and another verb slowed by a question that is not its
own. The copies are asked through `update_copies`; whether the checkout is
behind the branch it tracks is answered by `update_checkout`, and a run a
person asked for only reports it, printing the command they would run, because
the checkout may hold work nobody committed.

What a project holds — its AGENTS.md section and the file it points at — is not
checked: the project layer has no comparison of its own, and this command
writes into no project, named or not.

It is built to be run unattended as well as by hand: quiet, it prints nothing
when everything is current, and it fails only when the check itself could not
run, or a refresh it was asked for failed — a stale copy is an answer, and so
is a fetch that found no network.

Every `memar` invocation imports this file with the rest of the shelf, so what
only the check needs is imported inside it.
"""
from __future__ import annotations

import sys
from pathlib import Path


def checkout_line(checkout: Path, *, fetch: bool) -> tuple[str | None, str]:
    """A stale line when CHECKOUT is behind its upstream, and what to say when it is not."""
    from bundles.memar.update.services.checkout import upstream_of

    standing = upstream_of(checkout, fetch=fetch)
    if standing.branch is None:
        return None, f"the checkout at {checkout} tracks no upstream, so it was not compared"
    ahead = f", and {standing.ahead} ahead" if standing.ahead else ""
    as_of = f" ({standing.unfetched}; counted against the last fetch)" if standing.unfetched else ""
    if standing.behind:
        if standing.ahead:
            command = f'git -C "{checkout}" status, then reconcile the two by hand'
        else:
            command = f'git -C "{checkout}" pull --ff-only'
        return (
            f"behind: the Memar checkout at {checkout} is {standing.behind} commit(s) behind "
            f"{standing.branch}{ahead}{as_of}; to bring it up to date, run: {command}",
            "",
        )
    return None, f"the checkout at {checkout} is not behind {standing.branch}{ahead}{as_of}"


def check(checkout: Path, *, apply: bool, quiet: bool, fetch: bool) -> int:
    """Name each stale thing, and with APPLY refresh the copies; the exit status."""
    import subprocess

    from machine.editor_extension import stale_extensions
    from bundles.memar.update.services.copies import extension_lines, refresh_extensions, refresh_skills, stale_skill_lines

    try:
        skills = stale_skill_lines()
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        print(f"error: the skill copies could not be checked: {error}", file=sys.stderr)
        return 1
    extensions = stale_extensions(checkout)
    behind, standing = checkout_line(checkout, fetch=fetch)
    stale = [*skills, *extension_lines(extensions), *([behind] if behind else [])]

    for line in stale:
        print(line)
    if not stale and not quiet:
        print(f"Memar is current: the skill copies and editor extensions match {checkout}, and {standing}.")
    if not apply:
        return 0

    failed = False
    if skills:
        try:
            failed |= not refresh_skills()
        except (OSError, subprocess.SubprocessError) as error:
            print(f"error: the skill copies could not be refreshed: {error}", file=sys.stderr)
            failed = True
    if extensions:
        trouble = refresh_extensions(checkout, extensions)
        if trouble:
            print(f"error: {trouble}", file=sys.stderr)
            failed = True
    if behind:
        print("the checkout is left as it is; run the command above to bring it up to date")
    return 1 if failed else 0

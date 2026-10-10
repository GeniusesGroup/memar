#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/update_background.py — the daily run: the checkout fast-forwarded, the copies refreshed, one line left.

`memar update --background` is the run the launcher starts once a day through
`update_daily`, which owns when it starts, its lock, and the line it leaves
for the next command. It does what `--apply` does, through `update_copies`,
and before that asks `update_checkout.fast_forward` to bring the checkout up
to date — which that module does only for a consumer's checkout, and refuses
for any checkout that is marked, or looks, like someone's work on Memar.

Nobody is watching it, so what it prints goes to its log, and what a person
needs is the one line: the checkout moved, or is behind and why it was not
moved, or which copies were refreshed, or which could not be and what to run.
A failure in one step is said in that line and stops no other step.

Every `memar` invocation imports this file with the rest of the shelf, so what
only the run needs is imported inside it.
"""
from __future__ import annotations

from pathlib import Path


def background_update(checkout: Path, *, fetch: bool) -> str:
    """Bring a consumer's CHECKOUT up to date, refresh what is stale, and return the line a person needs, or ''."""
    import subprocess

    from machine.editor_extension import stale_extensions
    from services.update_checkout import fast_forward
    from services.update_copies import REFRESH, refresh_extensions, refresh_skills, stale_skill_lines

    said = []
    forwarded = fast_forward(checkout, fetch=fetch)
    standing = forwarded.standing
    if forwarded.moved:
        said.append(f"Memar was updated: {checkout} moved {forwarded.moved} commit(s) forward to {standing.branch}")
    elif standing.behind:
        said.append(
            f"Memar is {standing.behind} commit(s) behind {standing.branch} and was not updated because "
            f"{' and '.join(forwarded.refused)}; `memar update` says what to run"
        )
    print(f"checkout: {standing}; moved {forwarded.moved}; refused: {forwarded.refused or 'nothing'}")
    refreshed = []
    try:
        skills = stale_skill_lines()
        if skills and refresh_skills():
            refreshed.append(f"{len(skills)} skill copy(ies)")
        elif skills:
            said.append(f"the stale skill copies could not be refreshed; run `{REFRESH}`")
    except (OSError, subprocess.SubprocessError, RuntimeError) as error:
        print(f"error: the skill copies could not be checked or refreshed: {error}")
        said.append("the daily update could not check the skill copies; run `memar update`")
    extensions = stale_extensions(checkout)
    if extensions:
        trouble = refresh_extensions(checkout, extensions)
        if trouble:
            print(f"error: {trouble}")
            said.append(trouble)
        else:
            refreshed.append(f"{len(extensions)} editor extension(s), so reload the editor window")
    if refreshed:
        said.append("stale copies refreshed: " + ", ".join(refreshed))
    return "; ".join(said)


def run_in_background(checkout: Path, *, fetch: bool) -> int:
    """The daily run on CHECKOUT: one at a time, its line left for the next `memar` command."""
    from services.update_daily import daily_run, leave_notice, state_dir

    directory = state_dir()
    with daily_run(directory) as held:
        if not held:
            print("another update is running, so this one stops")
            return 0
        line = background_update(checkout, fetch=fetch)
        print(f"notice: {line or 'none'}")
        if line:
            leave_notice(directory, line)
    return 0

#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/services/update/services/copies.py — the copies Memar installed, asked whether they are stale and refreshed.

Installing Memar writes things out of the checkout — a pointer to the skill into
agent apps, the MCP server's registration in those apps, the editor extensions
into the editor — and the checkout keeps changing after they are written. This
file asks and relays; it compares and copies nothing itself. Each install layer
keeps what it already owns — which copies exist, whether one still matches, how
it is refreshed — and is asked here the way the installer asks it:

  - the skill copies belong to `bundles/memar/services/install/services/apps.py`, the agent-app layer,
    so it is asked in this process the way `memar install` asks it, through
    `bundles/memar/services/install/install.py`'s `ask_layer`: `stale` to ask and `update` to refresh,
    and its lines are relayed as they are;
  - the MCP registration belongs to `bundles/memar/services/install/services/apps_mcp.py`, asked
    the same way for a command that fell behind a moved launcher or a new interpreter;
  - the editor extensions belong to `machine/editor_extension.py`, a module, so
    `stale_extensions` and `install_extensions` are imported and called.

Both the check a person runs (`update_check`) and the daily run
(`update_background`) ask through here, so the two refresh the same way.

A refresh of the editor extensions moves the installed folder to the trash
before it copies, so a copy that fails leaves the editor without the
extension; nobody may be watching, so that is answered with a line saying what
to run rather than with a traceback in a log.

Every `memar` invocation imports this file with the rest of the shelf, and
`update` takes `REFRESH` from it for its help, so the layers are imported only
when one is asked.
"""
from __future__ import annotations
import contextlib
import io
from collections.abc import Collection
from pathlib import Path
APPS_STALE = 'stale'
APPS_REFRESH = 'update'
REFRESH = 'memar update --apply'

def apps_stale() -> None:
    """The agent-app layer's `stale`: one line per skill pointer, or full copy, that is not the pointer the checkout would write."""
    from bundles.memar.services.install.services import apps as install_apps
    install_apps.warn_stale(install_apps.checkout_skill())

def apps_refresh() -> None:
    """The agent-app layer's `update`: rewrite the existing skill folders as the pointer, a full copy included."""
    from bundles.memar.services.install.services import apps as install_apps
    install_apps.into_apps(existing_only=True)
APPS_ANSWERS = {APPS_STALE: apps_stale, APPS_REFRESH: apps_refresh}

def mcp_stale() -> None:
    """The MCP registration layer's `warn_stale`: one line per setting whose command is not current."""
    from bundles.memar.services.install.services import apps_mcp as install_apps_mcp
    install_apps_mcp.warn_stale()

def mcp_refresh() -> None:
    """The MCP registration layer's refresh: rewrite each app's Memar entry to the current command."""
    from bundles.memar.services.install.services import apps_mcp as install_apps_mcp
    install_apps_mcp.into_apps()

def ask_apps(command: str, *, capture: bool) -> tuple[int, str, str]:
    """Ask the skill copies' owner COMMAND: its exit status, and with CAPTURE what it printed and what it complained."""
    from bundles.memar.services.install.install import ask_layer
    printed, complained = (io.StringIO(), io.StringIO())
    with contextlib.ExitStack() as captured:
        if capture:
            captured.enter_context(contextlib.redirect_stdout(printed))
            captured.enter_context(contextlib.redirect_stderr(complained))
        status = ask_layer(APPS_ANSWERS[command])
    return (status, printed.getvalue(), complained.getvalue())

def stale_skill_lines() -> list[str]:
    """The lines the skill copies' owner prints, one per stale copy; raises when it cannot answer."""
    status, printed, complained = ask_apps(APPS_STALE, capture=True)
    if status != 0:
        said = complained.strip() or f'exit status {status}'
        raise RuntimeError(f'install_apps {APPS_STALE} failed: {said}')
    return [line for line in printed.splitlines() if line.strip()]

def refresh_skills() -> bool:
    """Refresh the stale skill copies; whether their owner says it did."""
    status, _, _ = ask_apps(APPS_REFRESH, capture=False)
    return status == 0

def stale_mcp_lines() -> list[str]:
    """The lines the MCP registration's owner prints, one per stale setting; raises when it cannot answer."""
    from bundles.memar.services.install.install import ask_layer
    printed, complained = (io.StringIO(), io.StringIO())
    with contextlib.redirect_stdout(printed), contextlib.redirect_stderr(complained):
        status = ask_layer(mcp_stale)
    if status != 0:
        said = complained.getvalue().strip() or f'exit status {status}'
        raise RuntimeError(f'install_apps_mcp stale failed: {said}')
    return [line for line in printed.getvalue().splitlines() if line.strip()]

def refresh_mcp() -> bool:
    """Refresh the stale MCP registrations; whether their owner says it did."""
    from bundles.memar.services.install.install import ask_layer
    return ask_layer(mcp_refresh) == 0

def extension_lines(stale: Collection[Path]) -> list[str]:
    """One line per editor extension in STALE, missing or different from the checkout's."""
    lines = []
    for target in stale:
        state = "differs from the checkout's" if target.exists() else 'is not installed'
        lines.append(f'stale: the editor extension at {target} {state}; refresh with: {REFRESH}')
    return lines

def refresh_extensions(checkout: Path, stale: Collection[Path]) -> str | None:
    """Refresh the editor extensions in STALE from CHECKOUT; what to tell a person when that failed, else None."""
    from machine.editor_extension import install_extensions
    try:
        install_extensions(checkout, only=stale)
    except (Exception, SystemExit) as error:
        return f'the editor extensions could not be refreshed ({error}); any copy moved aside is in the recycle bin, and `{REFRESH}` installs them again'
    return None

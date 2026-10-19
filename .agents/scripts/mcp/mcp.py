#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/mcp.py — `memar mcp`: Memar's verbs reached as MCP tools, by an agent app that starts it.

This is the provisional first face of the Memar server, the guest adapter the owner chose on
2026-10-18 (bundles/memar/memar.handoff.md, "The MCP adapter is the server's first face"). It sits
on this shelf until it moves to `modules-plugable/net/mcp/`, as the classification handoff's entry
"MCP as a guest adapter" says, and it maps tools only: no resources and no prompts.

What it serves is generated from the command line the services declare, so it adds no verb of its
own to what an agent can do, and the `memar` command is unchanged beside it. Its sub-verbs are in
`services/`; the files there whose names begin with `_` are its parts, which the router does not
route to.
"""
from __future__ import annotations

import argparse

# The verb this domain registers; its own verbs are not served as tools.
COMMAND = "mcp"


def describe(verbs):
    verbs.add_parser(
        COMMAND,
        help="reach Memar's verbs as MCP tools, from an agent app that starts the server",
        description=(
            "Memar's verbs as the tools of a Model Context Protocol server, one tool per verb,\n"
            "each answering exactly what the verb prints. An agent app starts the server and\n"
            "talks to it; `memar install` registers it in the agent apps it knows."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return None

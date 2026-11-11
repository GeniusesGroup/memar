#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""mcp/mcp.py — `memar mcp`: Memar's verbs reached as MCP tools, by an agent app that starts it.

This is the MCP face of `bundles/memar_cli`, the guest adapter the owner chose on
2026-10-18. It maps tools only: no resources and no prompts. Tool calls become a
Server_Call for the server; the server does not see argv.

What it serves is generated from the command line the services declare, so it adds no verb of its
own to what an agent can do. Its sub-verbs are in `services/`; files whose names begin with `_`
are its parts, which the router does not route to.
"""
from __future__ import annotations
import argparse
COMMAND = 'mcp'

def describe(verbs):
    verbs.add_parser(COMMAND, help="reach Memar's verbs as MCP tools, from an agent app that starts the server", description="Memar's verbs as the tools of a Model Context Protocol server, one tool per verb,\neach answering exactly what the verb prints. An agent app starts the server and\ntalks to it; `memar install` registers it in the agent apps it knows.", formatter_class=argparse.RawDescriptionHelpFormatter)
    return None

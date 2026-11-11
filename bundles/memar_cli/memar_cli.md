---
Title: "Memar CLI"
Labels: Draft
Start Date: 2026-11-10
---
# Memar CLI
## Abstract
This bundle is Memar's **face release**: the program a person or an agent types as `memar`, and the MCP server an agent app starts as `memar mcp serve`. It reads argv or MCP tool calls, composes the verb tree the services declare, and places a face-neutral `Server_Call` on the Memar server (JSON interim). The server release does not parse argv.

## What belongs here
- Command-line entry (`memar` on PATH via `bin/memar` / `bin/memar.cmd`).
- Argv reading, argparse/`describe` composition, help text.
- MCP protocol (`mcp/` in this bundle): tool schemas from the same declarations, tool calls → `Server_Call`.
- Encoding into `Server_Call` / decoding `Server_Answer` for print.

It does not own service behavior; that stays in the modules the call names.

## How it is invoked
- **Shell / agents without MCP:** `memar …` — PATH points at this face's release, not at a server argv parser.
- **Agent apps (Cursor, …):** `memar mcp serve` from the same PATH entry; registration is still the face script under `bin`.
- **Name:** the face bundle is `memar_cli`; the command word on PATH remains `memar` so existing recipes and skill text stay one word.

## Relation to the server
[`bundles/memar`](../memar/memar.md) is the server (resident / dispatch). This face starts or asks that process with `Server_Call` fields and runs — never argv. A separate server binary on `bin` is `memar_server` when installed.

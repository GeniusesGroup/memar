---
Title: "Memar MCP"
Labels: Draft
Start Date: 2026-11-11
---
# Memar MCP
## Abstract
This part of [Memar Adaptor](../memar_adaptor.md) serves Memar to an agent app over the Model Context Protocol. The program the app starts, `memar mcp_serve`, is the same small client as the [command line](../cli/cli.md): it reads JSON-RPC messages from the app's standard input and writes the answers back. The bridge stays alive for that connection; it answers protocol pings itself so they do not keep the separate resident server alive. Other requests reach the server, starting it again when needed. MCP tools use the same flat call names as the CLI. The bridge and its current limits are described in the [CLI part](../cli/cli.md). Calls are still translated to command words and return command text, so this is not yet a structured service request/response protocol.

## What belongs here
- `handler.py`: the relay handler; `services/_worker.py` holds the tool list and answers; `services/_tools.py` builds the tool list from the flat CLI catalog; a tool call maps to the corresponding command words.
- `services/serve.py`, `worker.py`, `_call.py`: the in-place relay and worker. A busy resident can run an individual relay message in a short-lived worker; a source run with `MEMAR_SERVER=0` uses the in-place relay.
- Nothing of what a verb does; that stays in the module the verb names.

## Limit
A tool call is turned into command words and answered as if typed. It therefore still has the command line's argument and text-result shape, and runs through the server's adaptor handlers. A typed request and structured result per service remain deferred.

## Where it was
The package was first written as a bundle `memar_mcp`, withdrawn on 2026-11-10 into the command-line bundle, and moved here on 2026-11-11 when the command line, file system and git bundles became parts of one adaptor bundle.

---
Title: "Memar CLI"
Labels: Draft
Start Date: 2026-11-10
---
# Memar CLI (a part of Memar Adaptor)
## Abstract
This part of [Memar Adaptor](../memar_adaptor.md) is how a person or an agent types Memar: the program `memar`, which is a small client. The server assembles one flat service-call catalog shared with MCP. The [Service Call Name contract](../../../modules/process/service/services/call-name/protocol/call-name.kh) derives each name from service details, with explicit declaration details taking precedence. Until services declare those details directly, a Python bridge supplies provisional details from existing command declarations. That bridge does not read or compile Khayyam source. The CLI presents flat names such as `memar task_ensure`, `memar content_get_section`, `memar mcp_serve`, and `memar git_commit`; root operations include `memar_commands`, `memar_install`, and `memar_update`. The client still sends command words and execution still uses the server's adaptor handlers.

## What belongs here
- `memar`, the client: finds the project, finds or starts the server, sends the call, writes the answer. It is built without the rest of Memar and knows no verb; the few calls it treats apart are listed in `face_policy.py`.
- `router.py`: the service catalog assembled from `describe(verbs)` / `DECLARATIONS`, flattened for the CLI and MCP. Domain twin files do not declare a public group; a silent legacy nest keeps provisional Details.Domain from the folder leaf. It is loaded by the server, or imported by a source run with `MEMAR_SERVER=0`. List every call with `memar memar_commands`; `memar --help` points there.
- `call_names.py`: the provisional Python bridge that derives one flat name for both faces and rejects collisions. The Khayyam contract is [Service Call Name](../../../modules/process/service/services/call-name/protocol/call-name.kh); its Python primitive is [`call_name.py`](../../../modules/process/service/primitive/call_name.py). The bridge adapts existing declarations until services provide details directly.
- `derive.py`: the CLI declaration adapter for services that use `modules/process/service/primitive/declaration.py`; it registers their arguments and run behavior with the router.
- `handler.py`: the handler of the kind `words`, which the current Python server loads. The server also imports the router for in-place calls; removing that dependency remains deferred.
- `services/commands.py`: `memar_commands`, the card of every call.

It does not own service behavior; that stays in the modules the call names.

## How it is invoked
- **Shell / agents without MCP:** `memar …`; PATH points at the client of the release. Each service is invoked by its flat call name (for example, `memar task_ensure`).
- **Agent apps (Cursor, …):** `memar mcp_serve` from the same PATH entry; it relays the app's messages to the server one line at a time ([mcp part](../mcp/mcp.md)).
- **Source run:** `python bundles/memar_adaptor/cli/memar …` behaves the same; with `MEMAR_SERVER=0` it composes and runs the call in its own process.

## Relation to the server
[`bundles/memar`](../../memar/memar.md) is the server. The server's executable sits in the `server` folder of the same release and is also named `memar`; only the client has a shim on `bin`. Given words, the server executable runs them in place as a command, which is how a child process of the server reaches a verb without asking the server it is part of.

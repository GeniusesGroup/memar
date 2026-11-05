---
Title: "Service Rule — A Rewritten Service Leaves the Filesystem; Storage Is One Method"
Labels: Draft
Start Date: 2026-11-03
---
# Service Rule — A Rewritten Service Leaves the Filesystem; Storage Is One Method
A rule of this repository, held for [Service](../../service.md). Owner (2026-11-03, task 20261103-T084755Z-4936). Its place in a refactor is the last step of [Modularity Rule — A Refactor Moves in Order](../../../../knowledge/modularity/rules/refactor/refactor.md).

## The rule
- **When a service is rewritten, it does not depend on the filesystem as its model of storage.** Paths, folders, `open`, and checkout layout are not the service's subject. Durable state is reached only through the memory/record **adapter** (or the domain's store contract that adapter realizes). The filesystem may exist only behind that adapter.
- **Until the adapter split is complete for a given service, every access to durable state lives in one method of the service's type** (or one clearly named storage collaborator owned by that type), so moving that method onto the adapter later is a local change and not a hunt through the service.
- **A rewrite that still imports filesystem helpers into its main path for anything other than that isolated storage method is unfinished.** Tests that mkdir on a bare task id in the process cwd are a failure of this rule's spirit and of the adapter cutover.

## Why it exists
Services under task and AI still treat folders as identity. The memory/files programme already advances the adapter; rewrites that keep embedding Path/`folder_of` re-pay the cost the programme removes and block scale (search, records, MCP).

## Keep it or drop it
An organization may keep filesystem-shaped services and remain conformant to Memar's concepts, at the cost that every later storage move rewrites every caller.

## What this rule does not claim
- It does not claim the filesystem module is removed; it claims services do not *own* storage as files.
- It does not name the adapter's protocol; that is the memory/record module's.

---
Title: "Memory Files Store"
Status: Draft
Start Date: 2026-11-01
ID: 498200
---

## Abstract
`files` is an adapter of the [store contract](../../../../../modules/computer/memory/store/store.md#the-contract) under `modules-plugable/computer/memory/store/files/`. It states the **correspondence** between upstream store addresses — the ones [record](../record/record.md) and [graph](../graph/graph.md) use for nodes, parts, labels and edges — and bytes on the project's filesystem. It knows **addresses and bytes** plus that correspondence. It does **not** redefine `file` / `directory`: those concepts are owned by [filesystem](../../filesystem/filesystem.md); this adapter **only uses** `Storage_File`, `Storage_Directory`, and `URI_Path`. It is not moved under `filesystem/` — that module has no graph view. Domains never name a file, folder or path ([No File Concept](../../filesystem/rules/no-file-concept/no-file-concept.md)). A project's final adapter for a class may still be [`git-store`](../git-store/git-store.md).

The adapter is Khayyam: [`protocol/files.kh`](protocol/files.kh) and the `files-*.kh` files beside it; its refusals are [`errors/errors.kh`](errors/errors.kh). Realization performs I/O only through the filesystem module. Conformance cases are owed at implement.

## What it is to the memory contract
It realizes the contract for a sparse store of any value length with compare-and-write and atomic batch. It declares `durable` (a committed batch survives the abrupt end of the writing process). It declares `leaves_working_tree_untouched` **false**: its medium is files under the project tree. It owes the `working-tree` conformance group in this module. It does not declare `fallback`, `replicated`, or `lockable` unless a later generation adds them. It removes nothing.

One **store** is one memory root and one `batch`/`state` order. Domain keys of a [record key](../record/protocol/record-key.eng.kh) select **parts inside** one file per node id — not separate stores and not domain folders: the adapter is for the graph/store type, not for each domain.

## Path encoding (stated once)
One memory-root directory (default `.agents/memar/memory/`). **One `Storage_File` per node id**, not per domain and not per store address. Domain key selects a **part inside** that file. No domain folders.

`{root}/{id_segment}`

- **Record keys** (16-byte id then 1–64 ASCII domain-key bytes, no separator): `id_segment` is the canonical UUID text of the id (else lowercase hex of the sixteen bytes). The domain key is **not** in the path; it names the part in the file body.
- **File body (one format):** a single UTF-8 JSON **object** (pretty-printed, trailing newline). Each property name is a domain key; each property value is the part. **No** binary length-prefix framing. Encoding of a part value:
  - if the part bytes are UTF-8 text that `json.loads`, the property holds that JSON value (object, array, string, number, bool, or null) and the store keeps the compact re-encoding `json.dumps(..., separators=(',', ':'), ensure_ascii=False)` as the part bytes (token is of those bytes);
  - if the part bytes are UTF-8 text that is not JSON, the property is `{"$files.text": "..."}` and the store keeps the exact text bytes;
  - otherwise the property is `{"$files.bytes": "<base64>"}` and the store keeps the exact bytes.
  `get` returns the part bytes for the address’s domain key (Absent if the file or key is missing). `batch` upserts keys and writes each affected id’s file **once** per batch.
- **Other address kinds:** filename is lowercase hex of the whole address; body is the raw value bytes (not a JSON object) — not the primary graph/record case.
- **Time order / sharding:** UUID v7 ids sort by time in a flat directory; the adapter’s default needs no shard folders. A later optional parameter may add an id-hex prefix directory when file count is large — still never by domain.
- **Suffix:** none forced; content-type is not this adapter’s.
- **Edges and reverse edges:** each edge remains a store address (id + domain key as part). Forward and reverse typically touch **two** node files; both writes go in **one** atomic `batch`. The adapter does not interpret edge vocabulary.
- **Labels:** the `labels` domain key is one part in the node’s file.

Token of a value is the SHA-256 of the **part** bytes as the store holds them after write (for JSON text parts, the compact re-encoding above), as the contract requires — not the hash of the whole file.

## What it refuses (adapter) vs domain rules
**Adapter refuses:** a bad `memar:` parameter for this capability; an address it cannot map to a path-safe relative path; a batch it cannot apply whole; medium failures as store Unavailable/Failed. **Adapter does not refuse:** which edges a domain stores; content media type; orphan policy. **Orphans** of medium bodies are prevented by process/composition (owner ruling), not by requiring store-batch atomicity alone—though a batch still applies wholly or not at all.

## Relation to `git-store` and task 20976
`git-store` remains a parallel pluggable medium. Task `20261031-T071511Z-20976` keeps `Text_Place` over any store and the path-as-address working-tree case for source/document files; this module's first duty is record/graph addresses under the memory root. Overlap work done here is notified on that task's timeline.

## Placement
Pluggable under `modules-plugable/computer/memory/store/files/`, as named in [Memory Store → What stands where](../../../../../modules/computer/memory/store/store.md#what-stands-where). Home of the **adapter** is here; home of **File/Directory** is [filesystem](../../filesystem/filesystem.md). This module imports and uses filesystem types (`Storage_Directory` as the bound root, `Storage_File` via `FileAt`, `URI_Path` from `Files_Path`) and does not restate their protocols. It is a **new** medium (first generation), not an `EndOfLife` replacement of `git-store`. Conversion from today's per-task folder shapes is owed by the consuming domains (e.g. task parent `20261101-T073218Z-4460`), not by swapping this adapter's generation.

## The cases this module owes
Core groups for sparse / any length / compare-and-write; `model` against `volatile`; `durable`; `working-tree` in this module's [`cases.py`](cases.py) (committed batches visible as files under the memory root). When bound as a record adapter, record's id/part/label cases run through the same medium. No `replicated`/`fallback` until declared.

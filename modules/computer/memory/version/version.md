---
Title: "Memory Version"
Status: Draft
Start Date: 2026-10-26
ID: 498061
---

# Memory Version

## Abstract
`version` holds the vocabulary of a versioned value: the number of versions, the offset of one, and the two observers `Versioned` and `MaxVersioned` that a storage service reads them through. It stays a kernel module because three kernel storage services (`rights/delegate`, `identity/uri/ui/quiddity-uri`, `economics/transaction`) name it, and a kernel file may not import a pluggable one ([Placement → The rule](../../../knowledge/modularity/rules/placement/placement.md#the-rule)).

## Explanation
### Why it has a module of its own
The record contract keeps no versions of a value: the history of a value is its chain of Requests ([Memory Store](../store/store.md)), so `version` belongs to no capsule of the store and to no address. It stood in `memory/protocol/`, a folder a category does not keep ([Category](../../../knowledge/label/labels/category.md#the-rules)), and moved here when that folder was dissolved by task `20261024-T160310Z-25344`.

### Its fate
Tentative. The declarations are the Go-era versioning of a record, and the twenty-three files that import them are storage services still waiting to be rebuilt on the contract. When they are, the declarations fall with them and this module is retired; until then it is the one place the vocabulary is written ([Documentation → A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)). The declarations are in [`protocol/version.kh`](protocol/version.kh).

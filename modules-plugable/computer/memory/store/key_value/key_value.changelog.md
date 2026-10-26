# Key-Value Changelog

## Changelog

---

### The key-value store is a capsule of the memory contract: its engine on page, the Go-era Model carried over, its suite named
- Time: 2026-10-24T18:30:00Z
- Type: Changed
- Cited:
  - [Memory](../../../../../modules/computer/memory/memory.md#retention-is-reached-through-one-contract) - Reference: the contract the capsule realizes
  - [Memory Record](../record/record.md#the-operations) - Reference: the operations and the suite the capsule follows
- Tasks:
  - main:.agents/tasks/20261024-T160311Z-25344/: Partial - the design task; the build task is queued after it
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that the module is its own on `page`, that the answers of a process are its own, and that the graph module is held
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted
  - Two sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — answered the open questions and critiqued the design; the critique's findings are applied and the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [key_value.md](key_value.md) states the key and its limits, what each operation of the Go-era `Model` becomes on the contract, the engine (a copy-on-write B+tree on `page` with two meta pages, a copy-on-write free list, a log of changes, recovery by one walk), why a tree and not a log-structured one, uniqueness by an `absent` expectation, the capabilities and limits, and the suite cases that name keys or the engine; the page and block store it needs is stated as three needs checked at opening.
- [key_value.handoff.md](key_value.handoff.md) is added with the Tentative design decisions and the questions for the owner.
#### Considered and not done
- A log-structured merge tree was not taken: uniqueness needs a lookup across levels and compaction runs at moments no batch names; it stays a capsule of its own for a write-heavy class.
- A read of the capsule that answers keys with values from one state was not added: it names nothing of keys, and a capsule adds no abstraction; it is asked of the contract.
- The key count, the value length and the empty-key refusal of the first draft were not kept, the last because its reason was circular.
- The Go-era files of `protocol/` are not replaced yet; the build task does it with its own record.

---

### The key-value capsule stands under the store modules
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division that gives the new path
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The folder moved unedited from `modules/storage/key_value/` to `modules-plugable/computer/memory/store/key_value/`.
- The citation of the memory contract now names [Memory Store](../../../../../modules/computer/memory/store/store.md#the-contract), and the path in Placement is `store/key_value/`.

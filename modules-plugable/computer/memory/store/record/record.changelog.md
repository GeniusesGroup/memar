# Memory Record Changelog

## Changelog

---

### The record contract: nodes, five operations, atomic batch, contract suite, binding
- Time: 2026-10-23T17:30:00Z
- Type: Added
- Cited:
  - [Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule) - Reference: the test applied to each part of the design
  - [Label](../../../../../modules/knowledge/label/label.md#a-name-is-one-label) - Reference: the form of an id and what a label is
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme; the build tasks are queued after it
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-22/23), ruled the premises it rests on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted
  - Three sub-agents (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; their findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- [port.md](record.md) is added: the node, the id (a UUID version 7), the part under a domain key, the token (SHA-256 of the bytes), the label, the class and the batch; the operations `get`, `parts`, `list`, `scan` and `batch` with the order of a batch's answers; what every adapter guarantees (atomic, linear, one place orders the writes, durable as declared, absent is not unknown, nothing is removed, derived structures never stale); the capabilities and limits; what the port does not know; its placement under Kernel Neutrality; the binding of adapters to classes in the `memar:` block; the contract suite named by its cases, with the groups core, durable, shared, fallback, working tree and model; and what each adapter's document states.
- [port.handoff.md](record.handoff.md) is added with the Tentative decisions that answer what the build tasks would ask the owner, the erasure question, and the anticipated work.
- [README.md](README.md) points to the document.
#### Considered and not done
- A head pointer was first refused as derived data, then adopted because tokens repeat and ids order by minting instant, so the last Request cannot be derived.
- The view in the port document, an adapter-built view, a default adapter for an unset class, a port that refuses invalid text, and `sub-request` as the chain edge's name were each considered and not taken; the reasons are in the port handoff and the request handoff.
- No Status history is recovered for the migration, since the old logs hold no Status values.

---

### The contract stands in the record folder; no separate port module
- Time: 2026-10-23T18:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-parts-of-the-memory-module-their-state-and-where-each-belongs-2026-10-23) - Reference: the state of the memory module's parts
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design task of the memory-port programme
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — steered: the record is the abstraction and no separate port module is wanted; File and Directory belong to the filesystem; the pluggable floor of `computer` is too crowded
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- The contract, its handoff and its changelog move from `modules/computer/memory/port/` to `modules/computer/memory/record/`, where the Go-era Record model stood; the module called port is not made, and the word port stays in the text as the role the contract plays.
- [record.md](record.md) gains the section on the Go-era Record model, saying where each of its operations went. The adapters are named `git`, `files` and `volatile` and stand at `modules-plugable/computer/memory/record/` (the view there too) and `modules/computer/memory/record/volatile/`, mirroring the module's path as `codec` does.

---

### The record is a capsule over the memory contract, not the contract
- Time: 2026-10-24T16:10:00Z
- Type: Changed
- Cited:
  - [Memory → Retention is reached through one contract](../../../../../modules/computer/memory/memory.md#retention-is-reached-through-one-contract) - Base: the contract this capsule realizes
- Tasks:
  - main:.agents/tasks/20261024-T052936Z-22844/: Partial - the modelling task
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that the adapters are independent modules and that `record` is used by every layer above it
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- A correction at the head of the document says which statements are the memory contract's and which are this capsule's, and that this text stands as the source of both until the build task splits them.
- Placement: the contract and its suite are the memory module's; ids, parts, labels and tokens are this capsule's, which is pluggable at `modules-plugable/computer/memory/record/`; `git` and `files` are modules of their own that know no id or label; `git` shards by a prefix of the address.

---

### The first design's build scope is narrowed until the owner rules on Lock and Unlock
- Time: 2026-10-24T17:20:00Z
- Type: Changed
- Cited:
  - [Memory → Retention is reached through one contract](../../../../../modules/computer/memory/memory.md#retention-is-reached-through-one-contract) - Base: the contract
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the last review of the design before the build
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled the renames this waits on
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted
  - A sub-agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed; its findings are applied, the corrected text was not reviewed again, so no `approved` is recorded

#### What changed
- The removal of the Go-era declarations is marked pending the owner's ruling on `Lock` and `Unlock`; the token is the contract's; the address of a node is its id bytes then its domain key; `open` is declared in `bundles/memar`; the adapter for git is `git-store`.

---

### Lock and Unlock are an optional capability; Record_Model becomes Records
- Time: 2026-10-25T15:00:00Z
- Type: Changed
- Cited:
  - [Memory Record Handoff](record.handoff.md#decisions) - Reference: the decision
- Tasks:
  - main:.agents/tasks/20261023-T074641Z-5420/: Partial - the design before the build
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled that Lock and Unlock stay as an optional capability on the sync Locker with a lease, and that `Record_Model` is misnamed and becomes `Records`
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- The open question on `Lock` and `Unlock` is resolved into a Decision; the pending note in this document names the ruling; the capability `lockable` joins the contract's capabilities in the memory module.

#### Considered and not done
- Removing `Lock` and `Unlock`: the first design's reason, that a lock outliving a process contradicts the contract, was a design choice and not a necessity; the lease answers it.

---

### The Go-era declarations are upgraded: Records, RecordUUID, and the capability Lockable
- Time: 2026-10-26T09:00:00Z
- Type: Changed
- Cited:
  - [Memory Record Handoff](record.handoff.md#decisions) - Reference: the owner's ruling of 2026-10-25 that the upgrade carries out
  - [Qualified Names](../../../../../bundles/khayyam/rules/qualified-names/qualified-names.md#the-rule) - Reference: the names checked
- Tasks:
  - main:.agents/tasks/20261024-T052938Z-22844/: Complete - the upgrade in place, without moving files
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — ruled the names and the capability
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- `protocol/model.kh`: `Record_Model` is `Records`, its methods lose the `Record_Model_` prefix, and `RecordsNumbers` is `Count`; `Lock` and `Unlock` leave it for `protocol/lockable.kh`, the new abstraction `Lockable` of the optional capability.
- `Storage_UUID` is `RecordUUID`; `Storage_Observer_RecordUUID` and `Storage_Observer_RecordsUUID` are `Observer_RecordUUID` and `Observer_RecordsUUID`; the importers in `record`, `index-one_one` and the seat edge of `economics` are repointed.
- This document's section on the Go-era model names the new names.

#### Considered and not done
- The lease is not a parameter of `Lock`: its length is a limit the store declares, written when the build task writes the capability's group in the suite.
- `save-options.kh`, `data_model.kh` (`Record_DataModel`), the `services/` drafts and `IndexOneOne_Model_*` keep their names; the build task or the owner decides them.

---

### Publishing to the shared store and the commit per batch are recorded as Tentative decisions
- Time: 2026-10-26T13:00:00Z
- Type: Added
- Cited:
  - [Memory Record Handoff](record.handoff.md#decisions) - Reference: the two decisions
- Tasks:
  - main:.agents/tasks/20261023-T074642Z-5420/: Partial - the build task carries the capability and the benchmark variant in a Note
- Contributors:
  - [Omid Hekayati](../../../../../CONTRIBUTORS.md#omid-hekayati) — asked whether each record is sent to the shared store at once and whether a reference needs a commit
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — answered from the documents and drafted; no reviewer, so no `approved` is recorded

#### What changed
- The handoff gains two Tentative decisions: a store with a shared store declares `replicated` and publishes each committed batch soon after, with a private reference for the acknowledged tip; and a reference points to one commit per batch, to be tested against a bare-tree variant.

#### Considered and not done
- Pushing before a batch is answered by default: it ties every write to the network; `publish: now` is the parameter for a class that needs it.
- A reference to a bare tree: allowed by git, not chosen for the reasons in the decision, and measured by the benchmark.

---

### The record capsule stands under the store modules
- Time: 2026-10-26T14:10:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../../../../../modules/computer/memory/memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division that gives the new path
- Tasks:
  - main:.agents/tasks/20261024-T160310Z-25344/: Partial - the files moved with `git mv` and the links and addresses repaired; the second division and the build tasks are still owed
- Contributors:
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — carried out the move and repaired the links; no `approved` is recorded

#### What changed
- The folder moved unedited from `modules/computer/memory/record/` to `modules-plugable/computer/memory/store/record/`; `protocol/lockable.kh` moved to `store/lockable/`.
- Links, `in` addresses and the citation of the memory contract (now [Memory Store](../../../../../modules/computer/memory/store/store.md#the-contract)) were repaired.

# Memory Store Changelog

## Changelog

---

### The contract is written in Python and takes the statements of the record contract that name no id, part or label
- Time: 2026-10-26T15:02:00Z
- Type: Changed
- Cited:
  - [Memory Handoff](../memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative) - Reference: the division that gives this module the contract and its statements
  - [Memory Record](../../../../modules-plugable/computer/memory/store/record/record.md) - Reference: where the operations' answers, the guarantees, the capabilities, the limits and the adapter's document were stated for ids
  - [Test Practice](../../../process/test/test.practice.md#the-cycle) - Reference: the cases written before the work, pending ones carrying the owed identifier
- Tasks:
  - main:.agents/tasks/20261026-T144222Z-11720/: Partial - the protocol and the suite are written and pass on `volatile`; the `durable`, `shared` and two `lockable` cases wait for an adapter declaring them
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the protocol, moved and restated the statements, chose what the handoff records as Tentative; no `approved` is recorded

#### What changed
- [`protocol/store.py`](protocol/store.py) holds once the signatures of `get`, `list`, `batch`, `state`, `changes` and `stats`, the answers and their reasons, the token, the parameters, the limits, the capability names (`lockable` and `replicated` with the five of the first design) and the seam.
- "The contract" states the operations' answers, the guarantees, the capabilities and limits, the seam and what an adapter's document states, for addresses; they left `record.md`.
- "The cases this module owes" points at the code of the suite. `Owed: memory.port.protocol` is gone, the protocol being written; `Owed: memory.port.contract-suite` came here from `record.md` and stays while cases are pending.

#### Considered and not done
- A refusal reason of its own for an expectation on a store that cannot compare and write: NotAtomic already names a batch needing an atomicity the adapter does not declare ([Memory Store Handoff](store.handoff.md#decisions)).
- Python files in `protocol/` are not read by the module-graph test as a module's code; the handoff records it rather than moving the protocol to `primitive/`, against the path the build task gives.

---

### The `durable` and `shared` groups run on `git-store`; only `lockable`'s cases stay owed
- Time: 2026-10-26T19:45:00Z
- Type: Changed
- Cited:
  - [Test Practice → The Cycle](../../../../modules/process/test/test.practice.md#the-cycle) - Reference: a pending Test that passes stops being pending in the same change
  - [Memory Git Store](../../../../modules-plugable/computer/memory/store/git-store/git-store.md) - Reference: the first adapter declaring `durable`, `shared_between_processes`, `fallback` and `leaves_working_tree_untouched`
- Tasks:
  - main:.agents/tasks/20261026-T181945Z-16468/: Done - step 3 of task `20261023-T074642Z-5420`
- Propagates to:
  - `modules/computer/memory/conformance/conformance.py`: Done - the mark leaves the eight cases of the two groups
  - `modules/computer/memory/conformance/conformance.md`: Done - names the module that codes the `fallback`, `working-tree` and `replicated` groups
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — ran the groups and revised the paragraph; no `approved` is recorded

#### What changed
- "The cases this module owes" names `git-store` as the first adapter owing `fallback` and `working-tree`, and says the `durable` and `shared` groups run on it; `Owed: memory.port.contract-suite` stays for the two `lockable` cases that wait for a lockable adapter.

---

### The memory store contract is stated in Khayyam, ahead of any code of the redo
- Time: 2026-10-30T12:00:00Z
- Type: Added
- Cited:
  - [Software Rule — Abstraction First](../../software/rules/abstraction-first/abstraction-first.md) - Reference: the abstraction is written in Khayyam and approved by an agent that did not write it, before any code
  - [Error Rule — Errors Folder](../../../process/error/rules/errors-folder/errors-folder.md) - Reference: the errors are declared in the module's `errors` folder
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - step 2 of the redo (skeleton and its review)
- Propagates to:
  - `modules/computer/memory/store/store.md`: Pending - reduced to concept, reasons and trade-offs once the realization is changed
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the skeleton through three sub-agents; reviewed by a fourth, fresh one
  - A fresh AI reviewer (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) — approved

#### What changed
- The store contract (`protocol/*.kh` with each type's `*.eng.kh`, and `errors/errors.kh` holding `Unavailability` and `Refusal`) stands in Khayyam beside `store.py`, which is not yet changed. The volatile, conformance, lockable, record, view and git-store modules and the `memory` and `view refresh` services have their skeletons in the same way.
- The reviewer's claim, quoted: "The Khayyam abstraction skeleton of the memory store contract and of its modules stands before any code of the redo ... It follows the rules and states the same behaviour as the Python it will replace." Its verdict was permitted, with no blocking item. It ran `grep` for comment forms over 247 files (only the license header), `memar content check` over four folders (391 files, 0 problems), a check that every type has its five `detail.kh` methods, a check that every import path exists, and a check that the 36 errors are in nine `errors` folders, and it compared the declarations with the Python of each module.
- Minor findings left to the realization: `Lock` of lockable returns an `Error` for a refused address where the rest answers `Store_Refused`; nothing reachable from a `Record` closes its store; the reference-collision rule and the `refs/memar-local/` refusal are not yet in `git-store.py`; whether `changes` answers every written address (volatile) or every changed address (git-store) is not stated by the contract; the Python must gain the time budget and cost of a case; `UserActionNote` and `DevActionNote` are empty.

#### Considered and not done
- The Khayyam was not compiled or parsed: no tool of this repository parses it, so what the review establishes is conformance to the rules and to the Python's behaviour, not that the files are valid Khayyam.

---

### Memory Store: the document states the concept and the reasons, and restates no contract
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - step S4d of the redo
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - reduced the document

#### What changed
- Removed from "The contract": the operations and their answers, the parameters of each call, the list of batch outcomes, the guarantees as lists, the capabilities, limits and `stats`, the seam, the list of what an adapter document states, and the git plumbing command list; they stand in `protocol/*.kh` (with `*.eng.kh`) and `errors/errors.kh`. "The cases this module owes" lost its description of the cases (now the suite, `conformance.md`). Kept as reasons: why the contract is parametric, why one atomic batch, why `state` and `changes`, why SHA-256 and one algorithm, why Unavailable is not Absent, why one writer location, nothing is removed, why derived structures are rebuildable, why no floor, why the seam, why the caller closes the store (`Close`), and "What stands where".

---

### A `Close` of the contract was proposed and not added
- Time: 2026-10-31T09:00:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - the redo of the memory store contract
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) — decided after a fresh reviewer's finding; no `approved` is recorded

#### What changed
- The earlier record's remark that nothing reachable from a `Record` closes its store no longer holds: `Record.close` and the `memory` service close the store they opened when it has a `close`.
- The contract declares no `Close`.

#### Considered and not done
- A `Close` on the `Store` abstraction: a fresh reviewer found it declared for every store and required of none (volatile has nothing to release), returning an error no realization returned, and disagreeing with the `Close` that `git-store` declares. Closing stays the adapter's own declaration.

---

### Memory Store: the operations list, the held-range rule, NotAtomic and record's address are linked
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - second reduction of the remaining restatements
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - reduced the document

#### What changed
- Removed: the list of operations from the Abstract (now [`protocol/store.kh`](protocol/store.kh)); the held-range mechanics and the refusal of a batch without an atomic batch from the "Why" bullets (now [`git-store-held.eng.kh`](../../../../modules-plugable/computer/memory/store/git-store/protocol/git-store-held.eng.kh) and [`errors/errors.kh`](errors/errors.kh)); the restated address of `record` from "What stands where" (now [`record-key.eng.kh`](../../../../modules-plugable/computer/memory/store/record/protocol/record-key.eng.kh)).
- Kept: every heading, the reasons (one place orders the writes, a stale copy never competes, no floor) and the owner's rulings.

---

### Memory Store: the held-range rule is back as a reason
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - fixes after review
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - edited the document

#### What changed
- Corrects the previous record: the held-range rule lives in "Why one place orders the writes" of this document, as a reason (what a copy of a shared store holds, and why it can decide alone inside the ranges and ask outside them). [`git-store-held.eng.kh`](../../../../modules-plugable/computer/memory/store/git-store/protocol/git-store-held.eng.kh) holds only what `git-store` holds by default.

---

### The reduction of this document to concept, reasons and trade-offs is reviewed
- Time: 2026-10-31T10:00:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - step S4d of the redo
- Contributors:
  - A fresh AI reviewer (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) — reviewed, approved
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) — reduced the document, fixed the findings of two earlier reviewers

#### What changed
- Claim reviewed, quoted: "state the concept, the reasons and the trade-offs and restate no code or Khayyam; every fact they dropped has a home in a .kh / *.eng.kh, in code, or in a document or handoff they link to; and no reason, trade-off, owner ruling or placement decision was lost." Evidence: `memar content check` on the six folders (0 problems); the diff of each document against its base commit, each removed passage grepped for its new home; the three defects an earlier reviewer found were checked fixed. Verdict: permitted. The reviewer left minor notes: a few sentences in `record.md` and `git-store.md` still repeat an `*.eng.kh` while carrying a reason, and the requirement that a `get` of many addresses costs no process per address has its home only in `store-stats.eng.kh` and `git-store.md`.

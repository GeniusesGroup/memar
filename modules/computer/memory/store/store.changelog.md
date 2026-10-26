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

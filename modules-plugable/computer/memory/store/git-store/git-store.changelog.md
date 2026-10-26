# Memory Git Store Changelog

## Changelog

---

### `git-store` built: a store in one reference, written by `fast-import` and one compare-and-swap, published to a shared store
- Time: 2026-10-26T19:40:00Z
- Type: Added
- Cited:
  - [Memory Store](../../../../../modules/computer/memory/store/store.md#the-contract) - Reference: the contract it realizes, and what "Adapters state themselves" asks of its document
  - [Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md#groups) - Reference: the `fallback` and `working-tree` groups an adapter that declares them owes
  - [Memory Record Handoff](../record/record.handoff.md#decisions) - Reference: "Every committed batch is published to the shared store" and "A reference points to a commit per batch"
  - [Test Practice → The Cycle](../../../../../modules/process/test/test.practice.md#the-cycle) - Reference: the document, then the tests shown red on a stub, then the code
- Tasks:
  - main:.agents/tasks/20261026-T181945Z-16468/: Done - step 3 of task `20261023-T074642Z-5420`
- Propagates to:
  - `modules/process/project/services/preferences.py`: Done - the form of a class's parameters, `class_values_preference`, which `memory` reads too
  - `modules/computer/memory/store/store.md`: Done - the `durable` and `shared` cases are no longer owed
  - `modules-plugable/computer/memory/store/record/record.md`: Done - the cross-process case runs on `git-store`, and the `Owed` line leaves
  - `manifest.yaml`: Done - `memory: work-records=git-store`
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the document, the cases, the code and the decisions; no `approved` is recorded

#### What changed
- `git-store.md` states what the adapter declares, its first configuration (one reference per class), the plumbing it uses, how it orders writers and recovers a lock a killed writer left, what it keeps outside the store's medium, the fallback, publishing, how it meets the suite, and what it cannot do.
- `git-store.py` holds the adapter, `bind`, the `Fallback` interface with its one implementation `NotFound`, `Lag`, `Publish`, and the command that prints a class's lag; `cases.py` holds the `fallback`, `working-tree` and `replicated` groups; `tests/git-store.py` runs them with the kernel suite, `lockable`'s group and `record`'s group.
- `git-store.handoff.md` holds the Tentative decisions the build took and two questions for the owner.

#### Considered and not done
- `commit-tree` and `mktree` for each batch: a process and a loose object each, where `fast-import` writes the same commit into the batch's one pack.
- Taking the project's `origin` as the shared store when none is named: it would publish work records to a host nobody chose.
- A `memar` verb for the lag: a route in `bundles/memar` and a name the owner gives; recorded as an open question.
- Coding the `replicated` group in the conformance module: its cases need a seam only an adapter with a shared store offers; it moves there when a second adapter declares the capability.

---

### The benchmark: what `git-store` costs, the bound on packs, and a bare tree's transfers
- Time: 2026-10-26T22:30:00Z
- Type: Added
- Cited:
  - [Memory Record Handoff](../record/record.handoff.md#decisions) - Reference: "A reference points to a commit per batch", which the numbers test
  - [Test Practice → Scaling](../../../../../modules/process/test/test.practice.md#scaling) - Reference: a benchmark's numbers live in one home
- Tasks:
  - main:.agents/tasks/20261026-T192807Z-36152/: Done - step 4 of task `20261023-T074642Z-5420`, part B
- Propagates to:
  - `modules-plugable/computer/memory/store/record/record.handoff.md`: Done - the decision on a commit per batch carries the measured bytes, and the Status names the view and the benchmark
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the procedure, ran it and recorded the numbers; no `approved` is recorded

#### What changed
- `git-store.research.001.md` records the benchmark: like for like against the baseline of task `20261020-T131910Z-22300`, 100,000 nodes, 10,000 single-write batches, and the bytes of a push and a fetch for a commit per batch and for a bare tree, in a folder Defender excludes and in one it does not.
- `services/_benchmark.py` is its procedure.
- `git-store.md` points to both; `git-store.handoff.md` keeps the pack bound as measured and records the saved index's write cost as anticipated work.

#### Considered and not done
- Measuring Defender's CPU and setting or reading its exclusion: both need elevation, which the run did not have; the command the owner can run elevated is in the research's Methodology.
- A bare-tree adapter: the variant is a second reference to the tree of the same state, which is all a transfer sees.

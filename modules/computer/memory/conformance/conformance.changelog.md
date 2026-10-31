# Memory Conformance Changelog

## Changelog

---

### The suite is coded, and the cases of the record contract that name no id, part or label moved here
- Time: 2026-10-26T15:02:00Z
- Type: Changed
- Cited:
  - [Memory Record](../../../../modules-plugable/computer/memory/store/record/record.md#the-contract-suite) - Reference: the first design's cases, written for ids
  - [Memory Store](../store/store.md#the-cases-this-module-owes) - Reference: the cases this contract adds and the groups owed elsewhere
  - [Test Practice](../../../process/test/test.practice.md#the-cycle) - Reference: the cases shown red on a stub of `volatile` before it was written
- Tasks:
  - main:.agents/tasks/20261026-T144222Z-11720/: Partial - every case that applies to `volatile` passes on its four instantiations; the `durable`, `shared` and two `lockable` cases are pending
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — restated the cases for addresses, wrote the runner and the cases, chose which half of a mixed case moved; no `approved` is recorded

#### What changed
- [`conformance.py`](conformance.py) holds the runner and the cases of the groups `core`, `dense`, `fixed-length`, `no-compare`, `durable`, `shared` and `model`, each a function whose docstring states it; the document says which cases are the contract's and why.
- The cases of `fallback` and `working-tree`, restated for addresses, are listed here until the adapter that declares them codes them.

#### Considered and not done
- Giving the half of a mixed case that stayed with `record` a name of its own: the halves keep the case's name.
- Coding the `lockable` group here: it is owed by the module that declares the capability, and runs through this runner.

---

### The `durable` and `shared` cases are no longer pending, and the adapter groups have their first home
- Time: 2026-10-26T19:45:00Z
- Type: Changed
- Cited:
  - [Test Practice → The Cycle](../../../../modules/process/test/test.practice.md#the-cycle) - Reference: when a pending Test passes, the mark leaves it in the same change
- Tasks:
  - main:.agents/tasks/20261026-T181945Z-16468/: Done - step 3 of task `20261023-T074642Z-5420`
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — ran the cases on `git-store` and removed the marks; no `approved` is recorded

#### What changed
- `conformance.py`: the eight cases of the `durable` and `shared` groups pass on `git-store` and carry `owed:memory.port.contract-suite` no longer; the module's docstring says so.
- `conformance.md`, "Groups": `fallback` and `working-tree` are coded first in `git-store`'s `cases.py`, which also codes the `replicated` group until a second adapter declares it.

---

### Memory Conformance: the groups and cases are linked, not listed
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - step S4d of the redo
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - reduced the document

#### What changed
- Removed from the Abstract: the description of `conformance.py`, its docstring-per-case and the runner `test_case`; new home `conformance-case.kh`, `conformance-runner.kh` and the other `conformance-*.kh`. Removed from "Groups": the sentences stating each fallback, held-only and working-tree case; they are the cases in `git-store/cases.py`, the kinds are `conformance-group-kinds.kh`. Kept: "Which cases are the contract's" and why each group is owed where it is.

---

### Memory Conformance: the group bullets are linked
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - second reduction of the remaining restatements
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - reduced the document

#### What changed
- Removed: the bullets restating the groups of the parameters and capabilities (now [`conformance-group-kinds.eng.kh`](conformance-group-kinds.eng.kh) and [`conformance-groups.eng.kh`](conformance-groups.eng.kh)).
- Kept: why `durable` and `shared` need the adapter to say how to open itself, why `volatile` is kernel and the reference, and why the optional groups are owed by their modules.

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

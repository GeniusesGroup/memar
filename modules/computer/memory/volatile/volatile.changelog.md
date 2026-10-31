# Memory Volatile Changelog

## Changelog

---

### The reference adapter is written
- Time: 2026-10-26T15:02:00Z
- Type: Added
- Cited:
  - [Memory Store](../store/store.md#the-contract) - Reference: the contract it realizes
  - [Memory Conformance](../conformance/conformance.md) - Reference: the suite it passes and is the model of
- Tasks:
  - main:.agents/tasks/20261026-T144222Z-11720/: Complete - `volatile.py` passes every case that applies to it, built four ways
- Contributors:
  - An AI agent (Claude, model claude-opus-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — wrote the adapter and its tests; no `approved` is recorded

#### What changed
- [`volatile.py`](volatile.py) keeps a store in the memory of the process, built with the parameters, the limits and the atomicity it is given, declaring no other capability; its docstring states its limits once.
- Its `tests/` run the suite on it sparse and dense, with fixed and any length, with and without compare-and-write, and check that every case no capability calls for runs on one of them.

#### Considered and not done
- Offering it to services as an in-process store: the question stays open in the memory handoff.

---

### Memory Volatile: the declarations are linked, not described
- Type: Changed
- Cited:
  - [Documentation Rule: A Document Restates No Code](../../../../modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md) - Reference: the rule the reduction applies
- Tasks:
  - main:.agents/tasks/20261026-T200842Z-21460/: Done - step S4d of the redo
- Contributors:
  - An AI agent (Claude, as reported by the runtime; no CONTRIBUTORS.md entry) - reduced the document

#### What changed
- Removed from the Abstract: the sentence that described what the docstring of `volatile.py` states (the parameters, limits and atomicity). Their new home is `volatile.kh`, `volatile-capabilities.kh` and `volatile-memory.kh`. Added: the refusal at build of a held range that dense and capacity disagree on, as an open point.

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

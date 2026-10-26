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

---
Title: "Memory Conformance"
Status: Draft
Start Date: 2026-10-26
ID: 498060
---

# Memory Conformance

## Abstract
The conformance suite is the decision procedure of the [store contract](../store/store.md): the stated inputs against which the contract's requirements are decided for an adapter, and the runner that applies them. It takes an adapter as input, runs the groups the adapter's declared capabilities call for (core by the three parameters of dense or sparse, fixed or any length, compare-and-write; durable; shared), and compares the adapter with the reference [Memory Volatile](../volatile/volatile.md) (the model group). It is a module of its own because it grows with every case the contract and its capabilities add while the store and `volatile` stay put, and because it needs `volatile`, which needs the store, so it cannot be the store's own `tests/`. The groups that belong to an optional capability (`fallback`, `working-tree`, `lockable`) are owed by the module that declares the capability and run through this runner; the cases that name an id, a part or a label are `record`'s.

The cases are code: [`conformance.py`](conformance.py) holds each as one function whose docstring states it, and the runner `test_case`, which an adapter's own `tests/` call with a function that makes a new, empty adapter; [`volatile/tests/volatile.py`](../volatile/tests/volatile.py) is the first, and `python modules/computer/memory/volatile/tests/volatile.py` runs it.

## Explanation

### Which cases are the contract's
The first design's suite was written for record ids ([Memory Record → The contract suite](../../../../modules-plugable/computer/memory/store/record/record.md#the-contract-suite)). A case moved here when what it checks can be stated with an address for a key and a value for a part and loses nothing: the answers of `get`, `list` and `batch`, the token, the expectations, the limits, atomicity, isolation, ordering and paging, durability and sharing, and the model. A case whose subject is the form of an id, the domain key, the parts of a node, its labels or `scan`, or an order of existence instants, stayed `record`'s and runs in `record`'s own tests through this runner; where a case checked both, the address half moved and the rest stayed. The cases this contract adds are those of `state`, `changes` and the three parameters. `changes-sees-other-process` needs a second process and is in the `shared` group.

### Groups
A group is named by what calls for it, and a case runs on an adapter only when its group applies and the store's parameters let it be stated (an `absent` expectation is not asked of a dense store, nor an expectation of a store that cannot compare and write, beyond the case that it is refused):
- `core`, for every adapter; `dense`, `fixed-length` and `no-compare`, for the instantiations those parameters name.
- `durable` and `shared`, for adapters declaring `durable` and `shared_between_processes`; their cases reach a child process, which opens the same adapter from what its `opener()` names.
- `model`, for every adapter: the same random sequence on the adapter and on [`volatile`](../volatile/volatile.md) built with its declarations.
- `lockable`, owed by its module ([`lockable.py`](../../../../modules-plugable/computer/memory/store/lockable/lockable.py)) and passed to the runner by an adapter's tests.
- `fallback` and `working-tree`, owed by the adapter that declares them and coded with it, with the seam that makes its shared store unreachable or hold given addresses: the first is [`git-store`'s `cases.py`](../../../../modules-plugable/computer/memory/store/git-store/cases.py), which also codes the group of `replicated` until a second adapter declares that capability. Restated for addresses from the first design, they are: `unavailable-is-not-absent`, with the shared store unreachable an address the adapter does not hold reads Unavailable and not Absent; `list-unavailable-is-not-short`, with part of the addresses unreachable a range that covers them answers Unavailable and one that does not answers completely; `held-only-updates`, with the held ranges set by the seam, an expectation of a value at an address outside them and a write to one are Unavailable as NotHeld, an `absent` expectation outside them is Unavailable as Unreachable until the shared store has answered, and inside them a creation commits without asking, and a batch with a stale expectation outside them is Unavailable and not Conflict; `fallback-not-found`, an address outside the held ranges that the shared store answers is not there reads Absent; `fallback-found`, an address the shared store holds reads Found with the shared store's value as of the asking, and a read after that value changed reads the new one; and `working-tree-unchanged`, after any sequence of the operations a listing of the project's working tree, its tracked files and its index are as they were.

A case whose group no adapter yet declares is pending, as [Memory Store → The cases this module owes](../store/store.md#the-cases-this-module-owes) says.

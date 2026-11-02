---
Title: "Memory Conformance"
Start Date: 2026-10-26
ID: 498060
---
# Memory Conformance

## Abstract
The conformance suite is the decision procedure of the [store contract](../store/store.md): the stated inputs against which the contract's requirements are decided for an adapter, and the runner that applies them. It takes an adapter as input, runs the groups the adapter's declared capabilities call for (core by the three parameters of dense or sparse, fixed or any length, compare-and-write; durable; shared), and compares the adapter with the reference [Memory Volatile](../volatile/volatile.md) (the model group). It is a module of its own because it grows with every case the contract and its capabilities add while the store and `volatile` stay put, and because it needs `volatile`, which needs the store, so it cannot be the store's own `tests/`. The groups that belong to an optional capability (`fallback`, `working-tree`, `lockable`) are owed by the module that declares the capability and run through this runner; the cases that name an id, a part or a label are `record`'s.

The cases are code and their shape is Khayyam: the case, the group, the group kinds, the verdict, the cost of a case (its time budget) and the runner are the `conformance-*.kh` files of this folder, for example [`conformance-case.kh`](conformance-case.kh), [`conformance-group-kinds.kh`](conformance-group-kinds.kh) and [`conformance-runner.kh`](conformance-runner.kh); [`conformance.py`](conformance.py) realizes them, and an adapter's own `tests/` call the runner with a function that makes a new, empty adapter ([`volatile/tests/volatile.py`](../volatile/tests/volatile.py) is the first).

## Explanation

### Which cases are the contract's
The first design's suite was written for record ids ([Memory Record → The contract suite](../../../../modules-plugable/computer/memory/store/record/record.md#the-contract-suite)). A case moved here when what it checks can be stated with an address for a key and a value for a part and loses nothing: the answers of `get`, `list` and `batch`, the token, the expectations, the limits, atomicity, isolation, ordering and paging, durability and sharing, and the model. A case whose subject is the form of an id, the domain key, the parts of a node, its labels or `scan`, or an order of existence instants, stayed `record`'s and runs in `record`'s own tests through this runner; where a case checked both, the address half moved and the rest stayed. The cases this contract adds are those of `state`, `changes` and the three parameters. `changes-sees-other-process` needs a second process and is in the `shared` group.

### Groups
A group is named by what calls for it, and a case runs on an adapter only when its group applies and the store's parameters let it be stated: an `absent` expectation is not asked of a dense store, nor an expectation of a store that cannot compare and write, beyond the case that it is refused. The kinds of group are [`conformance-group-kinds.kh`](conformance-group-kinds.kh) and the groups themselves [`conformance-groups.kh`](conformance-groups.kh). In words:
- The groups that follow the parameters and the declared capabilities are named in the files above. The cases of `durable` and `shared` reach a child process, which is why the adapter must say how to open itself there.
- `model` runs for every adapter against [`volatile`](../volatile/volatile.md), which is why `volatile` is kernel and is the reference.
- `lockable`, `fallback` and `working-tree` are owed by the module that declares the capability, which codes them with the seam its adapter offers: [`lockable`](../../../../modules-plugable/computer/memory/store/lockable/lockable.py) and, for the other two, [`git-store`'s cases](../../../../modules-plugable/computer/memory/store/git-store/cases.py), which also code the group of `replicated` until a second adapter declares that capability. Owing them there keeps this module from growing with every optional capability and from knowing a medium.

A case whose group no adapter yet declares is pending, as [Memory Store → The cases this module owes](../store/store.md#the-cases-this-module-owes) says.

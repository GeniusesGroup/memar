---
Title: "Memory Conformance"
Status: Draft
Start Date: 2026-10-26
ID: 498060
---

# Memory Conformance

## Abstract
The conformance suite is the decision procedure of the [store contract](../store/store.md): the stated inputs against which the contract's requirements are decided for an adapter, and the runner that applies them. It takes an adapter as input, runs the groups the adapter's declared capabilities call for (core by the three parameters of dense or sparse, fixed or any length, compare-and-write; durable; shared), and compares the adapter with the reference [Memory Volatile](../volatile/volatile.md) (the model group). It is a module of its own because it grows with every case the contract and its capabilities add while the store and `volatile` stay put, and because it needs `volatile`, which needs the store, so it cannot be the store's own `tests/`. The groups that belong to an optional capability (`fallback`, `working-tree`, `lockable`) are owed by the module that declares the capability and run through this runner; the cases that name an id, a part or a label are `record`'s.

The cases are specified in [Memory Store](../store/store.md#the-cases-this-module-owes) and, until the build task moves them, in [Memory Record → The contract suite](../../../../modules-plugable/computer/memory/store/record/record.md#the-contract-suite); they are coded by task `20261023-T074642Z-5420`.

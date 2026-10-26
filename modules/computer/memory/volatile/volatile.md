---
Title: "Memory Volatile"
Status: Draft
Start Date: 2026-10-26
ID: 498060
---

# Memory Volatile

## Abstract
`volatile` is the reference adapter of the [store contract](../store/store.md): a store that keeps its addresses and values in the memory of the process, address-generic, built with the limits and the parameters it is given. It is the executable form of the contract, the model against which [Memory Conformance](../conformance/conformance.md) compares every other adapter (`model-equivalence`), so a requirement of the contract that no input decides is found here as a case `volatile` cannot answer. It is kernel because the decision procedure of the contract is, and it depends only toward the foundation: on the store and the address. It is not the volatile memory of [Memory → Volatility](../memory.md#volatility-the-real-classifier), which is a classification of retention, and not the pair of the optional `nonvolatile` capability of the store.

It is [`volatile.py`](volatile.py), whose docstring states, once, what it declares: the parameters, the limits and the atomicity it is built with, and none of the other capabilities. Its own tests run the suite on it built four ways, sparse and dense, fixed and any length, with and without compare-and-write, so that every case no capability calls for runs on one of them. Whether `volatile` is also offered to services as an in-process store for use, beyond being the model, is open ([Memory Handoff](../memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative)).

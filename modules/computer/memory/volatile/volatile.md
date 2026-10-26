---
Title: "Memory Volatile"
Status: Draft
Start Date: 2026-10-26
ID: 498060
---

# Memory Volatile

## Abstract
`volatile` is the reference adapter of the [store contract](../store/store.md): a store that keeps its addresses and values in the memory of the process, address-generic, built with the limits and the parameters it is given. It is the executable form of the contract, the model against which [Memory Conformance](../conformance/conformance.md) compares every other adapter (`model-equivalence`), so a requirement of the contract that no input decides is found here as a case `volatile` cannot answer. It is kernel because the decision procedure of the contract is, and it depends only toward the foundation: on the store and the address. It is not the volatile memory of [Memory → Volatility](../memory.md#volatility-the-real-classifier), which is a classification of retention, and not the pair of the optional `nonvolatile` capability of the store.

Whether `volatile` is also offered to services as an in-process store for use, beyond being the model, is open ([Memory Handoff](../memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative)); the build task (`20261023-T074642Z-5420`) writes it.

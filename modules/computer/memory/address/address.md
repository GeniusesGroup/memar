---
Title: "Memory Address"
Status: Draft
Start Date: 2026-10-26
ID: 498060
---

# Memory Address

## Abstract
An **address** names a place that retains state: a byte string with equality and a total order, the byte order, whose kind and length are fixed by whoever instantiates it. It is the one thing a Task, a timeline or a Request needs in order to name a thing retained, and it is what a [store](../store/store.md) is keyed by. A position of a block, the 16-byte id and domain key of a record, a variable-length key and a path are kinds of address; each kind is a facet of the capsule that introduces it, and this module states only what every kind must be. The address is not a pointer: a pointer is a machine location with equivalence alone, and belongs with [references](../reference/protocol/reference.kh) (the `Memory_Pointer` and `MemoryAddress` declarations of `address/protocol/address.kh` and the address-sized integer ruled to memory on 2026-09-28 move there with the build of the contract, see [Memory Handoff](../memory.handoff.md#the-division-of-the-memory-contract-into-modules-2026-10-26-tentative)).

## Explanation
- **What every kind is.** A byte string; equality; a total order (the byte order); a fixed length or any length, declared by the kind. An address is a value: it carries no operation on the store.
- **What it is not.** It is not a position in volatile memory (`MemoryAddress` has equivalence only); volatile memory is an instance of a store when its positions are given an order.
- **Referring.** A document that only names a thing retained depends on this module. One that reads or writes it also depends on [Memory Store](../store/store.md), and on nothing of `record`, `file` or any adapter.

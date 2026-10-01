---
Title: "Abstract Data Types"
Status: Draft
Start Date: 2026-09-29
ID: "497411"
---

# Abstract Data Types

## Abstract
This document records what the repository already establishes about abstract data types: where the raw ADT protocols live, and how three reference-corpus shapes map to declared abstractions. It does not decide module placement or name every ADT protocol.

## Explanation

### Raw ADT protocols
Container, array, list, graph, hash table, queue, stack, and marker protocols are declared under [`modules/computer/adt/`](../../modules/computer/adt/).

### Established translations
- A dynamically sized ordered run — a slice in the reference corpus — is realized as `Array_Dynamic` ([`modules/computer/adt/array/protocol/dynamic.kh`](../../../modules/computer/adt/array/protocol/dynamic.kh)).
- An associative map is realized as `Array_Associative` ([`modules/computer/adt/array/protocol/associative.kh`](../../../modules/computer/adt/array/protocol/associative.kh)).
- The unconstrained element position in a raw ADT protocol is `Container_Element` only ([`modules/computer/adt/container/protocol/element.kh`](../../../modules/computer/adt/container/protocol/element.kh)); domain protocols take and return their own element types, not `Container_Element`.

Open questions on whether these declarations belong under `computer` or under `math` are tracked in the paired [handoff](../computer/adt.handoff.md).

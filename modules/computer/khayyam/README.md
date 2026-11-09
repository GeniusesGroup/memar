# Khayyam (`/modules/computer/khayyam/`)
This directory holds the design and specification documents of the **Khayyam programming language** — the language designed within Memar's design space so that source written in it already expresses the constraints Memar cares about. Its local realization is hosted in this repository under `modules/` (see [`modules/` → Where implementations live](../../README.md#where-implementations-live)). A document here answers "how does Khayyam realize X?" — neither "what is X?" (the concept documents in [Knowledge](../../knowledge/knowledge.md)) nor "what does *Memar's* module for X require?" (that module's own documents, under [`modules/`](../../README.md)).

These are base documents. Memar's modules are written in the language, and its grammar adopts no module's semantics ([Khayyam → The Grammar Refuses Protocol Semantics](./khayyam.md#the-grammar-refuses-protocol-semantics)), so the language stands below the modules. They have a folder of their own because they share one subject, the language, not because they are a layer of their own.

## Membership criterion
A document belongs here when it specifies a construct or concern of the Khayyam language itself — its grammar and syntax, and the design decisions and open questions behind its constructs. Compiler, linter, and runtime are not Khayyam's to specify: they are Memar's modules of those names in [`modules/`](../../README.md), written in the language and standing above it. Documents enter at whatever [Status](../../../modules-plugable/knowledge/documentation/explanation/explanation.md#labels) they carry, including Draft, and are developed here in place.

What does **not** belong here:
- **Concept documents** (System, Type, Modeling, ...) — general concepts stay in their knowledge modules. A concept's definition is owned there even when Khayyam is its first realization; Type's four categories are the standing example, defined in [Type](../type/type.md) and realized here as the `cp`/`mt`/`ab`/`sc` subtypes.
- **Module documents** — Memar's module contracts, which bind every realization whatever its language ([Framework → Khayyam and Other Languages](../../knowledge/framework/framework.md#khayyam-and-other-languages)), stay with their modules in [`modules/`](../../README.md). The direction runs one way: a module is written in Khayyam and cites the language down; no module's specification lives here.

## Citation direction
The documents themselves are not listed here — the folder listing is the index. This file only states the folder's role and criterion, which do not change when documents are added.

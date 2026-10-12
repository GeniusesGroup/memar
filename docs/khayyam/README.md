# Khayyam (`/docs/khayyam/`)
This directory holds the design and specification documents of the **Khayyam programming language** — the language designed within Memar's design space so that source written in it already expresses the constraints Memar cares about. Its local realization is hosted in this repository under `modules/` (see [`docs/modules/` → Where implementations live](../modules/README.md#where-implementations-live)). A document here answers "how does Khayyam realize X?" — neither "what is X?" (the concept documents at [`docs/` root](../README.md)) nor "what does *Memar's* module for X require?" ([`docs/modules/`](../modules/README.md)).

The language's weight in Memar's development approach is not what gives these documents their own folder. Layering is about what *kind of claim* a document makes, not about a document's importance: these documents make realization claims, and that kind needed its own home the same way the module layer did.

## Membership criterion
A document belongs here when it specifies a construct or concern of the Khayyam language itself — its grammar and syntax, and the design decisions and open questions behind its constructs. Compiler, linter, and runtime are not Khayyam's to specify: they are modules in [`docs/modules/`](../modules/README.md) whose protocols a Khayyam realization consumes. Documents enter at whatever [Status](../documentation-explanation.md#status) they carry, including Draft, and are developed here in place.

What does **not** belong here:
- **Concept documents** (System, Type, Modeling, ...) — general concepts stay at `docs/` root. A concept's definition is owned there even when Khayyam is its first realization; Type's four categories are the standing example, defined in [Type](../type.md) and realized here as the `cp`/`mt`/`ab`/`sc` subtypes.
- **Module documents** — Memar's language-independent contracts stay in [`docs/modules/`](../modules/README.md). The conformance direction runs one way: Khayyam realizes and consumes protocols; no module's specification lives here.

## Citation direction
A citation runs down the layers of the written content, never up, as [Documentation → Citation Direction](../documentation.md#citation-direction) states once for every layer.

The documents themselves are not listed here — the folder listing is the index. This file only states the folder's role and criterion, which do not change when documents are added.

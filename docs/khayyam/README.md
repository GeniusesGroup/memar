# Khayyam (`/docs/khayyam/`)
This directory holds the design and specification documents of the **Khayyam programming language** — the language designed within Memar's design space so that source written in it already expresses the constraints Memar cares about (one of Memar's language realizations; see [`protocols/` → Implementation repositories](../protocols/README.md#where-implementations-live)). A document here answers "how does Khayyam realize X?" — neither "what is X?" (the concept documents at [`docs/` root](../README.md)) nor "what is *Memar's* protocol for X?" ([`protocols/`](../protocols/README.md)).

The language's weight in Memar's development approach is not what gives these documents their own folder. Layering is about what *kind of claim* a document makes, not about a document's importance: these documents make realization claims, and that kind needed its own home the same way the protocol layer did.

## Membership criterion
A document belongs here when it specifies a construct or concern of the Khayyam language itself — its grammar and syntax, and the design decisions and open questions behind its constructs. Compiler, linter, and runtime are not Khayyam's to specify: they are protocols in [`protocols/`](../protocols/README.md) that a Khayyam realization consumes. Documents enter at whatever [Status](../documentation-explanation.md#status) they carry, including Draft, and are developed here in place.

What does **not** belong here:
- **Concept documents** (System, Type, Modeling, ...) — general concepts stay at `docs/` root. A concept's definition is owned there even when Khayyam is its first realization; Type's four categories are the standing example, defined in [Type](../type.md) and realized here as the `cp`/`mt`/`ab`/`sc` subtypes.
- **Protocol documents** — Memar's language-independent contracts stay in [`protocols/`](../protocols/README.md). The conformance direction runs one way: Khayyam realizes and consumes protocols; no protocol's specification lives here.

## Citation direction
The layering carries the same citation rule the protocols layer states for itself: citations run **down** — from a document here to the base document whose principle it applies, and to a protocol document whose contract it consumes. A base document never cites a document here as the authority for its own principles: a general principle the base layer needs is stated at the base layer, and the document here cites it upward. What remains legitimate in the upward direction is the **instance pointer** — a base document may name Khayyam as the place its principles are first realized, as [Type → Manifestation in Khayyam](../type.md#manifestation-in-khayyam) does — without deriving anything from the realization.

The documents themselves are not listed here — the folder listing is the index. This file only states the folder's role and criterion, which do not change when documents are added.

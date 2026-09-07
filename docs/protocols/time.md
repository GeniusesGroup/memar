---
Title: "Time"
Status: Draft
Start Date: 2026-09-06
ID: 496871
---

# Time

## Abstract
This document opens Memar's treatment of time as a framework concern, starting from a deliberately small position: **time is a concept, and its framework-level presence should be interface-shaped — a small contract about measurement and ordering — not a package-shaped bundle of everything an ecosystem has historically piled onto the name.** The broader ecosystem's "standard time library" bundles at least four separable concerns (instant representation, duration arithmetic, calendar/civil conversion, formatting/parsing) behind one type, and every one of them leaks into APIs that only needed one of them. This document records the position, the separation it demands, and the questions that must be settled before Memar defines its own representation — including a definitional question most engineering treatments skip: what *is* time, for a system that must use it?

## Introduction

### Motivation
Two sources motivated this document. The practical source: years of observing that APIs which accept or return a "Time" type acquire dependencies on parsing, locale, and calendar machinery they do not use, and that the type's mutability or pointer semantics propagate into cost questions (pointer-mediated mutation paying an indirection on every read) that have nothing to do with time itself. The deeper source is a question the project keeps returning to in its conceptual discussions: the *definition* of time is unsettled even in the sciences that use it most precisely, and a framework that treats "time" as one indivisible primitive inherits every unresolved philosophical and engineering argument bundled into that single word. Separating the concerns is what makes the arguments tractable.

### Methodology
This is an opening Draft: it records the position and the separation, keeps the representation questions genuinely open, and does not specify syntax or types. The definitional discussion draws on the project's own recorded discussions of measurement and observation (see [modeling](../modeling.md) and [system](../system.md) for the observer-position treatment this document assumes rather than repeats).

## Explanation

### The four separable concerns
What ecosystems bundle as "time" separates into four concerns with different shapes and different consumers:

1. **Instant** — a point on a shared reference timeline: the measurement concern. Its contract is comparison and ordering; everything else is optional.
2. **Duration** — a measured or specified span. Its contract is arithmetic against instants and other durations.
3. **Civil conversion** — mapping instants to and from human calendar conventions (dates, zones, local-time rules). Its contract is inherently political and historical: zone databases change by legislation, and an API that treats conversion as timeless embeds a frozen snapshot of human agreement.
4. **Formatting and parsing** — textual representation for humans and wire formats. A presentation concern, adjacent to but distinct from the [Error protocol](./error.md)'s rule that display text is resolved per audience at the ends, not carried in the middle.

An API that needs "when did this happen?" should be able to depend on the Instant contract alone. Bundling the four behind one type is why ecosystem code that merely orders events transitively depends on timezone databases and format tables. Memar's rule: the concerns are separate abstractions, and a component depends on exactly the ones it uses.

### Immutability and value semantics
Consistent with [Memory](./memory.md)'s contract rules: an instant is a value with fixed identity-by-content, not a mutable object behind a pointer. The observed ecosystem failure — mutable time values requiring pointer mediation and paying indirection on every read, or being defensively copied to prevent shared mutation — is a contract-design failure this document rules out in advance: time values do not mutate; the world they measure does, and later observations are new values, not mutations of old ones.

### The definitional question, kept open
What time *is* — whether it is a fundamental dimension of the systems being modeled, an emergent ordering of events, or an observer-relative measurement — is a question this document deliberately does not answer. What it does answer is the engineering consequence of not answering it: because the definition is unsettled, Memar's abstractions must not hard-code a metaphysics. The Instant/Duration contracts above are stated in terms of *ordering and comparison* — the minimal commitments any of the candidate definitions support — and richer semantics (causality, simultaneity across distributed components, monotonicity guarantees) are treated as separate questions for [networking](./networking.md) and [process](../process.md), not smuggled into the time contract.

The separation direction is visible across the ecosystem: language runtimes that grew a second, monotonic clock alongside their civil-clock type after real-world clock-smearing failures; the split between timestamp representations and calendar libraries in systems programming; and distributed-systems literature's careful distinction between physical-clock time and event ordering (Lamport and after) — the strongest evidence that "time" is more than one concern and that ordering is the part systems can actually depend on.

## Results
Insufficient time has passed (see the definitional question) to report outcomes. This document is a positional Draft expected to grow or to be absorbed once the representation questions settle.

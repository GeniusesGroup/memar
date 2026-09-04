---
Title: "Control Flow"
Status: Draft
Start Date: 2026-06-30
ID: 495215
---

# Control Flow

## Abstract
This document is the framework-level home for Memar's control-flow protocol: the rules governing how execution changes course in systems built with Memar, independent of any language. Khayyam's control-flow document establishes *why* the language ships no branching, looping, or exception syntax — library-driven conditionals over built-in keywords — and treats the deeper treatment as belonging to a framework-level document; this document is that home. It records the naming convention for domain-specific conditional method pairs (two etymologically distinct roots rather than base-plus-negation), the open design questions on the standard success/failure branching pair, and the topics still to be developed here: the conditional-pair protocol as an abstraction contract, loop- and iteration-shaped control flow, and halting semantics.

## Introduction

### Motivation
[Khayyam control flow](../khayyam-control_flow.md) confirmed that `IF`/`ELSE` are only a generic default, and that developers should prefer domain-specific conditional methods whose name expresses the actual condition (e.g. for branching on an `Error` value, instead of `IF(err.IsNull(), ...)`). That document answers the language-level question — why the grammar contains none of these mechanisms. A framework-level protocol layer remains above it: what rules a conditional pair must satisfy to be a well-formed protocol participant, what the standard library's success/failure branching pair should be named and where it should live, and how control flow behaves across boundary crossings where no language mechanism exists. Naming such pairs carelessly carries real readability risk: an antonym pair built by negation-prefix, such as `IfErrorOccurred`/`IfErrorNotOccurred`, is dangerously easy to misread, since the `Not`/no-`Not` difference is visually subtle both for a human skimming a diff and for an AI assistant reading code quickly.

## Explanation

### Two etymologically distinct roots, not base-plus-negation
For conditional pairs in general, prefer two etymologically distinct roots over a base term plus its negation — e.g. `Failed`/`Succeeded`-style pairs rather than `X`/`NotX`-style pairs. This makes each branch immediately, visually distinguishable rather than requiring the reader to notice a single added/missing word.

### Candidates for the success/failure branching pair
For the specific, very common case of branching on an `Error` value's success or failure, several naming and placement directions were explored during design discussion but none has been finalized. Not yet finalized — pending resolution of the [Unresolved questions](#unresolved-questions) below.

- `IfErrorOccurred`/`IfErrorNotOccurred` — rejected for the negation-prefix readability risk above.
- `IfFailed`/`IfSucceeded` as global, package-less functions — rejected because Khayyam has no package/namespace concept (document #0013), so a global function name carries no inherent domain context; it is unclear from the name alone what is being checked for failure/success without an explicit receiver.
- `storageErr.OnFailure(...)` / `storageErr.OnSuccess(...)` as instance methods on the `Error` value itself — closer to Khayyam's Uniform Invocation Syntax (the receiver supplies the missing domain context that a global function lacks), but raises a deeper, still-unresolved semantic question (see [Unresolved questions](#unresolved-questions) below): is it correct for an `Error` — whose identity already represents failure — to also expose an "on success" branch, or does this actually belong on a more general, shared abstraction instead?
- `storageErr.OnPresent(...)` / `storageErr.OnAbsent(...)` — a candidate built around the *existing* `IsNull()`/"Behavioral Nullability" abstraction already present in the language ([Memory Model](../khayyam-memory_model.md) nullability discussion), framed neutrally around "does a value exist" rather than "did the business operation succeed." This was proposed as a way to let the same method pair work naturally both for `Error` (`OnAbsent` = "no error occurred") and for any other presence/absence-style capsule (e.g. an optional search result), but it has not been confirmed as final.

### Topics to be developed here
The language-level rationale lives in [Khayyam control flow](../khayyam-control_flow.md); this document is expected to grow into the framework-level protocol over its subject. Planned topics, each to be added as it is actually designed rather than pre-registered in detail:

- **The conditional-pair protocol** — the contract a well-formed conditional method pair must satisfy: how the condition is evaluated, whether the two branches are symmetric, how the receiver's state is read, and how the pair relates to the presence/absence abstraction family.
- **Iteration and loop-shaped control flow** — the same library-driven treatment applied to repetition, where the condition lives.
- **Halting semantics** — abrupt control transfer (`PANIC()`-family behavior) as an ordinary method call, its contract, and its relationship to error propagation ([The Error](./error.md)).

## Results
Insufficient time has passed since this protocol question was opened to report real, observed outcomes. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
Any chosen pair adds two more standard method names developers must learn and use correctly across the entire `Error`-adjacent surface of the standard library; getting the abstraction placement wrong (see [Unresolved questions](#unresolved-questions)) risks duplicate, slightly-divergent implementations across many capsules.

### Prior art
This problem closely parallels `Result`/`Option` combinator naming in Rust (`.is_ok()`, `.map_err()`, `.unwrap_or_else()`) and JavaScript Promise's `.then()`/`.catch()` pairing, both of which were considered as background context but not adopted directly, since Khayyam has neither a generic `Result<T, E>` type ([Khayyam polymorphism](../khayyam-polymorphism.md)) nor Promise-style chaining (document #0004 rejects expression chaining).

### Unresolved questions
1. Should the eventual success/failure (or presence/absence) method pair live directly on the `Error` abstraction, or on a more general, shared underlying abstraction that `Error` merely implements alongside other nullable/container-like capsules (the same abstraction `IsNull()` already belongs to)? Asking an `Error` — whose identity already represents failure — "what to do on success" may be semantically backwards; this may be a sign the pair belongs one level up, on the shared abstraction, with `Error` only inheriting it.
2. No final naming choice has been made between `OnFailure`/`OnSuccess` and `OnPresent`/`OnAbsent`, or any other candidate.
3. If a shared abstraction approach (point 1) is chosen, how does this interact with RFC 0017's rejection of default implementations? Each implementing capsule would need its own Explicit Delegation Verification line to a shared internal implementation, to avoid duplicating the same check logic across every implementer without resorting to inheritance.

### Future possibilities
Once finalized, this document's resulting abstraction and naming convention should be cross-referenced from [The Error](./error.md) as the recommended standard pattern for branching on a returned error.

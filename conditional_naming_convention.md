---
RFC Number: 000020
Title: "Conditional Method Naming Convention (Presence/Absence Pattern)"
Status: Draft
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000003", "000009"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
This RFC addresses two related, still-open design questions about Khayyam's library-driven conditionals (RFC 0003): (1) what naming convention should govern domain-specific conditional method pairs in general, and (2) what the standard library's success/failure branching pair specifically should be named and where it should live.

## Motivation
RFC 0003 confirmed that `IF`/`ELSE` are only a generic default, and that developers should prefer domain-specific conditional methods whose name expresses the actual condition (e.g. for branching on an `Error` value, instead of `IF(err.IsNull(), ...)`). However, naming such pairs carelessly can reintroduce real readability risk: an antonym pair built by negation-prefix, such as `IfErrorOccurred`/`IfErrorNotOccurred`, is dangerously easy to misread, since the `Not`/no-`Not` difference is visually subtle both for a human skimming a diff and for an AI assistant reading code quickly.

## Guide-level explanation
For conditional pairs in general, prefer two etymologically distinct roots over a base term plus its negation — e.g. `Failed`/`Succeeded`-style pairs rather than `X`/`NotX`-style pairs. This makes each branch immediately, visually distinguishable rather than requiring the reader to notice a single added/missing word.

For the specific, very common case of branching on an `Error` value's success or failure, several naming and placement directions were explored during design discussion but none has been finalized:

- `IfErrorOccurred`/`IfErrorNotOccurred` — rejected for the negation-prefix readability risk above.
- `IfFailed`/`IfSucceeded` as global, package-less functions — rejected because Khayyam has no package/namespace concept (RFC 0013), so a global function name carries no inherent domain context; it is unclear from the name alone what is being checked for failure/success without an explicit receiver.
- `storageErr.OnFailure(...)` / `storageErr.OnSuccess(...)` as instance methods on the `Error` value itself — closer to Khayyam's Uniform Invocation Syntax (the receiver supplies the missing domain context that a global function lacks), but raises a deeper, still-unresolved semantic question (see Unresolved questions below): is it correct for an `Error` — whose identity already represents failure — to also expose an "on success" branch, or does this actually belong on a more general, shared abstraction instead?
- `storageErr.OnPresent(...)` / `storageErr.OnAbsent(...)` — a candidate built around the *existing* `IsNull()`/"Behavioral Nullability" abstraction already present in the language (RFC 0008's nullability discussion), framed neutrally around "does a value exist" rather than "did the business operation succeed." This was proposed as a way to let the same method pair work naturally both for `Error` (`OnAbsent` = "no error occurred") and for any other presence/absence-style capsule (e.g. an optional search result), but it has not been confirmed as final.

## Reference-level explanation
Not yet finalized — pending resolution of the unresolved questions below.

## Drawbacks
Any chosen pair adds two more standard method names developers must learn and use correctly across the entire `Error`-adjacent surface of the standard library; getting the abstraction placement wrong (Section "Unresolved questions" below) risks duplicate, slightly-divergent implementations across many capsules.

## Rationale and alternatives
See Guide-level explanation above for the specific alternatives already considered and the reasons each was set aside (or left open) so far.

## Prior art
This problem closely parallels `Result`/`Option` combinator naming in Rust (`.is_ok()`, `.map_err()`, `.unwrap_or_else()`) and JavaScript Promise's `.then()`/`.catch()` pairing, both of which were considered as background context but not adopted directly, since Khayyam has neither a generic `Result<T, E>` type (RFC 0007 rejects generics) nor Promise-style chaining (RFC 0004 rejects expression chaining).

## Unresolved questions
1. Should the eventual success/failure (or presence/absence) method pair live directly on the `Error` abstraction, or on a more general, shared underlying abstraction that `Error` merely implements alongside other nullable/container-like capsules (the same abstraction `IsNull()` already belongs to)? Asking an `Error` — whose identity already represents failure — "what to do on success" may be semantically backwards; this may be a sign the pair belongs one level up, on the shared abstraction, with `Error` only inheriting it.
2. No final naming choice has been made between `OnFailure`/`OnSuccess` and `OnPresent`/`OnAbsent`, or any other candidate.
3. If a shared abstraction approach (point 1) is chosen, how does this interact with RFC 0017's rejection of default implementations? Each implementing capsule would need its own Explicit Delegation Verification line to a shared internal implementation, to avoid duplicating the same check logic across every implementer without resorting to inheritance.

## Future possibilities
Once finalized, this RFC's resulting abstraction and naming convention should be cross-referenced from RFC 0009 (Error Handling) as the recommended standard pattern for branching on a returned error.

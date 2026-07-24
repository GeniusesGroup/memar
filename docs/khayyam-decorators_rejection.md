---
RFC Number: 000021
Title: "Decorators Rejection"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002", "000017"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam has no decorator syntax (Python's `@decorator`, TypeScript/Java-style annotations that wrap or modify a method's behavior). Any cross-cutting behavior a decorator would normally provide (logging, caching, retry logic) must be expressed as explicit, visible composition — typically by the caller explicitly invoking the cross-cutting behavior itself — rather than an attribute silently wrapping the original method.

## Motivation
Decorators silently alter what a method actually does at the call site without that alteration being visible in the call itself — a function annotated `@retry` or `@cached` behaves completely differently from its plain signature, and a reader must separately know to look for and understand the decorator's implementation. This is in direct tension with Khayyam's broader principle that nothing about a method's runtime behavior should be hidden from its declaration and call sites (RFC 0002, RFC 0005, RFC 0009).

## Guide-level explanation
Where another language would write `@retry(times=3) func fetchData()`, a Khayyam developer instead explicitly composes the retry behavior at the call site or within an explicitly named wrapping capsule, so that the retry logic is visibly present in the source rather than silently injected by an annotation.

## Reference-level explanation
There is no decorator/annotation syntax in the grammar capable of wrapping or altering a method's behavior. Any equivalent functionality must be built from ordinary capsules and explicit method calls.

## Drawbacks
Common cross-cutting concerns (retry, caching, timing/logging wrappers) that a decorator would express in a single line require explicit, repeated composition at every relevant call site or an explicitly named wrapping capsule, which is more verbose than the decorator-based equivalent in other languages.

## Rationale and alternatives
Decorator/annotation syntax (Python, TypeScript, Java, C#) was rejected because it lets a method's effective runtime behavior diverge silently from what its declaration shows — directly conflicting with Khayyam's explicitness principle.

## Prior art
Python decorators and Java/C# annotations are the primary prior art being rejected here. Languages without a decorator mechanism (C, Go) instead rely on explicit wrapper functions/structs for the same cross-cutting needs, which is closer to Khayyam's chosen approach.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.

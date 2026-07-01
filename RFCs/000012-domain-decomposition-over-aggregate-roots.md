---
RFC Number: 000012
Title: "Domain Decomposition over Aggregate-Root Modeling"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002", "000007"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Memar rejects the conventional DDD pattern where a domain "owner" entity (e.g. `User`) directly contains and owns sub-concerns like `username`, `email`, or `password` as its own fields/methods. Instead, each such concern is modeled as its own independent capsule, and any "User"-like concept is just one possible *aggregator* among several — aggregators are not fixed, singular, or domain-owned; they commonly form at the composition layer (GUI widgets/pages), though they are not limited to that layer.

## Motivation
The traditional aggregate-root pattern assumes a single, stable owning entity for a cluster of related data, but real systems frequently need different aggregations of the same underlying concerns depending on context. A canonical example: identity resolved via a local registration form needs a different aggregation shape than identity resolved via a third-party OAuth provider (e.g. Google login) — a single fixed `User` aggregator forces both flows into one shape that fits neither well, and tempts the owning entity to absorb logic (like credential validation) that does not actually belong to it.

## Guide-level explanation
`username`, `email`, and similar concerns are modeled as independent, self-contained capsules with their own validation and behavior. A composition-layer construct (typically a GUI widget or page, though this is the common case, not the only one) assembles whichever subset of these independent capsules a specific use case actually needs, and is responsible only for that assembly — not for absorbing the internal logic of the concerns it aggregates. Per RFC 0004's decomposition-signal principle, if an aggregator's body starts doing more than its one named responsibility (e.g. a "register comment" widget that also resolves "who is the current user"), that is the signal to split out a separate, dedicated widget (e.g. one that returns only an `ActiveUserID`), pushing that sub-concern's own validation and error-handling down into that separate widget rather than leaving it in the original caller.

## Reference-level explanation
There is no language-level "aggregate root" or "entity" construct distinct from an ordinary capsule. Any capsule that happens to compose several other capsules is, structurally, just another capsule — its role as an "aggregator" is a naming/architectural convention applied by the developer, not a special grammar feature.

## Drawbacks
Without a single canonical owning entity, code that needs "the whole picture" of a concept like a user must always go through some composition-layer construct rather than a direct, centrally-defined object — this can mean more indirection to assemble a complete view, and requires discipline to avoid quietly re-inventing a de facto aggregate root inside a frequently reused widget.

## Rationale and alternatives
The classical DDD aggregate-root pattern (a single, owning entity directly containing related sub-concerns) was rejected because, in practice, it tends to pull unrelated validation and identity logic into one type, and breaks down whenever a concept (like "the current user") genuinely has more than one valid shape depending on context (local form vs. OAuth-resolved identity).

## Prior art
This is closely related to, but distinct from, established critiques of Anemic/God-object Aggregate Roots within the DDD community itself; it also resonates with component-composition patterns common in modern frontend frameworks, where a "page" or "widget" composes several independent, narrowly-scoped pieces of state rather than a single monolithic model object.

## Unresolved questions
None at this time.

## Future possibilities
None recorded yet.

---
RFC Number: 0000
Title: "Composition Depth as a Decomposition Signal (No Expression Chaining)"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000001"]
  Extends: ["000003"]
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam method calls are statements, not chainable expressions (`a.Foo().Bar()` is not legal syntax). Every intermediate result requires an explicitly declared, named variable. A method or widget body that accumulates many such named steps is treated as a deliberate design signal calling for further decomposition, not a cost to optimize away with chaining syntax.

## Motivation
In nearly every mainstream language, the ability to chain method calls or pass one call's result directly into another is taken for granted. But this convenience also lets multiple distinct responsibilities silently accumulate inside a single function body or expression without any forcing function to notice. Khayyam treats the resulting verbosity as intentional: a method/widget that needs many named intermediate steps to do its job is very likely doing more than one job.

## Guide-level explanation
When a developer notices a method or widget accumulating multiple unrelated named steps — for example, a "register comment" widget that both resolves "who is the active user" *and* validates/saves the comment — this is the language pushing back against an under-decomposed model, not a syntax limitation to work around. The correct response is always further decomposition: split out a separate widget/capsule with its own narrow responsibility and its own error boundary (e.g. a dedicated widget that returns only an `ActiveUserID`), never a request for implicit chaining syntax.

This applies uniformly, including to things that *feel* like a single operation — for example a `parse → validate → transform → aggregate` data pipeline. Each stage is a distinct concern with its own failure mode and reuse potential, and Khayyam intentionally provides no syntactic shortcut letting these stages collapse into one undifferentiated block.

## Reference-level explanation
Because every method's outputs are written into pre-declared variables passed by reference (not returned as an expression value), there is no syntactic slot in the grammar for one call's result to be fed directly as another call's input. The verbosity of named intermediate steps is the price paid for forcing this discipline to be visible directly in the source, rather than living only in a developer's head or a comment.

## Drawbacks
Even a simple, genuinely single-purpose sequence (e.g. a three-step pure math calculation) requires multiple named temporary variables, which can read as noisier than an equivalent one-line chained expression in other languages, especially for short-lived, never-reused intermediate values.

## Rationale and alternatives
Allowing expression-level chaining (as virtually all modern languages do) was rejected because it removes the friction that currently makes over-large method/widget bodies visible and uncomfortable — without that friction, the language would have no organic pressure toward decomposition, relying entirely on developer discipline or external linting to catch the same problem after the fact.

## Prior art
Go and Rust both support method chaining freely; this is treated as the default in modern language design, which makes Khayyam's rejection here a deliberate, atypical choice rather than an oversight.

## Unresolved questions
None at this time. (An earlier concern — whether this rule could be misapplied to single-responsibility pipelines that only *look* like several operations — was resolved: it applies uniformly, since each pipeline stage genuinely is a distinct concern with its own failure mode.)

## Future possibilities
None recorded yet.

---
RFC Number: 495369
Title: "Immutable Infrastructure as a Memar Foundation"
Status: Draft
Start Date: 2026-07-06
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Contributor(s):
  - name: "Omid Hekayati"
    uri: "mailto:omid@geniuses.group"
    contribution: ""
    task: []
  - name: "Claude"
    uri: "https://claude.ai"
    model: "claude-sonnet-5"
    effort: "Medium - extended thinking enabled"
    contribution: "Recorded the concept as raised in conversation to preserve it for a dedicated future deep-dive; content intentionally left minimal"
    task: []
---

## Summary
Memar treats deployed infrastructure as immutable: any change to configuration is a change to the artifact itself, requiring a rebuild/recompile, rather than a runtime-interpreted change to an already-running instance. This is proposed as a foundational Memar principle (not specific to Khayyam), though Khayyam's compiler is expected to benefit from it directly — for example, by potentially reducing or eliminating the need for runtime profile-guided optimization in cases where configuration-driven behavior can instead be resolved at compile time.

## Motivation
(Deferred to dedicated future discussion. Raised here only to avoid losing the idea before that discussion happens.)
- talk more about unikernel that almost base on immutable infrastructure
- A closely related principle, raised in discussion and worth recording alongside immutable infrastructure itself: no logic or code may be added to a running Memar application at runtime — every capability increase must go through recompilation. This is treated as the same governance concern as "what code can be added to a repository," addressed once rather than duplicated across two separate control points (source review and a runtime-loading mechanism). Whether a narrow, explicitly pre-compiled emergency shutoff path (e.g. disabling an already-known feature, as opposed to adding new logic) is compatible with this principle, or itself needs to be treated as an exception requiring its own RFC, is an open question for the dedicated future discussion this file already defers to.

## Guide-level explanation
(Deferred.)

## Reference-level explanation
(Deferred.)

## Drawbacks
(Deferred.)

## Rationale and alternatives
(Deferred.)

## Prior art
(Deferred — likely candidates to research include immutable infrastructure practices in ops/deployment tooling (e.g. container image rebuilds instead of in-place config mutation), and their relationship, if any, to compile-time vs. runtime specialization in compilers.)

## Unresolved questions
- Full scope and definition of "immutable infrastructure" within Memar has not yet been discussed in depth; this file is a placeholder pending a dedicated session.
- Whether immutable infrastructure removes the need for Profile-Guided Optimization in the Khayyam compiler entirely, or only for a subset of currently PGO-addressed cases (e.g. configuration-driven behavior, as opposed to per-request/per-connection runtime-data-driven behavior), is unresolved and disputed — see the open dispatch-resolution question in [memar-go generics elimination RFC].

## Future possibilities
- Dedicated session to define immutable infrastructure's relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning.
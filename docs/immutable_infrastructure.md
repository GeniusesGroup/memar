---
Title: "Immutable Infrastructure as a Memar Foundation"
Status: Draft
Start Date: 2026-07-06
ID: 495370
---

# Immutable Infrastructure as a Memar Foundation

## Abstract
Memar treats deployed infrastructure as immutable: any change to configuration is a change to the artifact itself, requiring a rebuild/recompile, rather than a runtime-interpreted change to an already-running instance. A closely related governance rule forbids adding logic or code to a running application at runtime — every capability increase must go through recompilation, addressed once as "what code may enter the repository" rather than duplicated across source review and a separate runtime-loading mechanism. The principle is proposed as a Memar foundation (not specific to Khayyam), with Khayyam's compiler expected to benefit directly — potentially reducing or eliminating the need for runtime profile-guided optimization wherever configuration-driven behavior can instead be resolved at compile time. The document also records what that speed alone does not settle — an emergency-halt design thread and a connection-continuity thread — and its relationship of convergence without interdependence to [Type](./type.md)-level identity.

## Introduction

### Motivation
(Deferred to the dedicated future discussion. Raised here only to avoid losing the idea before that discussion happens.) Unikernels deserve particular attention in that discussion, being almost by construction based on immutable infrastructure.

### Methodology
This document was recorded minimally and deliberately: the concept was raised in conversation and written down only to preserve it for a dedicated future session, not designed inline. Since recording, it has grown exclusively by absorbing relationship analyses and open-question notes — the Type-identity relationship from the dissolved *Static Concepts Must Be Types* document, and the emergency-halt and connection-continuity threads from a working context note — rather than by forward design. Full scope definition, drawbacks, and alternatives analysis remain owed to the dedicated session.

## Explanation

### The Principle
Memar treats deployed infrastructure as immutable: any change to configuration is a change to the artifact itself, requiring a rebuild/recompile, rather than a runtime-interpreted change to an already-running instance. This is proposed as a foundational Memar principle (not specific to Khayyam), though Khayyam's compiler is expected to benefit from it directly — for example, by potentially reducing or eliminating the need for runtime profile-guided optimization in cases where configuration-driven behavior can instead be resolved at compile time.

A closely related principle, raised in discussion and worth recording alongside immutable infrastructure itself: no logic or code may be added to a running Memar application at runtime — every capability increase must go through recompilation. This is treated as the same governance concern as "what code can be added to a repository," addressed once (through source review) rather than duplicated across two separate control points (source review and a runtime-loading mechanism). Whether a narrow, explicitly pre-compiled emergency shutoff path (e.g. disabling an already-known feature, as opposed to adding new logic) is compatible with this rule, or itself needs to be treated as an exception requiring its own document, is an open question — developed further as the God-halt proposal under [Open Design Threads](#open-design-threads) below.

### Open Design Threads
Sub-minute unikernel image rebuild+redeploy was proposed as sufficient to remove the practical need for Erlang/BEAM-style hot code swapping. The two threads below record what that speed alone does not settle; they are preserved from a context note so the reasoning survives until the dedicated session. Nothing here is designed or decided yet.

#### Emergency halt ("God-halt") service
For reaction times faster than even a sub-minute redeploy (down to network-speed reaction), a dedicated, pre-compiled monitoring service that can halt all processes system-wide until re-authorized was proposed. This is **not** an exception to this document's governance rule — it selects between pre-compiled run/halt paths based on a runtime signal; it does not inject new code. Needs dedicated design for:

- Where this service lives in the graph model (Code vs. Rule distinction — is the halt condition itself a Rule node, evaluated dynamically, while the halt/run branches are fixed Code?).
- Single-point-of-failure and security-surface concerns: whoever controls this service can paralyze the whole system.
- Distributed-system propagation: whether "halt" is scoped per-instance/per-node or must reach an entire multi-node/multi-datacenter deployment, and what consistency guarantee (if any) applies to signal propagation — a distributed-coordination problem independent of how fast the halt logic itself executes locally.

#### Connection continuity across a sub-minute redeploy
Per the existing sRPC Connection/Session model, a Connection is a persistent identity between two `ApplicationInstanceID`s that must NOT be resumed if `ApplicationInstanceID` changes. Open question: does a sub-minute unikernel rebuild+redeploy preserve the same `ApplicationInstanceID` (allowing in-flight Connections to survive), or does every redeploy constitute a new instance identity (meaning long-lived Connections/streams are necessarily dropped on every redeploy-driven update)? If the latter, sub-minute rebuild speed alone does not replicate what Erlang's hot code swapping was originally built to guarantee (call/session continuity in telecom systems) — a distinct concern from *how fast* the swap happens. Needs a decision on whether a graceful-draining/handoff mechanism is required as a companion piece to this document's principles, and if so, where it's modeled (deployment layer vs. framework layer).

### Relationship to Type-Level Identity
Two framework principles converge here and must not be conflated: this document's governance rule — no logic or code may be added to a running Memar application at runtime — and the [Type](./type.md) identity principle — a static concept MUST be carried as its own named entity, never demoted to runtime data ([Type → Stateless Types](./type.md#stateless-types)). They are **compatible** and share an architectural inclination toward compile-time fixedness, but they are **logically independent**: they are *convergent* (both push toward compile-time fixedness) yet not *interdependent* — neither logically requires the other.

Each can hold without the other. A closed, compile-time-fixed set of immutable sentinel values with numeric IDs satisfies this document completely while still carrying identity as data — compatible with immutable infrastructure, yet in violation of type-level identity. Conversely, a hypothetical runtime type registry could register new concept Types without full recompilation — satisfying identity-in-type while violating this document's governance rule. Whether such a registry is desirable, architecturally sound, or within either document's scope remains an open question; like configuration-driven behavior generally, it is an optional feature whose presence must be deliberately designed and justified, never an implicit backdoor around the default governance model.

What type-level identity adds beyond this document alone is compile-time-*typed* identity: concepts are not merely fixed at compile time — the type system itself carries and verifies their identity, a stronger guarantee than compile-time-fixed data.

**A caveat on this entire section:** this document is itself a placeholder pending its dedicated session (see [Unresolved questions](#unresolved-questions)). The analysis reflects the currently understood shape of both principles, not finalized texts; if the dedicated session produces materially different formulations, this section should be revisited.

## Results
This document is an intentionally minimal placeholder pending its dedicated session; no outcome reporting exists yet. Several analyses are deliberately deferred to that session — full scope definition, Motivation depth, Drawbacks, Rationale and alternatives, and Prior-art research (candidate directions already noted under [Prior art](#prior-art)) — and this section will be populated once real deployment experience accumulates.

## Discussion

### Prior art
(Deferred — likely candidates to research include immutable infrastructure practices in ops/deployment tooling (e.g. container image rebuilds instead of in-place config mutation), and their relationship, if any, to compile-time vs. runtime specialization in compilers.)

### Unresolved questions
- Full scope and definition of "immutable infrastructure" within Memar has not yet been discussed in depth; this document is a placeholder pending a dedicated session.
- Whether immutable infrastructure removes the need for Profile-Guided Optimization in the Khayyam compiler entirely, or only for a subset of currently PGO-addressed cases (e.g. configuration-driven behavior, as opposed to per-request/per-connection runtime-data-driven behavior), is unresolved and disputed — see the open dispatch-resolution question in [memar-go generics elimination RFC].

### Future possibilities
- Dedicated session to define immutable infrastructure's relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning — including the connection-continuity decision under [Open Design Threads](#open-design-threads).

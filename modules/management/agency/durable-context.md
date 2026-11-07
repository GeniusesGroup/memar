---
Title: "Agency — Durable Context"
Labels: Draft
Start Date: 2026-11-03
ID: 498251
---
# Agency — Durable Context

## Abstract
This document is the protocol for **durable agent context** under [Agency](./agency.md): how a takeup binds to an ordered composition of materials, how that composition is resolved without a filesystem Path, and which byte-stability and continuity requirements a realization must meet. It decides the C0 form (ordered content/section addresses plus normative marks; agency owns order and bind only), states PrefixStability and Context Continuity as decidable requirements, names the BindTakeup / ResolveComposition / InvalidateComposition service contracts and the SerializeForIntelligence widget, and declares the adapter seams (vendor prefix cache, local durable KV, optional light model) that realizations plug into. Bodies and material identity stay with [content](../../knowledge/content/content.md); search stays with its owner. Init/act context CLI verbs become widgets over Resolve; fixing new-shape init-context is not this protocol's work.

## Introduction

### Motivation
Agents re-pay a large Stable body of materials on every new chat or similar case. Vendor prompt caches are opportunistic and short-lived. Memar already composes act and init context, but those verbs sit under `modules-plugable/ai` and couple to Path/folder layout. Owner rulings on research `20261103-T100552Z-14796` (2026-11-03) refuse deferring the right compose/bind home and require protocol first, adapters next. This document is that protocol.

### Methodology
The requirements below absorb research `20261103-T100552Z-14796` (Findings, Alternatives, Recommended protocols) and the owner decisions recorded on that task: structure now; C0 first unless it recreates Path/fs-style coupling; Session suffix-only for PrefixStability v1; light model only as an adapter after the protocol.

## Explanation

### Process governed
One process: **takeup of context for an agent** (human UI or intelligence runtime) — binding a principal to an ordered composition, resolving that composition to materials, and (when an intelligence runtime is used) serializing Stable / Session / Event segments for PrefixStability. Forked-subagent shared-prefix behavior is fed by Bind/Resolve; it is not replaced ([forked-subagent Expectation](../../../modules-plugable/process/forked-subagent/forked-subagent.md#the-expectation)).

### C0 trial — result
**C0 holds.** An ordered composition is a finite sequence of entries, each an addressable material (content's Addressability), a [Context layer](#context-layer), and a normative mark (content/normative section hash). Agency stores that sequence and the bind from a takeup to a [Composition version](#composition-version). It does not store bodies, does not open folders, and does not take a Path. A second agency address type for materials (**C1 / CompositionBinding as material identity**) is **not minted**: the composition version is the hash of the ordered entries, not a rival Addressability. If a realization of Resolve takes a Path or walks a tree, that realization fails this protocol; the failure is not grounds to mint C1.

Content exports [`Addressable_Entity`](../../knowledge/content/protocol/addressable-entity.kh) for Addressability (document/section identity with equality). Agency composition entries and Event locators use that type; a Path-shaped value remains non-conforming.

### Context layer
Each composition entry carries exactly one layer. The decidable values are Khayyam abstractions under `protocol/context-layer-kinds.kh`: `Context_Layer_Stable`, `Context_Layer_Session`, `Context_Layer_Event` (each a `Context_Layer`). PrefixStability's Stable segment is the serialization of entries whose layer is `Context_Layer_Stable` only.

- A Stable entry holds knowledge or materials that change when their owner revises them (skill, act norms, class handbook); content and norm owners revise it.
- A Session entry holds task-owned inputs referenced by bind (plan id, claim), not stored as task facts inside agency; task and timeline owners revise it, and agency holds only the reference in the composition.
- An Event entry holds this message or ticket delta; the takeup revises it.

Segmented Stable compositions (skill ∥ act-kind ∥ project prefs) are preferred over one monolith for invalidation blast radius (research `20261103-T100552Z-14796`, alternative C2).

### Composition version
Given an ordered composition C, `CompositionVersion(C)` is the cryptographic hash of the concatenation, in order, of each entry's `(material locator bytes, layer tag, normative mark)`. Two compositions that differ in order, membership, layer, or mark yield different versions. Version is agency's bind key; it is not a content address.

### Concepts (agency owns)
- **Ordered composition** — the sequence; agency owns order and bind; bodies stay with owners.
- **Composition version** — hash of that sequence as above.
- **Takeup binding** — record that a principal's takeup uses a composition version, optionally with an Event locator.

Working name **CompositionBinding** from research names the *bind record / version key*, not a new material address type.

### Service: ResolveComposition
**Contract (decidable).** Stated input: a `CompositionVersion`. Output: the `Ordered_Composition` (entries: locator, layer, normative mark) stored under that version — never bodies, never a Path.

Bodies are obtained from content owners only in the SerializeForIntelligence widget (or a later Context_Compose widget), which aggregates Resolve with content. A base Resolve service that fetches bodies fails [widget-aggregates](../../computer/ui/rules/widget-aggregates/widget-aggregates.md).

Requirements a party that did not write this protocol can decide:

1. Given the same `CompositionVersion`, Resolve returns the same ordered entries (locator, layer, mark sequence).
2. Resolve's inputs and outputs name no filesystem Path type; a call that supplies a Path fails the contract.
3. Resolve does not search text; retrieval of "which past tickets match" is outside this module.
4. Resolve does not return content bodies.

### Service: BindTakeup
**Contract (decidable).** Stated input: a principal identifier, a `CompositionVersion`, and an optional Event material locator. Output: a takeup binding record.

Requirements:

1. After BindTakeup(P, V, E?), Resolve(V) is defined for that V (or Bind refuses).
2. BindTakeup does not write task facts, content bodies, or search indexes ([What this module does not own](./agency.md#what-this-module-does-not-own)).
3. Two binds with the same (P, V, E?) are equivalent; Event may differ between binds without changing V.

### Service: InvalidateComposition
**Contract (decidable).** Stated input: a normative mark (source hash) that content reports changed. Side effect: every `CompositionVersion` whose ordered entries included that mark becomes invalid for new binds; Resolve of those versions refuses or returns a stated invalidation error. Output: the count of versions invalidated (`invalidatedCount`).

Requirement: Invalidate uses content/normative hash identity; it does not redeclare versioning. Callers that need only completion use the count; listing every version is not part of this service's surface.

### Widget: SerializeForIntelligence
Aggregation only ([widget-aggregates](../../computer/ui/rules/widget-aggregates/widget-aggregates.md)). Stated input: a takeup binding (hence a `CompositionVersion` and optional Event). It calls Resolve for the ordered entries, obtains bodies from content owners by locator+mark, and emits byte segments `Stable`, then optional `Session`, then `Event`.

Order of materials inside Stable (and Session) is Resolve's order. Stable includes only `Context_Layer_Stable` entries. No clock, random id, or per-chat nonce may appear in the Stable segment bytes.

### Protocol: PrefixStability
**Stated input:** a `CompositionVersion` V and a serializer S that realizes SerializeForIntelligence for V with empty Event and with Session omitted or placed only after Stable.

**Requirement:** For any two takeups that use the same V and the same S, the Stable segment bytes are identical. Session is **suffix-only for v1** (never a Stable breakpoint). Event is never part of Stable.

**Decision procedure:** hash(Stable bytes) equal across the two takeups.

### Protocol: Context Continuity
**Stated input:** two takeups bound to the same `CompositionVersion` V.

**Requirement:** Resolve(V) yields the same ordered materials for both (same locators and normative marks). Only Event may differ between the takeups.

**Decision procedure (human realization):** the listed materials are the same sequence. **Decision procedure (intelligence realization):** Stable segment hash under PrefixStability matches.

### Protocol: Fork feed
Bind/Resolve may supply the shared prefix a runtime needs to meet [forked-subagent Expectation](../../../modules-plugable/process/forked-subagent/forked-subagent.md#the-expectation). They do not replace that Expectation's rules.

### Adapter seams (interfaces only)
Realizations plug in through abstractions; consumers import the abstraction, never a vendor or host module.

1. **Prefix cache adapter** — get/put Stable prefix bytes keyed by `CompositionVersion` (vendor prompt-cache class). Opportunistic; never store of record.
2. **Durable KV adapter** — get/put byte values keyed by `CompositionVersion` (local APC / disk-KV class). Optional realization for PrefixStability hits across process life.
3. **Light model adapter** — given prefix+suffix bytes, return a completion. Optional cost path; agency requires PrefixStability of what it composes and never owns weights. Quality bar before any default is Left open to the owner.

### Migration
Conceptual ownership of init-context and act-context composition moves to agency: those CLI/MCP verbs become **widgets** that Bind + Resolve (+ Serialize when intelligence). Their public names may stay. Fixing `get-task-init-context` for new-shape (records-only) tasks is **another agent's work** (owner decision on `20261103-T100552Z-14796`); this protocol does not duplicate it.

### Boundaries
- Agency ≠ content Addressability ([content Addressability](../../knowledge/content/content.md#addressability)).
- Agency ≠ text search (sister task `20261103-T100549Z-14796`).
- Context Continuity is not the whole of [Interaction With an Agent](./agency.md#interaction-with-an-agent) (ten dimensions); it is the Continuity surface for materials.
- Documentation remains an Agency mechanism for Knowledge ([Documentation as an Agency Mechanism](./agency.md#documentation-as-an-agency-mechanism)); this protocol does not replace documentation with a cache blob. A precomposed cache blob is a derived artifact for PrefixStability hits only.

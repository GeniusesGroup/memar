# Control Flow Handoff

Open work for `protocols/control-flow.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is. This handoff received the body Discussion's open questions and future possibilities when the document migrated to the three-section skeleton, together with the retired Control Flow in Khayyam document's open work (see the paired changelog's absorption entry).

## Open Questions

### Should the success/failure pair live on the Error abstraction or on a shared abstraction?
- State: asking an `Error` — whose identity already represents failure — "what to do on success" may be semantically backwards; the pair may belong one level up, on the shared abstraction `IsNull()` already belongs to, with `Error` only inheriting it. Not yet decided.
- Next: resolve before finalizing the pair naming.

### No final naming choice between the candidate pairs
- State: `OnFailure`/`OnSuccess` versus `OnPresent`/`OnAbsent`, or another candidate — none confirmed as final.
- Next: decide alongside the shared-abstraction question above.

### Interaction with the rejection of default implementations
- State: if the shared-abstraction approach is chosen, how does it interact with [Abstraction in Khayyam](../khayyam/abstraction.md#rejection-of-default-implementations)'s rejection of default implementations? Each implementing capsule would need its own Explicit Delegation Verification line to a shared internal implementation, to avoid duplicating the same check logic across every implementer without resorting to inheritance.
- Next: design the delegation-verification mechanism if the shared abstraction is chosen.

## Anticipated Work

- Once finalized, the resulting abstraction and naming convention should be cross-referenced from [The Error](./error.md) as the recommended standard pattern for branching on a returned error.
- A standard-library `GOTO`/jump-based control-flow package, alongside the structured `IF`/`LOOP` family, so the unstructured path is not merely theoretical. (Carried from the retired Control Flow in Khayyam document's anticipated work.)
- A richer standard library of named, domain-flavored conditional and error-propagation methods, expected to grow over time. (Carried from the same source.)

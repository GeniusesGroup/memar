# Khayyam Rule — Commented Generic Bindings Handoff
Open state for [commented-generic-bindings.md](./commented-generic-bindings.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — applied 2026-09-28 to the ported corpus under `modules/` (excluding `modules/khayyam/`): 6 methods realized in 4 files with 6 `in` lines added; 44 methods over open type parameters left; 26 methods reported unresolved. A second run changes nothing.

## Decisions
- **A constraint naming one type fixes the binding** — Decided (2026-09-28, owner). In `timer.kh`, `ST` is `Timer_Status` and `TIME` is `time_p.Time`, which is `Time`.
- **An unresolved binding is left and reported, never invented** — Decided (2026-09-28, owner).
- **An open constraint is not a binding** — Tentative (2026-09-28, applied by the tool; awaiting the owner's review). `any` and `comparable` fix no type, so a method over them is neither realized nor counted as unresolved.

## Open Questions
- **What an unresolved method becomes.** The 26 reported methods fall into four kinds: a type parameter inside another type (variadic `...ELEMENT`, `Iterator[K, V]`, `EventListener[E]`, `Timer[TIME, ST]`), a self-referential constraint (`K Key[K]`), an interface with no Khayyam abstraction (`LastIndex`, `Iterate`, `Head`, `Tail`, `Enqueue`, `Dequeue`, `Iterator`, `EventListener`, `Per`), and an open parameter mixed with a binding (`Handlers.Process`, `SK any`). Each needs a form the documents do not state.
- **Whether a port rule belongs in this catalog.** As for the [go clue residue rule](../go-clue-residue/go-clue-residue.handoff.md#open-questions).

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [commented-generic-bindings.md](./commented-generic-bindings.md) | Base — the rule | Keep in sync with the tool |
| [qualified-names.md](../qualified-names/qualified-names.md) | Depends_on — how the constraint's name maps to a Khayyam name | None (read) |
| [receiver-method-names.md](../receiver-method-names/receiver-method-names.md) | Depends_on — the new method's name | None (read) |
| [result-parameter-names.md](../result-parameter-names/result-parameter-names.md) | Depends_on — the new method's parameter names | None (read) |
| [targets/go/abstraction_bridge.py](../../targets/go/abstraction_bridge.py) | Implements — `tidy --rule commented-generic-bindings` | Keep in sync |
| [targets/go/test_abstraction_bridge.py](../../targets/go/test_abstraction_bridge.py) | Implements — the `Tidy` tests | Keep in sync |

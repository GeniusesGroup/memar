# Metaprogramming in Khayyam Handoff

Open work for `metaprogramming.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Shape of the reflection-facing abstraction
- State: undesigned. The exact shape of the reflection-facing abstraction (or family of abstractions, if field-level, method-level, and full-structural reflection warrant separate contracts) has not been designed; `reflect_p.Structural` in the base document is illustrative naming only, not a settled proposal.

### Who provides the reflection implementation
- State: undecided. Whether the compiler provides the implementation automatically once a type composes the abstraction (similar to a derive), or whether the type's author must still write it by hand with compiler-provided helpers.

### Scoping of granted reflective access
- State: open. Whether reflective access, once granted via the abstraction, can be further scoped (e.g. field names only, no values; read-only, no modification) or is all-or-nothing per composed abstraction.

### Runtime-modifying reflection
- State: untested by the drafting. Whether runtime-modifying reflection (not just inspection) is in scope for Khayyam at all, or whether the document's position should be inspection-only by design — the drafting leaned on inspection-oriented examples throughout and has not tested the modification case.

## Anticipated Work

- A standard `reflect_p` package defining the canonical reflection-facing abstraction(s), analogous to `abstraction_p.Implements`, once real tooling needs (serialization, ORMs, debuggers) clarify what shape it should take. (From the Reflective Programming topic's retired `Future possibilities`; the retired document-level `Future possibilities` entry pointed to this same item.)

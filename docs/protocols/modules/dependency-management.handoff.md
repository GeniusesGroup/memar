# Dependency and Version Management Handoff

Open work for `protocols/dependency-management.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Transitive pinning ergonomics
- State: the strongest practical objection against the position — when a dependency updates its own internal references, the consumer's clone must be refreshed consistently; the tooling (a thin VCS-automation layer, not a resolver) is unspecified.
- Next: specify the refresh workflow; first evidence from the framework's own repository set.

### Private dependency access workflow
- State: VCS-native references handle authentication through the VCS's own credentials, but the team workflow (CI credentials, read-only mirrors) is unwritten.
- Next: write it down when the first private-dependency consumer appears.

### The framework's own module consumption mode
- State: whether modules within this repository consume one another via this mechanism from day one, or begin with direct source inclusion and migrate, is a project-management decision not yet made.
- Next: decide when the first implementation dependency between modules appears.

## Anticipated Work

- The thin VCS-automation tooling for reference refresh.
- The written workflow for private dependencies.
- If the ecosystem's registries converge on VCS-addressable pinning, a revision of this document recording which parts of the position have become moot.

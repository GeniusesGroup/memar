# Immutable Infrastructure as a Memar Foundation Handoff

Open work for `immutable_infrastructure.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Full scope and definition of "immutable infrastructure" within Memar
Full scope and definition of "immutable infrastructure" within Memar has not yet been discussed in depth; `immutable_infrastructure.md` is a placeholder pending a dedicated session.

### Does immutable infrastructure eliminate the need for Profile-Guided Optimization in the Khayyam compiler?
Whether immutable infrastructure removes the need for Profile-Guided Optimization in the Khayyam compiler entirely, or only for a subset of currently PGO-addressed cases (e.g. configuration-driven behavior, as opposed to per-request/per-connection runtime-data-driven behavior), is unresolved and disputed — see the open dispatch-resolution question in the memar-go [Elimination of Open Generic Type Parameters](https://github.com/GeniusesGroup/memar-go/blob/main/.agents/docs/Elimination_of_Open_Generic_Type_Parameters.md) document.

## Anticipated Work

- Dedicated session to define immutable infrastructure's relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning — including the connection-continuity decision under [Open Design Threads](./immutable_infrastructure.md#open-design-threads).

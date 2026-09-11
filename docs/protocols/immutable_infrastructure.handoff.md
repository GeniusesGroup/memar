# Immutable Infrastructure Handoff

Open work for `immutable_infrastructure.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Position within the deployment and change lifecycle
The document now states Memar's deployment-domain rule (infrastructure immutability; no runtime logic addition), but its position within the broader change lifecycle — release, versioning, environment promotion, rollback — has not been discussed. The base-layer concept document founding that direction now exists: [Software](../software.md) records the settled definition (the objective manifestation of a system of aggregated processes; not limited to the computer world) and carries the lifecycle positioning as open work. Configuration-management practice (configuration identification, baselines, change control, status accounting, audit) is the comparative prior art to examine. Separately, the term "ecosystem" — used loosely across documents for technology and AI environments — has no Memar definition; a terminology decision is owed before it carries weight here.

### Does immutable infrastructure eliminate the need for Profile-Guided Optimization in the Khayyam compiler?
Whether immutable infrastructure removes the need for Profile-Guided Optimization in the Khayyam compiler entirely, or only for a subset of currently PGO-addressed cases (e.g. configuration-driven behavior, as opposed to per-request/per-connection runtime-data-driven behavior), is unresolved and disputed — see the open dispatch-resolution question in the memar-go [Elimination of Open Generic Type Parameters](https://github.com/GeniusesGroup/memar-go/blob/main/.agents/docs/Elimination_of_Open_Generic_Type_Parameters.md) document.

## Anticipated Work

- Dedicated session to define immutable infrastructure's relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning — including the connection-continuity decision under [Open Design Threads](./immutable_infrastructure.md#open-design-threads).
- Deferred analyses for the dedicated session: full scope definition, Motivation depth, drawback accounting, rejected-alternative reasoning, and prior-art research (candidate prior-art directions recorded in the paired [changelog](./immutable_infrastructure.changelog.md)).
  - State: moved 2026-09-10 from the base document's removed `Results` section (three-section skeleton migration).
  - Next: carry these analyses into the dedicated session anticipated above.

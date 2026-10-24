# Immutable Infrastructure Handoff
Open work for `immutable_infrastructure.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Position within the deployment and change lifecycle
The document now states Memar's deployment-domain rule (infrastructure immutability; no runtime logic addition), but its position within the broader change lifecycle — release, versioning, environment promotion, rollback — has not been discussed. The base-layer concept document founding that direction now exists: [Software](../../../process/software/software.md) records the settled definition (the objective manifestation of a system of aggregated processes; not limited to the computer world) and carries the lifecycle positioning as open work. Configuration-management practice (configuration identification, baselines, change control, status accounting, audit) is the comparative prior art to examine. Separately, the term "ecosystem" — used loosely across documents for technology and AI environments — has no Memar definition; a terminology decision is owed before it carries weight here.

### Does immutable infrastructure eliminate the need for Profile-Guided Optimization in the Khayyam compiler?
- State: settled in direction, not in inventory. [The Principle](immutable_infrastructure.md#the-principle) states that Khayyam's compiler and runtime are expected "to benefit directly — for example, by reducing or eliminating the need for runtime profile-guided optimization wherever configuration-driven behavior can instead be resolved at compile time". So the whole-elimination reading is refused and the subset reading is taken, and the criterion is named: behavior resolvable at compile time because the configuration it depends on is fixed by the redeploy rule loses its runtime-data dependence and with it the reason for PGO; per-request and per-connection behavior does not, because a redeploy does not fix it. Residue: the passage is illustrative ("for example") and names no inventory, so which currently PGO-addressed cases fall in which class is unstated — that is the whole of the decision the entry was holding.
- Next: enumerate the PGO-addressed cases against the compile-time-resolvable criterion during the dedicated chat; nothing about the direction or the criterion is left to decide.

## Anticipated Work
- Dedicated chat to define immutable infrastructure's relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning — including the connection-continuity decision under [Open Design Threads](immutable_infrastructure.md#open-design-threads).
- Deferred analyses for the dedicated chat: full scope definition, Motivation depth, drawback accounting, rejected-alternative reasoning, and prior-art research (candidate prior-art directions recorded in the paired [changelog](immutable_infrastructure.changelog.md)).
  - State: moved 2026-09-10 from the base document's removed `Results` section (three-section skeleton migration).
  - Next: carry these analyses into the dedicated chat anticipated above.

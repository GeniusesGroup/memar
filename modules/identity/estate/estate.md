# Estate
Estate is an area where houses or buildings of a similar type have all been built together in a planned way.

## Positions confirmed in discussion (2026-08-05..09)

The modeling definition is deliberately **not settled yet** — narrative, hypotheses, and the full open-question map live in [estate.handoff.md](estate.handoff.md). What IS settled:

- **Land and building are two different estates.** A building is not an attribute/extension of its land; quantities like occupancy, density, and shadowing are observations over the building–land relation, not properties of either side. The spatial relations between estates live in [`edges/estate`](edges/estate/README.md).
- **Identity is immutable**: any change to an estate produces a new estate; the old one is never deleted. Creator-made changes are audit-logging semantics; third-party or no-change forks create new identities too (git fork analogy). There is no "latest version" — [supersedes](../thing/edges/supersedes/supersedes.md) designates which estate is currently realized. Lineage edges (`derived_from`, `forked_from`, `realized_from`) remain separate candidates for `thing`; a fork does not by itself supersede.
- **Multi-typing, not taxonomy**: a node takes identities from several domains simultaneously (thing + product + estate + ownership); domain categories are mental lenses with no objective graph representation. One identity/edge may forbid another — simultaneity is governed by edge rules.
- **What may become an estate is runtime policy** of each organization (e.g. whether an electrical switch qualifies) — never hard-coded; this domain's job is defining which edges an estate must/can take.
- **Out of this domain**: Ownership and Law (→ `modules/rights`), Address (→ URI domain), GPS/coordinates (→ location/URI domains; see `object/edges/coordinate-gps`).

Boundary questions shared with Product (furniture, museum, designs) are co-tracked in [../../economics/product/product.handoff.md](../../economics/product/product.handoff.md).

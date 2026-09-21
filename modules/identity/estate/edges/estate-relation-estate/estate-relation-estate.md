# Estate-Relation-Estate

Placeholder home for the generic spatial/physical relations **between two estates**, required by the confirmed decision that land and building are two different estates (so quantities like occupancy derive from their *relation*, not from either side's attributes). The individual edges (building-on-land, containment, adjacency, construction, realization, ...) are deliberately NOT named yet — per the vocabulary-discipline rule, relations come first, terms and Simple/Shortcut/Boundary classification after.

Model sketch (not final; both endpoints and edge kind per relation are still open):

- `(estate)-[spatial relation]->(estate)` candidates: on/constructed-on, contains, adjacent, connected, replaced-by, realized-on.

## Open questions (from the Estate session, 2026-08-05..09)

- Which of these relations are real, and does each one's existence depend on geometry (derived observation) or is it a first-class edge? (e.g. adjacency may be derived, not stored.)
- Is the "currently realized" relation (one of several alternative building designs realized on one land) estate-specific, or one instance of a generic current-realization mechanism shared with product batches and task outputs?
- Which edges are **mandatory** once a thing becomes an estate in an organization (runtime policy decides what qualifies — see [the estate handoff](../../estate.handoff.md)) — do any mandatory edges live here?
- For every candidate edge: what node types are at both ends, and is it a Simple, Shortcut, or Boundary edge (Memar's three edge models)?

Related: [the estate handoff](../../estate.handoff.md) — boundary suite (10 cases) that must pass through these relations.

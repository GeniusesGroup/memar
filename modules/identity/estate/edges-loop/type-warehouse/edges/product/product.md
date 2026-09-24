# Estate relation product

## Model

- Candidate (unconfirmed): `(estate)-[:relation_product]->(product)` carrying the labels `ManagerDecision` / `AllowedToEnter` — the warehouse loop's edge file defined only the two label names.
- Endpoints, direction, and whether the two labels are two states of one edge or two edges: nothing ratified.

## Policies (rules)

- Bare labels `ManagerDecision`, `AllowedToEnter` — no who-may-create/what-it-triggers recorded in the source; an edge without those semantics must not exist as ratified (no bare edges).

## Placement

- **Correct here** — admission of a product to a warehouse is instantiated at the warehouse, and this folder *is* the warehouse edge-loop: placement by entry point. If the decision later grows processing semantics, edge and processing stay together here (a module keeps its complete capability) — never "edge here, behavior there".
- **Not core economics `product`**: a product stays priceable and invoice-able without warehouse admission — core-by-necessity fails on the product side; the product kernel must not learn warehouse policy.
- **Core never knows Rule**: if `ManagerDecision` is the *output* of an organizational policy ("may this product enter?"), this side keeps only the structural relation/label and the decision arrives as a rule evaluation — the loop must not hard-code the policy.
- Not [inventory](../../../../../../../modules-plugable/economics/inventory/inventory.md) by default: stock bookkeeping is a separate removable capability while admission is warehouse identity — move only the part that proves to be stock-processing (see open questions).

## Open questions

- What do `ManagerDecision` and `AllowedToEnter` denote — one edge with a decision state, two labels, or a before/after pair?
- Who may set them, and what does setting them trigger (the missing no-bare-edges semantics)?
- If admission turns out to be stock-processing rather than warehouse policy, should the edge move with that processing into [inventory](../../../../../../../modules-plugable/economics/inventory/inventory.md) (pluggable owns complete capability)?
- Is this the warehouse loop's product endpoint, or a generic estate–product relation (museum piece vs stock)?
- If no who-may-create/what-it-triggers can ever be named, strip it entirely — the [coordinate](../../../../../../economics/product/edges/coordinate/coordinate.md) precedent (not an edge; lookup recipe to strip).


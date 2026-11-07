# Product relation estate

## Model

- Candidate (unconfirmed): `(product)-[:relation_estate]->(estate)` carrying the area label `LimitTo` — "DataModel is proper or appropriate location indicate specific area not specific location e.g. Taxi, ..." (direction unconfirmed).

## Policies (rules)

- "e.g. Taxi, ..." — the product's service area is a specific *area*, not a specific location; `LimitTo` names the area-based binding.
- Source records no who-may-set / what-it-triggers rules (no bare edges).

## Placement

- **Correct here — filed under [service.md](../../service.md) per the entry point** (the backlog entry sits with the service module's constraint shapes; place semantics of a served product — taxi area — belong to the serving capability; prefer existing homes over inventing new modules).
- **Not a new `estate-spatial` module:** one area label (`LimitTo`) on a product-estate link is a parameter of service placement, not independent processing (parameters vs semantics); estate stays the spatial domain and is referenced by identity (reference-not-embed).
- **Sibling vocabulary, one review:** the POS variant of the same idea lives in [estate](../../../pos/edges/estate/estate.md) (`ExactLocation` vs `LimitTo`, stations) — same `LimitTo` word, two attachment points (product-area vs pos-area); converge the spatial-relations question rather than grow two vocabularies.
- **Not core `product`:** location binding is serving semantics an org without services removes whole (removable ⇒ pluggable).

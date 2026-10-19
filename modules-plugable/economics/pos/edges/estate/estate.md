# Pos relation estate

## Model

- Candidate (unconfirmed): `(pos)-[:relation_estate]->(estate)` carrying placement labels `ExactLocation` / `LimitTo` (direction unconfirmed).

## Policies (rules)

- `ExactLocation` — the register binds to a specific point.
- "service provides in specific place e.g. stations(bus, train, airport, ...), ..." / `LimitTo` — area-based service: the register serves within a bounded area (stations and similar hubs).

## Placement

- **Correct here — POS placement is instantiated from the register capability**.
- **Not core estate / not a new spatial module:** estate stays the spatial domain and is referenced by identity (reference-not-embed); `ExactLocation`/`LimitTo` are placement parameters of a register (parameters vs semantics; prefer existing homes over inventing new modules).
- **Sibling vocabulary, one review:** the product-side area label lives in [estate](../../../service/edges/estate/estate.md) (`LimitTo`, Taxi) — same `LimitTo` word, two attachment points (product-area vs pos-point); converge the estate spatial-relations question rather than grow two vocabularies (receiving [pos.md](../../pos.md)/service backlog review: "LimitTo vs ExactLocation connects to the estate spatial-relations question").

## Open questions

- `ExactLocation` vs `LimitTo` — one edge with a mode flag, or two distinct edges? Shared with [estate](../../../service/edges/estate/estate.md)'s `LimitTo` — one vocabulary?
- What does the placement constrain (selling? printing? serving?) and who sets it — no-bare-edges test open; if gating, rule material (core never knows Rule).
- Target: estate node, station/hub label, or spatial sub-graph? Source types no target (label package only).
- Direction/naming unconfirmed — nothing ratified.


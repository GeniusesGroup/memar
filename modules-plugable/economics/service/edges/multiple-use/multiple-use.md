# Multiple use

## Model

- `(product)-[:multiple_use]->(---)` — candidate (unconfirmed): the record keys `Field_ProductID` plus `Maximum() uint64` — a cap on how often one service may be served.

## Policies (rules)

- `Maximum() uint64 // Maximum time this service can be served to buyer` — maximum serve-count per buyer (source wording: per buyer).

## Placement

- **Correct here — `modules-plugable/economics/service/edges/multiple-use` (already its home).** [service.md](../../service.md) lists multiple-use among the non-inventory offering shapes; edge + cap field travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** reuse caps are service semantics; an org without services removes it whole (removable ⇒ pluggable). Invoice claims without knowing reuse policy.
- **Not a new module:** one cap parameter is not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps live beside it ([number](../number/number.md), [reserve-quantity](../../../good/edges/reserve-quantity/reserve-quantity.md) across good) — one review, several edges.

## Open questions

- Is this one general capacity/limit pattern shared with inventory/restriction, or per-edge data? (Receiving [service.md](../../service.md) backlog review question; cf. [restriction](../../../restriction/restriction.md) global constraints.)
- Served "to buyer" — per buyer, per invoice, or per org? Source says buyer; confirm.
- Who enforces the cap (validation rule at sale; core never knows Rule)?
- Overlap with [number](../number/number.md) `Maximum()` — number caps total service volume, multiple-use caps per-buyer serve count: one edge with two fields, or two edges?

## Source

> Source: `modules-plugable/economics/service/edges/multiple-use/protocol/data_model.go` (in code).

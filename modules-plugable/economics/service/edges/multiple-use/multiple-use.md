# Multiple use

## Model

- `(product)-[:multiple_use]->(---)` — candidate (unconfirmed): a cap on how often one service may be served, declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)

- The cap is a serve-count per buyer.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/multiple-use` (already its home).** [service.md](../../service.md) lists multiple-use among the non-inventory offering shapes; edge + cap field travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** reuse caps are service semantics; an org without services removes it whole (removable ⇒ pluggable). Invoice claims without knowing reuse policy.
- **Not a new module:** one cap parameter is not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps live beside it ([number](../number/number.md), [reserve-quantity](../../../good/edges/reserve-quantity/reserve-quantity.md) across good) — one review, several edges.

## Source

> Source: `modules-plugable/economics/service/edges/multiple-use/protocol/data_model.kh` (in code).

# Number

## Model

- `(product)-[:number]->(---)` — candidate (unconfirmed): a min/max band with a per-buyer ceiling, declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)

- The minimum is a sale count before the service runs at all, the maximum is the total capacity, and the per-buyer ceiling limits one buyer's invoices.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/number` (already its home).** [service.md](../../service.md) lists `number` among the non-inventory offering shapes; edge + quantity fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** venue/hotel capacity rules are service semantics; an org without services removes it whole (removable ⇒ pluggable).
- **Not a new module:** a min/max/ceiling trio is parameters, not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps beside it: [multiple-use](../multiple-use/multiple-use.md) (per-borne serve count), [timing-interval](../timing-interval/timing-interval.md) (durations), [reserve-quantity](../../../good/edges/reserve-quantity/reserve-quantity.md) across good — one review, several edges.

## Source

> Source: `modules-plugable/economics/service/edges/number/protocol/data_model.kh` (in code).

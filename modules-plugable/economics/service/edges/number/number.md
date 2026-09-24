# Number

## Model

- `(product)-[:number]->(---)` — candidate (unconfirmed): the record keys `Field_ProductID` plus three decimal quantities — `Minimum()`, `Maximum()`, `MaximumInvoiceByBuy()` — a min/max band with a per-buyer ceiling.

## Policies (rules)

- `Minimum() decimal_p.Quantity // Minimum number of sale to serve the service e.g. cinema wouldn't play movie, ...` — a minimum sale count before the service runs at all.
- `Maximum() decimal_p.Quantity // Maximum number can be served to buyers e.g. cinema tickets, panic-room game, ...` — total capacity.
- `MaximumInvoiceByBuy() decimal_p.Quantity // Maximum buy e.g. hotel room, panic-room game, ... that must limit by buyer.` — per-buyer invoice ceiling.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/number` (already its home).** [service.md](../../service.md) lists `number` among the non-inventory offering shapes; edge + quantity fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** venue/hotel capacity rules are service semantics; an org without services removes it whole (removable ⇒ pluggable).
- **Not a new module:** a min/max/ceiling trio is parameters, not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps beside it: [multiple-use](../multiple-use/multiple-use.md) (per-borne serve count), [timing-interval](../timing-interval/timing-interval.md) (durations), [reserve-quantity](../../../good/edges/reserve-quantity/reserve-quantity.md) across good — one review, several edges.

## Open questions

- Is this one general capacity/limit pattern shared with inventory/restriction, or per-edge data? (Receiving [service.md](../../service.md) backlog review question.)
- `Minimum` below which "cinema wouldn't play movie" — a rule decision (may/must not run) or a status? No-bare-edges test open.
- Overlap with [multiple-use](../multiple-use/multiple-use.md): `Maximum` (total) vs `MaximumInvoiceByBuy` (per buyer) already here — is multiple-use's `Maximum` the same per-buyer concept under another name? Converge to one vocabulary.
- [good.md](../../../good/good.md) Unresolved: are `number` service-specific or a general schedulable-resource capability (cf. [timing-interval](../timing-interval/timing-interval.md), estate, device)?

## Source

> Source: `modules-plugable/economics/service/edges/number/protocol/data_model.go` (in code).

# Timing interval

## Model

- `(product)-[:timing_interval]->(---)` — candidate (unconfirmed): the record keys `Field_ProductID` plus three durations — `Minimum()`, `Expected()`, `Maximum()` (seconds) — a timing band per service.

## Policies (rules)

- "e.g. flight duration, doctor visit, carwash, ..." — the band describes how long a served service takes.
- `Minimum() duration.Second // Minimum time duration for this service`
- `Expected() duration.Second // Expected time duration for this service`
- `Maximum() duration.Second // Maximum time duration for this service`

## Placement

- **Correct here — `modules-plugable/economics/service/edges/timing-interval` (already its home).** [service.md](../../service.md) lists `timing-interval` among the non-inventory offering shapes; edge + duration fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** appointment/flight timing is service semantics; an org without services removes it whole (removable ⇒ pluggable).
- **Not a new module:** a min/expected/max trio is parameters, not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps beside it: [number](../number/number.md), [multiple-use](../multiple-use/multiple-use.md), [seat](../seat/) — one review, several edges.

## Open questions

- Is this one general capacity/limit pattern shared with inventory/restriction, or per-edge data? (Receiving [service.md](../../service.md) backlog review question.)
- [good.md](../../../good/good.md)/[service.md](../../service.md) Unresolved: are `timing-interval` service-specific or a general schedulable-resource capability that other domains (estate, device) also want — and does a future `schedulable` module absorb it?
- `Expected` vs `Minimum`/`Maximum` — scheduling estimate (analytics input) or contractual bound enforced by a rule?
- Who reads the band (booking engine? invoice?) and what does exceeding it trigger — no-bare-edges test open.

## Source

> Source: `modules-plugable/economics/service/edges/timing-interval/protocol/data_model.kh` (in code).

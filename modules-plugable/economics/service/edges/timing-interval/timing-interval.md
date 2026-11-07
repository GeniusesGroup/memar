# Timing interval

## Model

- `(product)-[:timing_interval]->(---)` — candidate (unconfirmed): a timing band per service, declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)

- "e.g. flight duration, doctor visit, carwash, ..." — the band describes how long a served service takes.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/timing-interval` (already its home).** [service.md](../../service.md) lists `timing-interval` among the non-inventory offering shapes; edge + duration fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ one service capability plus per-org configuration).
- **Not core `product`/`invoice`:** appointment/flight timing is service semantics; an org without services removes it whole (removable ⇒ pluggable).
- **Not a new module:** a min/expected/max trio is parameters, not independent processing (parameters vs semantics; prefer existing homes over inventing new modules).
- Sibling caps beside it: [number](../number/number.md), [multiple-use](../multiple-use/multiple-use.md), [seat](../seat/) — one review, several edges.

## Source

> Source: `modules-plugable/economics/service/edges/timing-interval/protocol/data_model.kh` (in code).

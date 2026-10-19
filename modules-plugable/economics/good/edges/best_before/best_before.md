# Best before

## Model

- `(product)-[:best_before]->(---)` (note: Duration(Second)) — the record keys `Field_ProductID` plus `Duration() duration.Second`.

## Policies (rules)

- `Duration() duration.Second // from production time` — the best-before window is measured from production time.
- https://en.wikipedia.org/wiki/Expiration_date

## Placement

- **Correct here — `modules-plugable/economics/good/edges/best_before` (already its home).** [good.md](../../good.md) names `best_before` among this module's inventory-facing semantics — edge + duration field travel together (pluggable owns complete capability).
- **Not core `product`:** expiry is physical-goods semantics an org without goods removes whole (removable ⇒ pluggable); product stays priceability.
- **Not `batch`:** [good.md](../../good.md) Unresolved asks whether `batch` is the right home for `best_before` — batch owns identity/lineage of produced goods ([batch](../../../batch/batch.md)), this module owns the product-level expiry parameter; keep both questions converging there (prefer existing homes; see Open questions).
- **Not a new module:** one duration parameter is not independent processing semantics (parameters vs semantics; prefer existing homes over inventing new modules).

## Open questions

- Receiving [good.md](../../good.md) Unresolved: do `batch` and `good` overlap on lot/expiry tracking, or is `batch` the right home for `best_before`?
- "from production time" — production timestamp of which realization: the product's batch (batch identity), a generic production event, or the record's own audit time? Converge with [batch](../../../batch/batch.md) identity questions (batch as realization vs grouping).
- Who enforces expiry — a rule reacting at sale time (core never knows Rule), or a status/label move?
- Lots of one product that differ in remaining shelf life are what the owner's leaning that a price belongs to the batch rests on (open in [pricing](../../../pricing/edges/pricing/pricing.md#open-questions)): if a nearer best-before lot is sold at its own price, is the best-before date then a fact of each batch, not only a window on the product?

## Source

> Source: `modules-plugable/economics/good/edges/best_before/protocol/service-set.kh` (in code).


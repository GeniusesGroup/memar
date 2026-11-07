# Item seat

## Model

- `(invoice_item)-[:invoice_item_seat]->(---)` — target unconfirmed: the record is declared in [data_model.kh](protocol/data_model.kh) and the seat id in [dt-seat_id.kh](protocol/dt-seat_id.kh) — a seat id on the item today; a `(seat)` node only if/when the resource-side seat record ([](../seat/)) is referenced directly.
- The storage services are declared in [storage.kh](protocol/storage.kh).

## Policies (rules)

- "service: reserve seat" — an invoice line holds a seat; occupancy is answered through invoice lines by (product, seat), by seat+status, or by status alone.
- Live protocol note widens the meaning: "It can also use to order buyers e.g. patient in doctor clinic" ([data_model.kh](protocol/data_model.kh)) — the seat may name a person-slot, not only a chair.
- No who-may-create / what-it-triggers rules recorded in the source; reserve/release semantics unconfirmed.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/item-seat` (already its home).** [service.md](../../service.md) states the split exactly: invoice-line occupancy ([item-seat](README.md)) is the seat capability realized at claim time, not Invoice kernel — edge and query services stay together (pluggable owns complete capability).
- **Not core `invoice`:** invoices exist without seating (a downloadable good has no seat) — core-by-necessity fails; removable with the service module ⇒ pluggable.
- **Not core `product`:** `Seat` is a service flag in the product flag-space (see the [product.md](../../../../../modules/economics/product/product.md) backlog) — a parameter of how a service is sold, owned by this module (parameters vs semantics; the product kernel never learns seat rules).
- Resource-side siblings ([seat](../seat/), timing-interval, number) live in the same module — no bare edge: meaning comes from the service reservation capability that maintains them.

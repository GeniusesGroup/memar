# Item seat

## Model

- `(invoice_item)-[:invoice_item_seat]->(---)` — target unconfirmed: [protocol/data_model.go](protocol/data_model.go) keys the record on `Field_InvoiceItemID` + `Field_SeatID` ([protocol/dt-seat_id.go](protocol/dt-seat_id.go), a `uint64`) — a seat id on the item today; a `(seat)` node only if/when the resource-side seat record ([../seat/](../seat/)) is referenced directly.
- Query services: `FIND_InvoiceIDs_BY_ProductIDAndSeatID`, `FIND_InvoiceIDs_BY_SeatID_AND_Status`, `FILTER_InvoiceIDs_BY_Status`.

## Policies (rules)

- "service: reserve seat" — an invoice line holds a seat; occupancy is answered through invoice lines by (product, seat), by seat+status, or by status alone.
- Live protocol note widens the meaning: "It can also use to order buyers e.g. patient in doctor clinic" ([protocol/data_model.go](protocol/data_model.go)) — the seat may name a person-slot, not only a chair.
- No who-may-create / what-it-triggers rules recorded in the source; reserve/release semantics unconfirmed.

## Placement

- **Correct here — `modules-plugable/economics/service/edges/item-seat` (already its home).** [service.md](../../service.md) states the split exactly: invoice-line occupancy ([item-seat](README.md)) is the seat capability realized at claim time, not Invoice kernel — edge and query services stay together (pluggable owns complete capability).
- **Not core `invoice`:** invoices exist without seating (a downloadable good has no seat) — core-by-necessity fails; removable with the service module ⇒ pluggable.
- **Not core `product`:** `Seat` is a service flag in the product flag-space (see the [product.md](../../../../../modules/economics/product/product.md) backlog) — a parameter of how a service is sold, owned by this module (parameters vs semantics; the product kernel never learns seat rules).
- Resource-side siblings ([seat](../seat/), timing-interval, number) live in the same module — no bare edge: meaning comes from the service reservation capability that maintains them.

## Open questions

- Seat id vs seat node: when does `dt-seat_id.go`'s `uint64` become a referenced seat entity (capacity, `MapID` SVG layout in [../seat/protocol/data_model.go](../seat/protocol/data_model.go))?
- Relation to the `Type_Seat` product flag — flag-plus-edge duplication (same review as Provider/SellLimit in [product.md](../../../../../modules/economics/product/product.md))?
- `Status` used by these queries: protocol-local status or the general status domain?
- [transaction.md](../../../../../modules/economics/transaction/transaction.md) filed these listings as "data-model pass material" — keep or drop at the pass?


# Reserve quantity

## Model

- `(product)-[:reserve_quantity]->(---)` — candidate (unconfirmed): the record keys `Field_ProductID` plus a fixed max-reserve quantity and a `Percent() uint64` — two reserve shapes on one record: an absolute count or a percent of the inventory.

## Policies (rules)

- `decimal_p.Field_Quantity // fix max reserve number` — a fixed maximum number of units that may be reserved.
- `Percent() uint64 // percent of the inventory` — alternatively a percentage of inventory.
- Source records no who-may-reserve / what-reserve-triggers rules (no bare edges).

## Placement

- **Correct here — `modules-plugable/economics/good/edges/reserve-quantity` (already its home).** [good.md](../../good.md) names `reserve-quantity` among this module's inventory-facing semantics — edge + reserve fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ one good capability plus per-org reserve configuration).
- **Not core `product`/`invoice`:** reservation is physical-goods semantics; an org without goods removes it whole (removable ⇒ pluggable). Invoice lines claim, they do not reserve inventory policy.
- **Not the restriction module:** pending-transfer reservations are named a restriction use case ([restriction](../../../restriction/restriction.md) — "pending-transfer reservations"); that module owns *global quantity constraints as observing nodes* with their own state, while this is a product-level reserve *parameter* — keep the constraint-machine there and the product reserve-cap here (prefer existing homes; converge in Open questions if the shapes prove identical).

## Open questions

- Is this one general capacity/limit pattern shared with inventory/restriction, or per-edge data? (Receiving [service](../../../service/service.md) backlog review question — number/multiple-use siblings live there.)
- Fixed quantity vs percent — one policy chosen per product, or both active together (whichever binds first)?
- Who may reserve, and what does a reserve trigger (blocking transactions? analytics only)? — no-bare-edges test open; if it is a blocking behavior, cf. [restriction](../../../restriction/restriction.md) "restriction rule reacts by creating its own blocking transactions".
- Overlap with `batch`/`good` unresolved questions ([good.md](../../good.md)) — does reserving interact with lot/expiry identity?

## Source

> Source: `modules-plugable/economics/good/edges/reserve-quantity/protocol/data_model.kh` (in code).

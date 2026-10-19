# Service Handoff

Load-bearing state for the service module: what converted, the one protocol file deliberately left alone, and the type disagreements the seat edge carries. Paired with [service.md](service.md), which owns the placement argument and the open question about a shared parent with `good`.

## Status

Active — five edge capabilities and the module's model converted; `protocol/dt-uuid.kh` left alone on purpose; `seat` has no document at all.

## Khayyam conversion (2026-10-03)

Converted, all returning `accept`:

| File | Declares |
|---|---|
| `protocol/model.kh` | `ServiceModel ab { ThingModel ProductModel }` |
| `edges/item-seat/protocol/dt-seat_id.kh` | `Service_SeatID ab { U64 }`, `Field_SeatID`, `SeatID` |
| `edges/item-seat/protocol/data_model.kh` | `ItemSeatDataModel` |
| `edges/item-seat/protocol/storage.kh` | `ItemSeatStorage` + `Save`/`Count`/`Get` |
| `edges/multiple-use/protocol/data_model.kh` | `Observer_MultipleUse_Maximum`, `MultipleUseDataModel` |
| `edges/multiple-use/protocol/storage.kh` | `MultipleUseStorage` + `Save`/`Count`/`Get` |
| `edges/number/protocol/data_model.kh` | `Observer_Number_Minimum`/`_Maximum`/`_MaximumInvoiceByBuy`, `NumberDataModel` |
| `edges/number/protocol/storage.kh` | `NumberStorage` + `Save`/`Count`/`Get` |
| `edges/seat/protocol/dt-type.kh` | `Service_Seat_Type ab { U8 }`, `Field_Service_Seat_Type`, `Type` |
| `edges/seat/protocol/data_model.kh` | `Observer_Seat_SeatCapacity`, `Observer_Seat_MapID`, `SeatDataModel` |
| `edges/seat/protocol/storage.kh` | `SeatStorage` + `Save`/`Count`/`Get`/`FindProductIDsByMapID`/`FilterProductIDsBySeatType` |
| `edges/timing-interval/protocol/data_model.kh` | `Observer_TimingInterval_Minimum`/`_Expected`/`_Maximum`, `TimingIntervalDataModel` |
| `edges/timing-interval/protocol/storage.kh` | `TimingIntervalStorage` + `Save`/`Count`/`Get` |

## Decisions

### `protocol/dt-uuid.kh` is left unconverted, and it should probably be deleted

The Go declares `Field_ProductID`, `Field_ProductsID` and `UUID record_p.UUID` in package `product_service_p`. The first two are already declared — and already valued as `ThingUUID` and `Array_ThingUUID` — in `modules/economics/product/protocol/dt-uuid.kh`, which this repository's ownership rule makes the single owner of the product identity. Declaring them again here would be exactly the "one concept declared twice" case the qualified-names rule answers with one declaration and an inclusion.

The third, `UUID record_p.UUID`, is a service identity that nothing in the module or the tree references: every storage in this module keys on the product's or the invoice's UUID, never on its own. So there is nothing left to declare, and the file stays as it is with its clue block. The main session may delete it; if the module ever needs an identity of its own, that is a new declaration with a real referent.

### Cap fields became `Observer_*` abstractions, matching the resource edges

The five data models each carry one to three numeric conditions. Following `management/group/edges/membership-term-member_limit/protocol/data_model.kh`, each condition is its own `Observer_<Edge>_<Condition>` abstraction with a `Get<Condition>` accessor, and the data model is a pure composition. This also resolves the collisions the Go would otherwise have created: `number` and `multiple-use` both declare `Maximum()`, and `timing-interval` and `number` both declare `Minimum()` and `Maximum()`.

### Durations are `Observer_Duration_Second`, not `duration.Second`

`duration.Second` is a capsule, and a signature owned by an abstraction names the concept. `Observer_Duration_Second` (`memar/modules/time/duration/protocol/second.observers.kh`) is memar's abstraction for "a duration measured in seconds" and supplies `GetDuration()`. Three of them compose into the three timing-interval observers, which is why those three observers have their own names rather than reusing one.

### `SeatID` and the seat type are qualified with the module, their accessors are not

`Service_SeatID` and `Service_Seat_Type` carry the module because the plain words are the repository's most generic. Their accessors stay bare — `SeatID`, `Type` — because the receiver already says which seat field or seat type is asked, which is what the receiver-method-names rule asks for, and because `identity/thing`'s criterion edge already sets the precedent with a bare `Type`.

### Storage query names moved to the repository's camel shape

`FIND_ProductIDs_BY_MapID` → `FindProductIDsByMapID` and `FILTER_ProductIDs_BY_SeatType` → `FilterProductIDsBySeatType`, matching `ListAccountSideIDsByAccountID` and the `Get_BY_TransactionIndex` → `GetByTransactionIndex` the bookkeeping conversion already made. The Go's `[]pp.UUID` results are `Array_ThingUUID`, imported from `identity/thing` rather than redeclared; the Go's `offset, limit uint64` are `Container_Offset` and `Container_Limit`.

## Unconverted, and what blocks it

- **`protocol/dt-uuid.kh`** — see above; nothing to declare without duplicating the product identity.
- **`edges/estate/`** — has no `.kh` files at all, only [estate.md](edges/estate/estate.md) and its README. The Go's estate relation was never written, and the document says so ("Source records no who-may-set / what-it-triggers rules (no bare edges)", "Direction/naming unconfirmed — nothing ratified"). Nothing to convert.

## Findings

### `MapID` was two different types in the same module

`seat/protocol/data_model.kh` declares `MapID() record_p.UUID` while `seat/protocol/storage.kh` declares `FIND_ProductIDs_BY_MapID(mapID op.UUID)`. Neither path exists — `memar/storage/record/protocol` and `modules/storage/object/protocol` are both absent — so the Go did not resolve on this point even before conversion. The domain meaning, from the Go's own comment, is a stored map file: "to show background and rows and seats. suggest use SVG format".

Both are valued as `Storage_UUID` (`memar/modules/memory/record/protocol/dt-uuid.kh`), the only declared record identity in reach. That is a compromise and it is the wrong kind of type: a seating map is a blob, not a row. What the field needs is an object-or-content identity, and the module that would own it — a storage object domain — does not exist in the tree.

### `item-seat`'s storage is keyed by the wrong endpoint

`ItemSeatDataModel` carries `Field_InvoiceItemID` + `Field_SeatID`, and [item-seat.md](edges/item-seat/item-seat.md) states the edge as `(invoice_item)-[:invoice_item_seat]->(---)`. But `ItemSeatStorage.Count` and `Get` both take `invoiceID`, not an invoice-item id. As converted, the storage can count and fetch records the data model cannot name, and cannot reach a record by the endpoint its own record claims. The Go had the same mismatch; this is a source gap.

### `seat` has no document

`edges/seat/` holds three protocol files and no `seat.md` and no `README.md` — the only edge folder in this module without one. Four other documents link to `../seat/` as though it had one, including [item-seat.md](edges/item-seat/item-seat.md), which asks "when does `protocol/dt-seat_id.kh`'s `uint64` become a referenced seat entity (capacity, `MapID` SVG layout)". The edge this module's `item-seat` capability depends on is therefore undocumented, and the one-folder-per-edge convention the Phase-0 review established is broken in exactly this place.

### `edges/estate/` and `edges/seat/` are not the same kind of folder

`estate` has a document and no code; `seat` has code and no document. [service.md](service.md) lists four offering shapes — seat, timing-interval, number, multiple-use — and `estate` is a fifth folder that is not one of them. Nothing states how the estate relation relates to the four shapes.

## Open Questions

- **The `Maximum()` vocabulary is not converged.** `number.Maximum` caps total service volume, `number.MaximumInvoiceByBuy` caps per-buyer invoices, `multiple-use.Maximum` caps per-buyer serve count, and [number.md](edges/number/number.md) already asks whether multiple-use's `Maximum` is "the same per-buyer concept under another name". All three are now declared as three separate observers with three separate names, so the conversion made the overlap visible rather than resolving it. [multiple-use.md](edges/multiple-use/multiple-use.md) raises the same question across `good`'s `reserve-quantity`.
- **A cap on how many invoices may consume something is a count, and two domains disagree on how to spell it.** `number.MaximumInvoiceByBuy` is a `Decimal_Quantity` (following its Go) while the same concept in [discount](../discount/discount.handoff.md) and [voucher](../voucher/voucher.handoff.md) is a `uint64`, converted as `U64`. A count of invoices is not a decimal quantity. Recorded rather than normalized: the two modules' documents are separate, and picking one is the repository's call.
- **Whether these are service capabilities at all is still open.** [service.md](service.md) asks whether `seat`/`timing-interval`/`number` are "service-specific or general schedulable-resource capabilities that other domains (estate, device) also want", and every one of the edge documents repeats it. Nothing in the conversion bears on it — but it does now have a cost: each edge is a concrete record with its own storage abstraction, so moving them into a `schedulable` module means moving four storages.
- **`ServiceModel` composes `ThingModel` twice, once directly and once through `ProductModel`.** Faithful to the Go, which listed both. `ProductModel` already extends `ThingModel`, so the direct entry is redundant; it is harmless (composition is transitive) and left in place rather than silently narrowing the Go's declaration.
- **No data model carries the seat's own identity.** `ItemSeatDataModel` keys on `Field_InvoiceItemID` + `Field_SeatID`, where `Service_SeatID` is a `U64` seat number, not a reference. [item-seat.md](edges/item-seat/item-seat.md) lists exactly this as its first open question — "seat id vs seat node" — and the conversion answers nothing: `Service_SeatID` remains a number, so the seating map, the capacity and the seat type in `SeatDataModel` cannot be connected to the seat a line occupies. That is the same shape of gap [money.handoff.md](../money/money.handoff.md) records for `Money`: two halves of a fact and no requirement joining them.

## Related Artifacts

- [service.md](service.md) — the pluggable placement argument and the shared-parent question with `good`.
- [item-seat.md](edges/item-seat/item-seat.md), [number.md](edges/number/number.md), [multiple-use.md](edges/multiple-use/multiple-use.md), [timing-interval.md](edges/timing-interval/timing-interval.md) — the four edge documents, each carrying its own placement verdict and open questions.
- [estate.md](edges/estate/estate.md) — the undocumented relation, and the `LimitTo` vocabulary question with POS.
- [money.handoff.md](../money/money.handoff.md), [discount.handoff.md](../discount/discount.handoff.md), [voucher.handoff.md](../voucher/voucher.handoff.md) — the sibling economics pluggables this module sits beside.

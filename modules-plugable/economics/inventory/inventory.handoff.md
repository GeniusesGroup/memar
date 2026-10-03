# Inventory Handoff

Load-bearing state for the inventory module: why its one protocol file is unconverted, which stale paths in it are evidence of a real placement question, and what the model still does not state. Paired with [inventory.md](inventory.md).

## Status

Active — nothing converted; `protocol/inventory-notify.kh` is blocked on the notification domain, and the domain's own record identity is unstated everywhere.

## What is not converted, and why

### `protocol/inventory-notify.kh` — blocked on `computer/notification`

The Go declares one interface, `ProductInventoryNotify`, over the fields `Field_NotificationID`, `Field_ProductID`, `OrgID() []org_p.UUID`, `WarehouseID() []estate_p.UUID`, `AmountOperator() []logic.ComparisonOperator`, `Amount() []int64`, `StockOperator() []logic.ComparisonOperator`, `Stock() []int64`, `Field_RequestID` and `Field_Request`.

Six of those bind today. Four do not, and one of the four is fatal:

- **`notification_p.Field_NotificationID` has no declaration anywhere.** `modules/computer/notification/protocol/dt-uuid.kh` is unconverted — it holds only its Go clue block — and no `.kh` in either repository declares `Field_NotificationID`. It is the record's endpoint: without it the notify record cannot be traced to the notification it governs, which is the same defect [bookkeeping.md](../../../economics/account/edges/bookkeeping/bookkeeping.md) calls worthless for audit. Declaring a local `Field_InventoryNotifyID` would give the notification domain's concept a second owner, so the file stays unconverted rather than shipping a record that compiles and cannot be traced.

  What unblocks it is one abstraction in another domain: `tp Field_NotificationID ab` plus `tp NotificationID mt (self Field_NotificationID) () (t ThingUUID)` in `modules/computer/notification/protocol/dt-uuid.kh`. That file is that domain's to write, not this one's.

  Everything else in the file is already verified and needs no other domain first:

  | Go | binds to |
  |---|---|
  | `product_p.Field_ProductID` | `org/modules/economics/product/protocol/dt-uuid.kh` |
  | `WarehouseID() []estate_p.UUID` | `org/modules/identity/estate/protocol/dt-uuid.kh` — `Field_EstateIDs`, already valued as `Array_ThingUUID`, so the plural needs no new type |
  | `request_p.Field_RequestID` | `memar/modules/process/request/protocol/dt-uuid.observers.kh` — `Observer_RequestID` |
  | `audit_time_p.Field_Request` | `memar/modules/process/time/protocol/dt-request.observers.kh` — `Observer_Time_Request` |
  | `logic.ComparisonOperator` | `memar/modules/math/logic/operator-comparison.kh` — declared, an `ab` |
  | `OrgID() []org_p.UUID` | no plural owner exists; see below |

### `_import/product-inventory/**` (9 files)

Legacy storage and query code over `libgo` — `ds.DataStructure`, Syllab codecs, `ganjine`/`pehrest` hash indexes, hard-coded to one SabzCity datastore. Same disposition as the economics, management, text and thing `_import` trees: legacy shims over a library the repository no longer has, re-stating identities the protocol owns. Not converted.

## Findings

### The `estate` path in the Go names a module that does not exist

The Go imports `estate_p "org/modules/rights/estate/protocol"`. There is no `modules/rights/` estate module in the tree. The owner is `modules/identity/estate/`, and it is already converted — so this is the second class of stale path in economics after the money one, and it points the same way: capabilities were filed under a domain namespace (`rights`) that does not own them, and the edge vocabulary moved to `identity`. `inventory.md` itself says nothing about estate or warehouse, so the document does not contradict the Go here; it is silent.

### The module has no record identity, and something else already assumes it has one

`inventory.md`'s Model is one line — `(batch)-[:product_inventory]->(invoice)` — and the module's only protocol file describes a *notify* record, not that edge. There is no `protocol/dt-uuid.kh` and no data model for the edge itself, so nothing in the tree declares what identifies an inventory record.

Meanwhile `modules-plugable/uri/number-serial/protocol/data_model.kh` composes `inventory_p.Field_InventoryID`, included from `org/modules/economics/inventory/protocol` — a path this repository has never had, exactly like the twenty-six money paths. So a module outside the domain already assumes the domain declares an inventory identity that no source states. That assumption was not converted into a declaration here: minting a public identity abstraction on the strength of one stale import and one line of Model would invent a concept, and the value type is genuinely undecided (`ThingUUID` from `identity/thing`, or `ThingUUID` reached through `Field_EdgeID` from `knowledge/edge`, since this record is an edge between two other domains' nodes). Recorded here so the domain's own next pass settles it deliberately.

### Two parallel arrays model one thing each

`AmountOperator() []logic.ComparisonOperator` alongside `Amount() []int64` is a pair of parallel slices with an implied index correspondence: operator *i* applies to threshold *i*. The same for `StockOperator()`/`Stock()`. Nothing in the type says the two runs have the same length, and nothing says what a shorter run means — which is the difference between "notify when any of these thresholds is met" and "notify at the *n*-th threshold", two different rules that the shape cannot distinguish. A single run of (operator, threshold) pairs is what the record means. This is a modeling change, not a conversion, so the conversion should not cement the parallel-array shape.

### The thresholds are quantities, not `int64`

`Amount() []int64` and `Stock() []int64` are stock and money thresholds on one product, in one record, with no unit. The repository's settled quantity representation is `Decimal_Quantity` (`memar/modules/math/decimal/protocol/dt-quantity.kh`), which is what `bookkeeping`'s `Field_Balance` and `transaction`'s `Observer_Quantity` are valued as, and what money's `Amount` was settled to on 2026-10-03. Valued as `S64`, these fields would reintroduce the primitive-obsession shape the quantity type exists to prevent, and a threshold with no unit cannot be checked against a stock level that has one.

## Open Questions

- **Which organizations does a notify record cover, and who owns that plural?** `identity/organization/protocol/dt-uuid.kh` declares `Field_OrganizationUUID` (singular, valued as `UserUUID`) and no plural, while `identity/estate` and `management/group` and `knowledge/label` all declare their plurals. Either the organization domain gains `Field_OrganizationsUUID` with its array type — the consistent answer — or inventory declares a locally qualified array as `rights/delegate/protocol/storage.kh` does with `Array_GivenDelegateUserUUID`. Recorded rather than decided because the first answer belongs to another domain.
- **Is `(batch)-[:product_inventory]->(invoice)` a shortcut edge, and whose is it?** Under the core-vs-pluggable rubric a shortcut edge is owned by the capability module that gives it meaning, never as a separate module. If the inventory record is a re-derivation of a stock level at a warehouse, then neither `batch` nor `invoice` owns it and the module that owns stock does. `inventory.md` states the edge and nothing else about its semantics — who may create or remove it, what it triggers — which is the rubric's "no bare edges" test failing on the domain's only model statement.
- **`inventory.md` has no Placement section**, unlike `money.md`. The `____Chats/core-vs-pluggable.wave1.md` audit recorded inventory under "Pluggable economics KEEP", but the durable argument for it lives nowhere in the domain. The stale estate and inventory paths above are the kind of evidence a Placement section should carry.

## Related Artifacts

- [inventory.md](inventory.md) — model, idea backlog (transfer re-index, record indexes, index write retry).
- [`../batch/edges/cost/protocol/data_model.kh`](../batch/edges/cost/protocol/data_model.kh) — the other economics file importing a money path this module's conversion now unblocks.
- [`../../../uri/number-serial/protocol/data_model.kh`](../../../uri/number-serial/protocol/data_model.kh) — the consumer that already assumes `inventory_p.Field_InventoryID`.

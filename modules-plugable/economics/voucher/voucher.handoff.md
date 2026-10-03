# Voucher Handoff

Load-bearing state for the voucher module: which facets converted, the absence contract the Go left as a stub, and the two facet files that are blocked on other domains. Paired with [voucher.md](voucher.md), which owns the model and the definition.

## Status

Active — every facet whose types exist is converted; two files are blocked on other domains and two more are unconvertible as they stand.

## Khayyam conversion (2026-10-03)

Converted, all returning `accept`:

| File | Declares |
|---|---|
| `protocol/dt-each.kh` | `Voucher_Each ab { U8 }`, `Field_Each`, `Each`, `IsNull` |
| `protocol/dt-max_each_use.kh` | `Voucher_MaxEachUse ab { U8 }`, `Field_MaxEachUse`, `MaxEachUse`, `IsNull` |
| `protocol/dt-proportion.kh` | `Voucher_Proportion ab { Myriad }`, `Field_Proportion`, `Proportion`, `IsNull` |
| `protocol/dt-worth.kh` | `Voucher_Worth ab { Amount }`, `Field_Worth`, `Worth`, `IsNull` |
| `protocol/dt-invoice-type.kh` | `Voucher_InvoiceType ab { U8 }`, `Field_InvoiceType`, `InvoiceType` |
| `protocol/duration.kh` | `Voucher_Duration ab { Field_Each Observer_Epoch Observer_Duration_Second }` |
| `protocol/estate.kh` | `Voucher_Estate ab { Field_EstateID }` |
| `protocol/group.kh` | `Voucher_Groups ab { Field_GroupsID }` |
| `protocol/invoice.kh` | `Voucher_Invoice_Condition`, `Voucher_Invoice_ID`, `Voucher_Invoice_Type`, `Voucher_Invoice_MaxUsage` |
| `protocol/label.kh` | `Voucher_Labels ab { Field_Each Field_LabelsID }` |
| `protocol/product.kh` | `Voucher_Product ab { Field_Each Field_ProductsID }` |
| `protocol/user.kh` | `Voucher_User_ID ab { Field_UserUUID }` |
| `protocol/value.kh` | `Voucher_Value ab { Field_Each Field_Proportion Field_Worth Field_FinancialCurrencyID }` |
| `analytics/voucher_issued-utc_hour/protocol/data_model.kh` | the two issued observers, `VoucherIssuedUtcHourDataModel` |
| `analytics/voucher_issued-utc_hour/protocol/storage.kh` | `VoucherIssuedUtcHourStorage` + `Save`/`Get` |
| `analytics/voucher_issued-utc_minute/protocol/data_model.kh` | the two issued observers, `VoucherIssuedUtcMinuteDataModel` |
| `analytics/voucher_issued-utc_minute/protocol/storage.kh` | `VoucherIssuedUtcMinuteStorage` + `Save`/`Get` |

## Decisions

### `Optional() bool { return false }` became `IsNull() (b Boolean)`

Four of the Go's value types — `Each`, `MaxEachUse`, `Proportion`, `Worth` — each carried a method `Optional() bool` whose body was a hardcoded `return false`. That is an absence hook the author left unfilled: it says "this field may be absent" in the signature and "it never is" in the body, and with four identical stubs it is plainly a placeholder rather than a decision.

Khayyam has no `nil` and absence is a method on a type's contract, and the repository's convention for that query is `IsNull()`. So each of the four `Field_*` abstractions now requires `IsNull() (b Boolean)`, valued with `Boolean` — the abstraction — rather than `Bool`, because a signature owned by an abstraction names the concept.

What this buys and what it costs: the contract now says the question exists, which is what a rule evaluator needs to ask ("is there a cap on this use of the voucher?"). What it does not do is answer it — the Go never decided whether any of these can be absent, and neither does [voucher.md](voucher.md). The `Voucher_Value` facet in particular requires `Field_Proportion` *and* `Field_Worth` while the definition says the voucher "is worth a certain monetary value", which suggests the proportion is the optional one and the worth is not. That is a domain question, left open below.

### `Duration() duration.Second` became `Observer_Duration_Second`

The Go named both the accessor `Duration` and the type `duration.Second`, and `Second` is a capsule. The abstraction memar provides for "a duration measured in seconds" is `Observer_Duration_Second` in `modules/time/duration/protocol/second.observers.kh`, whose accessor is `GetDuration`. Composing it says the same thing without putting a capsule in an abstraction signature or a name collision in the file. The Go's own comment — "from Epoch()" — is why `Observer_Epoch` is composed alongside it: the duration is only meaningful relative to the epoch it is counted from.

### The analytics bucket key is valued as `Container_ElementIndex`

Both analytics storages take the bucket as the Go's `utc.HourElapsed` and `earth.Minute`. Neither type is declared anywhere — `modules/time/earth/duration-hour.kh` is an empty file and `duration-minute.kh` carries only its Go clue block — so there is nothing to import. Both are "which bucket of the time axis is this record", which is what `Container_ElementIndex` names in this repository ("the location of given element in the container"), and it is the type the bookkeeping storage already uses for an ordinal key (`Field_TransactionIndex`).

This is a substitution, not a faithful binding, and it is the weakest conversion in this domain: an element index carries no epoch and no unit, so nothing in the signature says the bucket is an hour or a minute. What would make it exact is a `HourElapsed`/`MinuteElapsed` *abstraction* in memar's `time` module — the observer halves exist, the value halves do not. That is memar's file to add, not this domain's.

### Stale import paths, three of them

- `value.kh` imported `fc_p "org/modules/economics/currency/protocol"`. There is no such module. The owner is `org/modules/identity/thing/edges/count_unit/labels/currency/protocol`, already converted, which declares `Field_FinancialCurrencyID` valued as `ThingUUID`. [currency.md](../../../identity/thing/edges/count_unit/labels/currency/currency.md) is explicit that the currency label lives on a count unit, so the binding is right and not merely the nearest available name.
- `invoice.kh` imported `money_p "org/modules/economics/money/protocol"`; the module is at `modules-plugable/economics/money/`.
- `voucher_issued-utc_minute`'s storage imported `memar/time/earth` for `Minute`; nothing is declared there.

## Unconverted, and what blocks it

- **`protocol/pos.kh`** — blocked on `pos_p.Field_PosID`; `modules-plugable/economics/pos/protocol/dt-uuid.kh` is unconverted. Same blocker as [discount.handoff.md](../discount/discount.handoff.md)'s.
- **`protocol/user.kh`'s second half** — the Go declared both `User_ID` and `User_Type` in one file. `User_Type` is blocked on `user_p.Field_UserType`, which nothing in the tree declares; a user *type* has no constants list in any `.kh`. `Voucher_User_ID` converted, `User_Type` did not. Splitting them into two files would make the second one its own file with no declaration in it, so the Go's file was left as it is with half converted.
- **`_import/voucher/storage_mysql.sql`, `_import/voucher/storage_volatile-memory.kh`** — legacy storage over a SQL schema and an in-memory map, from before the repository's storage engine. Same disposition as the economics, management, text and thing `_import` trees. Not converted.
- **`pages/voucher.{css,html,js}`, `pages/vouchers.{css,html,js}`** — GUI assets, not Khayyam source. Untouched.

## Open Questions

- **`Field_MaxEachUse` is composed by nothing.** `dt-max_each_use.kh` declares it in the Go and it is now declared here, and no other file in the module composes it — not `Value`, not `Invoice_MaxUsage`, not `Usage`. So the cap on how many times one voucher may be used is declared but unreachable: nothing carries it. Either the per-use cap belongs on `Voucher_Value` next to `Field_Proportion` and `Field_Worth`, or `Voucher_Invoice_MaxUsage`'s `MaximumInvoice` is what the cap means and `Field_MaxEachUse` is a leftover. The Go has the same orphan; this is a source gap.
- **`Voucher_Each` has no meaning beyond a width.** `Each uint8` carries the comment "Each time use", no constants, and no accessor using it. `Field_Each` is composed by `Duration`, `Invoice_Condition`, `Labels`, `Product` and `Value`, so five facets answer a question nobody has phrased. Whether a voucher condition applies per use, per invoice, or per line is exactly the distinction `Each` is named for, and nothing in [voucher.md](voucher.md) or the Go says which.
- **Four absence contracts, none decided.** `Field_Each`, `Field_MaxEachUse`, `Field_Proportion` and `Field_Worth` each now require `IsNull()`; see the decision above for what that does and does not settle.
- **`Voucher_Invoice_Condition`'s `MinPrice` says in what currency.** The Go's comment is "Minimum invoice price, currency depend on voucher value" — the amount has no unit of its own and borrows the voucher's. As converted, `Voucher_Invoice_Condition.MinPrice()` returns an `Amount` and the currency lives on a different facet (`Voucher_Value`). Nothing connects them, which is the same gap [money.handoff.md](../money/money.handoff.md) records for `Money` itself: the pairing exists but no requirement says the amount is on the named currency's scale.
- **The module's rule record is nowhere.** `voucher.md`'s Model is `(rule)-[:voucher]->(---)`, and no protocol file declares the voucher rule node, its own identity, or a data model composing the facets — the same gap [discount.handoff.md](../discount/discount.handoff.md) records for discount. Voucher and discount are near-identical modules (same thirteen-ish facets, same `(rule)-[:X]->(---)` edge, both import the same money amount) and both state it without a record type. Whether one rule type with two labels is the right model, or two capabilities that happen to share a shape, is unasked.
- **`voucher.md` has no Placement section** and no Open questions section, unlike `money.md`. The wave-1 core-vs-pluggable audit recorded voucher under "Pluggable economics KEEP" without a durable argument here.

## Related Artifacts

- [voucher.md](voucher.md) — model and the definition of a voucher as a bond.
- [discount.handoff.md](../discount/discount.handoff.md) — the same facet architecture in the sibling module, including the two shared blockers (`Field_PosID`, `Field_UserType`).
- [money.handoff.md](../money/money.handoff.md) — the `Amount` and `Field_FinancialCurrencyID` declarations this module includes.
- [currency.md](../../../identity/thing/edges/count_unit/labels/currency/currency.md) — why the currency is a count-unit label rather than a field of the amount.

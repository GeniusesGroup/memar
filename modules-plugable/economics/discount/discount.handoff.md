# Discount Handoff

Load-bearing state for the discount module: which rule facets converted and which are blocked on other domains, what the facet shape turns out to be, and the modeling gaps the conversion exposed. Paired with [discount.md](discount.md), which owns the model and the placement of the analytics and packages sub-domains.

## Status

Active — every facet whose types exist is converted; three files are blocked on other domains and one on an open modeling question.

## Khayyam conversion (2026-10-03)

Converted, all returning `accept`:

| File | Declares |
|---|---|
| `protocol/dt-type.kh` | `Discount_Type ab { U16 }` |
| `protocol/location.kh` | `Discount_Location ab { Field_EstateID }` |
| `protocol/group.kh` | `Discount_Group ab { Field_GroupID }` |
| `protocol/user.kh` | `Discount_User ab { Field_UserUUID }` |
| `protocol/product.kh` | `Discount_Product ab { Field_ProductID }` + `MinAmount`/`MaxAmount`/`MinPrice`/`MinStock`/`Type` |
| `protocol/label.kh` | `Discount_Label ab { Field_LabelID }` + the same five accessors |
| `protocol/invoice.kh` | `Discount_Invoice ab` + `MinPrice`/`MinAmount` |
| `protocol/time-validity.kh` | `Discount_TimeValidity ab` + `Start`/`End` |
| `protocol/timing-utc.kh` | `Discount_TimingUTC ab` + `AllowedWeekdays`/`AllowedDayHours` |
| `protocol/usage.kh` | `Discount_Usage ab` + `MaximumInvoice` |
| `protocol/value.kh` | `Discount_Value ab` + `MaximumMyriad`/`MaximumPrice` |
| `analytics/discount_usage-utc-day/protocol/data_model.kh` | `Observer_DiscountUsageUtcDay_TotalRedeemed`, `..._TotalRedeemedAmount`, `DiscountUsageUtcDayDataModel` |
| `analytics/discount_usage-utc-day/protocol/storage.kh` | `DiscountUsageUtcDayStorage` + `Save`/`Count`/`Get` |
| `analytics/discount_usage-utc-minute/protocol/data_model.kh` | the minute pair, `DiscountUsageUtcMinuteDataModel` |
| `analytics/discount_usage-utc-minute/protocol/storage.kh` | `DiscountUsageUtcMinuteStorage` + `Save`/`Count`/`Get` |
| `analytics/price-payable/protocol/data_model.kh` | `Observer_PricePayable_Price`, `PricePayableDataModel` |
| `analytics/price-payable/protocol/storage.kh` | `PricePayableStorage` + `Save`/`Count`/`Get` |

## Decisions

### Every facet name is qualified with the module

The Go named its thirteen facet interfaces `Area`, `Group`, `Invoice`, `Label`, `Location`, `POS`, `Product`, `TimeValidity`, `TimingUTC`, `Usage`, `User`, `UserType`, `Value`. None survives bare: `Value` is declared by memar's `flag.kh`, `Location` is a method name in memar's `pagination.kh`, and the rest are exactly the bare words the qualified-names rule calls out. They are declared `Discount_<Facet>`.

The alternative — leaving them bare and letting the collision surface at the first import — is what the language document says not to do, and Khayyam has no alias to soften it.

### `LabelType` and `Type` were one concept and are now one declaration

`label.kh` declared `LabelType uint16` and `product.kh` declared `Type uint16`, with the same three constants (`Unset`, `Mandatory`, `Pair`) and the same trailing comment on each. Two names for one thing, in one module. It is declared once as `Discount_Type` in the new `protocol/dt-type.kh`, composing `U16` the way `management/authorization/protocol/dt-policy.kh` does for `GroupPolicy`, and both facet files include it.

### `Quantity() per.Myriad` and `Price() fmp.Amount` were renamed to say what they are

Both are ceilings — the Go's own comments read "max discount percentage" and "max discount price". `Quantity` was the worse of the two names by a wide margin: it names a quantity while returning a per-ten-thousand ratio, so a caller reading the signature learns nothing about the unit. They are `MaximumMyriad` and `MaximumPrice` on `Discount_Value`, which puts both caps of the same discount under one word and matches `Discount_Usage`'s existing `MaximumInvoice`. Recorded because a repository-wide naming sweep should see these as decided, not as pending.

### `Weekdays`/`DayHours` accessors were qualified

The types `Weekdays` and `DayHours` are included from memar and the Go's accessors had the same two names, so the bare form would have put two declarations of one word in one file. They are `AllowedWeekdays` and `AllowedDayHours` — the Go comment already said "what days in weekday in utc time week allow to use this discount", so the word is the comment's, not a new one.

### The `estate` and money import paths were repointed, not copied

- `area.kh` and `location.kh` imported `org/modules/rights/estate/protocol`, a path that does not exist. The owner is `org/modules/identity/estate/protocol`, already converted.
- Every money import said `org/modules/economics/money/protocol`. The module is at `org/modules-plugable/economics/money/protocol/`, deliberately outside core; [money.handoff.md](../money/money.handoff.md) records the reasoning and the fact that a core file importing it is a core-to-pluggable dependency.
- `timing-utc.kh` imported `memar/time/earth` for `Weekdays` and `DayHours`. Those two types moved to `memar/modules/time/utc/weekday.kh` and `dayhour.kh`; `modules/time/earth` has no such declarations at all. Third class of stale path in economics after money and estate, and this one crosses repositories.

### `currency uint64` became `Field_CountUnitID`

`price-payable`'s Go had `Currency() uint64` — a bare integer naming a currency, and the storage `Count`/`Get` keyed on it the same way. [price-payable.md](analytics/price-payable/price-payable.md) says the edge is `(product)-[:price_payable]->(count_unit)`, so the record is valued as `Field_CountUnitID`, whose value type is `ThingUUID`; the storage parameters follow as `ThingUUID`.

The document's word is the wider one, so this follows the document and not the Go's narrower `Currency`. If the owner wants the currency-only reading, `Field_FinancialCurrencyID` is declared and already valued as `ThingUUID` — the substitution is one import line.

### Analytics facets became `Observer_*`; rule facets did not

The two analytics sub-domains are data models, and a data model in this repository is a composition of field abstractions, each carrying its own accessor declared in the same file — the shape `computer/instance_of/edges/resource/protocol/data_model.kh` and `management/group/edges/membership-term-member_limit/protocol/data_model.kh` already use. So `TotalRedeemed` and `TotalRedeemedAmount` are `Observer_DiscountUsageUtcDay_*` / `Observer_PricePayable_*` abstractions with `Get*` accessors, composed into the data model.

The thirteen rule facets were left as one abstraction each with its conditions as accessors. They are not data models and not `Field_*` surfaces — a facet with `MinPrice()` and `MinStock()` is a rule aspect, and turning each condition into its own field abstraction would multiply thirteen interfaces without adding a contract. Rule 2's generator applies to getter/setter boilerplate over fields, which these are not. Recorded so the two shapes do not look like an inconsistency.

## Unconverted, and what blocks it

- **`protocol/pos.kh`** — blocked on `pos_p.Field_PosID`. `modules-plugable/economics/pos/protocol/dt-uuid.kh` is unconverted and declares nothing; the Go's `UUID` there is a `thing_p.UUID`, so the binding will be `ThingUUID`. One abstraction in the POS domain unblocks it.
- **`protocol/user-type.kh`** — blocked on `user_p.Field_UserType`. `modules/identity/user/protocol/dt-uuid.kh` declares `UserUUID`, `Field_UserUUID` and `UserID` and nothing else. What a user *type* is has no statement anywhere in the tree — the constants list does not exist in any `.kh`. This is not only a conversion blocker: a discount that applies to "users of type X" has no modelled X.
- **`protocol/area.kh`** — the Go's `Area` interface and `Location` interface were structurally identical (both compose only `Field_EstateID`), and the comment distinguishing them — a region rather than a specific point — is prose, not a type. Declaring both would be two abstractions that any estate-valued record satisfies at once. The one declaration is `Discount_Location` in `location.kh`; the distinction moved into [discount.md](discount.md)'s Model. `area.kh` keeps its clue block and now holds no Khayyam; the main session may delete it or fold the comment's content further.
- **`packages/protocol/business-services.kh`** — blocked on an open modeling question, not on a missing type. [packages.md](packages/packages.md) asks: "is the bundle a named node (packages/mealDeal) or just a rule grouping products?" and answers that the `maxNum` caps "look like node state" while "some rules may limit the bundle" "looks like rules *on* the node — confirm both layers." The Go carries no interface here at all, only the struct `mealDeal` with two slices of anonymous structs — which is a concrete capsule in a `protocol/` package, already a rule-1 violation. Declaring an abstraction for it now would ratify the answer to the open question. When it is settled, the shape is two named run types (products with a cap, label categories with a cap) each composing `Field_ProductID` or `Field_LabelID`, valued with `W64` (the Go said `int`, which has no Khayyam type), composed by whatever the node/rule answer turns out to be.
- **`analytics/discount_usage-utc-minute/protocol/data_model.kh` lost a field.** The Go had `request_p.Field_RequestID` commented out; only `audit_time_p.Field_Request` is live. The converted model composes `Observer_Time_Request` alone. If the request id is wanted on this record, add `Observer_RequestID` — the day-bucket record has it.

## Open Questions

- **The invoice and usage facets have no subject.** `Discount_Invoice` declares `MinPrice` and `MinAmount` and no reference to any invoice; `Discount_Usage` declares `MaximumInvoice` and no reference to anything. Every other facet composes an identity field (estate, group, user, product, label). As converted, a record satisfying `Discount_Invoice` says what the minimum is but not which invoice it governs, and the two facets are also the only two that are structurally satisfied by accident — `Discount_Invoice` is a two-method interface with no identity, so almost anything with those two accessors qualifies. The Go had the same gap; this is a source gap, not a conversion loss. `Field_InvoiceID` is declared (`modules/economics/invoice/edges/item/protocol/dt-uuid.kh`) and would be the binding; what the *usage* facet attaches to has no candidate at all.
- **`Discount_TimeValidity` has no absence.** `Start()` and `End()` return `Time` and the language has no `nil`; per the lifecycle-method-names rule absence is a method on the contract, and there is none. A discount with no end date and one that ends at the epoch are indistinguishable as converted. `IsNull()` on the facet, or an explicit open-ended flag, is the missing behavior.
- **`MinStock`'s "0 for unlimited" is a sentinel value.** The Go comment says "0 for unlimited until related product exist to sell", so zero carries two meanings and absence is not expressible. The same sentinel pattern is in `discount_usage-utc-day`'s `Count()`-less `Get` and in `price-payable`'s `Currency`. Whether these are worth an explicit absence contract is a domain call.
- **`discount.md` has no Placement section.** The wave-1 core-vs-pluggable audit recorded discount under "Pluggable economics KEEP", and the document's last paragraph does say analytics "must not return to core Invoice or Product" — but the pluggable argument itself lives nowhere durable.
- **The module's rule record is nowhere.** `discount.md`'s Model is `(rule)-[:discount]->(---)` — the edge is stated, but no protocol file declares the discount rule node, its own identity, or a data model composing the facets. The facets are thirteen separate abstractions that nothing composes, so "a discount" has no type. Whether the rule node belongs to `computer/rule` (the repository's rule domain) or to discount as its own record is unstated, and it is the same question `packages.md` asks for the bundle.

## Related Artifacts

- [discount.md](discount.md) — model, policies, placement of analytics and packages.
- [packages.md](packages/packages.md) — the node-vs-rule question blocking `business-services.kh`.
- [price-payable.md](analytics/price-payable/price-payable.md) — the `(product)-[:price_payable]->(count_unit)` edge the unit field follows.
- [money.handoff.md](../money/money.handoff.md) — the `Amount` declaration six of these files import.

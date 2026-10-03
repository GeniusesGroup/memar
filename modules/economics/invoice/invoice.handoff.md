# Invoice Handoff

## Topic & Purpose
Load-bearing commercial decisions that attach to Invoice: adjustment/aggregation field naming, party-role distinctions (customer / buyer / consumer), and core-vs-optional placement relative to organizational purpose. Migrated from the Organization ideas backlog (2026-09-16).

## Status
Active — party-role and core-vs-optional decided; invoice adjustment field naming still open.

## Decisions

### From Organization ideas backlog

- **Invoice should not carry a `discount` field.** Omid's proposal: an aggregation method (`RulePrice() → money_p.Amount`) summing all rules that applied (vouchers + discounts + gift + auctions); counter-argument recorded: naming the field after its cause (`RulePrice`) imports causality into the model and breaks when an adjustment comes from something that is not a rule (cost allocation, carbon tax, currency adjustment) — alternatives `PriceAdjustment` / `AdjustmentAmount` left Pricing to reveal composition. *(naming — open for the org)*
- **Customer ≠ buyer ≠ consumer.** A restaurant order may be placed by one person and consumed by two; the model connects through *User* with distinct identity edges per role. Care applies even in examples — dozens of "financial account" kinds differ only in unit, not in the nature of the account concept. *(decided)*
- **Core vs. optional is relative to purpose.** Discount without which the organization still buys and sells; Product/Invoice/Account without which an ERP is unrepresentable — but the attribute is not intrinsic to the module (a charity or a government has "sales" too). *(decided)*

## Open Questions
- Field naming for the invoice adjustment aggregation (`RulePrice` vs. `PriceAdjustment`) and the quantity-bookkeeping concept's final name. *(from consolidated open-questions backlog #10 — invoice half)*

## Related Artifacts
- [`README.md`](README.md)
- [`../product/product.handoff.md`](../product/product.handoff.md)
- [`../../../modules-plugable/economics/pricing/edges/pricing/README.md`](../../../modules-plugable/economics/pricing/edges/pricing/README.md)
- Invoice party edges: [`edges/user-customer`](edges/user-customer/README.md), [`edges/user-buyer`](edges/user-buyer/README.md), [`edges/user-consumer`](edges/user-consumer/README.md)

## Notes
- Provenance: Organization ideas backlog → Commercial / organizational concepts (2026-09-16 migration).
- **Enterprise-software foundations are stable.** The bases of organizational systems have not changed in ~200 years when modeled correctly; the churn ("requirements") is evidence of a bad model, not of a changing business — DDD attempted this correction but propagated wrong readings (its examples blurred the concepts). *(Omid's working thesis)*

## Khayyam conversion (2026-10-03)

Converted: `protocol/dt-uuid.kh` (`Field_InvoiceID` → `InvoiceID`, valued as `ThingUUID` imported from `identity/thing`), `edges/item/protocol/dt-uuid.kh` (`Field_InvoiceItemID` → `InvoiceItemID`, same value type), and `edges/item/protocol/gui-widget.kh`. All three return `accept` from the Khayyam frontend.

Decisions:

- **No local `InvoiceUUID` abstraction** for the Go's `type UUID thing_p.UUID`; `ThingUUID` is imported, matching the rule/module/taxon/estate/ownership conversions and rule 6.
- **`gui-widget.kh`'s two interfaces were qualified, not left bare.** Eight modules in the tree declare `GUI_Widget_Conditions` / `GUI_Widget_Service`, so the plain name would collide on import; they are declared `Invoice_ItemGUIWidget_Conditions` and `Invoice_ItemGUIWidget_Service`, following the shape `knowledge/question/widgets/question/gui.kh` already uses (`Question_GUI_Widget`). This is the first of that family to be converted — the other seven still carry the bare Go spelling in their clue blocks and will need the same treatment when their domains are converted, or a shared `GUI_Widget_Conditions` abstraction will have to be recognised as one concept declared many times.

### Unconverted, and what blocks it

- **`edges/item/protocol/data_model.kh` — blocked on the money module.** Four of its fields return `money_p.Amount`: `SuggestedPrice`, `DiscountedPrice`, `RulePrice`, `PayablePrice`. No `.kh` in the tree declares an `Amount`, and the path the Go names — `org/modules/economics/money/protocol` — does not exist; the module is at `modules-plugable/economics/money/`, whose `dt-money-amout.kh` is itself unconverted and whose own document lists "`int64` scaling vs `decimal_p.Quantity` used on bookkeeping fields — reconcile the two quantity representations" as unresolved. Declaring a local amount type here would give two owners of one concept. Until money declares an amount, this file cannot be written without either dropping four fields or inventing a type.
- **`edges/item/protocol/storage.kh` — blocked transitively.** Its signatures are `Get(invoiceID, productID)` and the two `FIND_*_BY_*` queries, none of which need money, but it names `DataModel`, which is the file above. Converting it first would produce a file importing a name its target does not declare.
- **`_import/invoice/**`, `_import/invoice-voucher/storage.sql`** — legacy service/storage code (Syllab/JSON codecs, `ds.DataStructure`), same disposition as product's `_import`: delete or re-model, not convert.

### Open from this pass

- **`invoice.md` has no `## Model` section.** Every other economics domain states its record fields and edge set; invoice states a purpose ("ChangeOwner of products"), a definition, and discussion. So the invoice record's own fields — as opposed to the `item` edge's — have no statement anywhere in the domain, and nothing in this pass could be derived from the document rather than from the Go. This is worth closing before invoice reaches the data-model pass: which fields the invoice record itself carries (total, currency, issue date, parties) is exactly what `item`'s aggregation and the `status/` folders assume.
- **`RulePrice` naming is still open** and this pass could not settle it — the Go already carries `RulePrice()`, and the Decisions section above keeps it open between `RulePrice` and `PriceAdjustment`. The converted `item` files do not touch it (the field lives in the blocked `data_model.kh`), so nothing is frozen either way.

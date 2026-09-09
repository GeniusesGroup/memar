# Good

A good is a physical/economic item tracked for inventory. It is pluggable, not core: each organization may draw the good/service boundary differently, and the accounting kernel works fine without any of them — a transaction over an account whose `count_unit` is "kg" needs no `good` node at all. What this module adds is inventory-facing semantics (`reserve-quantity`, `best_before`, `material`, `branch`) attached to products/stocks as capabilities.

## Discussion

### Drawbacks

- Inventory semantics (`reserve-quantity`, `best_before`) are genuinely important for physical-goods organizations; keeping `good` out of core means those orgs must install a module to get behavior that feels "basic". Accepted: basic-to-one is optional-to-another (a pure-money or shares system has no goods).

### Rationale and alternatives

- Kept out of core per the capability test in [product](../../../modules/economics/product/README.md): good is one way an organization may specialize a priceable thing, not a structural requirement of invoice/transaction.
- Alternative rejected: making `good` core alongside product — it would force every deployment to carry inventory concepts and re-couple the kernel to the physical-goods frame the redesign removed.

### Prior art

- ERP "material master" / inventory item — here decomposed into product (core) + good capabilities (pluggable).

### Unresolved questions

- Is `good` a specialization edge of `product`, or an independent node type that products reference? (Same question for [service](../service/README.md) — resolve both together.)
- Do `batch` and `good` overlap on lot/expiry tracking, or is `batch` the right home for `best_before`?

### Future possibilities

- Barcode/serial identity for goods via the `uri` domain (reference-not-field), not as good-node attributes.

## Idea backlog from edge code comments

Raw proposals from comment notes in `edges/*.go` (comments remain in code as source). Nothing below is ratified.

- **Material model** (`edges/material/protocol/data_model.go`): product-material key/value description (mobile-cpu, pizza-cheese) with min/base/max quantities; PrimaryNode = product (Mobile, Pizza), SecondaryNode = material (cpu, pizza cheese) which can be a substitute; edge = material relation kind (internal tool, pizza topping). Open TODO: is user-manual detail entry good, or is a quiddity-model better?
- **Reserve quantity** (`edges/reserve-quantity`): fixed max-reserve count or percent of inventory.
- **Best before** (`edges/best_before`): duration from production time.
# Product
In marketing, a [product](https://en.wikipedia.org/wiki/Product_(business)) is an object, or system, or service made available for consumer use as of the consumer demand; it is anything that can be offered to a domestic or an international market to satisfy the desire or need of a customer.[1] In retailing, products are often referred to as merchandise, and in manufacturing, products are bought as raw materials and then sold as finished goods. A service is also regarded as a type of product.

## Definition in Memar

Product is core by necessity: an invoice claims something, and that something must be identifiable and priceable. The test is a capability, not a relation: any node in the graph can become a product if it can be priced (`price`; independently evolving `pricing` lives in [pricing](../../../modules-plugable/economics/pricing/edges/pricing/README.md)). Good and service are NOT core — each organization may draw those boundaries differently, so they are pluggable specializations. Multi-typing applies: a product node can simultaneously be a `thing` with a name, unit, or any other identity edge.

Confirmed positions from the boundary discussion (2026-08-05..09; argument and evidence in [product.handoff.md](product.handoff.md)):

- **Product ≠ Sellable/Commercial Product.** A product may never enter formal sale and still need warehousing, transfer, location, and history (museum pieces, an organization's furniture — the industry's separate "asset management" modules). "Sellable" is a status/identity from another domain, not a product subtype.
- **Product ≠ physical good.** A service is a product (the marketing definition above already says so) and may have no physical realization ever; "does it need physical realization?" is not a product boundary question.
- **Product identity can precede production** — even the invoice (a car ordered today, delivered in six months has product identity from day one).
- **A node can take Product and Content identities simultaneously** (an educational course; sold, freed, or role-restricted) — product being is the economic/asset-management lens, not a different object.
- **Spec-like nodes are products**: the designer's "rebar A3, 4400 kg/cm²" node — brandless, producerless — is itself a product that other products may satisfy. See the [`brand`](../../../modules-plugable/economics/brand/edges/brand/README.md) edge questions.

## Product relation to product

We need this module due to some product have many relation product e.g. same product have different color or size! Because each specific product **MUST** track individually for e.g. price or inventory.

Open question (from [product.handoff.md](product.handoff.md)): the confirmed model is **parent/child products without a Variant/SKU entity** — same shoe differing only in size = parent product + one child *product* per size (same for car color/trim). Children are independent product nodes; the parent is itself a product even with no direct realization/transaction. Still open: is the product-to-product relation a single parent/child edge, or do several relations hide here — split for review across the per-edge docs [variant](edges/variant/variant.md), [optional](edges/optional/optional.md), [material](edges/material/material.md), [supplier](edges/supplier/supplier.md).

## Part Number

A [part number](https://en.wikipedia.org/wiki/Part_number) (often abbreviated PN, P/N, part no., or part #) is an identifier of a particular part design or material used in a particular industry. Its purpose is to simplify reference that item. A part number unambiguously identifies a part design within a single corporation, sometimes across several corporations.

For example, when specifying a screw, it is easier to refer to "HSC0424PP" than saying "Hardware, screw, machine, 4-40, 3/4" long, pan head, Phillips". In this example, "HSC0424PP" is the part number. It may be prefixed in database fields as "PN HSC0424PP" or "P/N HSC0424PP". The "Part Number" term is often used loosely to refer to items or components (assemblies or parts), and it's equivalent to "Item Number", and overlaps with other terms like SKU (Stock Keeping Unit).

## Discussion

### Drawbacks

- The capability test ("anything that can be priced") makes Product potentially a label on any node; without care it becomes a catch-all.

### Rationale and alternatives

- Core by necessity: an invoice claims something, and that something must be identifiable and priceable. The alternative — invoices referencing any `thing` directly with Product as a pluggable label — was rejected because price/pricing semantics need a single home.
- Good/Service kept out of core: organizations draw those boundaries differently; fixing them in core would force one taxonomy on everyone.

### Prior art

- The marketing definition above is market-facing and broad; Memar's definition is narrower: the unit of priceability.

### Unresolved questions

- Are `price`/`pricing` kernel edges of product or rule-driven capabilities?
- Does a price belong to the product or to the batch? The owner leans to the batch (2026-10-10); if it does, what does "priceable" mean in the capability test above, and what plays the batch's part for a service? — [Pricing Research 001](../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions), [price](edges/price/price.md#open-questions).
- Relation of product to `count_unit`: is pricing always expressed in the account's unit?
- Core-ness must survive contact with non-retail priceables: tax lines, rent, penalties, pure services (an invoice billing only a fee/penalty). If these can be billed without a `product` node, the capability test ("anything priceable") needs tightening or the node becomes a catch-all.
- **Capability test vs asset-management reading** (from [product.handoff.md](product.handoff.md)): the confirmed position says products may never be sold nor priced (museum pieces, an organization's furniture — the industry's separate "asset management" modules) while remaining products for warehousing/transfer/history. If pricing is the core test, what carries the asset-management half — product itself, or the inventory/asset pluggable? Converge with the product handoff's open #6.

### Future possibilities

- Product taxonomy (category, variant) as pluggable modules over the core.

Bundle attachment is [packages](../../../modules-plugable/economics/discount/packages/packages.md). Pricing that evolves on its own is [pricing](../../../modules-plugable/economics/pricing/edges/pricing/pricing.md).


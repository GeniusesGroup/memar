# Product

In marketing, a [product](https://en.wikipedia.org/wiki/Product_(business)) is an object, or system, or service made available for consumer use as of the consumer demand; it is anything that can be offered to a domestic or an international market to satisfy the desire or need of a customer.[1] In retailing, products are often referred to as merchandise, and in manufacturing, products are bought as raw materials and then sold as finished goods. A service is also regarded as a type of product.

## Definition in Memar

Product is core by necessity: an invoice claims something, and that something must be identifiable and priceable. The test is a capability, not a relation: any node in the graph can become a product if it can be priced (`price`, `pricing` edges). Good and service are NOT core — each organization may draw those boundaries differently, so they are pluggable specializations. Multi-typing applies: a product node can simultaneously be a `thing` with a name, unit, or any other identity edge.

Confirmed positions from the boundary discussion (2026-08-05..09; argument and evidence in [product.handoff.md](product.handoff.md)):

- **Product ≠ Sellable/Commercial Product.** A product may never enter formal sale and still need warehousing, transfer, location, and history (museum pieces, an organization's furniture — the industry's separate "asset management" modules). "Sellable" is a status/identity from another domain, not a product subtype.
- **Product ≠ physical good.** A service is a product (the marketing definition above already says so) and may have no physical realization ever; "does it need physical realization?" is not a product boundary question.
- **Product identity can precede production** — even the invoice (a car ordered today, delivered in six months has product identity from day one).
- **A node can take Product and Content identities simultaneously** (an educational course; sold, freed, or role-restricted) — product being is the economic/asset-management lens, not a different object.
- **Spec-like nodes are products**: the designer's "rebar A3, 4400 kg/cm²" node — brandless, producerless — is itself a product that other products may satisfy. See the [`brand`](edges/brand/README.md) edge questions.

## Product relation to product

We need this module due to some product have many relation product e.g. same product have different color or size! Because each specific product **MUST** track individually for e.g. price or inventory.

Open question (from [product.handoff.md](product.handoff.md)): the confirmed model is **parent/child products without a Variant/SKU entity** — same shoe differing only in size = parent product + one child *product* per size (same for car color/trim). Children are independent product nodes; the parent is itself a product even with no direct realization/transaction. Still open: is the product-to-product relation a single parent/child edge, or do several relations hide here (variant-of, spec-parent, bundle-component)?

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
- Relation of product to `count_unit`: is pricing always expressed in the account's unit?
- Core-ness must survive contact with non-retail priceables: tax lines, rent, penalties, pure services (an invoice billing only a fee/penalty). If these can be billed without a `product` node, the capability test ("anything priceable") needs tightening or the node becomes a catch-all.
- **Capability test vs asset-management reading** (from [product.handoff.md](product.handoff.md)): the confirmed position says products may never be sold nor priced (museum pieces, an organization's furniture — the industry's separate "asset management" modules) while remaining products for warehousing/transfer/history. If pricing is the core test, what carries the asset-management half — product itself, or the inventory/asset pluggable? Converge with the product handoff's open #6.

### Future possibilities

- Product taxonomy (category, variant) as pluggable modules over the core.

## Idea backlog from edge code comments

Raw proposals from comment notes inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified. These intersect the confirmed positions above - review must reconcile.

### Type flags - edges/product.go
- **Idea**: one Type flag-space splitting Good vs Service. Good flags: Inventory (owner-tracked capital goods: book, mobile, car), Custom (made on buyer requirements, product-ingredient), BestBefore (daily consumption goods), CustomIngredient. Service structure comment: TimeService (consultation in chat or real life), ActService (guarding, maintenance, cleaning), Transport; service flags TimeValidity, Transport, Shipping, Content (digital data), Timing, TimingInterval, MultipleUse (gym), Duration, Number (cinema, concert, transport), Area, Place (doctor-room, gym, station, airport), Seat, Provider_Staff, Provider_Role, Share (panic-room ticket). Common: ReserveValidity, ReserveQuantity (max one person can reserve before paying), PreSale (marked ?? - unresolved), NeedApprove (product-role), NeedPrescription (medical goods, not user-addable to invoice), InvoiceSell / OrderSell, SellLimit_Role / SellLimit_Group / SellLimit_User.
- **Review questions**: is the Good/Service split a flag pair or two identity lenses (per the confirmed multi-typing position above)? Do SellLimit flags belong here or to the rule domain? PreSale semantics unresolved (marked ?? in code).

### Product relations - edges/product-relation-group.go, product-relation-staff.go, product-relation-user.go, product-relation-content.go
- **Idea**: product-to-group labels (Comment, QA, Buyers; Provider = product operator supplying a service; SellLimit to specific groups; coordinate lookup via RoleID); product-to-staff (SellLimit to specific staff, Provider, coordinate via StaffID); product-to-user; product-to-content. Coordinate-by-role/staff appears repeatedly - a UI concern leaking into labels?
- **Review questions**: do Provider/SellLimit duplicate role and delegation machinery? Is coordinate lookup a GUI concern to strip from the model?

### Product-to-product relations - edges/product-relation-product.go
- **Idea**: same product, different provider (owner, price); same product, different attributes; Optional; Material or Ingredient.
- **Review questions**: map these onto the parent/child model in "Product relation to product" above - are all four the parent/child edge, or distinct relations (variant-of, spec-parent, ingredient-of)?
### Rule relations - edges/product-relation-rule.go
- **Idea**: MealDeal / DiscountBundle (product is part of a discount bundle; rules may constrain the bundle, e.g. minimum buy number); Pricing rule (some services have more complex pricing logic than a product.Price field, e.g. transport).
- **Review questions**: does the pricing rule duplicate accounting-invariants #9 (fees are rules producing transactions)?
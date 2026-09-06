# Product

In marketing, a [product](https://en.wikipedia.org/wiki/Product_(business)) is an object, or system, or service made available for consumer use as of the consumer demand; it is anything that can be offered to a domestic or an international market to satisfy the desire or need of a customer.[1] In retailing, products are often referred to as merchandise, and in manufacturing, products are bought as raw materials and then sold as finished goods. A service is also regarded as a type of product.

## Definition in Memar

Product is core by necessity: an invoice claims something, and that something must be identifiable and priceable. The test is a capability, not a relation: any node in the graph can become a product if it can be priced (`price`, `pricing` edges). Good and service are NOT core â€” each organization may draw those boundaries differently, so they are pluggable specializations. Multi-typing applies: a product node can simultaneously be a `thing` with a name, unit, or any other identity edge.

## Product relation to product

We need this module due to some product have many relation product e.g. same product have different color or size! Because each specific product **MUST** track individually for e.g. price or inventory.

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

### Future possibilities

- Product taxonomy (category, variant) as pluggable modules over the core.

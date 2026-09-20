# Brand

## Model

- `(product)-[:brand_is]->(brand)`
- `(brand)-[:is_brand_for]->(product)`

## Policies (rules)

- as category of products belong to same commercial name.

## Open questions (from the Estate/Product session, 2026-08-05..09)

- **How is a brandless product represented?** The designer's BIM case: "rebar A3, tensile strength 4400 kg/cm^2, diameter 16" - precise enough for design and later friction-free purchasing, but no brand, no producer, no offering. The node must exist as a product (see [product.handoff.md](../../product.handoff.md)); the question is what edges identify it and how concrete products relate to it as *satisfying* it.
- **One product, many sellers, many internal names**: a marketplace selling the same IKEA sofa under each store's own marketing name is still one product. Is `brand` the edge that anchors this common identity, or does the anchoring belong to product-to-product / definition relations?
- **Definer != producer != seller**: a body like AISC can define a standard product without producing or selling it. Does the definer take a `brand`-class edge, a definition edge, or something else?

Related: [product.handoff.md](../../product.handoff.md) - open question "Product vs Product-Definition/Standard".

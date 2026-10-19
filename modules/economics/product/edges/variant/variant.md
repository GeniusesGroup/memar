# Variant

## Model

- Candidate (unconfirmed): `(product)-[:variant_of]->(product)` — "same product, different attributes": color, size, trim, … where each specific product MUST track individually for price and inventory.
- Confirmed parent/child substrate (from [product.md](../../product.md) "Product relation to product", argument in [product.handoff.md](../../product.handoff.md)): **parent/child products without a Variant/SKU entity** — same shoe differing only in size = parent product + one child *product* per size; children are independent product nodes; the parent is itself a product even with no direct realization/transaction.

## Policies (rules)

- Each specific product MUST track individually for e.g. price or inventory.
- Children are product nodes in their own right (multi-typing: a child is simultaneously a product and a variant).

## Placement

- **Not a new module; not core-by-necessity as a separate capability** — the parent/child product nodes are already product nodes (core keeps the product and its price edges); the *relation name* (variant-of vs single parent/child edge) is the open question, not a processing capability.
- Prefer the confirmed parent/child reading over inventing a Variant/SKU entity (handoff decision); a named `variant_of` edge is a vocabulary choice on that substrate, not a pluggable module.

## Open questions

- Is the product-to-product relation a single parent/child edge, or do several relations hide here (variant-of, spec-parent, bundle-component)? — standing question from [product.md](../../product.md), split across [variant](variant.md), [optional](../optional/optional.md), [material](../material/material.md), [supplier](../supplier/supplier.md).
- Where does the parent/child model live relative to bundle-component ([packages](../../../../../modules-plugable/economics/discount/packages/packages.md))?
- "Each specific product MUST track individually for price": if a price belongs to the batch, as the owner leans, does each variant still carry a price of its own, or only its batches? — [Pricing Research 001](../../../../../modules-plugable/economics/pricing/pricing.research.001.md#open-questions).


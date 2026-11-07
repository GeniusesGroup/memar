# Variant

## Model

- Candidate (unconfirmed): `(product)-[:variant_of]->(product)` — "same product, different attributes": color, size, trim, … where each specific product MUST track individually for price and inventory.
- Confirmed parent/child substrate (from [product.md](../../product.md) "Product relation to product"): **parent/child products without a Variant/SKU entity** — same shoe differing only in size = parent product + one child *product* per size; children are independent product nodes; the parent is itself a product even with no direct realization/transaction.

## Policies (rules)

- Each specific product MUST track individually for e.g. price or inventory.
- Children are product nodes in their own right (multi-typing: a child is simultaneously a product and a variant).

## Placement

- **Not a new module; not core-by-necessity as a separate capability** — the parent/child product nodes are already product nodes (core keeps the product and its price edges); the *relation name* (variant-of vs single parent/child edge) is the open question, not a processing capability.
- Prefer the confirmed parent/child reading over inventing a Variant/SKU entity; a named `variant_of` edge is a vocabulary choice on that substrate, not a pluggable module.

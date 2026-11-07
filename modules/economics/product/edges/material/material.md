# Material

## Model

- Candidate (unconfirmed): `(product)-[:material]->(product)` — "Material or Ingredient": one product is material/ingredient of another ("category of products can be a material for a product", e.g. any `topping cheese` is a material for a `pizza`).
- Vocabulary note: `CommonIngredient` (source flag name; the Good flag `Type_CustomIngredient` in [product.kh](../product.kh) is the adjacent live flag).

## Policies (rules)

- Category of products can be a material for a product.
- e.g. any `topping cheese` is a material for a `pizza`.
- Material or Ingredient.
- CommonIngredient.

## Placement

- **Not core `product`:** composition is physical-goods semantics, not priceability — product stays the unit of priceability; good/material were deliberately kept pluggable (see [product.md](../../product.md)).
- **Product-identity side of an already-homed capability:** the good-side material edge with quantity fields lives in [material](../../../../../modules-plugable/economics/good/edges/material/material.md) (that doc's Placement explicitly defers "Material or Ingredient" product-identity questions here — one home for identity, one for the edge + quantities; converge before any Khayyam migration, never two copies).
- Not [item-ingredient](../../../../../modules-plugable/economics/good/edges/item-ingredient/item-ingredient.md): that is the order-time choice on an invoice line; this is the product-level identity relation.
- Not [task production](../../../../management/task/edges/production/production.md): task-side material dependency stays there.

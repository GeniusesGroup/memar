# Material

## Model

- `(product)-[:material]->(product)` — candidate (unconfirmed): `ProductMaterial` keys a product (PrimaryNode: `Mobile`, `Pizza`) to its material (SecondaryNode: `cpu`, `Pizza cheese`) with an edge naming the material relation kind (`internal tool`, `Pizza topping`, ...); the material "can be substitute of this product".
- Fields: `MinQuantity()`, `BaseQuantity()`, `MaxQuantity()` (decimal quantities) — a min/base/max band per product-material pair; product-material key/value description "e.g. mobile-cpu, ...".

## Policies (rules)

- "ProductMaterial store some key/value for a quiddity to describe it e.g. mobile-cpu, ..." — a descriptive binding of what a product is made of.
- `Edge indicate material relation e.g 'internal tool', 'Pizza topping', ...` — the relation kind itself is labeled (edge-as-label vocabulary in source comment).
- Open TODO in source: "is it good idea to add detail manually by users?? or quiddity-model is better??" — manual detail entry vs a quiddity-model alternative.

## Placement

- **Correct here — `modules-plugable/economics/good/edges/material` (already its home).** [good.md](../../good.md) states the inventory-facing semantics (`reserve-quantity`, `best_before`, `material`, `branch`) are this module's capability — edge + quantity fields travel together (pluggable owns complete capability).
- **Not core `product`:** the product kernel stays priceability (core test in [product](../../../../../modules/economics/product/README.md)); composition/material is physical-goods semantics an org without goods removes whole (removable ⇒ pluggable).
- **Not the product-side open question:** the sibling [task production](../../../../../modules/management/task/edges/production/production.md) Placement and the product-side [material](../../../../../modules/economics/product/edges/material/material.md) doc defer "Material or Ingredient" product-identity questions to that per-edge doc — this doc is the good-side material edge; keep product identity there and this here (one home, not two).
- Order-time sibling ([item-ingredient](../item-ingredient/item-ingredient.md)) is the same capability observed at invoice time — both stay in this module (converge in its Open questions).

## Open questions

- Source TODO: manual key/value detail entry by users, or a quiddity-model binding?
- Substitute materials ("it can be substitute of this product") — a label on the material edge, or a separate substitution edge?
- Recipe vs choice: this product-level material model versus order-time [item-ingredient](../item-ingredient/item-ingredient.md) choice — one capability observed at two times, or two distinct edges? (Converge with [item-ingredient](../item-ingredient/item-ingredient.md) Open questions.)
- Converge with [task production](../../../../../modules/management/task/edges/production/production.md) and the product-side [material](../../../../../modules/economics/product/edges/material/material.md): material dependency is task-side or product-side/good-side — one home.

## Source

> Source: `modules-plugable/economics/good/edges/material/protocol/data_model.go` (in code).

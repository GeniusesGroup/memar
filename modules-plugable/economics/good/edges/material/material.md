# Material

## Model

- `(product)-[:material]->(product)` — the record and its quantities are declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)

- A material binding is a descriptive binding of what a product is made of; the relation kind itself is labeled.

## Placement

The material edge and its quantity band travel together in this module; order-time choice of ingredients is the same capability observed at invoice time ([item-ingredient](../item-ingredient/item-ingredient.md)).

## Source

> Source: `modules-plugable/economics/good/edges/material/protocol/data_model.kh` (in code).

# Reserve quantity

## Model

- `(product)-[:reserve_quantity]->(---)` — the record is declared in [data_model.kh](protocol/data_model.kh).

## Policies (rules)

- A reserve is either an absolute maximum number of units or a percent of the inventory.

## Placement

A reserve is a product-level parameter of the good capability; the edge and its reserve fields travel together in this module.

## Source

> Source: `modules-plugable/economics/good/edges/reserve-quantity/protocol/data_model.kh` (in code).

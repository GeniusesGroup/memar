# Best before

## Model

- `(product)-[:best_before]->(---)` declared in [service-set.kh](protocol/service-set.kh).

## Policies (rules)

- The best-before window is measured from production time.
- https://en.wikipedia.org/wiki/Expiration_date

## Placement

The best-before duration is a product-level parameter of the good capability; the edge and its duration field travel together in this module.

## Source

> Source: `modules-plugable/economics/good/edges/best_before/protocol/service-set.kh` (in code).

# Brand

Brand is a pluggable commercial-name grouping. Product stays priceable when brandless; the `(product)-[:brand_is]->(brand)` edge therefore lives here, not in core Product.

## Model

- `(text)-[:brand]->(---)` (note: as category of products belong to same commercial name.)
- `(product)-[:brand_is]->(brand)` — see [edges/brand](edges/brand/README.md)

## Policies (rules)

- limit for organizations only.

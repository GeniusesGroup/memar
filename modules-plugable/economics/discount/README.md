# Discount

## Model

- `(rule)-[:discount]->(---)`

## Policies (rules)

- Discount or product-auction, sales, ...
- to reduce invoices price automatically by some rules

Discovered discount usage and payable-after-discount live under [analytics](analytics/price-payable/README.md). Meal-deal / package logic lives under [packages](packages/logic.go). Analytics is always pluggable; those records must not return to core Invoice or Product.

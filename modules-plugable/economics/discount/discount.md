# Discount

## Model

- `(rule)-[:discount]->(---)`
- The edge's endpoint is a subject the discount applies to, and the conditions on it are the rule's facets, each declared in [protocol](protocol/).
- A place condition is an estate, and an estate here is a region rather than a specific point; there is one place condition.

## Policies (rules)

- Discount or product-auction, sales, ...
- to reduce invoices price automatically by some rules
- A discount adjusts an invoice's payable; it never changes the product's stated price — an invoice-level rule making the payable zero does not make the price zero.

Discovered discount usage and payable-after-discount live under [analytics](analytics/price-payable/README.md). Meal-deal / package logic lives under [packages](packages/README.md). Analytics is always pluggable; those records must not return to core Invoice or Product.

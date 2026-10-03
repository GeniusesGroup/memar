# Discount

## Model

- `(rule)-[:discount]->(---)`
- The edge's endpoint is a subject the discount applies to, and the conditions on it are the rule's facets: location (`Discount_Location`), group, user, user type, product, label, invoice, POS, time validity, timing in UTC, usage, value.
- A place condition is an estate, and an estate here is a region rather than a specific point: a rule may depend on where a service was consumed — the source or the destination of a taxi journey, carried as a service product on an invoice. The source carried this distinction in a comment on a second interface (`Area`) that was structurally identical to the location one; there is one place condition, and the distinction between a region and a point is stated here rather than in a name.

## Policies (rules)

- Discount or product-auction, sales, ...
- to reduce invoices price automatically by some rules

Discovered discount usage and payable-after-discount live under [analytics](analytics/price-payable/README.md). Meal-deal / package logic lives under [packages](packages/README.md). Analytics is always pluggable; those records must not return to core Invoice or Product.

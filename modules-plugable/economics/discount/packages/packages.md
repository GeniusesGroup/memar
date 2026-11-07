# Packages (meal deal / discount bundle)

## Model

- Candidate (unconfirmed): `(package)-[:bundles]->(product)` / `(product)-[:bundled_in]->(package)` — "related product is part of a discount bundle".
- The structural seed is in code: [business-services.kh](protocol/business-services.kh).

## Policies (rules)

- "Some rules may be limit the bundle e.g. minimum buy number, ..." — bundle participation and its limits are *rules*, not product fields.
- Concrete deal shape from the companion source: "if user buy 5 pizza and 5 non-alcoholic drink (CocaCola, Pepsi, ...) categories, one pizza is free!" — cross-category bundle (products + label categories) with per-slot `maxNum` caps.

## Placement

The meal-deal package is a removable marketing capability that attaches to products; discount owns the complete capability (edge, processing and [protocol](protocol/business-services.kh)). Bundle rules and enforcement stay inside discount.

# Packages (meal deal / discount bundle)

## Model

- Candidate (unconfirmed): `(package)-[:bundles]->(product)` / `(product)-[:bundled_in]->(package)` — "related product is part of a discount bundle".
- Structural seed already in code: `mealDeal` holds chosen `products` (each with `maxNum`) and `categories` (label UUIDs, each with `maxNum`) — see [protocol/business-services.go](protocol/business-services.go).

## Policies (rules)

- "Some rules may be limit the bundle e.g. minimum buy number, ..." — bundle participation and its limits are *rules*, not product fields.
- Concrete deal shape from the companion source: "if user buy 5 pizza and 5 non-alcoholic drink (CocaCola, Pepsi, ...) categories, one pizza is free!" — cross-category bundle (products + label categories) with per-slot `maxNum` caps.

## Placement

- **Pluggable — home is `modules-plugable/economics/discount/packages` (already correct).** Meal-deal/package is a removable marketing capability that *attaches* to products; discount already owns the complete capability (edge + processing + [protocol](protocol/business-services.go)) — see [discount.md](../discount.md).
- **Not core `product`** and **not a new module**: product only carries a structural bundle attachment (same shape as [customable](../../../../modules/economics/product/edges/customable/customable.md)); bundle rules and enforcement stay inside discount (a pluggable keeps its complete enforcement).
- The generic product-side attachment, if kept, mirrors `customable`: `(product)-[:bundled_in]->(package)` maintained by discount — never bundle logic in the kernel.

## Open questions

- Node vs rule: is the bundle a named node (packages/mealDeal) or just a rule grouping products? The `maxNum` caps look like node state; "some rules may limit the bundle" looks like rules *on* the node — confirm both layers.
- Categories via `label_p` ([knowledge/label](../../../../modules/knowledge/label/label.md)) — is any label a bundle slot, or only labels flagged as bundle categories?
- How does this relate to `rule.handoff` §9 (fees are rules producing transactions)? — the standing review question in [product.md](../../../../modules/economics/product/product.md) ("does the pricing rule duplicate rule.handoff §9") applies to bundle limits too: keep limits as rules, not package code paths.


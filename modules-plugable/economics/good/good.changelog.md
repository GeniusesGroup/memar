# Good Changelog

## Changelog

### Materials as a made product's price basis; batch pricing by shelf life asked
- Time: 2026-10-10T14:45:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [material](edges/material/material.md#policies-rules) Policies state that a made product's replacement cost is summed from its materials' own replacement costs, so its price is derived from what its materials cost today, and that a material edge change re-evaluates it. Its Open questions ask whether substitute materials are alternatives for one input, and whether `BaseQuantity` is the quantity valued.
- [best_before](edges/best_before/best_before.md#open-questions) asks whether the best-before date becomes a fact of each batch if lots differing in shelf life are sold at their own prices.
- [item-ingredient](edges/item-ingredient/item-ingredient.md#open-questions) asks whether a chosen ingredient's price is part of the price the invoice item holds as its own fact, and whether a made-to-order item reads the ingredients' replacement cost as a material does.

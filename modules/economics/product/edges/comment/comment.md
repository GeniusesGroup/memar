# Comment

## Model

- Candidate (unconfirmed): `(product)-[:comment]->(group)` — the group related to the product as its comment/discussion audience (source was a product-to-group label file).

## Policies (rules)

- Bare label "Comment" among Comment / QA / Buyers — no rules recorded in the source; direction and semantics unconfirmed.

## Placement

- **Not core `product`** — a product remains priceable and invoice-able without a comment group; core-by-necessity fails.
- **Proposed: `modules-plugable/knowledge/` beside the `reaction` capability** — reactions already model the attach-to-anything pattern (`reactionable` targets content and more); discussion attaches the same way, and GUI already separates it as [page-comments](../../../../../modules-plugable/knowledge/content/ui/page-comments/). Alternative reading: comments anchor to the [content](../../../../knowledge/content/README.md) identity that a product may take simultaneously ([product.md](../../product.md) multi-typing) — then the edge is content-side, not product-side.
- Entry point: whatever page hosts discussion, never the product kernel.

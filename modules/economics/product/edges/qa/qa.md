# QA

## Model

- Candidate (unconfirmed): `(product)-[:qa]->(group)` — the group related to the product as its Q&A audience (source was a product-to-group label file).
- Questions themselves are already owned by core knowledge: [question](../../../../knowledge/question/question.md).

## Policies (rules)

- Bare label "QA" among Comment / QA / Buyers — no rules recorded in the source.

## Placement

- **Not core `economics/product`.** The asking/answering capability already has a root home in `modules/knowledge/question` (root modules, knowledge category); a product only *hosts* questions through its content identity ([product.md](../../product.md) multi-typing).
- Any "answerers group" (who is staffed to answer) is [management/group](../../../../management/group/) / role membership, not a product edge. GUI already separates the surface as [page-questionnarie](../../../../../modules-plugable/gui/page-questionnarie/).
- Verdict in the root-vs-pluggable terms: **root — but knowledge/management, not product**; no new pluggable warranted by this label alone.

## Open questions

- Distinct edge vs purpose label shared with [comment](../comment/comment.md) / [buyers](../buyers/buyers.md)?
- Is `(product)-[:qa]->(group)` needed at all, or is it content-anchored questions + ordinary group membership (no edge)?
- Derived (who actually answered) vs maintained team?


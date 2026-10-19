# Batch

Batch as the identity of produced goods, singly or as a group (see [the product handoff](../../../modules/economics/product/product.handoff.md) — the product side of this boundary).

## Open questions (from the Estate/Product session, 2026-08-05..09; traceability deferred to a dedicated batch/logistics session)

- Is Batch the **identity of a realization**, or a **grouping over realizations** (units with shared lineage)? These are different models:

  ```text
  Product → Batch #123 → Unit 1, Unit 2, ...   (batch as grouping)
  Product → Batch #123                          (batch as the realization itself)
  ```

  If the batch is the realization, what is a Unit? If it is a grouping, where does single-unit identity live?
- **Sub-batching**: a production batch can split into further batches with distinct physical identities (e.g. per invoice) — where does the new identity come from, and how does lineage follow?
- Consumer protection case driving this: a contaminated water batch must be recallable — the system must know where that batch (and its sub-batches) is right now, without granting identity to every single bottle. Identity granularity must be a policy/economics trade-off, not a fixed rule.
- Price ownership (owner's leaning, 2026-10-10, open): the owner holds that a sale price belongs to the batch, not to the product — lots of one product differ in what a buyer values (shelf life, place, grade). Does the batch then carry its own stated price, resolved most-specific-first over the product's? A batch never carries a price because its acquisition cost differed: the basis is replacement cost, and the batch's recorded [cost](edges/cost/cost.md) stays for accounting. Open in [pricing → Open questions](../pricing/edges/pricing/pricing.md#open-questions); scenarios in [Pricing Research 001](../pricing/pricing.research.001.md#goods-held-in-several-batches-bought-at-different-costs).

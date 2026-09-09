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

## Idea backlog from edge code comments

Raw proposal from comment notes in `edges/cost/protocol/data_model.go` (comments remain in code as source). Nothing below is ratified.

- **Cost structure**: Materials/Labor/Investments(Equipment) each as percentage + cost amount, TotalCost, then pricing chain Markup (%) -> WholesaleProfit -> Margin (%) -> RetailProfit -> Cost. This mirrors the budget-label list in the transaction shortcut comments.
- **Review questions**: is the cost/pricing chain batch-owned or shared with production and budget?
# Cost

## Model

- `(batch)-[:cost]->(account)` — the record keys `Field_BatchID` plus the cost/pricing chain fields below.

## Policies (rules)

- Cost structure per source: `Materials()`/`MaterialsCost()`, `Labor()`/`LaborCost()`, `Investments()` (comment: Equipment)/`InvestmentsCost()` — each a `per.Myriad` percentage paired with a money amount, rolled into `TotalCost()`.
- Pricing chain: `Markup() per.Myriad // the % added to the cost to determine the wholesale price` → `WholesaleProfit()` → `Margin() per.Myriad // the % of product price to determine the retail price` → `RetailProfit()` → `Cost()`.
- Source records no who-may-set / approval rules for the chain (no bare edges).
- When the chain sets a price, the cost it starts from is [replacement cost](../../../replacement-cost/replacement-cost.md), not this batch's recorded cost; the recorded cost stays for accounting ([pricing decision](../../../pricing/edges/pricing/pricing.md#decisions-2026-10-10)).

## Placement

- **Correct here — `modules-plugable/economics/batch/edges/cost` (already its home).** Batch is the identity of produced goods ([batch.md](../../batch.md)); its cost/pricing chain is that identity's money story — edge + chain fields travel together (pluggable owns complete capability; parameters vs semantics ⇒ per-org chain configuration).
- **Not core `account`:** the account kernel records postings without knowing markup/margin (core never knows Rule; fees-as-rules precedent — [rule.handoff.md](../../../../../modules/computer/rule/rule.handoff.md) §9 — if pricing becomes a rule reaction).
- **Not a new module:** a percentage/amount pair list is parameters of batch economics, not independent processing (prefer existing homes over inventing new modules).
- Mirrors budget vocabulary: [batch.md](../../batch.md) backlog notes the chain "mirrors the budget-label list in the transaction shortcut comments" — converge with budget-role vocabulary ([user](../../../budget/edges/user/user.md)) if the lists are the same concern.

## Open questions

- Receiving [batch.md](../../batch.md) backlog question: is the cost/pricing chain batch-owned or shared with production and budget? (Batch side asserted above; production/budget must not grow a second copy — one home.)
- Who may set Markup/Margin — configuration, or rule reaction on cost change (core never knows Rule)? The cost-change event now exists: `replacement_cost_changed` in [replacement cost](../../../replacement-cost/replacement-cost.md).
- `Cost()` vs `TotalCost()` — retail cost after chain, or raw total? Naming unconfirmed.
- "Mirrors the budget-label list in the transaction shortcut comments" — locate that list and converge (one vocabulary home).
- Is this batch's recorded cost the historical cost that holding-gain analytics subtracts from replacement cost (replacement cost − historical cost = holding gain; sale price − replacement cost = operating margin), beside FIFO and weighted-average cost kept for accounting? Which reports read which is open in [replacement cost → Unresolved questions](../../../replacement-cost/replacement-cost.md#unresolved-questions).
- If a sale price moves to the batch (the owner's leaning, open in [pricing](../../../pricing/edges/pricing/pricing.md#open-questions)), is the chain's output that batch's stated price, computed from replacement cost and stated as a new price version?

## Source

> Source: `modules-plugable/economics/batch/edges/cost/protocol/data_model.kh` (in code).

# Production

Production is a task label domain: a task may carry the `production` label with its sub-labels and status chain (see the task module for the Production/Fabrication/Manufacturing distinction).

A made product's sale price is derived from its materials' current [replacement cost](../replacement-cost/replacement-cost.md), never from what a production run recorded it cost ([decision](../pricing/edges/pricing/pricing.md#decisions-2026-10-10)); the recorded run cost stays for accounting, in batch [cost](../batch/edges/cost/cost.md).

## Unresolved questions

- Conversion cost of a made product (labour, overhead) is open in [replacement cost](../replacement-cost/replacement-cost.md#unresolved-questions): does a production task's recorded labour and duration supply it, valued at today's rates rather than the rates paid?

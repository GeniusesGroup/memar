# Pricing

Pricing is a pluggable module family attached to Product, not Product kernel. A difference in processing semantics (city, hour, route, demand) is a distinct module; Invoice-level payable adjustments are a different level and do not change Product price. A price is derived from [replacement cost](../replacement-cost/replacement-cost.md), never from the purchase invoices of stock held ([decision](edges/pricing/pricing.md#decisions-2026-10-10)). Who owns a price — product, batch, or a service's slot — and on what basis it is shown are open ([open questions](edges/pricing/pricing.md#open-questions); [Pricing Research 001](pricing.research.001.md)).

See [edges/pricing](edges/pricing/README.md).

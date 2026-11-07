# Pricing
Pricing is a pluggable module family attached to Product, not Product kernel. A difference in processing semantics (city, hour, route, demand) is a distinct module; Invoice-level payable adjustments are a different level and do not change Product price. A price is derived from [replacement cost](../replacement-cost/replacement-cost.md), never from the purchase invoices of stock held ([decision](edges/pricing/pricing.md#decisions-2026-10-10)).

See [edges/pricing](edges/pricing/README.md).

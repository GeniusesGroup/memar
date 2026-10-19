# Service

A service is a non-inventory economic offering (seat, timing-interval, number, multiple-use). Pluggable for the same reason as [good](../good/README.md): the kernel's unit-general bookkeeping does not need it; organizations differ in where "service" ends and "good" begins. Invoice-line occupancy ([item-seat](edges/item-seat/README.md)) is this capability realized at claim time, not Invoice kernel.

## Discussion

### Drawbacks

- "Service" is where most non-physical organizations live (booking, consulting, SaaS); keeping it pluggable means those orgs lean heavily on this module — but that is exactly what a pluggable module is for.

### Rationale and alternatives

- Invoice treats employee labor as a sold service (see [invoice](../../../modules/economics/invoice/README.md)) — evidence that "service" is a useful label, not a new primitive.
- Alternative rejected: a core service/good split — organizations disagree on the boundary (a bundled product+installation), so fixing it in core would force one taxonomy.

### Prior art

- Service-dominant logic in marketing treats goods as a special case of services; Memar stays neutral and lets both be specializations of product.

### Unresolved questions

- Shared parent abstraction with `good` (a not-yet-named "tradable thing" concept?) — deliberately not invented until requirements force it.
- Are `seat`/`timing-interval`/`number` service-specific or general schedulable-resource capabilities that other domains (estate, device) also want?
- What plays the batch's part for a service, if a price belongs to the batch (the owner's leaning, open in [pricing](../pricing/edges/pricing/pricing.md#open-questions))? A barber charging by time and place sells a slot — staff × place × time — which no node holds before it is sold. Is the slot made a node now, as a candidate instance for the `schedulable` module, or do service prices stay on the product with pricing rules until that module exists ([Pricing Research 001 → Open Questions](../pricing/pricing.research.001.md#open-questions))?
- Display basis: a service may be shown per hour, per month, per trip, or as "on request" rather than as one price; is the basis declared per product, and where ([Pricing Research 001 → Open Questions](../pricing/pricing.research.001.md#open-questions))?

### Future possibilities

- A `schedulable` capability module unifying service seats, device channels, and estate spaces.

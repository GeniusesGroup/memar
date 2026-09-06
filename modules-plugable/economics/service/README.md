# Service

A service is a non-inventory economic offering (seat, timing-interval, number, multiple-use). Pluggable for the same reason as [good](../good/README.md): the kernel's unit-general bookkeeping does not need it; organizations differ in where "service" ends and "good" begins.

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

### Future possibilities

- A `schedulable` capability module unifying service seats, device channels, and estate spaces.

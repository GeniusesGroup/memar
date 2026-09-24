# Supplier

## Model

- Candidate (unconfirmed): `(product)-[:supplier]->(product|owner)` — "same product, different provider (owner, price)": the same product sourced/sold by different providers, each with its own owner and price stance.
- Distinct from the service-operator reading of [provider](../provider/provider.md) (`(product)-[:provider]->(staff|role)` — who *operates* a service product).

## Policies (rules)

- Same product, different provider — owner and price may differ per provider.
- No who-may-create / what-it-triggers recorded in the source.

## Placement

- **Not core `product`:** products stay priceable and invoice-able without a supplier edge (removable capability ⇒ fails the core test).
- Candidate readings, decide before migrating:
  1. **Not an edge at all** — multi-vendor marketplace semantics: each provider lists the product as its own product node (parent/child or parallel nodes with provider identity), price already lives on `price`/`pricing`.
  2. **Pluggable supply/procurement capability** — only if assignment + price-per-supplier needs processing beyond what product nodes and rules already give.
- Converge with [provider](../provider/provider.md) (proposed `modules-plugable/economics/service`) — one supplier vocabulary or two (service operator vs goods supplier)?

## Open questions

- Map onto the parent/child model in [product.md](../../product.md): is "different provider" just a parallel product node, or a real edge?
- Overlap with [provider](../provider/provider.md): same edge with two readings (staff/role operator vs product-side supplier), or distinct?
- Who maintains price-per-supplier — `price` edge per node, or a supplier-specific pricing rule ([pricing](../../../../../modules-plugable/economics/pricing/edges/pricing/pricing.md))?


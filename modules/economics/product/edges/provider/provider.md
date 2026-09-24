# Provider

## Model

- Candidate (unconfirmed): `(product)-[:provider]->(staff|role)` — the product operator; flags `Type_Provider_Staff` / `Type_Provider_Role` sit in [product.go](../product.go) under *Services flags*.
- The group-file reading may instead be a supplying group (source lived in the product-to-group relation file).
- Invoice keeps its own party edge: `(invoice)-[:provider]->(user)` — see [user-provider](../../../invoice/edges/user-provider/user-provider.md) ("a rule set this relation and that rule call a staff not random user").

## Policies (rules)

- "product operator is to supply a particular service."
- Provider assignment is rule-driven on the invoice side (not arbitrary user choice).

## Placement

- **Not core-by-necessity:** products stay priceable and invoice-able without a provider edge (removable capability ⇒ fails the core test).
- **Proposed: `modules-plugable/economics/service`** — the provider flags already live in product.go inside the *Services* flag block; the complete capability (who supplies/operates a service product, with its assignment processing) belongs together with the other service edges (`seat`, `timing-interval`, …) under [service](../../../../../modules-plugable/economics/service/). Entry point: instantiation happens when the product is supplied as a service, not in the product kernel.

## Open questions

- Staff / role / group — three readings of "operator"; which is real (see also [product.md](../../product.md): "do Provider/SellLimit duplicate role and delegation machinery?")?
- Flag-space vs first-class edge: if provider is only a label on the supplier, flags may suffice (parameters-vs-semantics); if assignment triggers processing, the edge moves with that processing into the pluggable.
- Relation to [user-provider](../../../invoice/edges/user-provider/user-provider.md): one rule feeding both, or independent?


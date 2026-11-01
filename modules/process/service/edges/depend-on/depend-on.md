# Service-service relation

## Model

- Candidate (unconfirmed): `(service)-[:depend_on]->(service)` — label `DependOn` from the source.

## Policies (rules)

- One service requires another; no further semantics recorded.

## Placement

- **Core `service` keeps the structural service-to-service dependency as a UUID-reference edge.** No embedded types across domains (reference-by-UUID rule in [bookkeeping](../../../../economics/account/edges/bookkeeping/README.md)); label-only dependency is structure, not processing — no module (edge vs module).
- If dependency processing appears (call orchestration, health propagation), the complete capability (edge + processing together) is a pluggable candidate at the service entry point — decided only then.

## Open questions

- Do service-to-service and service-to-module `DependOn` share one edge semantics or stay distinct (see [module](../module/module.md))?
- Does this duplicate module-level dependency semantics (the review question recorded with this entry)?


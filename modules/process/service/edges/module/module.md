# Service-module relation

## Model

- Candidate (unconfirmed): `(service)-[:part_of]->(module)` and `(service)-[:depend_on]->(module)` — labels `PartOf`, `DependOn` from the source.

## Policies (rules)

- `PartOf` = the service belongs to the module; `DependOn` = the service requires the module.

## Placement

- **Core `service` keeps these as structural UUID-reference edges.** No embedded types across domains (reference-by-UUID rule in [bookkeeping](../../../../economics/account/edges/bookkeeping/README.md)); a label-only dependency is structure, not processing — no module (edge vs module).
- If dependency processing appears (orchestration, install order, health propagation), the complete capability (edge + processing together) is a pluggable candidate at the service entry point — decided only then.

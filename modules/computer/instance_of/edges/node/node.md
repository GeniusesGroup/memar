# Node types

## Model

- Candidate (unconfirmed): node-type label space on the node identity (iota `NodeType_*` flags in package `label`): `LocalNode`, `Cloud`, `Edge`, `GUI`.

## Policies (rules)

- None recorded beyond the type list itself.

## Placement

- **Core `instance_of` keeps node-type vocab — node identity is core-by-necessity for the running-instance concept, and a label list is a parameter (parameters vs semantics ⇒ one module + configuration), so no module is warranted.**
- Doc filed in the pre-existing concept folder `edges/node/` (it already owns the node [protocol](protocol/data_model.go)); no `edges/types/` folder was needed — basename `node` does not collide with the module folder `instance_of` (judgment, reported).

## Open questions

- Closed set or organizational-open?


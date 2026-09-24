# Authorization

## Model

- `(group)-[:group_rule_authorization]->(rule)`

## Idea backlog

### Group access types
- **Idea**: a "Group access type" flag-space — Public, Private, PrivateInDepartment, PrivateInRole — qualifying how open a group is.
- **Review questions**: does this type-space belong to this module (beside the `(group)-[:group_rule_authorization]->(rule)` attachment) or to [access-control](../access-control/access-control.md) — which module owns group access semantics (overlap flagged, not resolved)? Do PrivateInDepartment/PrivateInRole reduce to department/role membership read by rules, or carry processing of their own (parameters vs semantics)? How do the four types relate to the existing `Policy`/`Access` enums in [protocol/dt-policy.go](protocol/dt-policy.go) and [protocol/dt-access.go](protocol/dt-access.go)?

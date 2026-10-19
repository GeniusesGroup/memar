# Node-node relation (Replication)

## Model

- Candidate (unconfirmed): `(node)-[:replication]->(node)` — the source carries only the label comment; direction and cardinality unconfirmed.

## Policies (rules)

- Replication between nodes; which nodes replicate and in what role is not recorded.

## Placement

- **Uncertain (create now, decide later) — a structural edge stays core `instance_of` only while it has no processing; replication with real semantics (sync, failover, lifecycle) must keep edge + processing together, i.e. it becomes a capability (pluggable candidate) filed at the node entry point.** No bare edges: who may create/remove replication and what it triggers must be identified before anything ships.
- Note: the node protocol already carries `ReplicationID` ([protocol/data_model.go (no such file yet)](../node/protocol/data_model.kh)) — confirm whether that field binds this edge.

## Open questions

- Who may create/remove the replication edge and what does it trigger?
- Does replication processing make this a capability rather than a structural edge?
- Relation to the cluster-operation flags in [node-status](../node-status/node-status.md) (`Splitting`, `ReAllocate`, `AcceptWrite`)?


# Node-hardware relation

## Model

- Candidate (unconfirmed): a node-to-hardware edge carrying run-state labels `Running` / `Ran` — e.g. `(node)-[:running_on]->(hardware)`; edge name/direction unconfirmed (source records only the labels).

## Policies (rules)

- `Running` = live now over the node-hardware edge; `Ran` = past run (interpretation unconfirmed).

## Placement

- **Core `instance_of` keeps the structural node-hardware edge.** Entry point is the node; the state labels are parameters on that edge, and no processing is recorded — an edge without independent semantics does not become a module (edge vs module).
- If hardware-run telemetry or orchestration processing appears later, that complete capability (edge + processing together) is evaluated as a pluggable at the node entry point — not now.

## Open questions

- Direction and edge naming unconfirmed — nothing ratified.
- Do `Ran`/`Running` duplicate the lifecycle group in [node-status](../node-status/node-status.md), or are they states of the hardware link specifically?


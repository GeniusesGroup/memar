# Group relation group

## Model

- Candidate (unconfirmed): source is a group-to-group label file living in the role module — reading A: `(group)-[:relation]->(group)` (edge name/direction unconfirmed) carrying label `Default`; reading B: a role-side attachment (the TODO is about `role-relation-department`, and a Department is a Group — [group.md](../../../group/group.md)), i.e. role-to-group rather than group-to-group.
- Role's existing model is group-driven: `(group)-[:role]->(---)` — see [edges-loop/role](../../edges-loop/role/role.md).

## Policies (rules)

- Only label recorded: `Default` — no create/remove semantics, no triggers recorded.
- Source TODO: move the meaning of `role-relation-department` into this edge.

## Placement

- **Correct here — candidate in `role/edges`; unconfirmed, and explicitly not a second group-parent edge.** The file is the role module's own edge file and its TODO is role-centric, so this existing home develops it (prefer existing homes over new modules); the verdict stays pending because the source records only a label.
- Under reading A (a true group→group hierarchy) this would be the *same edge* as [group parent](../../../group/edges/parent/parent.md) and must converge there — structural/shortcut edges stay with the capability that gives them meaning; there is no second parent edge.
- Bare edge as recorded (no bare edges): until "who may create/remove, what it triggers" exists, `Default` is a label, not a capability; any role↔department authorization content is rule material (core never knows Rule), not role-kernel code.

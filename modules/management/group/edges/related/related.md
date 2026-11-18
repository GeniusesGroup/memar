# Related

One group depends on another group. The kind of that dependence is a label on the edge, not a second edge and not a role.

Membership and a role stay where they are: a group is a user, so it can join another group and can hold a role there. Parent stays the hierarchy edge. This edge is the general one the group domain offers for every other dependence (two groups in one community, a department, and the rest). The role module does not grow an edge for each of those.

## Model

- `(group)-[:related {label}]->(group)`
- The two ends are group identifiers. The label is a label identifier.

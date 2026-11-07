# Joined

## Model

- `(group)-[:joined]->(user)`
- reverse: `(user)-[:joined_to]->(group)`, written in the same batch, so the groups of a member are one read and not a scan of every group.
- One edge per role: the role word is in the edge's key, so a member in two roles has two `joined` edges and the members in one role are one read.
- What one edge says is [`Group_Joined`](protocol/group-joined.kh), its values keyed by their types' TypeUUIDs ([Graph → Typed edge fields](../../../../../modules-plugable/computer/memory/store/graph/graph.md#typed-edge-fields-typeuuid--value-not-opaque-buffers)). Who accepted the membership is the Request of the join (owner, 2026-11-05).
- A user joins the group of a thing by joining the group that has the thing's address, with a role ([Group → Membership](../../group.md#membership)). Who holds the thing now is Ownership's `claimer_is`, not this edge.

## Policies (rules)

- It can be more than just one label for associated users to a group
- e.g. `Member`, `Honorary Members`, `Supporter`, ...
- The role words are declared label words an organization chooses; Group fixes none of them.
- Associated
- e.g. Accept user join request if user is 1st friendship cycle of any member.
- A user already a member is refused a second `Join`; its roles are changed instead.

## JoinWay

- JoinByRule
- RequestID of making relation is made by inviter user.
- Invited user CAN check who invite itself to this group
- Invited

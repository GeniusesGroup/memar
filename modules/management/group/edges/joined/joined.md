# Joined

## Model

Membership is one `joined` edge from a group to a user, and the reverse `joined_to` written with it, so the groups of a member are one read. What one edge says is [`Group_Joined`](protocol/group-joined.kh). The group and the user are that record's identifiers. This edge records the membership alone. A role is another subject. A read of members in one role joins two edges, so that read is a widget's service.

Who accepted the membership is the Request of the join. Who holds the thing now is not this edge.

## Policies (rules)

- A user who already has the edge is refused a second add. Ending it is a separate service.
- The words an organization uses for roles are not fixed here, because they are not this edge's.

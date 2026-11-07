# Group
`Group` sits under the `management` domain (persons, other groups, or even whole organizations can be members). The conceptual `Organization` vs. `Group` distinction is settled and documented in [`modules/identity/organization`](../../identity/organization/organization.md); this file carries only the structural questions still open after source inspection.

## A group takes nothing along
A group is a lens on a node: its `joined` edges hang on the node's one address ([Identifiers Are Memory Addresses](../../computer/memory/address/rules/identifiers-are-memory-addresses/identifiers-are-memory-addresses.md#the-rule)). A group inside another is Group's own [parent](edges/parent/parent.md) edge, a relation with its own rules.

## Resolved via source inspection
- **Department ↔ Group typing link**: `department_p.Model` embeds both `thing_p.Model` and `group_p.Model` (Go interface embedding) — Department is a Group (and a Thing) at the compile-time type level, not just conceptually. `label.go` (no such file yet) additionally defines `department` as an edge label from Group, documented (in a comment marked "Policy (rule)") for organizational-chart display and staff-join purposes.
- **Containment membership vs. oversight membership — resolved direction**: proper modeling decomposes relationships into several small, single-purpose edges (e.g., membership + role as separate edges) rather than overloading one generic edge. A combined/derived-lookup edge ("edges-shortcut") may exist purely as a traversal optimization, but must never become the primary source of truth or influence core design.

## Membership
Someone becomes a member of a group by joining it, in one or more roles. A group is any node whose address is given, so the group of a thing has the thing's address and needs no node of its own: the thing's vertex is also the group's, and `joined` hangs on it. A group takes nothing from the group of any other node.

### Edges
Group's edge for membership is [joined](edges/joined/joined.md#model), with its reverse `joined_to`, one edge per role, written in one batch; what one edge says is [`Group_Joined`](edges/joined/protocol/group-joined.kh). How a membership was offered or asked for is [invite](edges/invite/invite.md) and [request_to_join](edges/request_to_join/request_to_join.md), and a group inside another is [parent](edges/parent/parent.md). Who accepted a membership is recorded by the Request of the join. The reverse is there because without it "the groups of a member" is a scan of every group ([Graph → What it is to the memory contract](../../../modules-plugable/computer/memory/store/graph/graph.md#what-it-is-to-the-memory-contract)); the role is in the key because what a read is searched by belongs there. Which role words exist is an organization's choice ([Kernel Neutrality](../../knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)), so they are declared label words, not Group's list.

### Membership is not holding
Membership says that a user is on a group, in a role. Holding a thing now is a different fact with its own owner, Ownership ([`claimer_is`](../../rights/ownership/edges/claimer/claimer.md)), and whether a second holder is refused is Rights'. Group answers only membership.

### The member
The member is a user, and the kind of user is Identity's ([user type](../../identity/user/protocol/dt-type.kh)): a person, a legal entity, a model, a tool. A group may be a member too, because a group is a user. When a user acts for another, the user that joins is the one that acts. The relation to its principal is Delegate's ([representative](../../rights/delegate/edges/representative/representative.md)); Group records no principal.

### Services
Joining, changing roles and leaving are [`Group_Join`](services/group-join/group-join.kh); the reads of members, of members in one role, of a member's groups and of one membership are [`Group_Membership_Read`](services/group-membership-read/group-membership-read.kh).

Both take the store [`Group_Membership_Store`](protocol/group-membership-store.kh). Each reads or writes only Group's edge. Neither checks whether the user may join; that is Rights', composed by a widget. The refusals are in [errors/membership.kh](errors/membership.kh).

A member leaves by `Leave`, and its `joined` edge is removed. The fact that it was a member is not lost: the join and the leave are recorded by the widget that composes them.

## Discussion

### Drawbacks

- Decomposing membership into several small single-purpose edges (the resolved direction above) makes common questions ("who's in this group and in what role?") cost multiple traversals instead of one edge read; a shortcut edge mitigates this but must stay non-authoritative.
- Allowing org-as-member and group→parent hierarchy makes cycles structurally possible; any authority/access inheritance must guard against them explicitly.

### Rationale and alternatives

- Small, single-purpose edges over one overloaded generic edge: keeps each relationship's authorization and lifecycle independent and matches the graph-modeling principle that a bare generic edge (`member_of`, `related_to`) hides real semantics.

### Prior art

- Organizational-chart and RBAC membership models; DAO/treasury and informal-group cases (below) are the stress tests that break registration-based assumptions.
- Spotify Model (Squads, Tribes, Chapters, Guilds) — cross-cutting group kinds over one generic group, explicitly not a tree; supports the "generic Group + distinguishing label" reading over separate entity types per group kind (from the 2026-08-04 discussion: groups are recognized by the labels they carry, and a Department is a Group that some authorized role has distinguished as such).

### Future possibilities

- A cycle-detection/authority-resolution utility once the membership-edge set is fixed.
- Reconciling these membership edges with `rights/delegate` so oversight/authority is not re-derived per domain.

## Test cases any resolved criterion must pass
- A registered NGO
- A sole proprietorship (one person acting as an "organization")
- An unregistered street vendor collective
- A DAO (decentralized, pseudonymous, no legal registration, but persistent identity/treasury)
- An informal group of friends / travel planning group
- A family unit
- A government agency
- A university committee with an external organization as an oversight member

## Idea backlog

Review discipline per `vocabulary-discipline.handoff.md`. Nothing below is ratified.

### Group deletion
- **Idea**: only users of ancestor groups may delete a child group — "Just Father (father of father, ...) groups users can delete their childs.".

### Org group listing
- **Idea**: listing an organization's groups must use Offset && Limit; sketch in the comment: `GET apis.sabz.city/groups/v1/{organizationID}/group/` → `["12587954126", "12587954135"]`.

Per-edge doc under [edges](edges/): [parent](edges/parent/parent.md) — group hierarchy edge (verdict: correct here).

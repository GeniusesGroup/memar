# Plaintiff
The user who brings this case. One edge per such user, on this case. Any user type may be that user.

## Model

- `(case)-[:plaintiff]->(user)`

## Policies (rules)

- The word is the label already written on [participant](../participant/participant.md): a person who brings an action. The edge is that part on this case. It is not a [role](../../../../management/role/role.md) node.
- A user who is plaintiff here may be defendant on another case, including a case that [answers](../answers/answers.md) this one.
- A user is not plaintiff and defendant on the same case.
- A user is not plaintiff and [judge](../judge/judge.md) on the same case.
- Organization and group are user types. An organization that brings the claim is the plaintiff at this edge's end. A group may be that end as well. The case still has no domain edge to Organization.
- One or more plaintiff edges may leave one case. A second user with the same part is a second edge of this type. A different part is a different edge type.
- Who may create the edge, other than the user at its end, is not recorded. Proposal, model v1, not ratified: a user who files for another user leaves this edge ending at the party, and the authorization to file for that party is [delegate](../../../delegate/delegate.md). That note is open on the [delegate handoff](../../../delegate/delegate.handoff.md).

## Placement

- **Here, as its own edge,** not as a label on one participant edge that lists every person on the petition. The defect is that a petition-level list does not say the part on each claim. The edge type is the part. The case is the claim.
- **Nearest alternative rejected:** a role node occupied by the user. A plaintiff part has no authorization beyond being the user the complaint names. The judge edge is the one attachment whose meaning is an authorization to vote. Calling the plaintiff a role would give a second office the premise does not state.
- **Nearest alternative rejected:** a new word, complainant. The repository already glosses Plaintiff. A second word would be terminology drift.
- **Not** [management/role](../../../../management/role/role.md). That module is a social role. This edge is one user's part on one case.

## Open questions

- None for the filer. The organization is a user type and may be this edge's end.

# Petition next
The petition (dadkhast) is this chain. Several cases filed together are ordered by one edge from each case to the next. A complaint is a tag, not a node in the chain.

## Model

- `(case)-[:petition_next]->(case)`

## Policies (rules)

- The edge is the order among case nodes. A petition of one case has no edge. The single case is the whole petition.
- At most one outgoing `petition_next` and at most one incoming `petition_next`. The chain is a path.
- The cases in one chain do not share a plaintiff or a defendant by being in the chain. Each case names its own users.
- The order is not an acceptance gate. A registry inquiry does not have to exist before this chain. The chain may change after the inquiry, or it may not exist yet, because the filer may not know the defendant.
- Who may create the edge is not recorded. Whether it may change after the later case leaves draft, for a reason other than that inquiry, is not recorded.

## Placement

- **Pluggable.** Links between claims are pluggable. The kernel stays small. This file stays at the mirrored path. The edge is the order reason, not a generic relation meaning that two claims are related. The petition has no lifecycle apart from the cases it orders: parties, evidence, the invoked service, and the votes sit on each case. A petition node would only connect those cases, which is the reification the order edge already is.
- **Nearest alternative rejected:** a petition node that owns the cases. Nothing the petition must do — order, a shared person-list, a shared ruling — survives on that node. A shared person-list is the defect this phase closes. A shared ruling would hide a skipped case.
- **Not** [claim](../claim/claim.md). That file records an unratified proceeding label. It does not say the label is an order. Until that question is answered, this edge stands beside it.
- **Not** [acceptance-required](../acceptance-required/acceptance-required.md). Order is not a completion gate. A registry inquiry does not hold later cases in draft.

## Open questions

- None for a generic `claim_relation`. That edge is not this one, and it is not drawn. Each reason is its own edge.
- May a case that [answers](../answers/answers.md) another also sit in that other case's petition chain? The afternoon list does not settle that. It does not block this order edge. The chain's relation to an inquiry is already decided: it may change afterwards, or be absent.

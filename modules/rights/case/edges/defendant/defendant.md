# Defendant
The user the case is brought against. One defendant on this case. Any user type may be that user.

## Model

- `(case)-[:defendant]->(user)`

## Policies (rules)

- The word is the label already written on [participant](../participant/participant.md): the person being sued or accused. The edge is that part on this case. It is not a role node.
- Organization and group are user types (`(user)-[:organization]`, `(user)-[:group]`). The end may be a group or an organization.
- On a registry inquiry, the defendant is the target organization.
- On the money example, this user is the one the invoked service would debit. The edge does not itself move money, and it does not store the amount. The amount is the quantity on the draft transaction that references the case. The service invocation proceeds if the ruling accepts the case.
- A user is not defendant and plaintiff on the same case, and not defendant and judge on the same case.
- One defendant edge leaves one case. A second defendant is a second claim, chained on [petition next](../petition-next/petition-next.md), not a second edge on this case.
- Solidary or unequal shares are chained claims, one defendant each. They are not one claim against many with shares.
- What would falsify the one-defendant rule: one vote that must bind more than one defendant, so that two chained claims would record two acts where the claim's own rule is one act. The rule also fails if a solidary or unequal share cannot be stated as its own claim against one defendant.
- Who may name the defendant is not recorded. The participant file has no who-may-assign rule.

## Placement

- **Here, as its own edge.** Same reason as [plaintiff](../plaintiff/plaintiff.md): the part is per case, and the edge type is the part.
- **Nearest alternative rejected:** reading the defendant off the service parameters (the debited account) and storing no edge. The service endpoint is unresolved, and a complaint can name a person the service does not debit. The part has to be stated even when the invocation is not a transfer.
- **Not** the stolen edge. Stolen stays an edge of that kind of claim. Kidnap is an edge from the case to the kidnapped user. Neither is this part, and this file does not redraw them.

## Open questions

- None for the end. A group or an organization may be the one defendant. A second defendant is a second claim.


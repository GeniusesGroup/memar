# Judge
The user seated to vote on this case. A role may exist together with this edge when assignment uses task management. The edge still points at the user.

## Model

- `(case)-[:judge]->(user)`
- A [role](../../../../../modules-plugable/rights/judicial-office/judicial-office.md) may exist together with this edge. If adjudication uses task management, assignment uses that role. The role is not a substitute end.

## Policies (rules)

- The edge ends at a user. The user is not plaintiff or defendant on this case.
- An arbitrator is this edge. The same edge serves an organization that calls itself arbitration, a state court, and an ordinary company such as a social network that resolves disputes among members. Who may sit is pluggable: the organization's list, or the parties in advance. There is no second adjudicator type. Whether any person may be a judge stays open.
- The falsifier of that one edge is a query one of those three organizations must answer that this graph cannot express from who may sit, which labels exist, and which services a claim may invoke.
- What would falsify that one edge, apart from that query: A seated roster judge retains the case while a contract-named person issues the binding ruling (Art. 8 referral pattern is exit, not delegation) — would require two deciding officers or a mis-modeled forum. Critique v2. That test is open, not settled. Critique v2 leaves whether forum and enforcement pathway are attributes on this edge or a reason for a second type blocked, so this file does not close the falsifier.
- An expert, or any other opinion-giver, who records a vote is seated on this same edge. Each seated person writes an independent opinion and an independent vote. One person drafting and the others signing is not a set of votes.
- The vote is that user's. The edge points at the user. This domain does not hide that person behind an alias, and it does not reveal the person through a competence claim. A person hiding their own identity is a choice in the user domain. That choice is not modeled here.
- Seated persons must not see each other's votes or reasons before casting their own. Until every required judge has voted, no party sees any judge's or expert's vote or explanatory text. That hide is not an alias.
- A judge must choose and must explain. There is no abstention.
- A judge may accept the maximum a party will pay, or decline the seat. How long the case continues is the margin rule on [ruling](../../edges-shortcut/ruling/ruling.md), not the party's wealth.
- Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. Conflict of interest and anti-fraud apply. They are not designed here.
- Who is chosen is [judge assignment](../../../../../modules-plugable/rights/judge-assignment/judge-assignment.md). The plaintiff does not write this edge.

## Placement

- **Kernel, on the case.** Every organization that hears a case needs which users vote on it. Who may name them is pluggable.
- **The edge points at the user, and the role may sit with it for assignment.** Ending the edge only at a role would replace the voter. An alias is not what a party sees.
- **Nearest alternative rejected:** a second adjudicator type for a person the parties named, for a state court, or for a social network.
- **Nearest alternative rejected:** keeping Judge as one label among others on [participant](../participant/participant.md). This attachment is the authorization to vote.
- The count is not a kernel constant. Continuation stops on the vote margin. The numeric thresholds are pluggable examples, not this edge.

## Open questions

- Whether any person may be a judge stays open. It does not block this edge, and it does not add a second adjudicator type.

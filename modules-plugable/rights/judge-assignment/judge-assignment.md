# Judge assignment
Which users receive a [judge](../../../modules/rights/case/edges/judge/judge.md) edge on a case. One edge serves an organization that calls itself arbitration, a state court, and a social network that resolves disputes among members. Who may sit is the pluggable part.

## Model

- This module writes judge edges. It does not define the edge or the vote. There is no second adjudicator type.
- Continuation depends on the vote margin, not on a fixed count and not on how long the parties pay. This module does not choose 1, then 3, then 5, and it does not choose a stop at 5 or at an expert panel of 11, 13, or 15.
- The examples of about 20 percent from the middle, and about 80 percent the same way, are examples. An organization may put its own thresholds here. They are not kernel constants, and this draft does not adopt those two numbers as its schedule.

## Policies (rules)

- A seated user is not plaintiff or defendant on that case. That limit is on the judge edge. This module does not relax it.
- A judge may accept the maximum a party will pay, or decline the seat. The cost inputs are on [filing fee](../filing-fee/filing-fee.md). There is no wealth cap on how long the case continues.
- While the margin rule allows continuation, this module may seat further judges. When the margin rule stops continuation, it stops seating. A new judge who enters outside the seated count and records an opinion is an example, not this rule.
- The organization's list, or the parties in advance, may name the person. Party-named judges are a rule this module may implement. The same rule slot is who may sit for a state court or for a social network. Whether any person may be a judge stays open. He doubts that "anyone" is right. This draft does not close that doubt, and it does not add a second adjudicator type. Which services a claim may invoke is not this module.
- What qualifications apply is pluggable policy on this edge, not part of who is named. Kernel holds the judge edge and vote authority; a pluggable module may state *who may name* the occupant and *what qualifications* apply. Critique v2.
- Party naming with optional qualification gates, not an unqualified free-for-all. Critique v2.
- What would falsify the rule that party-named judges are a rule this module may implement: A pilot rule that roster judges may be contract-named *without* qualification or forum metadata, and sources treat that as identical to UNCITRAL party-appointed *arbitrators* with Art. 11(5) gates. Critique v2. That test is open, not settled.
- If adjudication uses task management, assignment uses a role, together with the judge edge that points at the user. That premise is on [judicial office](../judicial-office/judicial-office.md).
- Seated persons must not see each other's votes or reasons before casting their own. Until every required judge has voted, assignment does not reveal those votes or texts to a party.
- Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. This module does not design a score. A party's score does not weight a vote.
- What would falsify that self-declaration and that a party's score does not weight a vote: an exam or a badge as the condition for specialty, rank, or fee; or a kernel scoring formula; or a vote whose weight is a party's score. Model v4 point 10.
- Conflict of interest and anti-fraud apply to judges. They are not designed here.

## Placement

- **Pluggable.** Who may name a judge, and which thresholds stop continuation, can change without a new edge type.
- **Nearest alternative rejected:** one selection method frozen on the judge edge for every organization.
- **Nearest alternative rejected:** a second adjudicator type for a person the parties named.
- **Nearest alternative rejected:** that "party-named judges via pluggable module is probably not right". That premise is not supported as stated. The worry belongs on **mislabeling** (calling a contract-named private adjudicator a *roster judge*) or on **missing qualification rules**, not on party naming itself. Critique v2.
- **Nearest alternative rejected:** a kernel count of seats.

## Open questions

- Whether any person may be a judge stays open. It does not block party-named judges as a pluggable rule, and it does not add a second type.

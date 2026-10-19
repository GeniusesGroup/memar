# Case — pilot context

Copy of the justice-pilot project context, placed beside the case draft so a later session can load the dated decisions without the Cursor store. The dated user-input sections below are unchanged. The development plan is not in this package. The review trail was critique v1-v4, model v1-v6, and the synthesis. What each record was is in the last entry of [case.changelog.md](case.changelog.md).

# Project context

Stable decisions for modeling `organization`. Execution detail is in development-plan.md. That plan is not in this package. Only phase 0 is authorized. Each later phase needs its own explicit approval.

## Goal

Model organization domains the Memar way so that an open question does not force the model to change again. A domain folder is a view of nodes and edges, not a final map. Go files in the tree are temporary and will later be rewritten in Khayyam. This phase does not do that rewrite.

## Constraints

- The pilot writes no code. No strong model. Cap: 6 runs, `composer-2.5` and `grok-4.7` only.
- The pilot runs in the cloud. Drafts stay in `docs/pilot-justice/` in the Project store. Omid copies approved files into his repository by hand. Agents do not commit, push, branch, or open a PR.
- Text an agent can receive is English. A Persian legal term appears only as a gloss, for example petition (dadkhast).
- Sources are formal and scholarly, mostly English. Persian websites are not sources.
- Example edges, including `kidnap`, `stolen`, and `illegal`, are not deleted. Petition (dadkhast) and complaint (shekvaieh) drafts mirror repo-relative paths under `docs/pilot-justice/organization/`.
- `modules-plugable/rights/claims/edges` is an input Omid will provide (push to GitHub, or copy to `docs/pilot-justice/inputs/claims-edges/`). Run 3 does not start without it. Runs 1 and 2 are already launched. Ideas in that tree are mostly raw. For each edge or concept a run touches, write the rationale an implementer would need. If the reason is only in Omid's head, ask. Do not invent it.
- Research writes `docs/pilot-justice/research/research-a.md` and `research-b.md`. Critique, reply, and synthesis write `docs/pilot-justice/review/`. Every run ends with `Questions for Omid`. The coordinator batches those sections to him.
- A finding for another domain, including representation (vakalat), is a note for that domain.
- Functional roles, mostly authorization, are not kernel. They belong under `modules-plugable`. The repository has no home for them yet.
- A human or an AI agent (hushvar) may do any part of the work.

## Phase 0 decisions

A petition is currently an ordered edge among several `case` nodes. An independent node needs a strong argument. Each claim has its own parties and roles. A single list of persons leaves that role ambiguous. The weight of the work is critiquing that model. The comparative set is accepted: Iran from Omid's premises plus scholarship, one civil-law system, one common-law system, one ODR system.

Pilot questions: a separate ruling per claim; whether functional roles are needed and where they are registered; which parts need `user` and which need `role`.

## User inputs 2026-09-26, justice pilot

Ideas that come from Memar or from Omid are judged on their own. They are not scored by how well they match a country's procedure. A prior-art run is in progress. That run is evidence, not a compatibility target.

Decided: the pilot designs the best dispute-resolution model between persons. Matching any country's law is not a goal.

Premise on the claim, not a finished model: a claim stays a claim until it is ruled. The ruling is a separate edge on that claim and holds the judges' consensus. Omid called the question this answers ambiguous.

Tentative, to be critiqued and not adopted:

- A claim is systemic. It names the other organization service it invokes. Example: "X owes me 1,000,000 money units" both states the claim and requests a judicial transaction that debits the defendant and credits the claimant. It also carries a text explanation of why it should be accepted, and attached evidence.
- He sees no difference yet between subject (mouzu) and request (darkhast). That split must be examined critically.
- Statuses exist. A registry inquiry is itself a first claim. A judge must accept it, and that acceptance is a ruling. Later claims in the chain stay draft until that ruling exists, and only then can they be completed.
- Only the judge is a role. Everyone else is a user on the claim node. He will think further. Not final.

Open:

- Re-filing the same claim by the same parties is reviewed by twice the previous number of judges, always an odd count, instead of res judicata. How the adjudication cost is computed. How judges are assigned to a claim. Whether those mechanisms are kernel modules or pluggable modules.
- An earlier judge's vote stays in the pool and is outvoted. A judgment is never overturned. It becomes a minority.

## User inputs 2026-09-27, justice pilot

Decided:

- A complaint (shekvaieh) is a tag or label that groups claim types, plus the text explanation a type already carries. It is not a node. He treats typed categories as a paper-era aid: an agent can derive claims from a conversation. Tags stay because Memar already recognizes them.
- A vote on one case is never a vote on another case.
- The same parties, even with the same amount, are not the same claim. The same sum may be claimed from the same person in different years.
- A past majority is not its own edge. The votes are enough.
- Any user type can be plaintiff, defendant, or expert. Organization and group are user types, so a defendant may be a group or an organization.
- Kidnap is an edge from the claim or case to the kidnapped user. It stays. Stolen stays an edge of that kind of claim. Neither is redrawn into something else.
- There is no cap on creating cases. Until the party accepts the full fee, only the fixed system fee is charged. That charge is the brake on empty cases.
- Adjudication cost is judge person-hours plus a fixed system fee. A party may state a maximum they will pay. A judge may accept that cap or decline the seat.
- Judges must not see each other's votes or reasons before casting their own. Independent opinion is required. A panel in which one expert's report is signed by the others is rejected.
- A registry inquiry is its own claim. It is not a draft-gate that must exist before other cases. The draft chain may change after the inquiry, or it may not exist yet, because the filer may not know the defendant. The inquiry's defendant is the target organization. Example: an Instagram account opened in someone else's name; the information must come from that organization into the forum. Joint adjudication across two organizations is allowed as a direction. Memar UUIDs already give identity. A blockchain is not required.
- After a ruling exists, a third party's attack is a new case linked to that case. The claim type is annulment of that ruling. During the proceeding, a third-party objection is a linked claim heard together.
- Human-language reasons are timeline texts on the case. They are not a field of the vote.
- Linking claims that are related but not ordered is required. One case is when the defendant says this was already claimed. Another is a similar case in another organization. Whether those edges are kernel or pluggable is open.

Premises, not settled type identity:

- He says the case UUID is at once a group, so it can be a timeline, and a task, so a judge can assign an expert. What would falsify that is recorded beside the case draft. It is not adopted as type identity.
- Judge confidentiality: a role may exist together with the judge edge that points at the user, because the judge's identity is not to be exposed. Role is also how assignment works if adjudication uses task management. Both are the working premise. What a party sees instead of the user is open.

Arbitrator, not concluded:

- An arbitrator is not a substitute judge and is not any person who can adjudicate. He rejects handing a seated, paid judge's case to an arbitrator. On his view, an arbitrator is an expert the contract parties named so the judge can rule from the aggregate of those experts' opinions. Criminal versus civil complaint, and arbitration versus adjudication, are paper-era splits he wants tested, not adopted. A separate research run covers that test. This note does not conclude it.

Open:

- Majority: he thinks he meant majority, not average, and asks what a majority is when votes are for the plaintiff, for the defendant, or abstain. He floats that an abstain counts as a negative, with a reason (a formal defect, or incomplete evidence), and says it needs deeper study.
- Partial quantum: a judge who would grant only part of the money, or three months instead of one year while another judge says six months. He asks whether that judge must file a new narrower claim, reject the original, and accept the narrower one, and how those opinions aggregate.
- How conflicting rulings relate when someone sues again. Refiling is not forbidden. The new case must not be an unlinked duplicate. The link rule is open.
- Whether judge rank changes the fee, and whether parties can summon a higher rank at a later stage.
- Whether the pool stops at a number (he mentions 5, and expert panels of 11, 13, and 15) or continues as long as the parties pay.
- How a ruling is executed. He is not sure settlement_for is that path.
- Which edges connect claims, and in which module.

## User inputs 2026-09-27 afternoon

Decided:

- Every judge, expert, or other opinion-giver records an independent opinion and an independent vote. One person drafting and the others signing is rejected. Until every required judge has voted, no party sees any judge's or expert's vote or explanatory text. Conditional visibility of a content record is a requirement to note for the content and timeline domains. Those domains are not modeled in this record.
- Parties see an alias such as "Judge 1", that alias's explanation, and that alias's vote. The person's identity stays hidden, except through a separate claim that attacks that judge's competence, which may reveal the person.
- Confidentiality is not only for judges. An inquiry returns an information package. The requester can file a claim against that package. The requester does not receive the underlying records.
- There is no abstention. A judge must choose and must explain the choice.
- A judge cannot change the claim. On a different amount, the judge can only reject. The rejection reason states that this exact amount is not accepted and states the amount the judge would accept. The claimant must chain a new claim for that amount. If several judges name different amounts, they still only reject and write their amounts. The claimant then files a new claim at a figure the claimant chooses. The average is an example of that figure. It is not a ruling that averages the judges' amounts. Storing several positive votes at several amounts is the scenario this rule avoids.
- Where that acceptable amount is stored is not decided. It may be timeline text, under the rule that human-language reasons are timeline texts, or a numeric field on the vote. That gap stays blocked.
- Opened sources that treat a partial grant as relief on the same claim disagree with reject-only plus a new chained claim. That disagreement is a recorded departure. It is not a reason to revert.
- A claim has one defendant. Solidary or unequal shares are chained claims, one defendant each, not one claim against many with shares.
- In the doctrines he looked at, an arbitrator is a judge. The difference is who names them: the organization's list, or the parties in advance. A pluggable module may implement party-named judges. Whether any person may be a judge stays open. He doubts that "anyone" is right. No second adjudicator type is added.
- Civil versus criminal is a label, not a different adjudication model. Pluggable modules may attach a process, for example what happens when a kidnap claim arrives. A subtlety he asked to have critiqued stays open.
- There is no single generic edge meaning "these two claims are related". Each reason, including third-party objection and annulment, is its own edge.
- Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. The pattern is wider than judges. He names a music mentor. Four items are examples, not the justice rule: a new judge may enter outside the seated count and record an opinion; closeness to the majority may raise a score; a party's complaint may lower a score; a party's score might affect the judge's vote. A party score is not put on a vote's weight. Conflict of interest and anti-fraud apply to judges too. No scoring formula is designed.
- There is no wealth cap on how long a party may continue. Continuation depends on the vote margin. His examples: while the weight sits near the middle, within about 20 percent, continuation is allowed; if about 80 percent of judges have voted the same way, continuation stops. The structure is stop on margin, not on wealth. The numeric thresholds are examples and belong in pluggable policy, not in the kernel.
- When the ruling is final under that margin rule, it executes automatically. A later break, such as a third-party objection or another attack, requires a reversal of that execution. The reversal is noted for the transaction domain. The transaction rules are not invented here.
- Links between claims are pluggable. The kernel stays small. Whether a repeated claim is even allowed is an organization choice. The defendant and the system may surface an earlier claim as evidence. That is not a kernel ban.
- Claim-type labels, including a complaint (shekvaieh) label, each get a folder on the pattern of `modules-plugable/rights/law-labels`.
- An inquiry is a claim like any other. He compares it to theft. The claimant must prove the need. If proof needs other claims, those are chained so the judge can see the inquiry is not a pretext to harvest information. Inquiry data stays off the person.
- Jury, suspect, lawyer, trial attorney, counsellor, judicial officer, and witness may exist as pluggable edges, each added for its own reason. A judge may say the claim needs ten jurors. That module assigns people by its own rules and may update their social rank for taking part. Those edges are not in the kernel.

Left open, and not closed by this record:

- Whether any person may be a judge.
- The civil-versus-criminal subtlety.
- The four score examples stay examples. They are not a vote weight, and no scoring formula is stated.

## User inputs 2026-09-27 evening

Decided:

- Do not hide a judge's identity inside the justice domain. Domain-specific secrecy may backfire. Drop the alias "Judge 1" and drop the separate competence-claim as the way identity is revealed. A person hiding their own identity is a choice in the user domain. Note that for the user domain. Do not model it here.
- Civil versus criminal stays a label. The subtlety is not a numeric constraint. Execution of a claim is a service invocation the system compels. The defendant is not the voluntary caller. The service input is not only a number. Example: a public apology invokes a service that writes a text on that person's timeline, addressed to the claimant. That is the shape of execution. The transaction-domain reversal note stays. The timeline write is another compelled service, not a second procedure.
- One adjudication model serves an organization that calls itself arbitration, a state court, and an ordinary company such as a social network that must resolve disputes among members. Who may sit, which labels exist, and which services a claim may invoke are pluggable. No second adjudicator type. The falsifier is a query one of those three organizations must answer that this graph cannot express.
- A plain reject remains allowed. Independent votes stay. The paper practice of one ruling text signed by several judges is not this model. A party score is not put on a vote.
- Stop treating the alternative as money. He described a conditional accept (accept, with a change to the execution request, and that change is another service request) and a chained claim whose type is consensus of the judges' opinions, the same judges sitting and producing one aggregation. That description replaces "reject only, claimant picks an average" as the way a partial or rewritten execution is handled. Critique v3 returned. The description is not ratified. The four forks below stay blocked.

Blocked, not solved:

- Conditional accept cannot be an enrichment of `vote_accept` if accept means "as filed". A third edge is not ratified either. The ballot type stays blocked.
- A consensus outcome derived without a fresh vote from each judge on one claimant-filed service collapses independent votes. Fresh-vote versus reuse is not picked. A consensus shortcut is not ratified. Conditional accepts are not reused as the consensus outcome.
- Alternate service parameters still have no home. Timeline text is not invocable. A field on `vote_accept` contradicts accept-as-filed. Placement stays blocked. The amount-only gap is not the open question.
- Whether a consensus case may itself be conditionally accepted stays blocked. The margin rule does not stop that chain.

## User inputs 2026-09-28, justice pilot

Recorded here as his points. The comparison is model v6. That record proposes one shape. It does not leave the three candidates open as a menu.

1. Conditional accept has problems, as the consensus claim does. The pilot must still leave a usable solution, or a later phase will be forced to add conditional accept.
2. If conditional accept has no good fix, re-examine every idea and adopt the best. Three candidates he named: A, full reject, tell the claimant the claim as filed is not acceptable and must be adjusted, and they chain a new claim; B, full reject, plus registering a consensus claim; C, conditional accept, which needs a consensus claim.
3. A judge who wants a change edits the draft request attached to the case for execution. Editing produces a new request. That new request is attached to the judge's vote. The vote's text explains, but the source of truth is the request content. A typo in the explanation, writing 100 where the request says 1000, does not change the request. The registered request wins.
4. On the consensus claim, conditional accept is not allowed. Consensus means choosing one of those requests. He asks whether it could mean anything else.

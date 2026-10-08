# Case Handoff

Open work for the case draft. Entries are the state a later session needs. Dated answers from Omid are in [case.pilot-context.md](case.pilot-context.md). This file does not add an answer he did not give.

## Topic & Purpose

Phase 0 models dispute resolution on `case`: petition, complaint, votes, the ruling shortcut, the pool and the margin, links between cases, and execution. The weight is a graph that will not have to be redrawn because an open question was papered over. Model v6 proposes one shape for a changed execution. That shape is not ratified.

## Status

Active

## Decisions

Confidence is Decided unless the bullet says otherwise. A draft sentence he did not say is not listed here.

- **Decided (2026-09-26).** The pilot designs the best dispute-resolution model between persons. Matching a country's procedure is not a goal. Prior art is evidence, not a compatibility target.
- **Decided (phase 0).** A petition is currently an ordered edge among several `case` nodes. An independent petition node needs a strong argument. Each claim has its own parties and roles. A single list of persons leaves the role ambiguous.
- **Decided (2026-09-26), premise, not a finished model.** A claim stays a claim until it is ruled. The ruling is a separate edge on that claim and holds the judges' consensus. He called the question this answers ambiguous.
- **Decided (2026-09-27).** A complaint (shekvaieh) is a tag or label that groups claim types, plus the text explanation a type already carries. It is not a node. Tags stay because a label is already recognized.
- **Decided (2026-09-27).** A vote on one case is never a vote on another case.
- **Decided (2026-09-27).** The same parties, even with the same amount, are not the same claim. The same sum may be claimed from the same person in different years.
- **Decided (2026-09-27).** A past majority is not its own edge. The votes are enough. An earlier judge's vote stays in the pool and is outvoted. A judgment is never overturned. It becomes a minority.
- **Decided (2026-09-27).** Any user type can be plaintiff, defendant, or expert. Organization and group are user types, so a defendant may be a group or an organization. A claim has one defendant. Solidary or unequal shares are chained claims, one defendant each.
- **Decided (2026-09-27).** Kidnap stays an edge from the claim or case to the kidnapped user. Stolen stays an edge of that kind of claim. Neither is redrawn.
- **Decided (2026-09-27).** There is no cap on creating cases. Until the party accepts the full fee, only the fixed system fee is charged. Adjudication cost is judge person-hours plus a fixed system fee. A party may state a maximum they will pay. A judge may accept that cap or decline the seat. There is no wealth cap on how long a party may continue. Continuation depends on the vote margin. The numeric thresholds he gave (about 20 percent from the middle, about 80 percent the same way; pools of 5, 11, 13, 15) are examples and belong in pluggable policy, not in the kernel. The 2026-09-26 doubling of judges on refiling was under Open and was not adopted.
- **Decided (2026-09-27).** Judges must not see each other's votes or reasons before casting their own. Every judge, expert, or other opinion-giver records an independent opinion and an independent vote. One person drafting and the others signing is rejected. Until every required judge has voted, no party sees any judge's or expert's vote or explanatory text. That visibility is a requirement to note for the content and timeline domains. Those domains are not modeled here.
- **Decided (2026-09-27 evening).** Do not hide a judge's identity inside the justice domain. The alias "Judge 1" is dropped. A competence claim is not how identity is revealed. A person hiding their own identity is a choice in the user domain. It is not modeled here.
- **Decided (2026-09-27).** There is no abstention. A judge must choose and must explain the choice.
- **Decided (2026-09-27).** Human-language reasons are timeline texts on the case. They are not a field of the vote.
- **Decided (2026-09-27).** A registry inquiry is its own claim. It is not a draft-gate that must exist before other cases. The draft chain may change after the inquiry, or it may not exist yet. The inquiry's defendant is the target organization. The claimant must prove the need. The requester receives an information package and does not receive the underlying records. Inquiry data stays off the person. Memar UUIDs name identity. A blockchain is not required. Joint adjudication across two organizations is allowed as a direction. The joint procedure is not drawn (open on the inquiry handoff).
- **Decided (2026-09-27).** After a ruling exists, a third party's attack is a new case linked to that case. The claim type is annulment of that ruling. During the proceeding, a third-party objection is a linked claim heard together. There is no single generic edge meaning "these two claims are related". Each reason is its own edge. Links between claims are pluggable. Whether a repeated claim is allowed is an organization choice. The defendant and the system may surface an earlier claim as evidence. That is not a kernel ban. The edge files for those reasons are not in this package (question 20).
- **Decided (2026-09-27).** In the doctrines he looked at, an arbitrator is a judge. The difference is who names them: the organization's list, or the parties in advance. A pluggable module may implement party-named judges. No second adjudicator type. He rejects handing a seated, paid judge's case to an arbitrator. One adjudication model serves an organization that calls itself arbitration, a state court, and a company such as a social network. Who may sit, which labels exist, and which services a claim may invoke are pluggable. The falsifier he stated is a query one of those three must answer that this graph cannot express. Whether any person may be a judge stays open on [judge assignment](../../../modules-plugable/rights/judge-assignment/judge-assignment.handoff.md).
- **Decided (2026-09-27).** Civil versus criminal is a label, not a different adjudication model. Execution of a claim is a service invocation the system compels. The defendant is not the voluntary caller. The service input is not only a number. A public apology invokes a service that writes a text on that person's timeline, addressed to the claimant. The timeline write is another compelled service, not a second procedure.
- **Decided (2026-09-27).** When the ruling is final under the margin rule, it executes automatically. A later break requires a reversal of that execution. The reversal is a note for the transaction domain. The transaction rules are not invented here. He is not sure `settlement_for` is the execution path (question 28).
- **Decided (2026-09-27).** Specialty, rank, and fee are self-declared and must carry evidence. Not an exam and not a badge. The kernel does not compute the fee from rank. A party score is not put on a vote's weight. No scoring formula is designed. Conflict of interest and anti-fraud apply to judges and are not designed here. The other three score examples stay open on the judge-assignment handoff.
- **Decided (2026-09-27).** Jury, suspect, lawyer, trial attorney, counsellor, judicial officer, and witness may exist as pluggable edges, each added for its own reason. They are not in the kernel. Which of them is added is question 37.
- **Decided (2026-09-27), premise, not type identity.** He says the case UUID is at once a group, so it can be a timeline, and a task, so a judge can assign an expert. What would falsify that is [case.research.001.md](case.research.001.md). It is not adopted (question 15).
- **Decided (2026-09-27 afternoon), then withdrawn as the ratified path (2026-09-27 evening).** Reject-only, with the acceptable amount in the reason and a new chained claim at a figure the claimant chooses, including an average as an example of that figure, was his afternoon rule. The evening description replaces it and is not ratified. Opened sources that treat a partial grant as relief on the same claim are a recorded departure from the afternoon rule. That disagreement is not, by itself, a reason he gave to revert.
- **Decided as his instruction (2026-09-28), graph Explored-but-unresolved.** He asked the pilot to leave a usable solution, or a later phase will be forced to add conditional accept. He named three candidates: A, full reject and the claimant chains an adjusted claim; B, full reject plus a consensus claim; C, conditional accept, which needs a consensus claim. He said a judge who wants a change edits the draft request, the edit produces a new request attached to the vote, the vote's text explains, and the registered request wins. He said conditional accept is not allowed on the consensus claim, and consensus means choosing one of those requests. He asked whether consensus could mean anything else. Model v6 proposes B, narrowed so the attachment sits only on reject, the claimant files exactly one of those requests, and the same judges cast a fresh accept or reject. **That proposal is awaiting ratification. The vote-to-request edge is not drawn.** Questions 1–5 are that gap. The rejected alternatives are in [case.changelog.md](case.changelog.md).

## Ambiguities Resolved

- **Abstain.** Morning of 2026-09-27 he asked what a majority is when votes are for the plaintiff, for the defendant, or abstain, and he floated that an abstain counts as a negative. Afternoon: there is no abstention. [case.research.005.md](case.research.005.md) questions 1 and 2 are closed by that sentence.
- **Blind voting and aliases.** [case.research.006.md](case.research.006.md) questions 1–6 are closed by the independence rule, the rejection of one draft the others sign, the drop of the justice-domain alias, and the judge edge pointing at the user with an optional role for assignment. Who may open a hidden binding does not arise here, because this domain does not hide the person.
- **Arbitration as a second type.** [case.research.007.md](case.research.007.md) questions 1, 2, 3, 5, and 6 are closed by one adjudicator type, party-named persons on the same judge edge, no referral of a seated case to a second forum, and civil versus criminal as a label. Question 4's remainder is whether any person may be a judge.
- **Inquiry as a draft-gate.** [case.research.004.md](case.research.004.md) question 6 assumed later claims stay draft until the inquiry is accepted. He rejected that gate on 2026-09-27.
- **Per-claim parties.** [case.research.002.md](case.research.002.md) question 2, [case.research.003.md](case.research.003.md) question 4, and [case.research.004.md](case.research.004.md) question 2 asked whether a person-by-claim role is required. He decided each claim has its own parties and roles. Only the judge was called a role, and he said that was not final; later the other offices may be pluggable edges, and plaintiff and defendant are user edges.
- **Petition shape.** [case.research.002.md](case.research.002.md) question 3 asked how multiple claims sit in one petition. The phase-0 decision is an ordered edge among case nodes. A petition node was not given the strong argument he required.
- **A vote counting on another case.** [case.research.002.md](case.research.002.md) question 4 asked which legal test allows a partial ruling to decide a joined claim. He decided a vote on one case is never a vote on another case. Country tests are not the rule.
- **Cost and who names judges.** [case.research.004.md](case.research.004.md) question 4. Cost inputs and pluggable placement are decided above. Who names a judge is the organization's list or the parties in advance, as pluggable policy.
- **Earlier decision in the pool.** [case.research.004.md](case.research.004.md) question 5. The vote stays and can be outvoted. The past majority is not its own edge. The average is not that rule.
- **Refiling counts.** [case.research.004.md](case.research.004.md) question 3 asked for judge counts on the first, second, and third filing. The doubling note was never decided. Later he decided the kernel does not ban a repeat, continuation stops on the margin, and the numbers are pluggable examples, not a kernel schedule.
- **Functional-role home.** [case.research.003.md](case.research.003.md) question 3. Functional roles are not kernel. They belong under `modules-plugable`. The CRT role names in that question were not adopted.
- **Pre-filing registry lookup.** [case.research.003.md](case.research.003.md) question 5. The inquiry is its own claim, not a provisional-filing gate.

## Open Questions

Each item he has not closed. A model-v6 sentence is a proposal, not his answer. Suggested path in every case: he ratifies, rejects, or replaces the cited sentence. This handoff does not pick.

1. **Ballot edge.** Critique v4 question 1 and model v5 blocked fork 1. Must every attached alternate sit on `vote_reject` only, with `vote_accept` strictly as filed? If yes, vote-reject has to carry an optional request. If no, which edge records accept-with-a-changed-service? Model v6 proposes the first reading and does not draw the edge. **Explored-but-unresolved. Proposal awaiting ratification.** Matters because the margin cannot classify an unnamed third outcome. Blocks the ballot and what a ruling executes. It does not block a plain accept of the filed service or a plain reject that points at nothing.

2. **Where a changed service input lives.** Model v5 blocked fork 3, and model v4's question on where an acceptable amount is stored. Timeline text is not invocable. A field on `vote_accept` contradicts accept-as-filed. Model v6 proposes one `computer/request` the reject may point at, and states that the proposal does not invent who may create that pointer, what validates the request, or what triggers execution. **Explored-but-unresolved. Proposal awaiting ratification.** Matters because execution cannot read a typo in the explanation. Blocks any service other than the one the case filed.

3. **Consensus act.** Critique v4 question 2 and model v5 blocked fork 2. On the later case, is the ballot a fresh accept or reject by each of the same judges of one service the claimant filed, chosen from the requests the rejects point at? Model v6 proposes that reading, and proposes that judges do not pick among several attachments on one ballot. His question, whether consensus could mean anything else, is not ratified with that proposal. Model v6 places the later case on the petition path. Which edge links it to the original case is not stated: `petition_next` is the order edge, and he decided each reason claims are linked is its own edge, so a consensus link would be one of the edges in question 20. Matters because reuse of an earlier vote collapses independent votes, and a multi-pick ballot is not what the margin counts. Blocks the consensus case as a rule.

4. **A further change on the consensus case.** Model v5 blocked fork 4 and critique v4 attack 3. May that later case be conditionally accepted, or grow a new attached request? Model v6 proposes that it may not, and that a further filing may name another request an original reject already points at without creating a new request. The margin rule does not stop the later case. Critique v4 asked who must file the later case, by when, and whether requests that rejects point at go stale. Model v6 answers who: the claimant. By when, and whether a pointed-at request expires, are not stated. Critique v3 named a pluggable filer that drafts the one service as an alternative to the claimant; it was neither adopted nor rejected. Matters because the chain otherwise does not end. Blocks any stop rule beyond the claimant not filing a further case. **Explored-but-unresolved. Proposal awaiting ratification.**

5. **The draft request on the case.** Critique v4 question 3. What edge attaches the editable draft request to the case: `computer/request` via `sub_request_of`, or only `claim_service` to the service endpoint? Who may edit after votes exist? Model v6 assumes a draft the judge edits. That edge is not drawn. The filed invocation in the draft is still `(case)-[:claim_service]->(service)`. Matters because the edit step has no home. Blocks that step.

6. **A skipped claim or a blanket rejection.** [case.research.002.md](case.research.002.md) question 1. When every claim is rejected with one formula (bi-haqqi), or only some claims in a multi-claim petition are addressed, is that one ruling with an unaddressed flag per claim, separate rulings only for claims actually ruled, or one merged outcome corrected on appeal? No English source in that research defines bi-haqqi. He did not pick. The vote-reject draft says a case with no vote is unanswered and that a path-wide blanket rejection is not a vote. That sentence is the draft. Matters because a skipped claim must stay visible. Blocks whether a missing per-claim ruling is a validation error.

7. **Amendment after the first session.** [case.research.002.md](case.research.002.md) question 5. Is an amended claim a new case node, a revision of the same case, or a petition-amendment event? He did not pick. Matters for the claim lifecycle. Blocks that graph. It does not, by itself, block questions 1–5, which are about a changed execution rather than this amendment.

8. **A ruling on every claim.** [case.research.003.md](case.research.003.md) question 2 and [case.research.004.md](case.research.004.md) question 1. Must each claim carry its own ruling edge, and is one disposition that rejects every claim a valid ruling on each of them? The phase-0 pilot question states the concern and does not decide it. Matters because silence can hide a skipped claim. Blocks the validation rule. The draft's "silence is not a rejection" is not his answer to this question.

9. **What one claim is.** [case.research.003.md](case.research.003.md) question 1. Does one claim correspond to a claim for relief, to a claim-plus-remedy pair, or to something else? Matching a country's unit is not the goal, and he did not define the unit. The draft says one case names one service. Matters for how petition edges attach and whether a remedy is part of the case. Blocks that identity.

10. **Partial grant.** [case.research.005.md](case.research.005.md) question 3. Do opened sources' same-claim partial grant (remainder rejected) stand, or does a smaller amount require another claim? The afternoon reject-only rule was replaced in the evening and not ratified. Model v6 proposes B, which is neither that source shape nor candidate A. **Explored-but-unresolved.** Matters because several positive votes at several amounts is the scenario he said the reject rule avoids. Blocks the partial result. Same ratification as questions 1–4.

11. **Numeric aggregation.** [case.research.005.md](case.research.005.md) question 4. For disagreeing quantities, which function is intended: median, average, majority on liability and then one judge sets the quantity, deliberative consensus, or something else? He rejected a system average as a ruling. He did not pick another function. Model v6 does not aggregate numbers. Matters if a quantity is still a vote outcome. Blocks that function. It does not block the rejection of the average.

12. **A quantity on the ballot.** [case.research.005.md](case.research.005.md) question 5. Does an adjudicator record only for or against, or also an amount? He left the home of the acceptable amount undecided, then the evening blocked placement of alternate service parameters. Model v6 proposes a request pointer rather than a numeric field, and that pointer is not drawn. Matters for what is stored on the vote. Blocks a numeric ballot. Same ratification as question 2.

13. **Issue-by-issue or bottom-line.** [case.research.005.md](case.research.005.md) question 6. Are liability, quantity, and remedy type aggregated separately, or only as one disposition of the filing? He did not pick. The draft margin counts accept and reject of one filed service. Matters because the protocol changes the outcome. Blocks that choice.

14. **Constraints on a quantity.** [case.research.005.md](case.research.005.md) question 7. If a quantity must satisfy a legal relationship, is aggregation constraint-aware rather than a raw median or majority? He did not answer. Matters only if a numeric aggregation is adopted. Blocks that rule. It does not force one.

15. **One UUID as case, group, and task.** [case.research.001.md](case.research.001.md). Is that type identity? He stated it as a premise. The research leaves it open. Adopting it would make the case a group and a task. Blocks that identity. It does not block timeline texts being noted for the timeline domain.

16. **`claim_relation` and `petition_next`.** Is `claim_relation` the petition order, or does `petition_next` stand alone? [claim.md](edges/claim/claim.md) still asks. [petition-next.md](edges/petition-next/petition-next.md) says the generic relation is not this edge and is not drawn. He decided there is no generic "related" edge. He did not say to delete the candidate file. Matters because two proceeding edges can drift. Blocks dropping one of them.

17. **One home for a proceeding relation.** Does `ClaimRelation` name the same concept as the claim links inside [claims](../../../modules-plugable/rights/claims/claims.md)? [claim.md](edges/claim/claim.md) asks. He did not answer. Matters for a single home. Blocks merging the two.

18. **Edge or proceeding node.** For a multi-case proceeding, is the relation one edge per related case, or a proceeding node both cases attach to? [claim.md](edges/claim/claim.md) asks, and points at an open question in ownership. He did not answer. Matters for a bare edge. Blocks that shape.

19. **Direction and name of `claim_relation`.** [claim.md](edges/claim/claim.md) says nothing is ratified. Matters because a bare edge is not ratifiable. Blocks ratifying that candidate.

20. **The pluggable link edges that are not drafted.** Which edges connect claims that are related but not ordered, and in which module? His examples are: the defendant says this was already claimed; a similar case in another organization; a third-party objection during the proceeding; annulment of a ruling as a new case. He decided each reason is its own pluggable edge, and that `answers` is not the third-party link. The edges are not in this package. Names, ends, and who may create them are not stated. Matters because the link rule he called open on the morning of 2026-09-27 is only partly closed. Blocks those edges. It does not block the rejection of one generic related edge.

21. **An answer on the petition path.** May a case that `answers` another also sit in that other case's `petition_next` path? [petition-next.md](edges/petition-next/petition-next.md) says the afternoon list does not settle it. Matters for a constraint between the two edges. Does not block the order edge by itself.

22. **Who creates `petition_next`.** Who may create the edge, and may it be added, removed, or retargeted after the later case leaves draft, for a reason other than the inquiry? The inquiry may change the chain or the chain may be absent. That part is decided. The creator and the later change are not recorded. [petition-next.md](edges/petition-next/petition-next.md) says so. **Proposal, not ratified:** model v2 and the pilot synthesis both stated that the edge may be created while the later case is still draft, including before the predecessor's shortcut is accept. That answers part of this question, and it is a draft sentence rather than his answer. Matters for a bare edge. Blocks those two rules.

23. **What creates a case.** [case.md](case.md) asks what triggers the node: a disputed invoice, a violated rule, or something else. He did not answer. Matters for the entry. Blocks that trigger. [complaint-url.md](edges/complaint-url/complaint-url.md) leaves the same trigger here.

24. **States.** What are the states of a case, and which transitions are valid? [case.md](case.md) asks. Shared draft is the only status the ruling draft uses. He did not give the state machine. The no-finality note says words that imply permanence wait on that machine. Matters for every status word. Blocks the machine.

25. **Liability.** Does liability live in this domain, or do cases only establish it? The chain is event, then liability, then obligation, then a transaction. Who owns each link? [case.md](case.md) asks. He did not answer. Matters for the rights boundary. Blocks placing liability.

26. **A case and a rule.** How does a case reference the rule allegedly violated, given the rule temporal-validity question in Memar is unresolved? [case.md](case.md) asks. He did not answer. Matters for the accusation's ground in policy. Blocks that reference.

27. **Enforcement.** How does resolution of a case interact with the enforcement capability? [case.md](case.md) separates that capability from the dispute process and leaves the interaction open. He did not answer. Matters so execution, which is a compelled service, is not silently treated as enforcement. Blocks that interaction.

28. **`settlement_for`.** Is that relation the invoked service, or a different relation? On the morning of 2026-09-27 he was not sure it is the execution path. Execution is the compelled filed service. The ruling draft says `settlement_for` is not recorded as that path. [claims](../../../modules-plugable/rights/claims/claims.md) asks whether it belongs with the claim kinds. What the edge is remains open. Matters because the file still sits on the case. Blocks folding it into `claim_service` and blocks moving it.

29. **`orgID` on the complaint URL.** Does it select the receiving organization or the accused organization? [complaint-url.md](edges/complaint-url/complaint-url.md) asks. The URL is not an edge. He did not answer. Matters only if that intake sketch is pursued. Does not block the complaint label.

30. **What complaint intake opens.** Does it feed claims, or open a bare case? [complaint-url.md](edges/complaint-url/complaint-url.md) asks. He did not answer. Same limit as question 29.

31. **The cited `case.go` comment.** The complaint-URL draft says the backlog attributed the sketch to `case.go`, and that no tracked copy of that comment lived there. Is the citation mislabeled? He did not answer. Matters for the sketch's provenance. Does not block the model.

32. **Witness.** Is a witness a user-attachment on the case, or only a person related to the thing evidence points at? [evidence.md](edges/evidence/evidence.md) asks. He said witness may be a pluggable edge when its own reason is stated. He did not state that reason, and he did not choose the end. Matters for a witness edge. Blocks that edge.

33. **Participant labels and management role.** Are the remaining participant labels the same mechanism as `modules/management/role`, or are they case-specific? [participant.md](edges/participant/participant.md) asks. The judge edge is not that management role. He did not answer for the other labels. Matters for where a later edge is registered. Blocks using the management role as their home.

34. **Decision words.** Do Dismissal, Invalidate, Guilty, and Conditionally need an explicit state machine before any of them is a state? [participant.md](edges/participant/participant.md) asks, from the no-finality note. He did not answer. Same block as question 24 for those words.

35. **Suspect.** Is Suspect a planned role or a rejected one? [participant.md](edges/participant/participant.md) says it was commented out in the source. He listed suspect among offices that may exist as pluggable edges, and he did not say the commented-out label is rejected. Matters for that one label. Does not by itself add the edge.

36. **Direction and name of `participant`.** [participant.md](edges/participant/participant.md) says nothing is ratified, and an implementer does not write that edge. The three edges plaintiff, defendant, and judge are his working attachments. Matters so the inventory is not implemented beside them. Blocks ratifying `participant`.

37. **Which unratified labels are added.** Which of Jury, Suspect, Lawyer, TrialAttorney, Counsellor, JudicialOfficer, and Witness is a user-attachment in this phase? He said each may be a pluggable edge for its own reason, and that a gloss is not that reason. A judge may say the claim needs ten jurors. That module is not written. Matters for every such edge. Blocks all of them. It does not block leaving them out of the kernel.

38. **Economics and sequence.** Is `claim_service` an edge to the economics service domain, and does an order of services need sequence semantics? [service.md](edges/service/service.md) asks. He did not answer. The draft says one case names one service and that this phase does not write the transaction module. Matters for the end of the edge. Blocks pointing it at economics by default.

39. **Where `claim_service` lives.** Does it move into claims with the accusations, or stay on the case? [service.md](edges/service/service.md) asks. He did not answer. Matters for the module boundary. Blocks the move.

40. **Direction and name of `claim_service`.** [service.md](edges/service/service.md) says nothing is ratified. Matters for a bare edge. Blocks ratifying the edge. It does not withdraw his decision that execution is a compelled service.

41. **Who writes grounds, evidence, and answers.** Critique v1 found that who may create each edge is mostly unrecorded. Most files now say so for their own edge. [grounds.md](edges/grounds/grounds.md), [evidence.md](edges/evidence/evidence.md), and [answers.md](edges/answers/answers.md) state no creator and do not ask for one. He did not answer. Matters because an edge with no who-may-create rule is a bare edge. Blocks ratifying those three edges.

## Assumptions

- **Strong.** Matching any country's law is not a goal. If that were reversed, questions 6, 8, 9, 10, 13, and 14 would have to be re-read against the opened sources as targets rather than as evidence.
- **Strong.** This phase writes no code. A Go file is not the model.
- **Weak.** Sentences in the case drafts that he has not ratified, including model v6's pointer, describe a proposal. If he rejects B, questions 1–5 and 10–12 move with that rejection, and the rejected list in the changelog stays as the record of what was not done.

## Proposed Next Steps

1. He ratifies or rejects model v6's B, including whether a vote-to-request edge is drawn. Depends on questions 1–5.
2. He does not treat draft sentences cited under questions 6–41 as his answers. Each one is still his question.
3. A file that carries an unratified sentence marks it in place. Entering the repository does not ratify it. The model v6 proposal stays in that set for as long as the vote-to-request edge is not drawn and he has not ratified it.

## Related Artifacts

- [case.md](case.md) — Review. The draft states the proposal and links this handoff for enforcement.
- [case.changelog.md](case.changelog.md) — None beyond what that entry already says. Rejected alternatives live there.
- [case.pilot-context.md](case.pilot-context.md) — None. Dated inputs.
- [case.research.001.md](case.research.001.md) through [case.research.007.md](case.research.007.md) — Review. Question disposition is in the notes below.
- Critique v1-v4, model v1-v6, and the synthesis, which this handoff's questions cite by name — None. They were the pilot's review records. What each one was is in the last entry of [case.changelog.md](case.changelog.md), and each question above carries what it needs from them.
- [claim labels](../../../modules-plugable/rights/claim-labels/claim-labels.handoff.md) — None for the complaint label. Action there is the handoff's own.
- [registry inquiry](../../../modules-plugable/rights/claims/edges/registry-inquiry/registry-inquiry.handoff.md) — Review. Joint procedure and the identity-theft service list.
- [judge assignment](../../../modules-plugable/rights/judge-assignment/judge-assignment.handoff.md) — Review. Who may be a judge, the score examples, a later higher rank.
- [judicial office](../../../modules-plugable/rights/judicial-office/judicial-office.handoff.md) — Review. A standing authorization with no case.
- [Transaction handoff](../../economics/transaction/transaction.handoff.md) — None. Its open question 6 holds the draft-transaction proposal and the reversal of an executed service.
- [Delegate handoff](../delegate/delegate.handoff.md) — None. Its open question 5 holds filing a case for another user.
- User, content, and timeline domains — Create is not this phase. Notes only: identity hiding, and visibility until every required judge has voted.

## Notes

Model v6's own Questions for Omid says the comparison picks B and asks nothing further. That is the proposal's stance. It is not ratification. Questions 1–5 stay open because the edge is not drawn.

Disposition of every Questions-for-Omid item in the researches, so none is dropped:

| Source | Item | Where it stands |
|---|---|---|
| case.research.002 | 1 skipped or bi-haqqi ruling | Open, question 6 |
| case.research.002 | 2 per-claim role | Answered, 2026-09-26 and 2026-09-27, parties per claim |
| case.research.002 | 3 claim individuation | Answered, ordered edge among case nodes |
| case.research.002 | 4 indivisibility test | Answered, a vote never counts on another case |
| case.research.002 | 5 amendment graph | Open, question 7 |
| case.research.003 | 1 claim unit | Open, question 9 |
| case.research.003 | 2 per-claim ruling | Open, question 8 |
| case.research.003 | 3 functional-role placement | Answered, `modules-plugable`; which of his labels is question 37 |
| case.research.003 | 4 role per person per claim | Answered, with research 002 question 2 |
| case.research.003 | 5 pre-filing registry | Answered, inquiry is not a gate |
| case.research.004 | 1 ruling edge on a claim | Open, question 8 |
| case.research.004 | 2 person × claim × role | Answered, with research 002 question 2 |
| case.research.004 | 3 refiling panel size | Answered, no kernel count; margin; numbers are pluggable examples and were not adopted |
| case.research.004 | 4 cost and assignment | Answered, person-hours plus fixed system fee; who names a judge is pluggable |
| case.research.004 | 5 earlier decision in the pool | Answered, the vote stays and is outvoted; no history edge |
| case.research.004 | 6 inquiry as draft-gate | Answered, he rejected the gate |
| case.research.005 | 1 three-way ballot | Answered, no abstention |
| case.research.005 | 2 abstain counted against the claimant | Answered, no abstention |
| case.research.005 | 3 partial numeric grant | Open, question 10 |
| case.research.005 | 4 aggregation function | Open, question 11 |
| case.research.005 | 5 quantity on the ballot | Open, question 12 |
| case.research.005 | 6 issue-by-issue | Open, question 13 |
| case.research.005 | 7 linked constraints | Open, question 14 |
| case.research.006 | 1–6 blind voting | Answered, see Ambiguities Resolved |
| case.research.007 | 1, 2, 3, 5, 6 | Answered, one judge edge |
| case.research.007 | 4 party-chosen judge | Answered as the same edge; "any person" is open on the judge-assignment handoff |
| critique-v4 | 1 ballot edge | Open, question 1 |
| critique-v4 | 2 consensus act | Open, question 3 |
| critique-v4 | 3 draft request | Open, question 5 |
| model v5 | fork 1 ballot type | Open, question 1 |
| model v5 | fork 2 consensus act | Open, question 3 |
| model v5 | fork 3 parameter placement | Open, question 2 |
| model v5 | fork 4 conditional accept again | Open, question 4 |
| model v5 | any person may be a judge | Open on the judge-assignment handoff |
| model v5 | four score examples | Party-score weight is rejected; the other examples are open on the judge-assignment handoff |
| model v6 | Questions for Omid | No question asked; B is awaiting ratification, questions 1–5 |
| model v2 and synthesis | 1 what a complaint can do that a case cannot | Answered 2026-09-27, a complaint is a label, not a node |
| model v2 and synthesis | 2 claim relation as the petition order | Open, question 16 |
| model v2 and synthesis | 3 identity theft and the inquiry's ends | Defendant answered 2026-09-27, the target organization; the service list is open on the registry-inquiry handoff, question 2 |
| model v2 and synthesis | 4 indivisibility | Answered 2026-09-27, a vote on one case is never a vote on another |
| model v2 and synthesis | 5 contract voter | Answered 2026-09-27, an arbitrator is a judge on the one judge edge |
| model v2 and synthesis | 6 unratified labels | Open, question 37 |
| model v2 and synthesis | 7 kidnap and stolen ends | Answered 2026-09-27, kidnap runs from the claim or case to the kidnapped user; stolen stays an edge of that kind of claim |
| model v2 and synthesis | 8 settlement for | Open, question 28 |
| model v2 and synthesis | 9 same claim, for a larger pool | Answered in part 2026-09-27, the same parties and amount are not the same claim, and there is no kernel pool to enlarge; what one claim is stays question 9 |
| model v2 and synthesis | 10 fee inputs | Open on the filing-fee handoff, question 1 |
| model v2 and synthesis | 11 standing office | Open on the judicial-office handoff, question 1 |
| model v2 and synthesis | 12 companions of a waiting draft | Withdrawn with the inquiry gate 2026-09-27; no case waits on an inquiry |
| model v2 and synthesis | 13 organization filer | Answered 2026-09-27, an organization is a user type and is the plaintiff edge's end; filing for another user is open on the delegate handoff, question 5 |
| model v2 and synthesis | 14 past majority | Answered 2026-09-27, not its own edge |
| model v2 and synthesis | 15 third party | Answered 2026-09-27, `answers` is not the third-party link; that link's edge is question 20 |
| model v2 and synthesis | 16 defendant's end | Answered 2026-09-27, a group or an organization |
| model v2 and synthesis | 17 vote reason | Answered 2026-09-27, reasons are timeline texts on the case, not a field of the vote |
| model v2 and synthesis | 18 answer on the path | Open, question 21 |
| pilot context, morning of 2026-09-27 | how conflicting rulings relate on a refiling | Answered in part, votes stay where cast, a past majority is not its own edge, and a repeat is an organization choice; the link edge is question 20 |

Model v1's nineteen questions are merged into model v2's eighteen. Critique v2 and critique v3 questions are the same forks. Critique v2's adjudicator-collapse question is closed by one judge edge, except the enforcement and challenge queries he named as the falsifier, which stay the falsifier and are not a second type. Critique v2's partial-quantum and numeric-reason questions are questions 10 and 12. Critique v3's four questions are questions 1–4.

## Earlier thread: graded enforcement and coercion capability

The sections below are the content this file held before the justice pilot was merged into it. They are kept in full, and they concern a different topic: the graded enforcement capability and the Go to Khayyam conversion of this domain. Their headings sit one level lower than the pilot sections above.

### Topic & Purpose
The graded enforcement/coercion capability question: whether the ability to restrict another party's freedom of action (detaining a person, enforcing settlement of a debt) is a government-exclusive attribute or a graded capability any organization can hold in different scopes. Raised during tax-modeling/enforcement discussion; explicitly deferred to a dedicated chat.

### Status
Paused - deferred to a dedicated session; the core claim is untested.

### Decisions
None. The working hypothesis is under exploration:
- **Enforcement/coercion capability is a graded capability or permission scope** attached to an Organization (via certification, legal registration type, or explicit grant) - analogous to privilege rings in an OS kernel - rather than being hardcoded as an attribute exclusive to a "government" label (Tentative).
- **Core claim behind it**: small organizations (building security guard, private security company, a shop owner dealing with a dine-and-dash customer) exercise restricted forms of this capability today, implemented informally (paper records, ad hoc process) only because no affordable unified software made it explicit - not because they do not need it (Tentative).

### Ambiguities Resolved
- "Enforcement" is not a government monopoly by nature - resolved as a modeling question (graded scopes), though the legal boundaries per jurisdiction remain open.

### Open Questions
1. What determines the scope/ceiling of an organization's enforcement capability (a building guard can detain briefly and must hand off to police; a government has broader and different constraints like courts and due process)? - **blocks** the capability model.
2. Is this capability an edge property, a separate node type (a "Mandate" or "Authorization" node), or something else? - **blocks**.
3. Interaction with Code/Rule separation - hypothesis so far: the *existence* of an enforcement-capable edge/relationship is Code; the specific limits, due-process requirements, and escalation paths are Rule. Does not block, but shapes the split.

### Assumptions
- **Privilege-ring analogy transfers from OS kernels to organizational enforcement** - stability: Weak; motivating metaphor, not verified against legal reality.
- **Certification/registration type can serve as the grant mechanism** - stability: Unexamined; connects to the certificate concept in the estate discussions.

### Key Definitions Established
- Enforcement/coercion capability (working): the ability to restrict another party's freedom of action, existing in graded scopes across organization types.

### Proposed Next Steps
1. Run the test scenarios below against a candidate model (edge property vs Mandate node), one graph sketch each.
2. Decide the Code/Rule split for limits and escalation.
3. Reconcile with the rights-domain-boundaries work (Authority != Permission; does enforcement capability derive from Authority, Law, or registration?).

Test scenarios the model must pass:
- A residential/commercial complex guard detaining a dangerous individual temporarily
- A restaurant handling a customer who refuses to pay
- A government enforcing tax collection
- A private security company under contract to a business
- An online platform banning/suspending a user account (a "soft" form of restriction)

### Related Artifacts
- [`Readme.MD`](Readme.MD) - the Case domain this capability interacts with (Review during the session)
- [`../../computer/rule/README.md`](../../computer/rule/README.md) - Code/Rule separation (None)
- [`rights-domain-boundaries.handoff.md`](../rights-domain-boundaries.handoff.md) - Authority/Permission split (Related)
- Memar `docs/modeling.md` -> Separating Structure (Code) from Policy (Rule) (None)

### Notes
- The original context note (edges/topic-coercion-graded-capability.md) is retired into this handoff; its stale references (topic-case-dispute-domain.md, rfc-code-rule-separation.md) pointed to documents that have since moved - the current homes are this module's Readme.MD and the rule README respectively.

### Go → Khayyam conversion (protocol layer)

#### Status
The domain's one `.kh` file accepts under the Khayyam frontend. Nothing in the five edge folders was converted, and their own documents say why.

#### Converted
- `protocol/dt-uuid.kh` — `Field_CaseID` + `CaseID () (t ThingUUID)`

#### Decisions
- **The case's identity is `ThingUUID`**, imported from `identity/thing/protocol/dt-uuid.kh`. The Go declared `type UUID group_p.UUID`; `group_p.UUID` was itself `user_p.UUID`, so the alias reached one identifier concept through a third domain's name and the owner is now imported directly.
- **No edge label became a type.** `claim`, `complaint-url`, `participant`, `service` and `settlement_for` hold label vocabulary only, and each of their documents says the labels must not be ratified as edges ("no bare edges") — [participant.md](edges/participant/participant.md) records an iota set and scattered decision/responsibility notes with no edge code behind them; [complaint-url.md](edges/complaint-url/complaint-url.md)'s own Placement reads "Not an edge - UI, not model." An edge label declared as a Khayyam type would be an empty abstraction, which is the one thing the governing rules refuse. Nothing was written for any of them.

#### Findings
1. **A definition of "case" is legal content and is not in `case.md`.** The Go carried the sentence "a comprehensive term for any proceeding in a court of law whereby an individual seeks a legal remedy". [case.md](./case.md) opens "This domain is the dispute node" and carries the kinds-of-dispute and no-finality principles, but not the definition. Recorded here rather than encoded; it belongs in `case.md` if it is to be stated at all.
2. **No disagreement between the documents and the Go.** The Go had one declaration and it fits the node the documents describe — the changelog's "the case node is the kernel" and `settlement_for`'s `(case)-[:settlement_for]->(thing)` both read naturally against a case that has an identity.

#### Open Questions added by the conversion
1. **Where the definition of a case goes** — see finding 1. [case.md](./case.md)'s open question "What triggers the creation of a Case node" is still the larger gap: nothing declares what a case must carry before it exists.
2. **Whether a case references the rules it allegedly violates.** [case.md](./case.md) raises it; `Field_CaseID` says nothing about it, and `computer/rule` is not converted, so the same missing-abstraction problem the delegate domain hit applies here.
3. **Whether `settlement_for` stays** — [case.md](./case.md) asks whether it is part of this type or another optional kind. It is unaffected by the conversion but unresolved by the documents.

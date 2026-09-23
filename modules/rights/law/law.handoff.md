# Law Handoff

## Topic & Purpose
Working state of the law *type*. Duration lives at plugable [Law Validity](../../../modules-plugable/rights/law-validity/law-validity.md). Optional drafts live per concept, starting with [Family](../../../modules-plugable/rights/family/family.md) and [Marriage](../../../modules-plugable/rights/marriage/marriage.md).

## Status
Active — the type states the signed instrument, what is in force, and what is outside the type. Shared companions with contract, and the digest, remain open. Law labels are registered in the plugable module.

## Decisions
- The four companions are present before a binding signature. After that signature the payload stays as signed. Critique can continue in the same period; a reaction is not a signature. *(Decided — owner)*
- Changing a disputed number is a new node because its effects are not small. *(Decided — owner)*
- Executive guarantee is how the law takes effect, not a mandatory sanction. *(Decided — owner this session)*
- A law is typically realized as one or more [Rule](../../computer/rule/rule.md) nodes. Law and Rule are layers, not islands. The Rule set is inside the digest. *(Decided — owner this session)*
- Folk labels attach to comments, not to the law node. Influence filters reading, not vote weight. *(Decided — owner this session)*
- Specific statutes are instances, not this type. *(Decided — owner)*
- Do not dual-maintain the type. *(Decided — owner)*
- Duration of votes and laws is a plugable organisational capability. *(Decided — owner; git mv to `modules-plugable/rights/law-validity`)*
- Appointing a voter is [Delegate](../delegate/delegate.md). The delegate's signature on each proposition is visible. Replacing that signature on one proposition, while the appointment continues, is the owner's rule. Whether the empty rule on the delegate record (the whole appointment given back) is also that one-proposition case is open. *(Decided — owner for the rule; gap against the existing record is open)*
- Family and marriage are separate plugable modules a bundle includes or leaves out. *(Decided — owner)*
- Two contradictory laws do not both stay in force for a later choice of which one executes. Passing a new law that conflicts cancels the previous one, through a link stated with the proposal. That is not a complaint for a judiciary to resolve. *(Decided — owner, reviewing research 002)*
- No-retroactivity, and when a contract yields to a law, are statutes in [laws](../../../modules-plugable/rights/laws/laws.md), not the type. *(Decided — owner)*
- What a vote does to another law is the case request the organization included. Annul-for-conflict annuls the second law. Annul-for-update makes the new law supersede the previous one. *(Decided — owner)*
- `supersedes` is an edge of thing. A contract and the estate that is now realized need the same relation. Content's current direction keeps one identity and change events, so that direction does not use this edge for an edit. *(Decided — owner for the shared-home test; placement checked against contract, estate, content, and product)*
- Statuses of this domain are loop-edges under `status/`. The account of what a status is, including the query, is [status](../../knowledge/status/status.md). *(Decided — owner asked where they are defined)*

## Ambiguities Resolved
- **Where instance statutes live after the society corpus left Memar.** Settlement-specific statutes are modules of the bundle that enforces them. Duration/sunset is not one of those; it is plugable.
- **`### Model` on a domain document.** A Cypher/edge list is a cache of `edges/` and `aggregation.go`. Removed from [law.md](law.md).
- **Wholesale bundle→plugable.** Only duration left government. Membership and judiciary are split questions on [bundles.handoff.md](../../../bundles/bundles.handoff.md).
- **Post-vote explanation-append.** Not an owner rule. It was Grok's inference from "later precision appends to interpretation." Once voting starts, nothing in the payload changes. *(How: owner this session, answering research 001 finding 1.)*
- **Empty computer_code as the only draft gate.** Too strong a reading of one example. Any empty required companion keeps the record in draft. *(How: owner this session.)*
- **Guarantee as sanction.** A misread of ضمانت اجرایی. *(How: owner this session.)*
- **The node and the order.** A law node is one signed instrument. The legal order is which instruments are in force together. The human code and computer code state the position (duty, permission, power, or immunity). The type does not add a companion that only names that position. *(How: research 002, written into the type.)*
- **Goal against the sentence.** The goal does not outrank human code or computer code. A result the sentence refuses is a drafting failure before signature. A more general reason is still a goal. *(How: research 002.)*
- **Unsatisfiable computer code.** A form no input can satisfy is not opened for a signature. *(How: research 002.)*
- **Publicity.** The human code in the signed payload is how a person reads the law they sign. The type adds no separate publication record. Who is bound without having signed stays with law-validity. *(How: research 002.)*
- **Critique scenarios.** Scenarios generated from the computer code, in human language, stay outside the digest. *(How: research 002.)*
- **Constitution is a label.** It is not a second kind of law. The same cycle applies to every instrument. A label does not block change and does not hold a wish the sentence does not state. *(Decided — owner)*
- **Not only a government.** A society's statute and an organization's articles of association are both this type. *(Decided — owner)*
- **A law superseding a contract** is a statute an organization may adopt, [law supersedes contract](../../../modules-plugable/rights/laws/law-supersedes-contract/law-supersedes-contract.md), not the type. *(Decided — owner)*

## Open Questions
1. **Vote edges and the election widget stay in this folder?** The widget records critique and signature. Whether the folder stays here is still open.
2. **One proposition, or the whole appointment.** [Delegate](../delegate/delegate.md) records who gave and who received the appointment, and an empty rule means the appointment was given back. The owner's rule also allows a signature on one proposition while the appointment continues. Is that empty rule the one-proposition case, or a different fact?
3. **Departed member's vote.** Delete the signature, or keep it as history and omit it from a live count?
4. **Consent vs Agreement vs vote artifact** — from [normative-bootstrap.handoff.md](../normative-bootstrap.handoff.md). Blocks representing founding acts, not the law type.
5. **Authority / legitimacy** — same bootstrap handoff; still blocking bootstrap, not the type.
6. **`_import/law-vote` constants** (`IntervalVoteChanging = 30`, `IntervalLawSuggestion = 30`) look like the rejected post-ratification clock. Unexamined.
7. **Digest and signature home.** No hash module exists in this repository. [signature](../../computer/request/edges/signature/signature.md) is on request. What computes the payload digest, and what type is the vote signature?
8. **TTL vs law-validity.** Unchanged from research 001 finding 8.
9. **Where the under-one-thousand law aim is stated.** The owner set that scale. It no longer has an umbrella module. Which single document carries it?
10. **Shared companions with contract.** The names are settled: human code is the human-language sentence, computer code is the machine-checkable form. Law has both. Contract's former `code` edge is computer code and points at a rule. Contract `terms` still points at text and at a Solidity object. Is terms the contract's human code, a mix that should split, or a third relation? Are law's computer code and contract's computer code one shared edge? Same question for executive guarantee, which contract does not yet have. *(with [contract.handoff.md](../contract/contract.handoff.md))*
11. **What the shared edge would attach to.** If computer code is one edge, whose signature digest includes it when the record is a contract rather than a law? A contract is signed by its parties. A law is signed by the people the vote binds.

## Anticipated Work
- If vote edges move, the Boundaries bullet in [law.md](law.md) updates in the same session.
- Resolve whether a one-proposition signature is the delegate record's empty rule or a separate fact.
- Do not open `law-priority` or a separate retroactivity module. Basic statutes are [laws](../../../modules-plugable/rights/laws/laws.md). Kinds of dispute are [claims](../../../modules-plugable/rights/claims/claims.md).

## Assumptions
- The five-field interface in `edges/aggregation.go` is the intended schema, not a sketch. Stability: Strong.
- Human-readable law bodies are Text-domain nodes via `human_code_is` / `goal_is` / … Stability: Strong.
- Among instruments in force, computer-code forms do not contradict. A proposal is not in force until an update claim succeeds and the new instrument supersedes the earlier one. Stability: Decided.
- Grok's vote-count recommendation (keep artifact, omit from live tally) is not an owner decision. Stability: Unexamined as owner intent.
- Two in-force laws with a stated winner were the research's proposal. The owner refused that shape. The effect is the case request the organization included. Stability: Decided.

## Related Artifacts
- [`law.md`](law.md) — type (Update only if a decision above graduates)
- [`law.changelog.md`](law.changelog.md) — history (None)
- [`law.research.001.md`](law.research.001.md) — critique and owner review (Review)
- [`law.research.002.md`](law.research.002.md) — published accounts; placement not applied (Review)
- [`../../../modules-plugable/management/politics/politics.md`](../../../modules-plugable/management/politics/politics.md) — politics (Related)
- [`../../../modules-plugable/rights/family/family.md`](../../../modules-plugable/rights/family/family.md) — optional household draft (Related)
- [`../../../modules-plugable/rights/marriage/marriage.md`](../../../modules-plugable/rights/marriage/marriage.md) — optional marriage draft (Related)
- [`widgets/election/election.md`](widgets/election/election.md) — critique and signature (Related)
- [`../normative-bootstrap.handoff.md`](../normative-bootstrap.handoff.md) — Law / Consent / Authority at founding (Related)
- [`../../../modules-plugable/rights/law-validity/law-validity.md`](../../../modules-plugable/rights/law-validity/law-validity.md) — duration (Related)
- [`../../../modules-plugable/rights/laws/laws.md`](../../../modules-plugable/rights/laws/laws.md) — basic statutes (Related)
- [`../../../modules-plugable/rights/law-labels/law-labels.md`](../../../modules-plugable/rights/law-labels/law-labels.md) — registered comment labels (Related)
- [`../../../modules-plugable/rights/claims/claims.md`](../../../modules-plugable/rights/claims/claims.md) — optional kinds of dispute (Related)
- [`../../identity/thing/edges/supersedes/supersedes.md`](../../identity/thing/edges/supersedes/supersedes.md) — shared successor edge (Related)
- [`../../computer/rule/rule.md`](../../computer/rule/rule.md) — Rule as realization layer (Related)

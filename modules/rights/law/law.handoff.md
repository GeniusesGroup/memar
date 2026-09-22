# Law Handoff

## Topic & Purpose
Working state of the law *type*. Duration lives at plugable [Law Validity](../../../modules-plugable/rights/law-validity/law-validity.md). Optional drafts live per concept, starting with [Family](../../../modules-plugable/rights/family/family.md) and [Marriage](../../../modules-plugable/rights/marriage/marriage.md).

## Status
Active — the type was corrected for freeze-at-voting, executive guarantee, Rule-layer, and comment-labels; several attachments of this folder are still not placed.

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
- Statuses of this domain are loop-edges under `status/`. The account of what a status is, including the query, is [status](../../knowledge/status/status.md). *(Decided — owner asked where they are defined)*

## Ambiguities Resolved
- **Where instance statutes live after the society corpus left Memar.** Settlement-specific statutes are modules of the bundle that enforces them. Duration/sunset is not one of those; it is plugable.
- **`### Model` on a domain document.** A Cypher/edge list is a cache of `edges/` and `aggregation.go`. Removed from [law.md](law.md).
- **Wholesale bundle→plugable.** Only duration left government. Membership and judiciary are split questions on [bundles.handoff.md](../../../bundles/bundles.handoff.md).
- **Post-vote explanation-append.** Not an owner rule. It was Grok's inference from "later precision appends to interpretation." Once voting starts, nothing in the payload changes. *(How: owner this session, answering research 001 finding 1.)*
- **Empty computer_code as the only draft gate.** Too strong a reading of one example. Any empty required companion keeps the record in draft. *(How: owner this session.)*
- **Guarantee as sanction.** A misread of ضمانت اجرایی. *(How: owner this session.)*

## Open Questions
1. **Vote edges and the election widget stay in this folder?** The widget records critique and signature. Whether the folder stays here is still open.
2. **One proposition, or the whole appointment.** [Delegate](../delegate/delegate.md) records who gave and who received the appointment, and an empty rule means the appointment was given back. The owner's rule also allows a signature on one proposition while the appointment continues. Is that empty rule the one-proposition case, or a different fact?
3. **Departed member's vote.** Delete the signature, or keep it as history and omit it from a live count?
4. **Consent vs Agreement vs vote artifact** — from [normative-bootstrap.handoff.md](../normative-bootstrap.handoff.md). Blocks representing founding acts, not the law type.
5. **Authority / legitimacy** — same bootstrap handoff; still blocking bootstrap, not the type.
6. **`_import/law-vote` constants** (`IntervalVoteChanging = 30`, `IntervalLawSuggestion = 30`) look like the rejected post-ratification clock. Unexamined.
7. **Digest and signature home.** No hash module exists in this repository. [signature](../../computer/request/edges/signature/signature.md) is on request. What computes the payload digest, and what type is the vote signature?
8. **Constitution as classification.** Earlier ruling: categorising label. Folk labels live on comments. Is constitution a restricted classification process, or still a label with a restricted writer?
9. **TTL vs law-validity.** Unchanged from research 001 finding 8.
10. **Where the under-one-thousand law aim is stated.** The owner set that scale. It no longer has an umbrella module. Which single document carries it?

## Anticipated Work
- If vote edges move, the Boundaries bullet in [law.md](law.md) updates in the same session.
- Resolve whether a one-proposition signature is the delegate record's empty rule or a separate fact.

## Assumptions
- The five-field interface in `edges/aggregation.go` is the intended schema, not a sketch. Stability: Strong.
- Human-readable law bodies are Text-domain nodes via `code_is` / `goal_is` / … Stability: Strong.
- Non-contradiction is a check on machine-checkable forms, not a walk of prose. Stability: Stronger than before this review; still Weak as implementation.
- Grok's vote-count recommendation (keep artifact, omit from live tally) is not an owner decision. Stability: Unexamined as owner intent.

## Related Artifacts
- [`law.md`](law.md) — type (Update only if a decision above graduates)
- [`law.changelog.md`](law.changelog.md) — history (None)
- [`law.research.001.md`](law.research.001.md) — critique and owner review (Review)
- [`../../../modules-plugable/management/politics/politics.md`](../../../modules-plugable/management/politics/politics.md) — politics (Related)
- [`../../../modules-plugable/rights/family/family.md`](../../../modules-plugable/rights/family/family.md) — optional household draft (Related)
- [`../../../modules-plugable/rights/marriage/marriage.md`](../../../modules-plugable/rights/marriage/marriage.md) — optional marriage draft (Related)
- [`widgets/election/election.md`](widgets/election/election.md) — critique and signature (Related)
- [`../normative-bootstrap.handoff.md`](../normative-bootstrap.handoff.md) — Law / Consent / Authority at founding (Related)
- [`../../../modules-plugable/rights/law-validity/law-validity.md`](../../../modules-plugable/rights/law-validity/law-validity.md) — duration (Related)
- [`../../computer/rule/rule.md`](../../computer/rule/rule.md) — Rule as realization layer (Related)

# Law Research 001 — Critique of the type as recorded

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Owner review](#owner-review)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)

## Status
Active

## Question and Goals
- **Questions:**
  - Does the law type recorded in [law.md](law.md) hold under its own criteria (domain boundaries, attribute-or-edge, Code/Rule, concept existence)? — Answered (holds after the freeze, guarantee, Rule-layer, and comment-label corrections; see Owner review)
  - Which of its failures are structural (the type must change) and which are placement (the type is sound; a companion is in the wrong folder)? — Answered (freeze and guarantee wording were structural misrecords; duration placement already moved; vote-count on death remains placement/consent)
- **Goals:**
  - Give the owner an examinable critique of *this* model, not of traditional statute books. — Met (this file)
  - Graduate accepted points into [law.md](law.md) via changelog, or record a negative result. — Partially met (freeze, guarantee, Rules-as-realization, comment-labels, politics definition graduated; vote-count on death and digest-algorithm home have not)

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Reviewed — not approved as a package; per-finding outcomes in Owner review)
- [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — Researcher

## Methodology
First pass: single reasoning against [law.md](law.md) as then written, `edges/aggregation.go`, vote edges, [law-validity](../../../modules-plugable/rights/law-validity/law-validity.md), Memar modeling, and the law changelog. Findings were arguments, not measured results.

Second pass: owner review of those findings. Several findings were inferences the owner never granted. The first-pass text is kept below so the misread is auditable; the Owner review is the standing outcome.

## Findings

### 1. Explanation-as-append recreates the note under another name
The type's own example of a good law is one sentence — every resident pays 20 percent of income yearly — with everything else in explanation. The motivation for dropping articles was that the proposer must state *coverage in the text*. If "who is a resident" and "what is income" live in explanation, coverage has moved, not disappeared. Worse: explanation is allowed to grow *after* the vote, without rewriting the text the vote attached to. Defining "income" to include or exclude capital gains changes the effective norm. The type treats explanation as non-normative clarification; under its own criterion (the text is the law) those definitions *are* the law. (Grok, first pass)

Standing after review: the post-vote half was Grok's inference from the changelog sentence "later precision appends to interpretation," not an owner claim that a record may change after voting starts. The coverage-in-explanation half remains a writing discipline (definitions that change who pays belong in the text, and still before the vote). (see Owner review)

### 2. Computer code as a voting gate binds the type to this platform
A record may not leave draft while `computer_code` is empty. That is a completeness rule of *this software*, not of "what a law is." Constitutive norms and qualitative duties either become ineligible or fill the field with a description that is not executable. The same gate also lets whoever can code shape what may be voted. Code/Rule in Memar already separates structure from policy; "must be coded before voting" is policy, currently written as if it were Code. (Grok, first pass)

Standing after review: empty *any* required companion keeps the record in draft. Freeze-at-voting and the digest are Code of this type. Extra eligibility an organization adds is plugable Rule. The four companions are default eligibility for ratification, not a disposable example. A law that cannot show itself in computer language and be independently evaluated is, on the owner's criterion, inherently problematic. A law may be realized as several Rule nodes; Law and Rule are layers, not islands. (see Owner review)

### 3. Mandatory executive guarantee assumes every law is a sanction
The type requires a stated consequence of disobedience. Power-conferring and constitutive rules (Hart) have no natural "disobedience." Forcing a guarantee onto them either invents a fake sanction or declares them not-laws. (Grok, first pass)

Standing after review: Grok read "what follows if disobeyed" as sanction. The owner meant executive guarantee: how the law takes effect. Constitutive and power-conferring texts still have an operational path. (see Owner review)

### 4. Non-contradiction is not a type-level check this graph can run
Detecting contradiction among natural-language texts is not a graph traversal. If a human judges it, the type has smuggled adjudication into Law. If only computer_code is checked, the human text can still collide. (Grok, first pass)

Standing after review: independent evaluation is the computer form. Text remains so humans need not learn that language (score vs listening). A record whose text and computer form diverge is not eligible. Contradiction among machine-checkable forms is then a check this graph *can* run. A remainder that "must" be judged only as prose was requested; Grok did not find a predicate that must stay unevaluable — only offices that *delegate* evaluation, and that delegation is itself codeable. (see Owner review)

### 5. Rival nodes without a cheap correction path
A typo in explanation becoming a new node with a new vote is a cost the model had not priced. Explanation-append was meant to be that cheap path; finding 1 said append was already doing normative work. (Grok, first pass)

Standing after review: same answer as finding 1. After voting there is no cheap path. That cost is the point. 20 percent to 30 percent is not a small edit. The cheap path is draft and get-critique, before the digest is signed. (see Owner review)

### 6. Consent is modeled as an edge of the law while the type denies it
`(law)-[:vote_agree_by]->(user)` makes agreement a relation of the law node. Consent has its own lifecycle. (Grok, first pass)

Standing after review: a vote is a signature over the payload digest, a consent record, not a field of what a law is. Counting when a member leaves (delete the signature vs keep it and omit it from a live count) is unanswered. (see Owner review)

### 7. Unbounded labels can break the comparison the type depends on
Whoever may attach "extortion" or "tax" shapes what voters think they are comparing. (Grok, first pass)

Standing after review: labels are applied by people when they comment, beside the comment. Not every comment is read. Filters: badges, and domain-influence the reader has already granted. Influence filters reading, not vote weight. (see Owner review)

### 8. Duration was placed as if it were a Geniuses.Group statute
Time-bounding of a vote and of a law is a general organisational concern. Placement is now `modules-plugable/rights/law-validity`; overlap with kernel TTL is not yet examined. (Grok)

Standing after review: placement stands. TTL overlap still unexamined.

## Owner review

Owner (Omid Hekayati), answering the first-pass findings in order:

1. Nobody granted that a law may change after voting starts. Status may move (draft, get-critique) and those stages may still edit the record. Once status is voting, no part of the record may change. Voting is a digital signature over a hash of the whole content; the smallest change means the votes were for a different law. That is why a law must be written clearly: changing it imposes a large cognitive cost on the community, and must not be treated as cheap. Moving a rate from 20 percent to 30 percent is not a small edit; its effects are large. Today's statute books treat law as unserious words whose execution is the deceptive behavior of rulers. "Policy" and "politician" were not the words used for that theater, because سیاست is a general concept: wherever a question has several correct answers, the science of politics is needed — in a company, a family, and a friendship, not only in governing a society.

2. Empty any field means the record cannot leave draft. The computer-code-only example was too strong a reading of one illustration. Some completeness rule is needed in order to run voting. A law can include several Rules; writing them as isolated islands was wrong.

3. The subject is executive guarantee (how the law takes effect), not a mandatory sanction. The first pass misread the field.

4. A law that cannot manifest in computer language and be independently evaluated is inherently problematic. An example was requested of a law that *must* be judged only as text. Text was kept because a community cannot be forced to learn a computer language in order to live under a law — as listeners cannot be forced to learn music notation in order to hear a piece.

5. Same as (1). After voting, no cheap repair.

6. Vote counting is unfinished. When a person leaves the society (including by death), is that person's vote deleted from the law, or kept and merely omitted from a live (for example daily, exploratory) count?

7. Labels are applied by people when they comment, beside the comment. Comments are not all read. Mechanisms such as badges, and filtering to comments of people the reader has already voted as influential in a domain, are needed. Law and rights must not be seen in the traditional shape; the reading layer has to be invented, not copied from a statute book.

Grok, after that review:

- The post-vote append was my sentence. It entered [law.md](law.md) from the changelog line "later precision appends to interpretation and does not rewrite the law," which I treated as a cheap path after ratification. The owner never said that. (Grok)
- Freeze-at-voting plus a digest the signature binds to is Code of consent, not a plugable preference. A checklist of *extra* eligibility beyond the four companions can be plugable Rule. (Grok)
- Completeness-as-nonempty-companions is needed to run honest voting: a signature on an empty meaning is theater. (Grok)
- Law realized as several Rules is the layering the first pass should have written. If a Rule can be added after voting, the freeze is fake; the Rule set belongs in the digest. (Grok)
- Executive guarantee and computer_code can collapse if both only say "the machine will do it." The split worth keeping: guarantee is the observable effect and the fallback when the machine path cannot run; computer_code is the independently evaluable score. If they say the same thing in two languages, one field is redundant. (Grok)
- Requested example of a law that must be judged only as text: mercy ("the assembly may forgive a debt when keeping it would destroy a household") looks like one. The *office* (who may forgive, that they did) is codeable. Whether *this* household is destroyed is unevaluable until the law states measurable criteria. If even that remainder must be machine-checkable, then discretionary mercy without a metric is a poorly written law, not a proof that evaluation must stay prose. The interesting remainder is delegated judgment (an office authorized to decide), which is itself a Rule, not a hole in the law. I do not have a predicate that *must* stay unevaluable. (Grok)
- That mercy example, and an assembly calendar, do not survive the later test. Ask whether the topic needs to be a law. Mercy is a power in a contract or a case. A meeting date is a group rule. Marriage is already a [contract](../contract/contract.md). None of these is a statute this domain should grow. (Grok)
- Music analogy: listeners need no notation; *performers* do, if the performance is to be checked. Citizens listen; the platform and officers perform. If text and score diverge, the record is ineligible. The leftover drafting-monopoly is real: whoever can write the score still shapes what may be signed, unless critique-stage tools show what the code will do in human language *from the code*, not as a free-hand story. (Grok)
- Vote on death: keep the signature as history; omit it from the live count. Deleting the artifact makes it impossible to explain why a law passed. Civic sunset is about weight in the live tally, not erasure. Distinguish a diagnostic daily count from the count that keeps a law in force. This is a recommendation, not an owner decision. (Grok)
- Labels on comments: constitution-as-categorising-mark is then not a folk comment-label. If it is still "a label," it needs a restricted writer (a founding process), or it is a different relation. (Grok)
- Influence that filters reading can recreate representation: people vote influencers, the feed shapes what voters think they are signing, while the signature stays "direct." The boundary that keeps this from becoming a senate: influence never weights the vote, and the default feed must include a disagreement sample (comments whose labels contradict the current filter) so a reader cannot only hear their side. Badges are queryable attestations (this person wrote code that compiled; this person lives in the basin), not rank. (Grok)
- Politics: the owner's definition is the right refusal of government-theater. Without a qualifier it swallows every tradeoff (chess, recipes). The qualifier written in [politics.md](../../../modules-plugable/management/politics/politics.md) was disagreement among people who must share one binding outcome. That qualifier was removed from the definition when kernel placement was refused. (Grok)

## Open Questions
- Delete a departed member's vote artifact, or keep it and omit it from a live count? (owner, from finding 6)
- Is the live count that keeps a law in force the same query as a diagnostic daily count? (from finding 6)
- Digest algorithm and signature type: no hash module exists in this repository; [signature](../../computer/request/edges/signature/signature.md) is on request, not yet on law. (Grok)
- Are status markers loop-edges in the status module? Yes. Domain documents leave the catalog there. (updated)
- Is "constitution" a restricted classification process, or a folk label after all? (from finding 7 vs the earlier constitution-as-label ruling)
- Politics qualifier "shared binding outcome" — withdrawn from the definition. Remaining critiques are in [politics.handoff.md](../../../modules-plugable/management/politics/politics.handoff.md).
- Does vote/law sunset compose with kernel TTL? (from finding 8; unchanged)

## Related Artifacts
- [law.md](law.md) — type after owner review (Update)
- [law.handoff.md](law.handoff.md) — remaining live questions (Update)
- [law.changelog.md](law.changelog.md) — freeze, guarantee, Rule-layer, comment-labels (Related)
- [politics.md](../../../modules-plugable/management/politics/politics.md) — definition opened this review; later moved out of kernel (Related)
- [rule.md](../../computer/rule/rule.md) — Law realized as Rules (Update)
- [normative-bootstrap.handoff.md](../normative-bootstrap.handoff.md) — Law / Consent / Authority (Related)
- [ttl.md](../../identity/time/edges/ttl/ttl.md) — general time-to-live (Related)

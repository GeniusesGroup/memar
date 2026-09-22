# Law Changelog

## Changelog

### Law form recorded; traditional article-and-note model rejected
- Time: 2026-09-21T11:04:01Z
- Type: Added, clarified
- Cited:
  - [____Chats/law.md](../../../____Chats/law.md) - Relation: Evidence: owner model of law as text-plus-companions, labels instead of titles, rival versions as new nodes, and domain separation; Gemini's first reply as the specimen of importing article-and-note structure
  - [Law Form and Validity](https://github.com/GeniusesGroup/memar/blob/main/docs/society/governance/law-form-and-validity.md) - Relation: Evidence: later owner rulings on the computer-code gate, constitution-as-label, and non-contradiction; conventional-model flaw of vague articles without an execution mechanism
- Propagates to:
  - Memar `docs/society/governance/law-form-and-validity.md`: Done — corpus left Memar; leftover form prose on [law-validity.md](../../../bundles/government/modules/law-validity/law-validity.md) stripped 2026-09-21 (see later entry)
  - `modules/computer/rule/rule.md`: Done — Rule-vs-Law bullet now points at this definition
  - Instance catalog: Done — instances are bundle modules ([Bundles](../../../bundles/bundles.md)), not this type
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Gemini](../../../CONTRIBUTORS.md#gemini) — argued (counter-model; rejected)
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
The law module now states the type: a law is a text, not a title; goal, explanation, and executive guarantee are mandatory companions; computer code is a completeness gate into voting, not a post-ratification clock; rival versions are new nodes; constitution is a categorising label; new law must not contradict existing law. Open questions left the README for [law.handoff.md](law.handoff.md).

#### Deliberation
Owner (Omid Hekayati): a law is a text. Naming is only a label on that text, and labels may be many and conflicting — "tax", "income", "stable public revenue", "extortion". For each text the proposer must also write goal, interpretation of the words used, and an executive guarantee. Nobody may offer a law for ratification without a guarantee. If the text is interpretable, every used word must be defined; later precision appends to interpretation and does not rewrite the law.

Owner: traditional law-writing puts a name on a statute and then writes articles and notes. That model is badly designed. Articles mix goal with how the text is to be executed. In this model the whole law can be one sentence — example: every resident person must pay 20 percent of income to the government each year — and everything else is interpretation toward executing that sentence. Without articles and notes, the proposer is forced to examine coverage. Iranian direct-tax practice that split employee, merchant, legal person, and building owner made enforcement cost exceed the levy in places the government itself admitted.

Gemini's first reply reintroduced a title, a scope clause, articles, notes, monitoring machinery, and an amendment procedure. Owner: that is the cognitive error of staying inside the current model. Articles and notes *are* the interpretations; putting them back as a parallel structure undoes the split. The same error is analogical thinking importing "ماده" and "تبصره" from the surrounding legal medium.

Gemini then offered extra fields on the law itself: change history, lists of opponents and supporters, vote tallies. Owner: those fields must not sit in the law model. Domain boundaries matter: each model answers one need; a new need gets its own model. Vote statistics, discussion, and history are other domains. The cost of that discipline is high; the payoff is models that later need the least change.

Owner: a change to a live proposal is not an in-place edit. The modifier submits a new version in the same model; a graph of relations among proposals is presented simply — rival texts compared by labels — and people vote for the law they actually have in mind. If one text says 20 percent and someone argues that is too little, they create a rival at 50 percent; the votes on the two texts show which wins.

Owner: a large part of software development is the same process as law-writing. The useful comparison is not "developers should study intellectual-property statutes". It is that a constraint such as "a username may use only English letters" is itself a law; a developer who understands law-writing understands why such a sentence is written that way, and the team needs fewer later clarifications.

Later owner rulings recorded on the Memar society page, applied here as type rules rather than as a society's statutes: a record may enter voting only when complete, including executable code; an empty code field stays draft; once in voting it may remain as long as the community keeps it there; there is no 30-day code-or-return clock after ratification; "constitution" is a category label, not a higher tree; a new law must not contradict an existing one.

#### Considered and not done
- Keep a title (or "law name") as a field of the law — rejected: a name is a label in the label domain; one text may wear many labels.
- Keep articles and notes as the body, with goal / interpretation / guarantee as extra sections around them — rejected: that restores the mix the split exists to prevent; coverage hid in notes.
- Add scope, monitoring, and an in-place amendment procedure as fields of the law — rejected: scope belongs in the text and its explanation; monitoring and amendment are other processes; amendment is replaced by rival nodes.
- Store change history, opponent/supporter lists, and vote tallies on the law node — rejected: wrong domain.
- Treat Gemini's "four-facet plus title plus articles" hybrid as a compromise — rejected: the hybrid is the traditional model with extra headings.
- Dual-maintain this type definition in Memar `docs/society` as a pointer or a shortened copy — rejected this session: a pointer makes the framework repo incomplete without Organization; a copy drifts. The society corpus as a whole is leaving Memar for the libraries layer.

#### Related work
Traditional statute books (a title, numbered articles, rider notes, a later official interpretation or implementing bylaw) are the prior art this model refuses. The refusal is not that those books sometimes write poorly; it is that the article-and-note shape lets a proposer hide coverage, mix purpose with procedure, and leave enforcement unstated, so judges and officers fill the gap with preference. Software constraints (username rules, protocol MUST/MAY) are the closer analogue: a single normative sentence plus definitions, not a committee redline of numbered clauses.

### Form-only type; leftover duration page stripped of type prose
- Time: 2026-09-21T13:50:07Z
- Type: clarified, Fixed
- Cited:
  - [Law](law.md) - Relation: Depends_on: the type this session restates
  - [Law Validity](../../../bundles/government/modules/law-validity/law-validity.md) - Relation: Evidence: leftover four-facet body was still restating the type after the society corpus landed as a bundle module
  - [Bundles](../../../bundles/bundles.md) - Relation: Depends_on: instance statutes are bundle modules, not a libraries catalog
- Propagates to:
  - `bundles/government/modules/law-validity/law-validity.md`: Done — four-facet approach is a stub pointing here; page is duration-only
  - `bundles/government/modules/decision-and-deliberation-process/decision-and-deliberation-process.md`: Done — four-facet syn and related-docs point at this type
  - `bundles/government/modules/government-organs/government-organs.md`: Done — same
  - `bundles/justice/modules/judiciary-and-dispute/judiciary-and-dispute.md`: Done — same
  - `bundles/government/modules/narrating-the-system/narrating-the-system.md`: Done — same
  - `modules/rights/rights.md`: Done — instances point at bundles, not libraries
  - `modules/computer/rule/rule.md`: Done — Law link is `law.md`
  - `bundles/bundles.md`: Done — landing sentence no longer calls form prose leftover
  - `bundles/government/modules/land-housing-tenure/land-housing-tenure.md`: Done — time-bounding syn points at law-validity
  - `bundles/land/modules/buildable-share-and-density-allocation/buildable-share-and-density-allocation.handoff.md`: Done — non-contradiction cites the kernel type
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
The type document now states its claim in an Abstract and names the article-and-note failure as Motivation, without moving the session critique out of this changelog. Instance home is [Bundles](../../../bundles/bundles.md), not Memar `docs/society` and not a libraries folder. [Law Validity](../../../bundles/government/modules/law-validity/law-validity.md) no longer restates goal/explanation/guarantee/computer-code; inbound four-facet syn lines point at this type.

#### Deliberation
The earlier entry left a Pending propagation to Memar. That corpus is gone from Memar; what remained was the imported bundle module still carrying the type as an "approach". Completing the original split — type here, duration there — is this session's work, not a new model.

### Model list removed; type critique opened; duration moved to plugable
- Time: 2026-09-21T14:25:00Z
- Type: Fixed, Added, moved
- Cited:
  - [Law Research 001](law.research.001.md) - Relation: Evidence: critique of this type, not of traditional statute books
  - [Documentation → Content Rule](https://github.com/GeniusesGroup/memar/blob/main/docs/documentation.md#content-rule-no-fabricated-or-redundant-provenance) - Relation: Depends_on: no derivative inventories; an edge list is a cache of `edges/`
- Propagates to:
  - `modules-plugable/rights/law-validity/`: Done — `git mv` from `bundles/government/modules/law-validity`
  - `bundles/bundles.handoff.md`: Partial — remaining bundle→plugable candidates still to classify
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote, argued

#### What changed
`### Model` left [law.md](law.md); relations stay in `edges/` and `edges/aggregation.go`. [law.research.001.md](law.research.001.md) records a critique of this type (explanation-append, computer-code gate, mandatory guarantee, non-contradiction, rival-node cost, consent-as-edge, unbounded labels, duration placement). Duration of votes and laws moved by `git mv` to `modules-plugable/rights/law-validity`.

#### Deliberation
Owner: a Model heading on a domain document is a cache of the live edge set and goes stale. Point at the files; do not index them.

Owner: time and validity of a law is not a Geniuses.Group bundle opinion; many organisations need it. Plugable, not `bundles/government`.

Owner: the traditional-model changelog was not the requested critique of *this* repository's law type. That critique is research 001, not yet reviewed.

### Bundle→plugable wholesale pass closed
- Time: 2026-09-21T14:29:00Z
- Type: clarified
- Cited:
  - [Bundles Handoff](../../../bundles/bundles.handoff.md) - Relation: Evidence: classification result and remaining split questions
- Propagates to:
  - `bundles/bundles.handoff.md`: Done — wholesale question resolved; splits stay open there
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — recorded

#### What changed
The remaining-candidates Partial from the previous entry is closed. Only duration left this type's instance home for plugable. Membership and judiciary are not law-type work.

#### Deliberation
Owner: review everything transferred to bundles; move general capabilities with `git mv`. The pass found no second wholesale candidate. Splits wait for owner confirmation and live on the bundles handoff.

### Freeze at voting; executive guarantee; Rules as realization; comment-labels; politics
- Time: 2026-09-21T16:20:00Z
- Type: Fixed, clarified, Added
- Cited:
  - [Law Research 001](law.research.001.md) - Relation: Evidence: owner review of the type critique; several first-pass findings were inferences the owner never granted
  - [Politics](../../management/politics/politics.md) - Relation: Depends_on: politics is not a field of law
- Propagates to:
  - `modules/rights/law/edges/`: Done — code, explanation, goal, executive guarantee, computer_code, vote-agree
  - `modules/computer/rule/rule.md`: Done — Law realized as Rules, layers not islands
  - `modules/management/politics/`: Done — concept opened
  - `modules/rights/rights.md`: Done — type line names freeze
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — reviewed, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — misread, then rewrote, argued

#### What changed
[law.md](law.md) no longer says later precision appends to explanation after a vote. Once status is voting, the payload is frozen; a vote is a signature over a digest of the whole content. Any empty required companion keeps the record in draft. Executive guarantee is how the law takes effect, not a sanction-for-disobedience. Computer code is a machine-checkable realization, typically as Rule nodes, and that Rule set is inside the digest. Folk labels attach to comments. [Politics](../../management/politics/politics.md) is defined as a general skill, not government-theater.

#### Deliberation
Owner: who wrote that a law may change after voting starts? That claim is refused. Status may move (draft, get-critique). Once voting starts, nothing in the record may change. Voting is digital signature plus hash of the whole content; the smallest change means the votes were for a different law. A law must be written clearly because change has a large cognitive cost. 20 percent to 30 percent is not a small edit.

Owner: empty any field means the record cannot leave draft. The computer-code-only gate was too strong a reading of one example. Some completeness rule is needed to run voting. A law can include several Rules.

Owner: the field is executive guarantee (ضمانت اجرایی), how the law takes effect — not a mandatory sanction.

Owner: a law that cannot show itself in computer language and be independently evaluated is inherently problematic. Text remains because a community cannot be forced to learn computer language, as listeners cannot be forced to learn music notation.

Owner: vote counting is unfinished. When a person leaves (including by death), is the vote deleted, or kept and omitted from a live count?

Owner: labels are applied when commenting. Comments are not all read. Badges and domain-influence filters are needed. Do not see law and rights in the traditional shape.

Owner: سیاست is a general concept. Wherever a question has several correct answers, the science of politics is needed — company, family, friendship, not only governing a society.

Grok: the post-vote append was my inference from the earlier changelog sentence "later precision appends to interpretation," attributed to the owner. The owner never granted mutation after voting. Freeze-at-voting is Code of consent. Extra eligibility beyond the four companions can be plugable Rule.

Grok: Law and Rule as islands was wrong. If a Rule can be added after voting, the freeze is fake.

Grok: guarantee and computer_code collapse if both only say "the machine will do it." Keep guarantee as observable effect plus fallback; computer_code as the independently evaluable score.

Grok: no predicate was found that *must* stay unevaluable as prose. Mercy looks like one until the *office* is coded and the remainder is either measurable criteria or delegated judgment. Discretion without a metric is, on the owner's criterion, a poorly written law.

Grok: keep a departed vote as history; omit it from the live tally. Deletion destroys audit. This is not an owner decision.

Grok: influence that filters reading can recreate representation. Boundary: influence never weights the vote; the feed must include a disagreement sample. Constitution-as-label is in tension with folk labels-on-comments.

Grok: politics without a "shared binding outcome among people who disagree" qualifier swallows chess and recipes. That qualifier is in politics.md and is this writer's until confirmed.

#### Considered and not done
- Leave explanation-append as a cheap post-vote repair — rejected by owner: after voting, any change is a different law.
- Treat completeness as only a plugable Rule with no default companions — rejected: without filled companions a signature does not bind to a meaning; the four companions are this type's default eligibility.
- Treat Law and Rule as disjoint islands — rejected by owner.
- Put the politics definition only inside law.md — rejected: politics is broader than law.

### Traditional order set aside; status folders; politics left kernel
- Time: 2026-09-22T07:10:00Z
- Type: clarified, Added, moved
- Cited:
  - [Contract](../contract/contract.md) - Relation: Evidence: marriage is already a contract, not a law-type per relationship
  - [Politics](../../../modules-plugable/politics/politics.md) - Relation: Evidence: not kernel; critiques of the definition live on its handoff
  - [Status](../../knowledge/status/status.md) - Relation: Depends_on: draft is the shared label; a transition is an event a rule may block
- Propagates to:
  - `modules/rights/law/status/`: Done — get-critique and voting; draft not copied
  - `modules-plugable/politics/`: Done — left `modules/management/politics/`
  - `modules/knowledge/status/status.md`: Done — status is the label; assignment is a rule
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided, questioned
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — wrote, argued

#### What changed
[law.md](law.md) now refuses the inherited shape of writing, execution, and dispute-resolution. Marriage and family are contract drafts. The scale named for this type is conflict-of-interest resolution in under a thousand laws, against a corpus of hundreds of thousands. Examples must be asked whether they need to be a law; an assembly calendar, a mercy power, and a household arrangement fail unless they resolve a shared conflict of interest. Revealed-vote reading (public vote, per-viewer like on the reason) is ideation on the handoff, not a field of the type. Politics left kernel. `draft` stays the shared status; law holds `status/get-critique` and `status/voting` as types without an invented assignment edge.

#### Deliberation
Owner: this domain must firmly set aside traditional writing, execution, and dispute-resolution. Topics that used to be statutes, such as marriage and family, can be draft contracts. Do not accept a past topic quickly. After an example, ask whether that kind of law is actually needed. A society can flourish with fewer than a thousand laws by resolving conflicts of interest. Hundreds of thousands, as in Iran, is a failure.

Owner: voting can be ideated further. People weight comments of those whose vote is visible. The act is revealing one's own vote, with a reason, not a private "I vote no." Like and dislike on that reason are per person. If I value A, and A liked a comment that carries a revealed negative vote, that comment is worth more to me.

Owner: is politics surely a kernel domain? And was there a critique of what I said?

Owner: beside `edges/`, a domain should have `status/`, one folder per status, because statuses become types code can use. Some statuses are general and currently sit in `modules/knowledge/status/edges-loop`, which is not final. A status may just be the label a rule assigns; we do not fix the assignment, because it can differ over time. `draft` is the same status in every domain. Moving from it to another status is an event a rule may block.

Grok: the mercy example and the assembly-calendar example do not survive the owner's test. They are not laws this domain should grow. Marriage was already a contract in the estate session; the law page had not been using that.

Grok: revealed votes are a reading layer. If revelation is required for the tally, coercion and blocs are the cost. Like already has a plugable reaction overlay. Per-viewer preference must not become a global sort, and must not weight the ballot.

Grok: politics is not kernel. No type. The critiques of the owner's sentence are on the politics handoff: undefined "correct", science versus skill, and friendship choices that may be contracts rather than this concept.

#### Considered and not done
- Copy `draft` into `law/status/` — rejected: one shared label; only the transition rule differs.
- Sweep `status/` into every domain — not done: apply the shared-versus-local test per label; law is the instance.
- Write revealed-vote into the type — not done: ideation, and it must not become ballot-weight.
- Keep politics under `modules/management/` — rejected: the path claimed kernel without a type.

### Catalogs leave the law type
- Time: 2026-09-22T08:05:00Z
- Type: clarified, moved
- Cited:
  - [Status](../../knowledge/status/status.md) - Relation: Depends_on: a status is a loop-edge; the catalog lives there
  - [Founding Arrangements](../../../modules-plugable/rights/founding-arrangements/founding-arrangements.md) - Relation: Evidence: marriage, family, and the small law set
  - [Election](widgets/election/election.md) - Relation: Evidence: critique and signature are separate acts; delegation is stated there
  - [Politics](../../../modules-plugable/management/politics/politics.md) - Relation: Evidence: nearest parent, interest-weighing definition
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
[law.md](law.md) states what a law is and no longer lists status names, folder paths, or founding tests. Those live in the status module, the election widget, and founding-arrangements. Politics sits under plugable management. Law-local `status/` folders are removed.

#### Deliberation
Owner: a domain document that names other folders' contents is a cache. The place and the reason for status belong in one document. Repeating which statuses a domain uses means every rename has to be hunted down.

Owner: founding tests and contract drafts belong in a plugable module that can actually hold the drafts, written as what the module offers.

Owner: like and dislike are the critique. A signature is the vote. The two can run in the same period. A person may delegate; the delegate's signature on each proposition is visible; the person may replace that one signature and keep the appointment for the rest.

Owner: politics stays under the nearest category. The science weighs conflicting interests among agents. The host example and the road example are the definition. Governance stays a separate topic.

### Domain statuses restored; drafts split per concept
- Time: 2026-09-22T08:20:00Z
- Type: Fixed, Added
- Cited:
  - [Status](../../knowledge/status/status.md) - Relation: Depends_on: a status query reads the loop-edge type
  - [Delegate](../delegate/delegate.md) - Relation: Evidence: appointment is already this module
  - [Family](../../../modules-plugable/rights/family/family.md) - Relation: Evidence: one concept, one optional module
  - [Marriage](../../../modules-plugable/rights/marriage/marriage.md) - Relation: Evidence: separate from family
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — corrected
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — rewrote

#### What changed
Law statuses are loop-edges under `status/` again (`voting`, `get-critique`). The account of the query stays on the status module. The umbrella founding module is gone. Family and marriage are separate plugable modules. The election widget points at delegate.

#### Deliberation
Owner: a query for every law in a status can run on a loop-edge, and still the identity of that query seems to make the status a node.

Grok: the rows of that query are laws. The status is the edge type, which is already the code identity. A node is the shape when other records take the status itself as their subject. Confirmation is open on the status handoff.

Owner: removing `law/status/` left this domain's statuses with nowhere to be defined. The shared account stays in the status module. This domain's own statuses are the `status/` folders.

Owner: one founding module will overflow with drafts and laws. Each concept, such as family, is a module a bundle can include alone.

Owner: delegation is already `modules/rights/delegate`. The open gap is the one-proposition signature while the appointment continues, against a record whose empty rule means the whole appointment was given back.




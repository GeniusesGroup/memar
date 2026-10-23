# Law Research 002 — Published accounts and where a change would sit

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Owner review](#owner-review)
- [Open Questions](#open-questions)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)

## Status
Complete

Owner review on 2026-09-23 revises two placement rows. The findings stay the inquiry as written. Standing for priority and for retroactivity is [Owner review](#owner-review).

## Question and Goals
- **Questions:**
  - What do published accounts say a law is, and where does the instrument in [law.md](law.md) — a human text with goal, explanation, executive guarantee, and computer code — sit among them? — Answered
  - For each change those accounts support, does the change belong in the kernel type `modules/rights/law`, in `modules-plugable/rights`, or in neither? — Answered
- **Goals:**
  - Critique this type from sources outside the organization, and leave a placement the owner can review. — Met as a record. The type's wording was not revised in this inquiry.
- **Scope:** The concept, the four companions, the agreement sentence, and the freeze-as-new-node rule. Out of scope: opening the books of Hart, Kelsen, Fuller, or Dworkin; writing a statute; adding edges or plugable modules before review. [Research 001](law.research.001.md) stays as it is. It examined this type against itself and cited no external source. This file does not supersede it.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Reviewed — priority between two in-force laws refused; retroactivity refused as its own module; see Owner review)
- [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.7 via Cursor) — Researcher
- [Gemini](../../../CONTRIBUTORS.md#gemini) (Gemini 3.8 flash via Cursor) — Critic of the placement judgments before they were written into this file. The narrowings marked below are the ones accepted. This is not a review of the finished file.

## Methodology
Pages and papers fetched and read on 2026-09-23.

Wikipedia, [Law](https://en.wikipedia.org/wiki/Law): the lead, the philosophy-of-law section, and the opening of legal systems. Wikipedia, [Wesley Hohfeld](https://en.wikipedia.org/wiki/Wesley_Hohfeld): the theory-of-rights section.

Stanford Encyclopedia of Philosophy, fetched the same day and read in the sections named here, not end to end: [The Nature of Law](https://plato.stanford.edu/entries/lawphil-nature/) (command theory, power-conferring norms, Hart's secondary rules, the separation thesis, Dworkin); [The Pure Theory of Law](https://plato.stanford.edu/entries/lawphil-theory/) (legal meaning versus the enacting events, the basic norm, efficacy of a system versus validity of one norm); [Legal Positivism](https://plato.stanford.edu/entries/legal-positivism/) (Hart's rule of recognition as a practiced social rule); [The Rule of Law](https://plato.stanford.edu/entries/rule-of-law/) (Fuller's desiderata as stated there).

Matthew H. Kramer, "On the Non-Equivalence of Norms and Norm-Formulations," *The American Journal of Jurisprudence* (2026), open access, https://doi.org/10.1093/ajj/auag006. Read: the abstract, the opening account of deontic conflict, and the passage that quotes Kelsen on sham contradictions in linguistic expressions. The rest of the article was not used. Kelsen's *General Theory of Law and State* was not opened; the sentence below is taken from Kramer's quotation of it.

OECD, James Mohun and Alex Roberts, *Cracking the Code: Rulemaking for humans and machines* (Observatory of Public Sector Innovation, 2020), https://doi.org/10.1787/3afe6ba5-en. Read: the working definition of Rules as Code, the isomorphism passage, and the paragraph on unresolved legal status, versions, and error correction. The rest of the primer was not used.

Andromachi Georgosouli, "Metarules, Judgment and the Algorithmic Future of Financial Regulation in the UK," *Oxford Journal of Legal Studies* 43 (2023): 777–803, https://doi.org/10.1093/ojls/gqad014. Read: the abstract and the introduction through the statement of the three arguments. The body of those arguments was not read.

OASIS, *LegalRuleML Core Specification Version 1.0*, https://docs.oasis-open.org/legalruleml/legalruleml-core-spec/v1.0/legalruleml-core-spec-v1.0.html. Read: the glossary entries for Obligation and Override, and the defeasibility section, including its citation of Prakken and Sartor. The schemas were not read.

Placement was then put to Gemini. Where that critique narrowed a judgment, the finding says so. Books named above were not opened. No count in this file is a measurement.

The owner's placement rule, already recorded on [law-validity](../../../modules-plugable/rights/law/edges/validity/validity.changelog.md), is the one used here. The kernel is what a law node is. Plugable is an optional capability many organisations need. A statute instance belongs to the bundle that enforces it. Freeze-at-signature, the four companions, executive guarantee as how the law takes effect, and duration's home in law-validity are owner decisions. This inquiry does not reopen them.

## Findings

### The node is one instrument inside an order
[Law](https://en.wikipedia.org/wiki/Law) opens by calling law a set of rules created and enforced by governmental or societal institutions, and says the precise definition is a longstanding debate. The same page reports Hart's picture as a system of primary rules of conduct and secondary rules for recognition, change, and adjudication, and reports that the rule of recognition is a social rule officials practice, not a sentence that must appear inside each statute. [The Pure Theory of Law](https://plato.stanford.edu/entries/lawphil-theory/) says the hall, the vote, and the string of words are not themselves the law: those events get a legal meaning from another norm. It also says a single new norm can be valid before anyone has complied with it, while efficacy is a condition on the order as a whole. Kramer, quoting Kelsen, *General Theory of Law and State* (1945), 375: "It is one of the main tasks of the jurist to give a consistent presentation of the material with which he deals. Since the material is presented in linguistic expressions, it is a priori possible that it may contain contradictions." Kramer's own claim, in the passage read, is that those contradictions sit in the formulations. Two norms that would put the same person under a duty to φ and under a liberty not to φ, toward the same other person, are not both in effect in one jurisdiction.

[law.md](law.md) uses "law" for two of those layers at once. The opening sentence says law determines which rights, obligations, and behaviors are possible, valid, forbidden, or enforceable. The abstract says a law is a text that travels with four companions. The sources keep the instrument, the norm it formulates, and the order apart. This type already has the instrument: the signed payload. The order is the set of such nodes in force. That set is not a field stored on one node. (Grok, from those pages)

Home: the kernel wording of [law.md](law.md). No new module. The sentence was not changed in this inquiry. A wording the owner can accept or refuse: a law node is one signed instrument in a legal order; the order is which of those instruments are in force together. The boundary that law is an independent source, already in Boundaries, stays. It is what keeps this node off a contract and off an attribute of a right. (Grok)

### The four companions, and what Rules as Code leaves open
Mohun and Roberts propose an official machine-consumable version of some types of government rules, drafted alongside the natural-language text so the two can reach isomorphism, "an effective 1-to-1 mapping." They also write that the legal status of machine-consumable laws, the governance of versions, and the correction of errors in the coded form are unresolved. This type already answers those three more strictly than the primer does. Both formulations are inside the digest. A version change is a new node. An error after the signature is not patched in place. That strictness is the owner's cognitive-cost rule from [research 001](law.research.001.md). The primer does not require it, and this inquiry does not loosen it. The primer's limit — some types of rules, not every rule — disagrees with the owner's criterion that a law which cannot be stated for an independent evaluation is problematic. Georgosouli's introduction argues that human interpretation should be preserved, and names limited translatability of rulebook content into code as the first argument. That is the same disagreement. It is recorded. It is not adopted. Research 001 already left delegated judgment as a Rule, and discretion without a metric as a poorly written law. (Grok; Mohun and Roberts; Georgosouli)

The goal companion is the primer's alignment of intent and outcome, frozen into the payload. [law.md](law.md) says execution stays with the reason the law was written. If a later reader treats the goal as permission to depart from the operative text, the freeze is undone by interpretation, which is the failure the Motivation names. Gemini's critique of an earlier draft of this finding: a goal is often loftier than the operative text on purpose, and a mechanical sameness-test of the kind used for text and computer code would reject ordinary drafting. The accepted narrowing: the goal does not outrank the operative text. A goal that would license a result the operative text refuses is a drafting failure to repair before signature. A goal that is only more general is not, by itself, that failure. No predicate for the operational clash was settled here. (Grok; Gemini)

Home: a clarification on the kernel [goal](edges/goal/goal.md) companion, after that predicate is stated. Not a plugable module. Not written in this inquiry.

Explanation, as frozen definitions of the words in the text, is this type's way of doing Kramer's reconstrual before anyone signs, instead of leaving it to a later jurist. That home is already the companion. Nothing in the sources adds a second explanation module.

Executive guarantee, as how the text takes effect, matches the power-conferring point in [The Nature of Law](https://plato.stanford.edu/entries/lawphil-nature/): a norm that only states how a will, a contract, or a further law is made is not a command to a subject, and recasting it as a command to officials distorts it. Research 001 already corrected the sanction misreading. The sources support that correction. They do not add a field.

### The opening sentence mixes positions the payload already has to state
Wikipedia's account of Hohfeld separates claim-right (correlative: duty), privilege or liberty (correlative: no-right), power (correlative: liability), and immunity (correlative: disability). [The Nature of Law](https://plato.stanford.edu/entries/lawphil-nature/) uses the same cut against the command theory: duty-imposing norms are the ones a command can resemble; power-conferring norms are not. LegalRuleML's glossary likewise separates Obligation (a course of action which, if not performed, is a Violation) from Permission and from Override. [The Pure Theory of Law](https://plato.stanford.edu/entries/lawphil-theory/) separates validity from use: a norm just enacted can be valid though nobody has followed it yet. The opening sentence of [law.md](law.md) puts rights, obligations, what is possible, what is valid, what is forbidden, and what is enforceable into one determination.

The human text has to say which of those the instrument creates. People sign that text. The computer form has to state the same operator, or the eligibility rule already in the type fails. A fifth companion that only labels the operator would copy the text and the code. (Grok; Gemini noted the same limit: the operator is not "only in the code" if the text is what people sign.)

Home: the kernel wording proposed in the first finding, so the opening sentence stops making one determination out of those positions. No Hohfeld module in the kernel and none under `modules-plugable/rights`.

### Agreement between nodes is two different relations
[law.md](law.md) says a new law's machine-checkable form agrees with the laws already in force, and that rival texts are a graph people compare. LegalRuleML's defeasibility section says a normative conditional does not correspond to the material conditional of propositional logic. When two rules can conclude a head and its negation, classical consequence treats the set as entailing anything. Defeasible reasoning withholds both conclusions unless a superiority relation picks one. Override, in that specification, is an ordered pair: one legal rule takes precedence over another. The same section reports Prakken and Sartor: specificity, the usual reading of lex specialis, is not always the relation to use; lex superior and lex posterior also apply; a more specific local rule need not prevail over a less specific constitutional norm.

Kramer's claim, as far as it was read, does not by itself require an override edge. He says interpretation removes the appearance of contradiction from the formulations, so that contradictory norms are not both in effect. Forcing that work to happen before signature, rather than in a later dispute, is this type's existing refusal of judge-made gap-filling. It is an owner decision. It is not a theorem of the paper. (Grok; Gemini)

Two relations are easy to collapse and should not be.

A successor is this type's own rule that a change is a new node. Without an edge from the new node to the node it replaces, the graph can compare rivals and still cannot say which one the earlier signature yielded to. Home: a kernel edge under `modules/rights/law/edges/`. Not law-validity. That module is how long a vote or a law binds, and it already says form is not its subject. The edge was not added.

A priority between two nodes that are both in force is different. A single instrument needs no such pair. Gemini's critique is accepted: LegalRuleML shows a stated precedence, and Prakken and Sartor show that a silent specificity rule is the wrong default, and neither shows that superiority is part of what every law node is. Home: a plugable module under `modules-plugable/rights`, working name `law-priority`, whose relation is a precedence the signers state. A constitutional classification, still open on the handoff, would be one ground that module can record. It would not be an algorithm that guesses the more specific text. The module was not created.

What "agrees with the laws already in force" should mean until that module exists: the drafter does not sign a computer form that contradicts a node still in force. An exception that must remain beside a general rule waits for the stated precedence, or is written inside one instrument. Authorization of a lower instrument by a higher one, Kelsen's chain, is the authority question already on [normative-bootstrap.handoff.md](../normative-bootstrap.handoff.md). It blocks founding, not the shape of this node.

### Fuller's desiderata do not share one home
[The Rule of Law](https://plato.stanford.edu/entries/rule-of-law/) distils Fuller into eight desiderata for governing through enacted rules: general in scope and application, public, prospective, coherent, clear, stable, practicable, and congruence between official action and declared rule, citing Fuller, *The Morality of Law* (1969), 39. The book was not opened. The same entry says these are formal virtues of that kind of rule, and that enacted general rules are not the right tool for every task of governing.

Generality is already the type's cut between this node and a case-by-case order. Clarity is the Motivation and the explanation companion. Stability is the freeze: a change costs a new node because people live under the previous one. Coherence is the agreement sentence, read with the two relations in the previous finding. None of these four is a new module.

Congruence, in that encyclopedia's wording, is official action matching the declared rule. The executive-guarantee companion states the declared path. It does not record whether officials later followed it. Gemini's narrowing is accepted. The companion does not discharge the desideratum. The later mismatch is a fact about enforcement, outside this node. No field was added.

Practicability — a rule people cannot comply with — is, for a machine-checkable form, an unsatisfiable rule. That is the same kind of eligibility as a text and a computer form that diverge: the record is not ready for a signature. Home: a policy on the kernel [computer code](edges/computer_code/computer_code.md) companion. Not a new module. Not written here. Georgosouli's untranslatable standard is a different case, already left as the disagreement in the Rules-as-Code finding.

Prospectivity is not a property of every instrument. Curative statutes are a known practice, and this inquiry did not find a source that makes retroactivity impossible for something to be a law. Home, if an organisation wants a default ban: a future plugable module. Law-validity is the wrong file. It answers how long a vote or a law binds people who did not vote, including at death or departure. It does not answer whether a new instrument reaches acts done before it. The module was not created.

Publicity, in the same encyclopedia entry, is epistemic access: norms promulgated as public knowledge so people can study them and plan. Law-validity's sunset does not answer whether the text was knowable. The human-language companion is already this type's reason for a readable text. Whether the signature itself is notice to the people bound, or a further publication record is required, is open. A gazette, if it is required, would be plugable. It was not designed here, because the inquiry does not yet know that the signature is insufficient.

### What was considered and given no module
Dworkin, as [The Nature of Law](https://plato.stanford.edu/entries/lawphil-nature/) reports him, treats principles of justice and fairness as part of working out what the law requires, through an interpretation that both fits the practice and justifies it. That is a rival account of legal content. It asks for a weighing after enactment. This type's owner has already refused unevaluable discretion. A principles companion would be that refusal reversed. No module, in either layer.

The separation thesis, as that entry states it, is that the legality of a norm does not necessarily depend on its moral merits. This type's validity is a signature over a complete payload plus agreement with nodes in force. A moral test as a gate on every node would be a different theory. A community that wants a moral limit can enact it as a higher instrument the machine form must agree with. That is the priority module's lex superior case, or the bootstrap authority question. It is not a natural-law module.

Custom, which [Law](https://en.wikipedia.org/wiki/Law) names as a source in civil-law systems, has no text and no computer form until someone writes the instrument. Under this type it is not a law node before that writing. No customary-law module.

Scenario tests of the computer form are Mohun and Roberts's ex-ante modelling, and they are also the human-language view of the code that research 001 asked for at critique time. If the scenarios sat inside the digest, editing a test would be a new law. Home: a policy on [get-critique](status/get-critique/get-critique.md). The scenarios are generated from the computer form, during critique, and they stay outside the payload. The policy was not written.

## Owner review

Owner (Omid Hekayati), on the placement table:

The stated-priority row was refused. A precedence between two laws that are both still in force is a conflict left for someone to pick a winner. The owner reads that as a complaint the judiciary would then have to settle at the root. The aim is the opposite: the chance of executing contradictory laws is zero. A proposal that conflicts with a law in force is linked to that law. If the proposal passes, it cancels the previous law. Both do not remain executable.

The retroactivity row was refused as a module, and also refused as the nature of the type. A ban on retroactive effect matters, and it is itself a law. It is not written as its own statute. One law-instance states how law works. Clauses of that instance include the retroactivity ban, the refusal to enact a contradiction beside a law still in force, and the link by which a new law that passes cancels the previous one.

The cancellation link is the relation this inquiry called `supersedes`. The override relation, and the plugable module `law-priority`, are not. No edge was added in the review.

A later review placed the effect of a vote on another law as an optional edge in [claims](../../../modules-plugable/rights/claims/claims.md), not as part of the case type and not as a claim node. [Annul law for conflict](../../../modules-plugable/rights/claims/edges/annul-law-for-conflict/annul-law-for-conflict.md) annuls the second law. [Annul law for update](../../../modules-plugable/rights/claims/edges/annul-law-for-update/annul-law-for-update.md) writes [supersedes](../../identity/thing/edges/supersedes/supersedes.md). Supersedes is on thing, because a contract and an estate need the same relation. The prohibitions live as statutes under [laws](../../../modules-plugable/rights/law/laws/laws.md).

## Open Questions
The priority module and the separate retroactivity module are answered in [Owner review](#owner-review). The following were written into [law.md](law.md) after the inquiry.

The node is one signed instrument and the order is which instruments are in force. The goal does not outrank human code or computer code. A computer-code form that no input can satisfy is not signed. Critique scenarios stay outside the digest. The human code in the signed payload is the type's publicity. Who is bound without having signed stays with law-validity.

## Conclusion
[Owner review](#owner-review) is the standing placement for priority and for retroactivity. The table below is the inquiry's proposal, and those two rows do not survive that review.

The published accounts support this type's instrument: a human formulation and a machine formulation of one norm, signed together, with a goal, frozen definitions, and a path by which the text takes effect. They do not support the opening sentence's single determination of rights, validity, and enforceability. They leave the legal order as the set of instruments in force.

Rules as Code, in the OECD primer, is less strict than the freeze about legal status, versions, and error correction. That strictness stays. The primer's and Georgosouli's limit — not every rule is worth coding, and human interpretation should remain — stays a recorded disagreement with the owner, not a change.

Placement, none of it applied to the type or to a new module:

| Proposal | Home |
| --- | --- |
| Node as one signed instrument; the order is which instruments are in force | Kernel wording of [law.md](law.md) |
| Goal does not outrank the operative text; a merely loftier goal is not a failed match | Kernel [goal](edges/goal/goal.md), once a clash-predicate exists |
| Unsatisfiable computer form cannot be signed | Kernel [computer code](edges/computer_code/computer_code.md) |
| This node replaces that one | Kernel edge `supersedes` |
| Stated precedence between two nodes still in force | Plugable `modules-plugable/rights/law-priority` |
| Scenarios that show the computer form in human language | Kernel [get-critique](status/get-critique/get-critique.md), outside the digest |
| A default ban on retroactive effect | A future plugable module, if wanted |
| A publication record beyond the readable text | Open; plugable if the signature is not notice enough |
| Hohfeld labels, principles, a moral-validity gate, custom, tests inside the digest | No module |

Law-validity stays duration. It does not receive prospectivity or publicity. The owner has not reviewed this file. The 1961, 1964, 1965, and 1969 books were not opened.

## Related Artifacts
- [law.md](law.md) — pointer added; wording of the type not revised (Review)
- [law.handoff.md](law.handoff.md) — the questions above (Update)
- [law.research.001.md](law.research.001.md) — internal critique; not superseded (Related)
- [law-validity.md](../../../modules-plugable/rights/law/edges/validity/validity.md) — duration; not the home for priority, prospectivity, or publicity (Related)
- [normative-bootstrap.handoff.md](../normative-bootstrap.handoff.md) — authorization and authority; not this node's shape (Related)
- [Law](https://en.wikipedia.org/wiki/Law), [Wesley Hohfeld](https://en.wikipedia.org/wiki/Wesley_Hohfeld), [The Nature of Law](https://plato.stanford.edu/entries/lawphil-nature/), [The Pure Theory of Law](https://plato.stanford.edu/entries/lawphil-theory/), [Legal Positivism](https://plato.stanford.edu/entries/legal-positivism/), [The Rule of Law](https://plato.stanford.edu/entries/rule-of-law/) (Related)
- Kramer, *American Journal of Jurisprudence* (2026), https://doi.org/10.1093/ajj/auag006 (Evidence)
- Mohun and Roberts, *Cracking the Code* (2020), https://doi.org/10.1787/3afe6ba5-en (Evidence)
- Georgosouli, *Oxford Journal of Legal Studies* 43 (2023), https://doi.org/10.1093/ojls/gqad014 (Evidence)
- OASIS, LegalRuleML Core Specification 1.0 (Evidence)

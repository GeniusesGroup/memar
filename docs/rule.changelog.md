# Rule Changelog

## 2026-09-29 — Initial concept document

### What changed
- Created `docs/rule.md` (Draft) as the language-neutral Rule and rule-engine concept document at `docs/` root beside `modularity.md`.
- Created `docs/rule.research.001.md` (Complete) recording terminology research (rule vs policy vs constraint vs convention; SBVR, BRG, production rules).
- Created `docs/rule.handoff.md` with open questions and an inventory of 32 document-level rule passages proposed for relocation to Module `rules/` folders.
- Linked from [modularity.md → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) and [modules/khayyam/rules/README.md](../bundles/khayyam/rules/README.md).

### Why
- Owner position: Rule is a Memar-wide concept; any Module may carry `rules/` beside `protocol/`; rules are owner-introduced, not language/protocol properties; rule-making is general practice.

### Cited
- [Rule Research 001](./rule.research.001.md) — `Evidence`
- [Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) — `Extends`
- [Linter](./modules/computer/linter.md) — `Reference`
- [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule) — `Reference`

### Applied to
- modularity.md: Done — pointer to `rule.md` added; section no longer marked provisional in title.
- modules/khayyam/rules/README.md: Done — link to general Rule concept at top.

### Considered and not done
- **Relocating inventory entries in the same session**: scoped out; recorded in handoff only.
- **Promoting `rule.md` to Proposed immediately**: left Draft until framing open question is reviewed.

## 2026-09-29 — Rules, code, and services boundary

### What changed
- Added [rule.md → Rules, Code, and Services](./rule.md#rules-code-and-services): a Rule states a condition; generation/scaffolding/rewriting is a service capability, not Rule text; enforcement by a service keeps behavior in code.
- Extended [rule.handoff.md](./rule.handoff.md) with Memar server doc gap note, Khayyam rules classification inventory (25 rules: 4 / 5 / 16), and anticipated relocation work.
- Recorded "generate a service from its name and path" in [SDK handoff](./modules/process/service-sdk.handoff.md) and [Khayyam execution handoff](../bundles/khayyam/khayyam.handoff.md).

### Why
- Owner position (2026-09-29): Rule must not replace code and services; generative work belongs in the Memar server; many `modules/khayyam/rules/` entries are mis-placed.

### Cited
- [Khayyam execution handoff → Rule model](../bundles/khayyam/khayyam.handoff.md) — `Reference` (Memar server mention; no defining doc)
- [Knowledge → Knowledge and Code](./knowledge.md#knowledge-and-code) — `Reference` (callable generative services)

### Considered and not done
- **Linking to a Memar server protocol document**: none exists under `docs/`; noted in handoff instead of inventing one.

## 2026-09-29 — Observer/mutator rule relocated to ADT module

### What changed
- Moved observer/mutator governance from `modules/khayyam/rules/observer-mutator-abstractions/` to `modules/computer/adt/rules/observer-mutator/`.
- Updated [rule.handoff.md](./rule.handoff.md) Khayyam rules classification: observer-mutator under (a) ADT; Khayyam index count 24; (a) 5 / (b) 5 / (c) 15.
- Added `modules/computer/adt/rules/README.md` index.

### Why
- Owner decision (2026-09-29): Liskov & Guttag observer/mutator families are ADT protocol subject matter, not Khayyam grammar.

### Cited
- [observer-mutator.md](../modules/computer/adt/rules/observer-mutator/observer-mutator.md) — `Extends`
- [ADT handoff](./modules/computer/adt.handoff.md) — `Reference`

---

### The module a Rule belongs to
- Time: 2026-10-03T12:01:30Z
- Type: Added
- Cited:
  - [Linter → A rule's home is its subject's document](./modules/computer/linter.md#a-rules-home-is-its-subjects-document) — `Evidence`: the principle this criterion extends from the claim to the `rules/` folder
  - [Khayyam → Minimal Legislation](./khayyam/khayyam.md#minimal-legislation-a-principle) — `Evidence`: `:177` and `:181` for the language test
  - [Modeling → Constraints Belong to the Constraining Concern](./modeling.md#constraints-belong-to-the-constraining-concern) — `Evidence`: a condition is owned by the concern that originates it
  - [Control Flow Model → Halt](../modules/process/control-flow/control-flow.md#halt) — `Reference`: `:129` for the name `Halt` and `:131` for the refused `panic`
  - [protocols → Where implementations live](./modules/README.md#where-implementations-live) — `Reference`: `:16` names the module the relocated Rule's protocol claims
  - [Test → Placement](../modules/process/test/rules/test-placement/test-placement.md) — `Reference`: a Rule already filed in the module that owns its subject

#### What changed
- Added [rule.md → Which Module a Rule Belongs To](./rule.md#which-module-a-rule-belongs-to): a Rule belongs to the module that owns its subject; it belongs to a language exactly when no program satisfies every Rule of that language's catalog and still violates it; enforcement does not decide the home; and the two cases the subject test does not decide are named as undecided.
- Relocated [Disregarded Error](../modules/process/error/rules/disregarded-error/disregarded-error.md) from `modules/khayyam/rules/` to `modules/process/control-flow/rules/` and then, on the owner's ruling that the concern it governs is failure, to `modules/process/error/rules/`, on that criterion. Its normative claim is [The Error](./modules/process/error.md) at `:88` and `:130` together with [Control Flow → Error Propagation](./modules/process/control-flow.md#error-propagation) at `:141` and `:143`, and the same document's `:139` is what the first relocation read as claiming the subject away from The Error.
- Created `modules/process/control-flow/rules/` with a catalog index and two Rules: the relocated Disregarded Error and [Halt Declaration](../modules/process/control-flow/rules/halt-declaration/halt-declaration.md), which gives the halting concern a Rule of its own rather than a refusal inside a Rule about a failure.
- Added [Scope Visibility](../bundles/khayyam/rules/scope-visibility/scope-visibility.md) to the Khayyam catalog; its subject is name resolution in the language.
- Updated the [Khayyam rules index](../bundles/khayyam/rules/README.md) — the Disregarded Error row removed, the Scope Visibility row added, and a pointer to the module catalogs added — and repaired every link into the relocated Rule.

#### Deliberation
The owner's challenge of 2026-10-03 asked whether all rules relating to Khayyam belong in the language's rules folder, whether the Khayyam language itself claims to solve them, and whether a concern such as `panic` should be a module with its own rules written imperatively rather than a prohibition carried elsewhere. Measured over the catalog as it stood, it held 26 Rules of which 13 had a subject this repository chose rather than the language — a subject the catalog's own membership criterion excludes — while the concern about halting existed only as a sentence inside another Rule's refusal. The answer given is a criterion rather than a move in either direction, and it is placed here because this document is what owns where Rules live: `modules/README.md` puts specifications and general claims in `docs/` and not in the implementation layer.

#### Considered and not done
- **Moving the catalog's 13 repository-convention Rules out of it**: named as the measurement that motivates the criterion, not performed. Each is a separate relocation with its own subject to argue, and the question was where a Rule goes rather than which Rules leave.
- **Placing the relocated Rule in `modules/process/error/rules/`**: that folder exists and is empty and the owner named it as a candidate; not taken, because what an Error *is* is that module's subject and how execution continues once one has occurred is not — `docs/protocols/process/control-flow.md:139` draws that line itself.
- **Creating an independent `panic` module**: not taken; `modules/process/control-flow/` already holds the concept, its two declarations, and its contract, and `panic` is a refused name at `control-flow.md:131`.
- **Writing the Scope Visibility claim into `docs/khayyam/`**: not written. `docs/khayyam/khayyam.research.001.md:444` records the statement of a `sc` block's reach as owed beside `khayyam.md:129`, and that folder is not this session's to write; the Rule cites the debt rather than closing it.
- **Settling the two cases the criterion leaves undecided**: recorded in the body as undecided rather than answered, because those two are questions about subjects and no placement rule can decide them.

---

### Correct the standing of a vocabulary source in a completed research
- Time: 2026-10-04T13:27:43Z
- Propagates to:
  - rule.md: Reference - its definition derives from this repository's own practice and rests on no external source, so no change was needed
  - rule.handoff.md: Done - an open question added recording that the vocabulary findings are a reading and are provisional against the specification
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed, argued, applied

#### What changed
- `rule.research.001.md` no longer cites the industry-community articles and the tertiary compilation it read as `Evidence`, and no longer records their URLs. Each affected finding is now attributed to internet research with the `Reference` relation.
- `### Methodology` now states what those sources may carry: an industry-community article belongs to the vendor class of source and a tertiary compilation is a pointer toward primary sources, so neither supports a claim, and every claim drawn from them is the research's own reading rather than a finding those sources establish.
- `### Methodology` names the limitation the record did not: the specification defining that vocabulary was not consulted, so a finding stating what the vocabulary says is provisional against it.
- `### Conclusion` states that the standing of those sources bears on how far the vocabulary findings may be relied upon and not on the Rule definition, which `rule.md` derives from this repository's own practice.
- No finding's content was altered. What changed is the standing claimed for the material each was read from.

#### Considered and not done
- A superseding research was not opened (Omid Hekayati — declined). The facet's own lifecycle makes supersession the correction mechanism for a frozen record, and that rule was set on the owner's approval; he directed that the record be corrected in place regardless of its status, and the tension between the two instructions is recorded here rather than resolved by this entry.
- Re-attributing the vocabulary definitions to the specification was rejected as fabrication (Space Bunny Alpha — argued). The inquiry did not read that specification, and attributing a reading to a document nobody opened is exactly what [Documentation → Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) forbids. The gap is recorded as a limitation and as an open question instead.
- Withdrawing the vocabulary findings as prior art no document relies upon was not done (Omid Hekayati — pending). It is a defensible outcome and is now a question in `rule.handoff.md`.

#### Deliberation
The new `Source standing` rule in `documentation.md` was found to invalidate citations this record had carried since it was written, and the record's `Complete` status would normally have left the defect in place (Space Bunny Alpha — argued). The owner directed that the record be fixed and that its status not be treated as a reason to leave it (Omid Hekayati — decided). The two instructions conflict on their face, and the entry records the conflict so a later reader sees that the in-place correction was a decision and not an oversight (Space Bunny Alpha — argued).

---

### One concept seen through two lenses: the framing question settled
- Time: 2026-10-05T08:59:05Z
- Propagates to:
  - modularity.md: Done - the paragraph that left the two framings open replaced with a link to the settled statement; the section's own modular consequence kept
  - modeling.md: Done - the graph-lens requirement kept and joined to the module lens through the same link
  - rule.handoff.md: Done - the two-views question and the anticipated-work items that existed only to settle it removed; every other entry left open
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- Added [Rule → One Concept, Two Lenses](./rule.md#one-concept-two-lenses): a Rule is one thing seen through two lenses, and each lens carries obligations the other does not discharge. The graph lens owes it an identity of its own — addressable and nameable apart from the Code element it governs — and reach into the model through named edges; the module lens owes it a stated boundary, its own identity and lifecycle, and attachment across an explicit relationship rather than through a host's essential identity.
- `### Motivation` now points at that section instead of recording the module-attachment and graph-node descriptions as a reconciliation left open.
- `### Relationship to Modularity and Modeling` now states the modular boundary as what holds: a Rule is a Module developed on its own, related to the Module whose subject it governs.
- `## What This Document Does Not Define` no longer carries the item asking which framing is primary.

#### Considered and not done
- **Naming one lens the primary framing**: rejected (Omid Hekayati — ruled). A primary lens settles the question by dropping the other lens's obligations, and both sets of obligations are requirements on the same Rule; a formulation that answers only one of them is not the concept either subject document was describing.
- **Treating the two descriptions as two concepts wanting two names**: rejected (Omid Hekayati — ruled). What the two lenses look at is one thing — one condition, one subject, one boundary — and it is [Modularity → One Term, One Identity](./modularity.md#one-term-one-identity) applied in reverse that produced the doubt: the collision would exist only if the module attachment and the graph node were independently identified, which they are not.
- **Promoting `rule.md` beyond `Draft`**: not done. The status is the owner's to move, and this entry records the front matter as it stands.
- **Naming what a Rule's own edges must be called**: not done. [Modeling → Edge Types and Their Traditional Counterparts](./modeling.md#edge-types-and-their-traditional-counterparts) owns the taxonomy, and whether an ordinary edge is addressable in its own right is open there.

#### Deliberation
The question on record — which framing is primary, or whether the two are views of one concept — was mis-shaped as a choice, and the owner's ruling settled it by answering that no choice exists (Omid Hekayati — decided). "Which is primary" presupposes two descriptions competing for one name, and it was the presupposition that kept both documents hedged: `modularity.md` wrote that a Rule *may* be a Module, and `modeling.md` wrote of a separate framing. The concept is one; what differs is what a session must produce when it works in either lens, so the obligations were stated per lens rather than ranked between them (Space Bunny Alpha — argued).

---

### Ontology checks and Rule retirement settled by what the concept already holds
- Time: 2026-10-05T09:53:19Z
- Type: Added
- Propagates to:
  - rule.handoff.md: Done — the ontology-checks question and the retiring-a-Rule question were deleted; each is answered in the body
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `### Who Owns and Introduces Rules` now states that a grammar's well-formedness condition is a Rule and that its being part of the language does not stop it being one: a condition is outside a language, protocol, or concept until an owner elevates it by stating it in that subject's own document, and a well-formedness condition is elevated there by the owner of the language it constrains.
- A new `### Retiring a Rule` states what retiring owes: the normative claim and the executable form leave together or are re-owned together, and where what the Rule held was part of the subject's own identity, removing it gives the same source a second meaning and the document that owns the subject changes with it, while a Rule that held only posture leaves without the subject document changing.
- `rule.handoff.md` no longer carries "Are ontology checks Rules at all?" or "Retiring a Rule". The first posed a choice between two clauses that do not conflict once the elevation clause is applied to a grammar's own conditions; the second asked what a retiring party must establish, and what the two-part rule and the language test already establish is now in the body.

#### Considered and not done
- **Reading the ontology question as a genuine alternative and answering it by choosing one side**: rejected. "Ontology checks are not Rules" contradicts what this document already calls a Rule in *What a Rule Is* and what the Linter protocol calls a compiler rule, and "not part of the language holds only for governance rules" contradicts a clause the document states without that limitation. Neither side was available to pick.
- **Stating that every well-formedness condition is elevated**: not done. The section says what a condition's membership in a language depends on — an owner stating it in that language's document — which leaves a condition no owner has stated exactly where the section already puts it.
- **Writing a duty to record why a Rule was retired**: not done. Recording why a change happened belongs to the changelog that carries the change, and a rule about how to retire belongs to a Practice companion that does not exist; the body states what may not be left behind, not a procedure.
- **Adding the retirement rule to `### Normative Claim and Executable Form` instead of a topic of its own**: not done. That section states the two parts and their link; retirement is a lifecycle event a reader arrives at looking for what removing a Rule requires, and it deserves the heading the handoff entry already used for it.

---

### A Rule's claim is a Type; its notation is a rendering
- Time: 2026-10-05T17:15:06Z
- Type: Changed
- Cited:
  - [Type → Abstract](./type.md#abstract) — Evidence: "every semantic entity is a Type", which is what a checkable condition on a governed subject is
  - [Type → Type and Rules](./type.md#type-and-rules) — Evidence: a rule exists at the modeling level as a stated constraint or valid-behavior description, and the checking code is one realization rather than the rule itself
- Propagates to:
  - [Linter → How a governance rule is authored](./modules/computer/linter.md#how-a-governance-rule-is-authored): Done — that document's closing paragraph now carries the sentence, recorded in its own changelog
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- *Normative Claim and Executable Form* now adds that the members a governance Rule carries for linter consumption describe the authoring form a Rule takes, while the claim itself is a Type on the subject it governs, and a notation is one rendering of that statement rather than its carrier. The two halves of the section are now stated as separate: the normative claim is what a Rule says, and the members — Subject, Tier, Default, Override — are how it is written down.

#### Considered and not done
- The shared-notation question was not answered and the entry recording it was left untouched. What settles in this document is only what a notation may not become; which notation is chosen, and whether a Practice companion follows, remain exactly as open as they were.
- The follow-up inventory row for the Linter protocol's required members was not edited. That row describes where the members would live once relocations begin, and the change here does not move them.
- No statement was added about where a Rule's condition is represented internally. That question is registered in `rule.handoff.md` and belongs with whoever examines declarative expressions, decision tables, and external references; this sentence does not prejudge among them.

#### Deliberation
The finding was that the document's principal carrier of normative semantics is a document of prose fields, which a document declaring every semantic entity to be a Type cannot leave unqualified. The tension was latent rather than load-bearing — no rule a reader needs changes — so the fix was scoped to one sentence at the point where the document already distinguishes claim from executable form (Space Bunny Alpha — argued, drafted). Whether the same sentence belongs in the Linter protocol, whose closing paragraph is where the notation question is actually owned, was recorded as a propagation rather than attempted, since that document belongs to another owner (Omid Hekayati — decided).

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:44:11Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to `rule.md`, `rule.handoff.md`, `rule.research.001.md` and this changelog against HEAD: the link repointing after the `protocols/` to `modules/` and `modules/khayyam/` to `bundles/khayyam/` moves (`memar content check` reports no problem), the new sections [One Concept, Two Lenses](./rule.md#one-concept-two-lenses), [Retiring a Rule](./rule.md#retiring-a-rule) and [Which Module a Rule Belongs To](./rule.md#which-module-a-rule-belongs-to), the sentence on a grammar's well-formedness condition and the Type sentence in the body, the three entries added to this changelog, and the handoff's removed questions and added measurement.
- Restored the handoff question [What a retiring party must establish](./rule.handoff.md#what-a-retiring-party-must-establish), narrowed. The 2026-10-05T09:53:19Z entry records the retiring-a-Rule question as answered by the new body section, but that section states only what retirement does to a Rule's claim and executable form. The removed question asked what a retiring party must establish (the problem the Rule held, whether it remains, and the three positions), and the same entry lists a duty to record why as "Considered and not done", so it remained open and its deletion lost it.
- Recorded here, without changing the files, two gaps in the existing history. The handoff section "The ownership half applied to the whole catalog: fourteen Rules no module claims" has no changelog entry; it records a measurement of 27 folders and two blockers, which the Khayyam rules README (`Which rules here are the language's own`) corroborates. The rewording of a contributor's tool label in the 2026-10-04 source-standing entry (`space-bunny-free` to `space-bunny`) is a correction of a label, not of content.

#### Considered and not done
- The other removed handoff questions (framing, ontology checks) stay removed: each is answered in `rule.md` and recorded in the 2026-10-05 entries.
- The unmatched `process.research.002.md` link in the removed question was not restored, since the file is no longer in `docs/`.

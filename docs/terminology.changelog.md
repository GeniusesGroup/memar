# Terminology Changelog

## Changelog

### Initial version
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — drafted
  - [Claude](../CONTRIBUTORS.md#claude) (Claude Sonnet 5) — reviewed, expanded

#### What changed
- Created, introducing Memar's terminology philosophy, terminology layers, terminology debt, concept-first reasoning, tool-first anti-patterns, scientific-methodology rationale, terminology-governance principles, and AI-interpretation guidance; establishing terminology as a first-class architectural concern within the Memar ecosystem; and defining the relationship between terminology quality, mental-model quality, and architectural quality (Omid Hekayati — claimed the core concepts, terminology philosophy, architectural rationale, and the three-tier classification; ChatGPT — initial drafting, critique, synthesis; Claude — critical review, clarification, grounding citations, expansion).
- The worked examples (heat pump, container/docker, cloud) were defined (Omid Hekayati — claimed).
- A critique of AI-drafted material was included (Omid Hekayati — claimed).
- The position that independent AI review serves as interim external scrutiny was recorded (Omid Hekayati — claimed).

---

### Review cycle with ChatGPT
- Time: 2026-06-23T00:00:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — reviewed, argued.

#### What changed
- Strengthened the Graph example to explicitly cite Graph Theory and Graph Rewriting rather than naming only the anti-pattern.
- Strengthened the Business Terms definition to describe business terminology as optimized for adoption and communication efficiency rather than precision, avoiding an unprovable claim about intent.
- Added Cloud and Container/Docker as worked examples.
- Established the dependency direction that other Memar documents should depend on this document, and not the reverse.

#### Considered and not done
- **Listing the Protocol document in this document's Citations (rejected — explicit decision)**: Protocol is a specific application of the principles established here, not a peer or a prerequisite; the decision was part of establishing the dependency direction above.

---

### Critical review cycle with Claude
- Time: 2026-06-27T00:00:00Z
- Type: Fixed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- A substantial critical-review pass was applied; the internal inconsistency in the Scientific-terms tier was corrected.
- Explicit, criterion-based definitions were added for the Scientific and Technology layers, supplying tier-assignment criteria.
- The open question of whether Protocol belongs in the Scientific layer was resolved by clarifying that the layer is defined by methodology rather than prior academic membership.
- An explicit note was added on what "independent verification" currently means for Memar in practice.
- A deep "Protocol vs. API Specification" section that had begun restating Protocol's own ontology was removed, consistent with the decision that this document should not depend on or import content from other documents.
- The concept-vs-representation pattern was grounded in two citable frameworks instead of an informal "terms migrate" intuition: the "conceptual leakage" pattern was named, grounded in genericized trademark theory and prototype theory.
- The AI Implications section's core claim was marked as an explicit working hypothesis rather than a stated fact.
- The document was expanded throughout from an outline into full explanatory prose.

#### Deliberation
- The Scientific-terms layer, as originally written, was flagged as silently conflating mathematical/formal, empirical/scientific, and philosophical/foundational concepts under a single label (Claude).

#### Considered and not done
- **Describing conceptual leakage as a term "migrating" or "evolving" toward its representation (raised, then rejected).** Reframed as conceptual leakage instead — the underlying concept does not change; usage collapses it with a popular representation of it. This replaces any notion that the concept itself changes over time.

---

### Definition vs Explanation expansion
- Time: 2026-07-05T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote.

#### What changed
Precisely defined Comprehensive and Exclusive as the two directions of necessary and sufficient conditions, rather than leaving them as intuitive labels. Clarified that a definition composed of several necessary properties (as in the Protocol document) remains a Definition, not an Explanation, and gave a practical test for telling the two apart. Introduced the regress problem and primitive notions to explain why some Memar concepts are necessarily left without a complete independent definition at a given point in the framework's development, and why this is expected rather than a defect. Added an explicit requirement that a Memar Definition state, rather than leave implicit, when it diverges from a term's common ecosystem usage.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-15T00:00:00Z
- Type: refactor
- Propagates to:
  - system.md: Reference only — no change needed there; this entry only corrects terminology.md's own stale description of System.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- This document is now structured per `documentation-explanation.md`: restructured from `Summary/Motivation/Guide-Level Explanation/Reference-Level Explanation/Drawbacks/Rationale and Alternatives/Prior Art/Unresolved Questions/Future Possibilities/Change Rationale` into the current template (`Abstract → Introduction → Explanation → Results → Discussion`).
- The front-matter `Contributor(s)` roster and the prior `## Change Rationale` narrative moved into this changelog's entries (Citations was already empty; the narrative migrated into the changelog entries above); the document's Contributor roster and full change history now live entirely in this file rather than in front matter and a document-level `## Change Rationale`.
- Discussion sub-heading casing was normalized to match the template.
- A nesting inconsistency was corrected: Business Terms sat as a sibling of "Terminology Layers" instead of nested under it, unlike its two sibling layers (Scientific Terms, Technology Terms).
- A stale claim in "The Regress Problem and Primitive Notions" was corrected: System was said to lack a complete formal definition — System now has one, in system.md, so the passage was reframed as a historical illustration of the general pattern rather than a claim about System's current status.

#### Deliberation
- The migration of this document to the current structure with a paired changelog file was requested, along with a check that any Process-related content be examined for migration to process.md, following the same treatment already applied to protocol.md (Omid Hekayati — requested).

#### Considered and not done
- **Migrating Process-related content to process.md (examined, none found)**: this document was checked for Process-specific content, following the same review applied to protocol.md. Found none: this document's only uses of the word "process" are either the ordinary-English sense ("evaluation process," "review process") or the informal, non-Memar sense of an OS process ("Container before Process Isolation," "a process is not defined by an operating system") — neither is Memar's formal Process concept, so no content was moved.

---

### Terminology Authority and Governance, and Word-Weight Rebalancing, absorbed from framework.md
- Time: 2026-08-16T00:00:00Z
- Type: Changed
- Cited:
  - [Framework](./framework.md) — Depends_on: the content absorbed into this entry's additions originated in framework.md's "Document Authority and Terminology Governance" topic; this also resolves the "Migration to the Explanation-facet document template" entry's own open question about eventually citing a stable Framework document, since framework.md now exists with a settled ID (495003) rather than only as informal working material.
- Propagates to:
  - framework.md: Done — its "Document Authority and Terminology Governance" topic was shrunk to a short pointer to the sections added here in the same pass.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- `framework.md`'s "Document Authority and Terminology Governance" topic substantially duplicated this document's own "Diverging From Ecosystem Definitions" and "AI Implications" sections, and in the AI case stated the same claim with a different, more confident level of certainty than this document uses for it; the non-duplicate content was absorbed here and `framework.md` was left with a pointer instead of a parallel restatement.
- "Terminology Authority and Governance" was added as a new subsection under Definition vs Explanation, right after Diverging From Ecosystem Definitions, covering how a Definition's authority is established (the four elements Comprehensive and Exclusive and Diverging From Ecosystem Definitions already imply, made explicit) and maintained (subsequent documents follow it; revision is possible but costly and recorded in that document's own changelog; popularity does not override precision), without repeating what Diverging From Ecosystem Definitions already states.
- "Word-Weight Rebalancing" was added as a new subsection under AI Implications, carrying over framework.md's mechanism sketch but rewritten to match this document's own epistemic register — presented as one proposed way to act on AI Implications' working hypothesis, not as a settled mechanism.

#### Deliberation
- The principle that a shared concept should live in exactly one place was agreed (Omid Hekayati — approved).
- The extension of this document rather than a rewrite was requested, since it already existed in the current template with its own changelog (Omid Hekayati — requested).

#### Considered and not done
- **Keeping Word-Weight Rebalancing at framework.md's original, more confident phrasing (rejected)**: considered on the grounds that it was already written and reviewed; rejected because this document's AI Implications section is explicit that the underlying claim is an unvalidated working hypothesis, and a mechanism built to act on a hypothesis should not be stated with more certainty than the hypothesis itself carries — doing so would let the more confident copy quietly become the ecosystem's working understanding of AI Implications by virtue of being the more citable-sounding of the two versions. framework.md's original phrasing ("an AI model... would: 1. Load... 2. Resolve...") stated the mechanism far more confidently than this document's own AI Implications section states the hypothesis it would be acting on.

---

### The Default Meaning of an Unreferenced Term added; Vocabulary document retired
- Time: 2026-09-03T00:00:00Z
- Type: Added
- Cited:
  - `docs/vocabulary.md` (deleted) — Evidence: the retired document's own state motivated the rule; it held only two external links (connection-oriented/connectionless, consumed by chapar.md's Ethernet-comparison discussion) and no membership criterion, no front matter, and no changelog of its own, so it had begun functioning as an unmanaged catch-all — the exact failure mode an ungoverned vocabulary list invites.
- Propagates to:
  - `docs/vocabulary.md`: Done — deleted. Its two links moved into `docs/modules/net/networking.md`'s Layer presence topic (the classification question is a cross-layer networking concern, not a layer-2 protocol's); the RFC-process paragraph it carried was RFC-era boilerplate rather than governed content, so it died with the file without loss — the substance of that paragraph (a consistent, reviewed path for changes to enter the project's documentation, with statuses that say what may be depended on) is specified authoritatively in [documentation-explanation.md](./documentation-explanation.md)'s Status section, and its remaining wording was generic GitHub pull-request boilerplate.
  - thinking.md: Done — the Discourse Norms' definitions-outrank-terminology entry previously pointed to vocabulary.md as a lookup home; it now points to this document's new section instead.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- **The Default Meaning of an Unreferenced Term** was added as a new section directly after Terminology Authority and Governance, completing that section's boundary statement: governance covers the terms Memar has defined; this section covers all the others (Super Z — drafted). The rule: an unreferenced word carries exactly its general (dictionary or established scientific) meaning — ecosystem redefinitions, industry mythology, and framework narratives do not attach to it. Referencing a Memar Definition is the explicit act that switches a word to its specialized sense.
- The rule replaces the retired `vocabulary.md`, whose role had been to hold pointers to general meanings but which had no membership criterion and had become an unmanaged catch-all.
- The vocabulary links were relocated and the inbound references repointed (Super Z).
- The monolithic example was supplied (Omid Hekayati).

#### Deliberation
- vocabulary.md was judged unsalvageable as a registry: without a hard membership criterion it would only accumulate entries nobody governs — "a place where anything can be dumped" (Omid Hekayati — decided).
- The default-meaning rule was directed to live in this document as an independent section, stated as a general principle rather than tied to the retired file (Omid Hekayati — directed).
- The general-meaning default was further directed to exclude ecosystem definitions and narratives entirely, not merely business-layer ones — a word without a Memar reference means its dictionary/general sense, nothing more (Omid Hekayati — directed).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - terminology.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../CONTRIBUTORS.md#opencode)) - moved

#### What changed
- The `terminology.md` body now carries only the fixed four top-level sections (Abstract, Introduction, Explanation, Results); the `## Discussion` heading and its subsections — `Drawbacks`, `Rationale and alternatives` (with its five `Why…` entries), `Prior art`, `Unresolved questions`, `Future possibilities` — no longer exist in the document.
- The document-level Drawbacks accounting and the four surviving rejected-alternative rationales moved to this entry's `Considered and not done`; the comparative survey of engineering disciplines' reasoning order moved to this entry's `Related work`.
- The nine open questions and eleven future-possibility items moved to the newly created paired handoff (`terminology.handoff.md`) as `Open Questions` and `Anticipated Work`.
- Two `Rationale and alternatives` entries were dropped as already graduated rather than copied: "Why prefer scientific terminology?" is carried by the body's Scientific Terms and Science as Methodology sections, and "Why Three Layers, and Not More" is carried by the Abstract and the Scientific Terms simplification note.
- Body pointers to retired sections were repointed: the Abstract and Scientific Terms references to "Why Three Layers, and Not More" were replaced by the graduated body text and a link to the handoff's `Open Questions`, and the Word-Weight Rebalancing pointer to "Future possibilities" now links to the handoff's `Anticipated Work`.

#### Considered and not done
- **The terminology-first method's costs were recorded, not treated as disqualifying (migrated from the removed document-level `Drawbacks` section)**: the approach increases documentation, learning, review, terminology-analysis, and concept-clarification effort; discussions may initially become slower, because participants are encouraged to clarify concepts before proposing technologies rather than jumping straight to a familiar tool; and some widely accepted industry terminology may require decomposition into more fundamental concepts before it can be used safely within Memar, which itself takes time and can feel, to a newcomer, like unnecessary ceremony around a word everyone already understands well enough for ordinary purposes. Some participants may view the process as unnecessary complexity, particularly under deadline pressure, when a familiar but imprecise term would let a conversation move faster in the short term. Memar considers these costs significantly lower than the long-term costs of reasoning from distorted mental models, which tend to surface much later, much more expensively, and in a form far harder to trace back to their terminological origin; the objective of the method is quality of understanding, not speed of discussion.
- **Using popular terminology as-is (rejected; migrated from the retired "Why not simply use popular terminology?")**: popularity does not imply precision — many popular terms accumulate conflicting meanings over time precisely because their popularity is driven by broad appeal rather than by narrow, precise applicability — so popularity is insufficient on its own as a foundation for architectural reasoning, even though it remains useful for other purposes (discoverability, communication with newcomers, marketing).
- **Eliminating technology terminology (rejected; migrated from the retired "Why not eliminate technology terminology?")**: technology terminology remains necessary, because implementation eventually requires technologies and no system can be built entirely out of scientific principles without ever naming an actual technique or tool; only technology terminology redefining foundational concepts is rejected — technology is a consumer of concepts and should not become the source of concepts.
- **Eliminating business terminology (rejected; migrated from the retired "Why not eliminate business terminology?")**: business terminology often carries valuable historical, organizational, operational, and commercial knowledge — Agile and DevOps, whatever their definitional instability, both encode real, hard-won lessons about how software gets built by actual teams under actual constraints — so the problem is not its existence but its misuse as a conceptual foundation, and it can remain useful provided it does not replace more fundamental concepts in architectural reasoning.
- **Classifying terminology not at all (rejected; migrated from the retired "Why classify terminology at all?")**: terminology influences mental models, mental models influence architecture, and architecture influences system outcomes, so terminology is an architectural concern, not merely a stylistic one; classification provides a mechanism for evaluating terminology quality before it affects architectural decisions, rather than discovering the problem only after the architecture built on top of it has already calcified.

#### Related work
- Most mature engineering disciplines naturally move from Scientific Principles, to Engineering Models, to Technologies, to Tools, before making implementation decisions — structural engineering does not begin with CAD software selection, aeronautical engineering does not begin with simulation tool selection, thermal engineering does not begin with product selection — while software development frequently reverses this order and begins with tools, arguably because software's tooling is cheap and immediate to acquire in a way that a wind tunnel or a structural test rig is not, which removes much of the friction that would otherwise force earlier disciplines back toward first principles. This document's attempt is to restore, within Memar, that direction of reasoning commonly found in mature engineering disciplines, while acknowledging that software's low barrier to tool acquisition makes the discipline harder to sustain than it is in fields where reaching for a tool prematurely is simply not an option. (Migrated from the removed document-level `Prior art` section)

---

### The obligation to correct a term used against its Definition
- Time: 2026-10-02T00:00:00Z
- Type: Added
- Propagates to:
  - docs/framework.md: Done — the pointer to *Terminology Authority and Governance* and *Word-Weight Rebalancing* resolves against the new section heading and the promoted one, so the topic it delegates to now carries the correction obligation as well as the weighting hypothesis.
  - docs/system.md: Rejected — no change. *System → Structure* already excludes "the arrangement of a system's parts" from Structure and records that the concept's name is open, and *System → Architecture* already separates the design processes from the structure they produce; both were cited rather than restated.
  - docs/modeling.md: Rejected — no change. Decomposition into concerns is already stated in terms no document restricts to code, and the reach of that argument is demonstrated by a worked case rather than by an added rule.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
- A `Correcting a Term Used Against Its Definition` section states the obligation this document previously implied but never placed on anyone: when a participant uses a term Memar has Defined to mean something else, the term is corrected where it appears and the correction names its reason. It binds human and AI participants alike, and it places the correction in the work — report, document, naming, commit message — rather than in a private judgement, on the ground that an uncorrected term enters the documents and the next session's reading, where the reader meets a sense nobody chose and has no signal that it is not Memar's.
- The section states that the correction names the word and not the reasoning. A participant whose sense is right and whose word is wrong has observed something correctly and misnamed it; replacing the word leaves the observation standing, while rejecting the observation over the word discards correct work for a spelling. It states this in the direction that carries the most weight, where the participant of highest authority uses the everyday sense: authority settles who may decide a question, not which sense of a word is correct.
- Two boundaries are stated so the obligation does not exceed its subject. It is not a licence to correct the wider world, since the section it depends on already states that the point is not to correct how the world outside Memar uses a word, and a participant describing an external system is describing that system's own vocabulary. And it does not reach words Memar has not Defined, where the ordinary sense governs and an ordinary word used ordinarily is not a misuse.
- The section states what to do when the concept is real and the word for it does not exist yet: report that the concept is the one under discussion, that the two neighbouring Defined terms exclude it, and that its name is an open question in the handoff. Substituting the nearest defined word is rejected in the body as worse than the misuse, because it attaches a precise term to a concept that term does not claim and the error then reads as settled.
- `Terminology Authority and Governance` was promoted from a fourth-level heading under *Definition vs Explanation* to a section of its own, so that governance of a term and construction of a Definition are siblings rather than one inside the other. Its anchor is unchanged.
- *Word-Weight Rebalancing* no longer lists surfacing a usage conflict as one item of a mechanism left open. It now states that the obligation to surface the conflict is settled and cited, while a mechanism enforcing the weighting remains unsettled, and that an unsettled mechanism is not a reason to withhold the correction meanwhile.

#### Considered and not done
- Writing the rule into `cognition.md`'s discourse norms instead — rejected: the norms govern how a discussion is conducted, and this is a rule about a term's referent, which is what this document governs. A cross-reference is cheaper than a second statement.
- Naming the concept "the arrangement of a system's parts" needs, so a correction has a word to offer — rejected: the name is the owner's open question in `system.handoff.md`, and a terminology document inventing the term its own companion document records as undecided would settle by drafting what was left open by decision.
- Leaving *Word-Weight Rebalancing* untouched on the ground that its hedge already covers the case — rejected: its hedge covers the *mechanism*, and listing the correction among the items "left open" told a reader the correction itself was unsettled. Two statements in one document contradicting each other is the drift this document exists to prevent.

---

### Corpus vs. The Sources: a body of source is not a body of text
- Time: 2026-10-04T06:38:54Z
- Type: Added
- Cited:
  - [Documentation — File Naming](./documentation.md#file-naming) — `Reference`: the criteria a name is chosen by — it communicates meaning, preserves conceptual boundaries, avoids implementation-specific vocabulary, and stays stable over time
  - [Terminology — The Default Meaning of an Unreferenced Term](./terminology.md#the-default-meaning-of-an-unreferenced-term) — `Reference`: the rule this ruling relies on, that a word no document defines carries exactly its general meaning
  - [Terminology — Correcting a Term Used Against Its Definition](./terminology.md#correcting-a-term-used-against-its-definition) — `Reference`: the correction names the word and not the reasoning, and the observation stands
- Propagates to:
  - modules/README.md: Done — the topic *The sources, and what they are not* states what this repository's sources are, what standing the owner has given them, and what the name does not claim
  - modules/README.changelog.md: Done — created to carry that change
  - docs/system.md: Rejected — no change. *System → Ecosystem* records the framework's own collective nouns, and this term names one repository's source tree, not a System any framework document defines
  - docs/cognition.md: Rejected — no change. *Definitions outrank terminology* already routes a reader of an undefined word here; this entry is what such a reader now finds
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — drafted, applied

#### What changed
- A worked case, *Corpus vs. The Sources*, states the distinction the word had been blurring. *Corpus* is a word about language — a body of written text gathered so something can be examined across it — and that sense is an ordinary dictionary sense that needs no definition. A body of program source is a different thing: nothing about it is text to be sampled for frequency, and nothing about it comes from a language's literature. What it is, plainly, is **the sources**.
- The case states why the distinction is not cosmetic. *Corpus* reads as a settled, collected, whole body of material — something a claim may appeal to — so naming a half-finished conversion "the corpus" lends it that standing by the word alone. **The sources is the neutral name**: it says what the files are and claims nothing about whether they are worth arguing from. A project that has ruled its sources to be neither evidence nor premise says so in its own documents; the name does not say it for it and is not chosen to.

#### Considered and not done
- Naming the concept in a base document of any project — rejected: *the sources* is a repository's own name for its own tree. What belongs here is the rule about the word and the standing it lends, both of which hold for any project; what the thing is belongs to the project, and is recorded in `modules/README.md` instead.
- Defining *the sources* as a Scientific Term — rejected: it would claim a falsifiable boundary the repository has not drawn, and a Definition is supposed to fix one.
- **Archive** — rejected: it fits only the Go and JavaScript blocks carried inside the source files, which the repository already calls *the two archives*, so the name would name a part and be read as the whole.
- **Residue** — rejected: it is the owner's verdict written into the name, and the repository already uses it for the narrower thing — the `// TODO(go-migrate):` clue blocks the port left — so the wider use would collide.
- **Library** — rejected: it claims a standing the owner has explicitly refused, in the same sentence the tree's neutrality depends on.
- **The port** — rejected: the port is the attempt, and the sources are what the attempt left. It also collides with `modules/go-port/`, whose subject is the work, and it launders the argumentative use — a sentence resting on what the sources happen to contain would read as a fact about the port rather than a caution about a residue.
- Correcting the word in the architecture documents' substance — rejected: the owner has ruled it out. The rename changes how the concept is addressed; it does not re-argue the documents that already record the ruling.

---

### Task is used, never defined, and says so on purpose
- Time: 2026-10-04T00:00:00Z
- Type: Added
- Cited:
  - [Process Research 001 — Work Decomposition](./process.research.001.md) - **Reference**: the inquiry whose Question 3 asked whether a Memar document should own a definition for *Task*, and whose finding was that no document did while three documents leaned on the word.
- Propagates to:
  - [knowledge.md](./knowledge.md): Done - [Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) now marks its use and links here.
  - [documentation-changelog.md](./documentation-changelog.md): Done - the `Tasks` field's deferral now names this position rather than standing alone as a refusal to model one.
  - [README.md](../README.md): None needed - the Enterprise scope this entry points at is already the README's own subject.
  - [terminology.handoff.md](./terminology.handoff.md): None needed - no question this entry answers was carried there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - claimed the position across earlier sessions, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - drafted, argued

#### What changed
- [Terminology](./terminology.md) gains [A Term Deliberately Left Open](./terminology.md#a-term-deliberately-left-open), a class of term alongside the defined and the merely-unreferenced ones. A term in this class is used in Memar's documents, never defined by one, marked as the deliberate use it is at each appearance, and defined where the work on the concept is actually being done. The section states why the class exists at all: for a concept larger than the framework, the ordinary meaning is not thinner than Memar's would be but misleading, because it arrives carrying the settled, familiar shape of the concept and a reader who takes it as Memar's has adopted a definition no Memar document made.
- The section states the cost of naming a term into the class rather than leaving it implicit. Memar's documents then use a word the framework does not own, and a reader who wants the concept must leave the framework to get it; the price is accepted because the alternative is that a framework needing a settled word takes the word, and in taking it settles by definition the part of the design space the word names — before the work that would have explored that space has been done. The concept then grows in spite of its own name rather than because of it. The GitHub vocabulary stands as the illustration of the pattern: the ordinary tracker sense was fixed early under the name *issue*, and the wider structural reading was not afterwards available to anything built on it.
- The class has a membership test rather than a membership by memory, and it is narrow: the concept must be larger than the framework's current scope, work on it must be happening in a scope outside this repository, and defining it here must narrow a design space that work has not explored. A term that merely lacks a definition, or whose concept Memar recognizes but has not named, is not in the class — [Correcting a Term Used Against Its Definition](./terminology.md#correcting-a-term-used-against-its-definition) and the handoff's open questions answer those.
- **Task is the class's one member.** The concept is one of the general-purpose graph domains the [Organization](https://github.com/GeniusesGroup/organization) project develops as the identity and structural core for any collective entity, alongside groups, departments, and staff, and Memar's Enterprise scope is where a built answer to it is delivered. Two Memar passages carry weight on the word — [Knowledge → Task-Centric Knowledge Evolution](./knowledge.md#task-centric-knowledge-evolution) and this facet's `Tasks` entry field — and both now link here, so each reads as chosen rather than as an oversight waiting to be corrected.
- Until this entry, the position existed only as a judgment held across earlier sessions and written down nowhere. Under [Cognition → Definitions outrank terminology](./cognition.md#definitions-outrank-terminology) an undefined term carries its ordinary general meaning, so *Task* meant three different things in three passages with nothing marking the difference: the ordinary sense of a thing one process asks another to perform, the primary unit of knowledge evolution, and an entry in a tracker nobody here has chosen. A reader resolving any of them had been given an answer by accident.

#### Considered and not done
- **Defining Task in Memar (rejected by the owner):** the concept is larger than the framework and is being developed as a domain model elsewhere; fixing it here would close a design space that work has not explored, which is the whole reason the class exists.
- **Letting the ordinary meaning stand unremarked, on the ground that the default rule already covers it (rejected):** the default rule is what made the ambiguity harmful. It hands a reader a settled definition of a concept the framework has never examined, and it does so silently.
- **Removing the word from Memar's passages and using `decision` or `investigation` instead (not taken):** it would leave the knowledge-evolution principle weaker, since the passage's point is that a *task* is the unit rather than a snapshot, and the parenthetical already shows the concept generalising past any one of them. The section states the ordinary sense explicitly at the site, which is the smaller cost and the reversible one.
- **Naming a broader class of terms (rejected):** the class is defined by a three-part test, not by a mood about avoiding definitions. A wider class would take in ordinary words that simply need no definition, and would make the section a licence rather than an exception.
- **Writing the definition here and marking it Enterprise's (rejected):** a definition in Memar is a definition in Memar. Marking a section as belonging elsewhere does not stop the next reader, or the next agent, from citing it.

---

### Two handoff entries closed against Scientific Terms and Word-Weight Rebalancing
- Time: 2026-10-04T18:21:00Z
- Type: Fixed
- Propagates to:
  - terminology.handoff.md: Done — two open-question entries removed; Scientific Terms and Word-Weight Rebalancing are their homes, and the handoff's Anticipated Work is where building the mechanism stays tracked.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- Two entries left `terminology.handoff.md`'s Open Questions, each verified against the passage that settles it before its block was deleted:
  - the sub-tiers question is answered by [Scientific Terms](./terminology.md#scientific-terms) — "Memar accepts this simplification deliberately, for the reasons stated in terminology.md's Abstract", with the finer-grained alternative named in the body instead of left as an unexamined simplification. The coarser single layer is therefore the stated trade-off, not a pending decision.
  - the AI-weighting question is answered by [Word-Weight Rebalancing](./terminology.md#word-weight-rebalancing), which states what such a mechanism must do (load Definitions as precedence context, prefer the document's sense within Memar work, stay consistent at the point of origin) and separates what is settled from what is not: "the first is unsettled, the second is settled" — whether to build the mechanism remains open, while the obligation to surface a conflict between a person's usage and a Definition is not among the things left open.
- Whether to build the weighting mechanism, and in what form, was already carried by this handoff's Anticipated Work; removing the Open Questions entry therefore retires nothing that is still owed an answer there.
- The Scientific Terms section's pointer to this handoff's open questions now names a question this entry settles; correcting that pointer is owed to a later pass on the base document.
- No base document body was edited.

#### Considered and not done
- **Keeping the sub-tiers question open because the body still calls the alternative an open question (rejected)**: the body already decides the single layer deliberately and states why; an answered question re-registered as pending keeps surfacing in the search for unfinished work it no longer belongs to. The pointer noted above is a wording defect in the base document, not a reason to keep the question in the handoff.
- **Building the weighting mechanism as part of this removal (not done)**: the section's residual is the mechanism's design and worth, already named by the Anticipated Work entry; a handoff entry is the place for an unanswered question, not for work nobody has committed to.

---

### No terminology registry as a source of authority
- Time: 2026-10-04T20:16:22Z
- Type: Added
- Propagates to:
  - terminology.handoff.md: Done — the registry open-question entry removed; the section below is its home.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance) now states that a registry would be a second home for claims Memar has already placed, that the authoritative home of a Definition is the document that establishes it, and that a registry indexing or restating those Definitions is generated from them and is corrected where the two disagree.
- `terminology.handoff.md` no longer carries "Should Memar maintain a formal terminology registry?".

#### Considered and not done
- **Deleting the Anticipated Work lines "Framework-wide terminology registry" and "Auto-generated Memar glossary, tagged by terminology layer" (rejected)**: what is settled is authority, not the artifact. Those lines already scope the registry as generated, and they remain the place where building it is tracked.
- **Recording the registry as out of scope entirely (rejected)**: an index derived from the document set is useful to a reader and carries no authority of its own, which is a position rather than a prohibition.
- **Relying on per-term layer tags in a registry to make layer classification consistent across documents (rejected)**: [Terminology Layers](./terminology.md#terminology-layers) defines each layer by what distinguishes it so the classification applies to terms it has not listed, so the tags add no consistency the rule does not already carry.

---

### A document states its terms, not a layer tag for each
- Time: 2026-10-05T09:35:23Z
- Type: Changed
- Cited:
  - [Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance) - Evidence: the authoritative home of a Definition is the document that establishes it, and an index restating those Definitions is corrected where they disagree
- Propagates to:
  - terminology.handoff.md: Done - the entry asking whether future documents should tag their key terms by terminology layer removed, heading and body line with it
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Terminology Layers](./terminology.md#terminology-layers) now states that because each layer's criterion settles the layer wherever a term appears, a document states its terms and their Definitions rather than tagging each term with a layer. The passage carrying it is that section's own second sentence — "Each layer is defined below by what distinguishes it, not only by example, so that the classification can be applied to a term this document has not already listed" — which makes the tag an answer the criterion already gives, and [Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance), which makes a per-term tag in another document a second home for a classification this document already places.
- `terminology.handoff.md` no longer asks whether future documents should explicitly identify which terminology layer each of their key terms belongs to.

#### Considered and not done
- **Relying on per-term layer tags to make classification consistent across documents (rejected, and already rejected for a registry)**: [Terminology Layers](./terminology.md#terminology-layers) defines each layer by what distinguishes it so the classification applies to terms it has not listed, so the tags add no consistency the rule does not already carry. The tags would be checked by the same criterion that makes them unnecessary, and two copies of one classification can drift.
- **Requiring the tag only on a term the document defines (rejected)**: the same criterion settles the layer of a term this document has never seen, which is the case a reader most needs it for.
- **Adding the requirement to the layer examples as an instruction to their authors (rejected)**: an example listing a term's layer is a demonstration of the classification, not an instruction binding every document, and stating it as one would repeat in every example what the defining sentence already says once.

---

### Modeling's foundation is stated, not chosen
- Time: 2026-10-05T17:15:06Z
- Type: Changed
- Cited:
  - [Type → Abstract](./type.md#abstract) — Evidence: the document "is not one framework among several that a system may choose or decline", which is the fact this entry's wording now rests on
  - [Type → Type Beyond Programming Languages](./type.md#type-beyond-programming-languages) — Evidence: "There is no system whose semantic entities have no Type, and none that would decline to model itself this way"
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- *Scientific Terms* now says Memar treats scientific terminology as the preferred foundation for learning and for reasoning, and then says that for modeling the position is stronger than a preference because it is not one: every system's semantics are stated in mathematics, which in this framework is type theory, so a term is precise enough for modeling when it states a Type cleanly. The sentence that called the preference pragmatic rather than ideological is replaced; the criterion that remains is reasoning quality rather than scientificity for its own sake, which is the claim the paragraph's evidence supports.

#### Considered and not done
- The paragraph above it, which flags a finer-grained split of the Scientific layer into formal/mathematical, empirical, and philosophical sub-tiers, was left exactly as it stands, and its open question stays open. The ruling supplies a fact about the layer a system's semantics are stated in, which is not the same fact as whether Identity and Graph belong in one tier or two; writing the split down now would record a decision this entry has no evidence for.
- Nothing was written into `terminology.handoff.md`. The sub-tier question the body defers there is unchanged, so no entry was narrowed or removed.
- *Concept-First Thinking* was left alone. Its ordering claim — concept before principle before technology — does not rest on the modeling foundation being a preference, and nothing in this entry disturbs it.

#### Deliberation
The finding was that "preferred foundation for learning, modeling, and architectural reasoning … pragmatic rather than ideological" would have had a reader hold two incompatible positions: that the ground modeling stands on is a preference to be weighed, and that it is a declared layer a system may not decline. The wording keeps the document's actual justification intact — the mechanisms science subjects its terms to — and narrows only what it claims about modeling (Space Bunny Alpha — argued, drafted, applied). Whether the deferral in the paragraph above can be converted into a stated fact was examined and held back, because the ruling fixes where semantics are stated rather than how terms are tiered, and mistaking one for the other would have closed an open question by substitution (Omid Hekayati — decided).

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:47:00Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed, revised

#### What changed
- Reviewed the uncommitted change to [terminology.md](./terminology.md), [terminology.handoff.md](./terminology.handoff.md), and this changelog (working tree against HEAD). Checked: the registry sentence and the layer-tag sentence in the base document each carry their reason and have the changelog entries above (2026-10-04T20:16:22Z, 2026-10-05T09:35:23Z); the AI-weighting question is answered by [Word-Weight Rebalancing](./terminology.md#word-weight-rebalancing), whose settled/unsettled sentence exists in HEAD and is quoted faithfully, with the mechanism still tracked in Anticipated Work; the Scientific Terms rewording matches its entry (2026-10-05T17:15:06Z); the two link and contributor-alias edits in old entries only repoint `protocols/net/networking.md` to the existing `modules/net/networking.md` and use the alias CONTRIBUTORS.md lists (`space-bunny`); no changelog entry was removed; the new handoff question's citation to the `organization` project's `supply-chain.changelog.md` was read and holds; `memar content check` reports no problem.
- [terminology.handoff.md](./terminology.handoff.md): restored *Should the Scientific layer eventually be split into sub-tiers?* verbatim from HEAD. The entry dated 2026-10-04T18:21:00Z removed it as answered, but the base document's Scientific Terms section still flags the split as an open question and points to this handoff, and the later entry dated 2026-10-05T17:15:06Z records, on the owner's ruling, that the question stays open and that nothing was removed from the handoff. The question is therefore still owed an answer and its removal left the body's pointer dangling.
- Not recorded by any entry above and recorded here: the handoff gained the open question *Is borrowing a mathematical term for a non-mathematical relation a named error?* and two Anticipated Work lines on recognising review graduation (a proposal only, pending contributor governance); they are additions of open work, not answers, and need no base-document change.

#### Considered and not done
- The 2026-10-04T18:21:00Z entry still says the sub-tiers entry was removed; it was left as written because changelogs are history, and this entry records the restoration.

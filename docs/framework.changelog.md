# Framework Changelog

## Changelog

### Initial draft
- Time: 2026-06-21T00:00:00Z
- Type: Added
- Cited:
  - [Terminology](./terminology.md) — Depends_on: this document builds directly on the terminology philosophy, classification layers, and concept-first thinking established there; its definitions must stay consistent with those principles.
  - [System](./system.md) — Depends_on: this document depends on the foundational definitions of System, Structure, Framework, and Architecture established there — particularly the co-equal relationship between Framework (design space) and Architecture (concrete realization), and the distinction between domain-level and system-level constraints.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Gemini](../CONTRIBUTORS.md#gemini) (3.1 pro, extended thinking) — drafted
  - [Claude](../CONTRIBUTORS.md#claude) (claude-sonnet-5, medium effort, extended thinking) — reviewed
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) — argued
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM 5.2, medium effort) — rewrote

#### What changed
- The initial draft was produced (Gemini — drafted).
- Established Framework's atomic definition ("a framework is a description of a system"), its co-equal relationship with Architecture (Constraint Space vs. Decision Space), the Framework/Model distinction, explicit vs. implicit frameworks, Framework vs. Development Framework, goal-oriented frameworks and Purpose Space, Framework vs. Library vs. Toolkit, the Framework/Sub-Framework distinction (the degree-of-silence criterion), Memar's own design-space-over-implementation-layers stance, and Document Authority and Terminology Governance including the Word-Weight Rebalancing concept for AI models.
- The residual "Framework is a System" claim was removed in a reconciliation pass with System (Claude).
- The "level of abstraction" Framework/Model test was replaced with the particular-instance-vs-space-of-instances test (Claude).
- The upstream-process example was added to Purpose Space (Claude).
- The Description definition was added (Claude).
- The Document Authority and Terminology Governance topic was rewritten, along with restructuring to broader scope, Framework/Sub-Framework formalization, and the Word-Weight Rebalancing concept for AI model integration (Super Z — rewrote).

#### Deliberation
- The core architectural stance was claimed and argued: the document authority principle; the terminology governance concept; the word-weight rebalancing vision; the Framework/Sub-Framework distinction and the degree-of-silence criterion; the Terminology Caveat; Framework vs. Development Framework as a specialization; frameworks may be implicit as well as explicit; goal-orientation (Purpose Space) as a first-class dimension alongside Constraint Space (Omid Hekayati — claimed, argued).
- "Framework is a System" was rejected as the core definition, and Description was established as Framework's core identity instead (Omid Hekayati — claimed, argued).
- Alternatives were argued for and against, and revisions incorporated (Gemini).
- A critical review was conducted: the Framework-as-Aspect ambiguity was identified; the framework/sub-framework distinction and the degree-of-silence criterion were pressed for; whether ISA-scale is the threshold for Architecture-as-System was challenged; Edge Types were identified as needing independent formal treatment (Claude — reviewed).
- Argumentation for and against alternatives was provided, and revisions incorporated (ChatGPT — argued).

---

### Revision: Framework as Description
- Time: 2026-07-01T00:00:00Z (approximate — this document had no per-revision timestamps prior to this changelog; correct if a more precise date is known)
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — approved.
  - [Claude](../CONTRIBUTORS.md#claude) — argued, rewrote

#### What changed
- Replaced the previous definition — "a structured set of constraints, conventions, and reusable components that provides a foundation for building systems within a defined problem domain" — with the atomic definition: "a framework is a description of a system," applying the Definition vs. Explanation principle (proposed for Terminology).
- All additional properties (hypothetical nature, goal-orientation, relationship to Model, implicit vs. explicit, development framework as specialization) became explanatory content rather than definitional content.
- *Hypothetical* was retained but explicitly disambiguated from its colloquial meaning ("assumed before realization," not "imaginary or unrealizable").
- Framework and Model were distinguished by purpose and level rather than treated as interchangeable — a model describes what a system *is*, a framework describes what systems *may be* within a space; all frameworks employ models, but not all models constitute frameworks.
- Explicit and implicit frameworks were distinguished as a difference of accessibility, not of kind (Linux's "everything is a file" principle as the example of an implicit framework element).
- Framework and Development Framework were separated, with "development framework" as the specialization colloquial usage almost always actually means.
- Goal-oriented frameworks and Purpose Space were introduced: frameworks are purpose spaces as well as constraint spaces, with a consistency requirement that a development framework's own goals must be achievable by its own development process, not only by the systems built within it.
- Explanatory sections were also cleaned of word-layer conflicts — "constraints" and "capabilities" as components of Structure were no longer used ambiguously where Framework's relationship to Structure was discussed.

#### Considered and not done
The atomic-definition approach was chosen over continuing to pile qualifying adjectives into the definition itself, on the grounds that discriminative power should come from the explanatory structure surrounding a definition, not from the definition trying to do all the work alone — the same principle later applied consistently across Memar's other foundational documents.

---

### Revision: Reconciling Framework-as-Aspect with the Atomic Definition
- Time: 2026-07-18T00:00:00Z (approximate, aligned with the corresponding System changelog entry — "Framework-as-System regression fix" — since the two were resolved together)
- Type: Fixed
- Propagates to:
  - system.md: Done — the corresponding section there was retitled and rewritten in the same pass; see system.changelog.md's "Framework-as-System regression fix" entry.
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — reviewed, rewrote

#### What changed
- The Explicit and Implicit Frameworks topic now states the Linux "everything is a file" example without asserting that Linux, as a framework, is a System — the Framework-as-Aspect relationship (a framework's influence becoming part of a built system's Structure) holds regardless of whether the framework, considered on its own, independently qualifies as a System.
- The now-resolved Future Possibilities item asserting Framework-as-System was removed.
- System's corresponding section was retitled and rewritten in the same pass so that "Framework Considered as a System" is presented explicitly as an optional, instance-specific lens (available to sufficiently rich, evolving frameworks such as Khayyam) rather than a co-equal sense of what "Framework" means — consistent with the general principle, applied elsewhere to Technology and to Architecture, that System is never baked into a concept's core definition.

#### Deliberation
- It was identified that this document's own Future Possibilities section still asserted "the framework itself is an independent System (Framework-as-System)" as settled, and that System's own Framework treatment still presented "Framework is a System" as one of two co-equal, definitional senses of the word — both left over from before the atomic definition above was adopted, and both in direct tension with it (Claude — reviewed).

---

### Revision: Framework/Model Test, Purpose Space Example, Description Definition
- Time: 2026-07-20T00:00:00Z (approximate, aligned with the corresponding System changelog entry — "Attribution corrections, Description definition, and Systems Thinking note")
- Type: Changed
- Propagates to:
  - system.md: Done — the Description definition was added there, at the point where Framework's definition first depends on it, in the same pass.
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- Three corrections raised in review.
- The Framework/Model distinction was corrected: the previous test ("level and purpose of abstraction") was misleading, since a model can describe something arbitrarily large (a cosmological model still describes one universe) and a framework can describe something arbitrarily small (a framework with two admissible configurations is still a framework). The corrected test is particular instance vs. space of instances — a model describes a *this*, however large; a framework describes a *kind*, however small its space of members.
- Purpose Space gained a second, distinct example: beyond a framework's stated goals shaping the design space directly, a framework constraint (e.g., "nothing may be assumed by default") can force a *prior* clarifying process into existence — illustrated by the 100-unit residential example, where a detailed description of residents' intended lifestyle must happen before the private-kitchen question can be evaluated, because a habitual answer would itself be an unexamined default.
- Since Framework's definition depends on the word "description," which was previously undefined anywhere in Memar's documents, a short definition — "a statement that represents something in words, or more broadly in any symbolic form" — was added in system.md at the point where Framework's definition first depends on it, using the term's ordinary dictionary sense rather than introducing a new specialized concept.

---

### Migration to the Explanation-facet document template
- Time: 2026-08-16T00:00:00Z
- Type: refactor
- Propagates to:
  - modularity.md, process.md, modeling.md, system.md: Reference — this document's cross-references to system.md's Structure and Responsibility topics were checked against their current content as part of this pass, since those documents were revised earlier in the same review effort.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- Restructured the document from `Summary/Motivation/Guide-level explanation/Reference-level explanation/Discussion/Change Rationale` into the current template per `documentation-explanation.md` (`Abstract → Introduction → Explanation → Results → Discussion`).
- Merged the Guide-level building analogy into Explanation as its own topic rather than keeping a separate Guide/Reference split.
- Moved front-matter `Citations` and `Contributor(s)` into this changelog's entries.
- Migrated the three-round `## Change Rationale` history into the changelog entries above, with approximate dates aligned to the corresponding system.changelog.md entries where the two documents were revised together, flagged as approximate.
- Replaced "RFC" with "document" or "Document" throughout the body and its cross-references to other documents (`[System RFC]` → `[System](./system.md)`, etc.).
- Replaced "capabilities and limitations" with "capabilities and constraints" in Explicit and Implicit Frameworks, matching the term system.md uses.
- Removed the specific identifier "(RFC 495465)" from the Protocol cross-reference under Document Authority, since a document's numeric identifier is not a stable citation form and the relative link already does that job.
- Folded the Purpose Space topic's own nested Unresolved questions and Future possibilities into Framework as Description's single topic-level Discussion, rather than leaving a separately-nested Discussion one level deeper than every other subsection.
- Added a new Unresolved question connecting Purpose Space's goal-orientation to system.md's newly-added Responsibility property.
- Added two Unresolved questions raised by this review — whether Document Authority and Terminology Governance belongs in this document or in terminology.md, and the dangling, unlinked citation to "memar-go generics elimination RFC" under Memar's Framework.
- No definitional content was changed in this pass beyond the terminology and structural migration and the capability/constraint wording fix; substantive findings from this review are recorded as new Unresolved questions rather than resolved unilaterally.

#### Deliberation
- It was requested that this document be migrated to the current structure; that "RFC" be replaced with "Document" throughout (per the project-wide convention that RFC names a change-status pathway, not the artifact itself); that a changelog file be created since none existed; and that a critical review be conducted now that more of the surrounding documents have been worked through (Omid Hekayati — requested).

#### Considered and not done
Considered moving Document Authority and Terminology Governance out of this document into `terminology.md` directly, since its content is general to every Memar document rather than specific to Framework. Deferred instead: `terminology.md` has not been reviewed in this pass, and moving a substantial topic across documents without first checking the destination document's own scope and content risks creating the same kind of duplication or contradiction this whole review effort has been trying to remove. Logged as an Unresolved question instead of decided unilaterally.

---

### Document Authority and Terminology Governance moved to terminology.md
- Time: 2026-08-16T00:00:00Z
- Type: refactor
- Propagates to:
  - terminology.md: Done — "Terminology Authority and Governance" and "Word-Weight Rebalancing" added there in the same pass; see terminology.changelog.md's corresponding entry.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested, approved
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- "Document Authority and Terminology Governance" is no longer duplicated in this document; its content now lives in `terminology.md`, extended in place rather than rewritten.
- The section was shrunk to a short paragraph pointing at terminology.md's now-expanded sections, keeping only the one piece that is Framework-specific: the Protocol document as a worked example of a Definition built to that standard.
- The topic's own nested Discussion was removed (its Unresolved question about placement is now resolved).
- The corresponding item was removed from this document's top-level Unresolved questions.

#### Deliberation
- After reading terminology.md in full, it was confirmed that "Document Authority and Terminology Governance" substantially duplicated terminology.md's "Diverging From Ecosystem Definitions" and "AI Implications" sections, and that the AI-facing half (Word-Weight Rebalancing) stated the same underlying claim with more confidence than terminology.md's own AI Implications section states the working hypothesis it depends on (Claude — rewrote).
- Once the duplication with terminology.md was confirmed by reading terminology.md directly, it was agreed the section should move (Omid Hekayati — requested, approved).
- It was asked that terminology.md itself be extended rather than rewritten (Omid Hekayati — requested).

---

### Fixed: Memar's Framework overclaimed "the entire software stack" as Memar's scope
- Time: 2026-08-16T00:00:00Z
- Type: Fixed
- Cited:
  - [README.md](../README.md) — Reference: the project's own README already states Memar's domain-agnostic identity ("developing... technology, software, hardware, apps, gadgets, buildings, organizations/society, and more") and already names "Computer" as the specific software-implementation category under System Categories; this fix aligns the document with that existing scope rather than introducing a new one.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Claude](../CONTRIBUTORS.md#claude) — rewrote

#### What changed
- "Memar's framework defines the design space for the entire software stack" is only true of Memar's software instantiation, not of Memar as a project — the project README already establishes Memar as domain-agnostic (software, hardware, buildings, organizations, and more) and already calls the software-specific instantiation "Computer."
- The Abstract and the *Memar's Framework* topic's opening were rewritten to state explicitly that this document, and that topic specifically, describe Memar's Computer (software) system category, cross-referencing the README for Memar's broader identity — now saying so explicitly and pointing to the README, instead of implicitly equating Memar with its software instantiation or letting the software-stack claim read as a claim about Memar as a whole.
- No content was moved into a new `memar.md`; the existing README already serves as Memar's single, correctly-scoped identity statement.
- A corresponding Unresolved question was added about whether Memar's other system categories need a comparable design-space treatment somewhere.

#### Deliberation
- It was identified that the Abstract's claim — "Memar's framework defines the design space for the entire software stack" — reads as a claim about Memar as a whole, contradicting Memar's own domain-agnostic identity (also stated in his skill definition for Memar: "developing... any system such as technology, software, hardware, apps, gadgets, buildings, organizations/society, and more") (Omid Hekayati — requested).
- It was asked whether Memar's project-level identity should be consolidated in the project README or in a new, dedicated `memar.md`, deferring to the reviewer's recommendation (Omid Hekayati — requested).
- Keeping Memar's project-level identity in the existing README rather than creating `memar.md` was recommended, since the README already states that identity correctly and at the right scope (domain-agnostic, with "Computer" already named as the software-specific category) — a new document would duplicate rather than consolidate (Claude — rewrote).

#### Considered and not done
Considered creating a dedicated `memar.md` to hold Memar's project-level identity, migrated out of the README into the Explanation-facet template. Rejected: the README already states this identity, at the correct domain-agnostic scope, and a README is read by a different audience (first-time visitors to the repository) than an Explanation-facet document is — forcing it into that template would not consolidate anything, it would create a second "what is Memar" document that the README and `memar.md` would then need to be kept consistent with each other, which is the exact duplication risk this whole review effort has been working against.

---

### Memar's Purpose Space: the knowledge-then-thinking-then-intelligence-then-agency chain stated as the framework's goal
- Time: 2026-09-05T11:30:00Z
- Type: Added
- Cited:
  - [Knowledge](./knowledge.md) — Reference: owns the first link of the chain; its Concept Web topic defers the chain statement to this document.
  - [Thinking](./thinking.md) — Reference: the activity whose material knowledge is and whose quality intelligence names.
  - [Agency](./agency.md) — Reference: the exercise of intelligence toward objectives.
- Propagates to:
  - README.md: Done — the Goals section now points to this statement instead of standing alone; the four engineering bullets are labeled as means.
  - knowledge.md: Done — its Concept Web topic links here for the chain's authoritative home.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- Added the *Memar's Purpose Space: From Knowledge to Agency* topic, drafted against this document's own goal-specificity criterion, giving the framework an explicit goal statement as this document's own Goal-Oriented Frameworks criterion requires.
- The topic states the knowledge→thinking→intelligence→agency→goals chain with each link's owning document.
- It defines intelligence inline without a dedicated document (following the precedent of Science in system.md).
- It states Memar's goal through the framework-as-system lens.
- It subordinates the README's engineering bullets as means.
- The README's Goals section now carries a pointer here rather than a competing statement.

#### Deliberation
- It was stated that the purpose of defining knowledge and thinking is intelligence, and the purpose of intelligence is agency toward further goals such as quality of life, and that this reasoning thread — one of Memar's primary goals — had gone missing from the documents (Omid Hekayati — claimed).
- The goal definition was adopted: a system that, across a wide range of cognitive tasks and without task-specific training, builds a reliable model of reality, revises it with new evidence, and reasons and decides independently toward a goal (Omid Hekayati — decided).
- It was ruled that stating it as "Memar is a system that…" is legitimate because every framework is also observable through the system lens, per this document's own Framework-as-Aspect position (Omid Hekayati — decided).
- A standalone intelligence document was rejected, since intelligence is an output relation of the other concepts (Omid Hekayati — decided).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - framework.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's fixed top-level sections are now Abstract, Introduction, Explanation, and Results only; the top-level `## Discussion` and the nested Discussion wrappers under the Framework-as-Description, Framework-and-Sub-Framework, Memar's-Framework, and Memar's-Purpose-Space topics are retired.
- Fifteen open questions (seven under Framework as Description, three under Framework and Sub-Framework, two under Memar's Purpose Space, three document-level) and four anticipated-work items now live in the newly created paired [framework.handoff.md](./framework.handoff.md); the Sub-Framework document item, stated identically under two topics, is carried once there.
- The memar-go generics-breakage premise evidence was folded inline into the *Memar's Framework: Design Space Over Implementation Layers* topic at the claim it supports (inherited layer assumptions become expensive constraints); the topic's Practical Implications already carry the multi-language implementation state the retired Drawbacks restated, so that sentence was dropped as graduated.
- Rejected alternatives and topic drawbacks are recorded in this entry's *Considered and not done* below; the two retired Prior art surveys are recorded in this entry's *Related work* below.
- The document-level *Future possibilities* pointer ("See the Future possibilities subsections under each Explanation topic above") was dropped with no relocation: it carried no content of its own and its referents now live in the handoff.
- In-body pointers to retired sections now target the handoff: the Goal-Oriented Frameworks topic's "see Unresolved questions below" and the *Memar's Framework* evidence note's "see Unresolved questions at the end of this document".

#### Considered and not done
- **Provide guidelines rather than a framework (rejected; migrated from the Framework-as-Description topic's retired Rationale and alternatives)**: guidelines lack the structural enforcement that a framework provides. Without concrete constraints, conventions, and components, different contributors will make incompatible choices, and the coherence of the resulting systems will suffer.
- **Position Framework as a subset or parent of Architecture (rejected; migrated from the same topic's retired Rationale and alternatives)**: making one subordinate to the other implies a hierarchy that does not exist. Framework and Architecture address different questions — permissible design space vs. concrete realization — and neither contains the other. A system has both a framework (or operates within one) and an architecture; they coexist as parallel, co-dependent aspects of the system.
- **Frameworks constrain architectural freedom (drawback recorded per the migration; migrated from the Framework-as-Description topic's retired Drawbacks)**: frameworks can constrain architectural freedom by imposing structure that may not be optimal for every system. A developer who uses a framework may unconsciously accept architectural decisions that the framework makes implicitly, treating them as inevitable rather than as choices that could have been made differently. Memar mitigates this risk by making its own architectural decisions explicit and by encouraging contributors to understand *why* each constraint exists, not merely *that* it exists.
- **Constraint-conflation risk of the co-equal relationship (drawback recorded per the migration; migrated from the same topic's retired Drawbacks)**: because both use the word "constraint," readers may conflate framework and architecture constraints. Memar mitigates this by distinguishing them as *domain-level* constraints (framework) versus *system-level* constraints (architecture), and by ensuring that the dependency chain in [System](./system.md)'s Relationships topic makes their distinct roles clear.
- **Terminological cost of the framework/sub-framework distinction (drawback recorded per the migration; migrated from the Framework-and-Sub-Framework topic's retired Drawbacks)**: every existing system called a "framework" in the industry must now be re-evaluated: is it a framework or a sub-framework? This re-evaluation is labor-intensive and may be perceived as gatekeeping — as Memar declaring that most of the industry's "frameworks" are not "real" frameworks. The mitigation is the same as for all of Memar's terminological divergences: the distinction exists because it captures a real structural difference that affects how systems are built, and the cost of not making the distinction (silent gaps in guidance, integration friction between incompatible sub-frameworks) is higher than the cost of the unfamiliar terminology.
- **The conventional model — framework inside language and OS (rejected; migrated from the Memar's-Framework topic's retired Rationale and alternatives)**: it guarantees that the framework will eventually be constrained by assumptions it did not make and cannot change. The cost of that constraint compounds over time — each new capability the framework needs must be negotiated against what the language and OS already decided, rather than being specified from first principles. Memar's approach accepts a higher initial cost (no incremental adoption, no reuse of existing language/OS tooling without design review) in exchange for eliminating that compounding constraint cost.
- **A dedicated `intelligence.md` (rejected; migrated from the Memar's-Purpose-Space topic's retired Rationale and alternatives)**: intelligence is what the other three documents jointly produce; a standalone document could only restate them and would become the project's first tautology-bearing file. The chain needs a home, not each link of it.
- **Stating the chain inside [Knowledge](./knowledge.md) (rejected; migrated from the same topic's retired Rationale and alternatives)**: one link of the chain cannot own the whole chain without every other document either duplicating it or deferring to a sibling that is not its owner; the purpose space of a framework belongs in the framework document — [framework.md](./framework.md), by its own Purpose Space rule.
- **Stating the goal only in the README (rejected; migrated from the same topic's retired Rationale and alternatives)**: the README is a first-visitor index, not a normative home; it now carries a short pointer to the statement in [framework.md](./framework.md#memars-purpose-space-from-knowledge-to-agency) rather than a competing one.

#### Related work
- The concept of a software framework is well-established in the literature (Johnson and Foote, "Designing Reusable Classes," 1988; Fayad and Schmidt, "Object-Oriented Application Frameworks," 1997). The distinction between framework and library is discussed in Gamma et al. ("Design Patterns," 1994). (Migrated from the Framework-as-Description topic's retired Prior art)
- **Unikernel projects** (MirageOS, IncludeOS, Nanos): the closest architectural parallel, specifically in their treatment of the OS as a consequence of the application's requirements rather than a given substrate. (Migrated from the Memar's-Framework topic's retired Prior art)
- **Singularity (Microsoft Research)**: an OS research project that co-designed the language (Sing#) and the OS from shared first principles, rather than fitting a language onto an existing OS. (Migrated from the Memar's-Framework topic's retired Prior art)
- **Erlang/BEAM**: a language+runtime that is, in practice, its own OS-like substrate — the BEAM VM defines process scheduling, memory isolation, and fault tolerance in ways that make the underlying OS largely irrelevant to application code. (Migrated from the Memar's-Framework topic's retired Prior art)
- **General-purpose OS + framework combinations** (Spring Boot on JVM on Linux, Rails on Ruby on Linux): the conventional prior art being explicitly rejected, not because they are bad engineering for their context, but because their inherited-assumption problem is well-documented and the cost of navigating it is visible in every large codebase that has lived long enough. (Migrated from the Memar's-Framework topic's retired Prior art)

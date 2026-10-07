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
  - [Thinking](./cognition.md) — Reference: the activity whose material knowledge is and whose quality intelligence names.
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
  - [Qwen](../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../CONTRIBUTORS.md#opencode)) - moved

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

---

### Framework handoff: constraints-versus-flexibility question removed

- Time: 2026-10-04T18:17:13Z
- Type: Fixed
- Propagates to:
  - framework.handoff.md: Done — the "Balancing framework constraints against architectural flexibility" open question was deleted; `framework.md` already answers it (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, applied

#### What changed
- `docs/framework.handoff.md` no longer carries the open question "Balancing framework constraints against architectural flexibility". Its answer is already in the governing document: [Framework → Framework as Description → The Co-Equal Relationship](./framework.md#the-co-equal-relationship) states that Framework and Architecture are "two distinct, co-equal aspects of a System", and distinguishes framework constraints as *domain-level* from architecture constraints as *system-level* — the framework fixes what kinds of solutions are allowed, the architecture chooses which one, so the two are not competing claims on the same space.
- No other open question in that handoff was touched.

#### Considered and not done
- Adding the answer to the handoff as a resolved entry, or marking the question "Answered": a handoff records what a discussion still stands at, and a rule already landed in its governing document must not be duplicated there — the copy is what drifts. The question therefore leaves the artifact without a trace, per [Documentation Handoff → Decisions and Open Questions](./documentation-handoff.md#optional-sections).
- Deleting an `## Anticipated Work` line: the two lines nearest the deleted question (framework goals as a named section, goals-as-design-space notation) schedule different work and stay.

---

### A framework's goal is the Purpose of the system it describes
- Time: 2026-10-04T21:40:00Z
- Type: Changed
- Cited:
  - [System](./system.md) - Consumed definitions: Purpose (a system exists toward one or more purposes, in a functional rather than teleological sense) and Responsibility (Purpose viewed from the vantage point of a containing System), including the coherence criterion applied to it.
- Propagates to:
  - framework.handoff.md: Done - the framework-goals-versus-Purpose-and-Responsibility open question is removed; the answer is the body's.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Goal-Oriented Frameworks and Purpose Space](./framework.md#goal-oriented-frameworks-and-purpose-space) states what a framework's goal is: the **Purpose** of the system the framework describes, stated for a *hypothetical* system, and stated by a framework that is itself realized as that System's own Purpose. It states that a framework's goal is never a Responsibility — a Responsibility is a Purpose seen from a containing System, and neither the framework nor the system it describes is contained by the other.
- The paragraph sits with the section's residential-building example of goals that determine which constraints are imposed, ahead of the paragraph narrowing the discussion to development frameworks, because the relation holds for frameworks in general.
- The handoff's open question "Framework goals versus System Purpose and Responsibility" is removed; [framework.md](./framework.md) now checks its own use of "goal" against both definitions.

#### Considered and not done
- A framework's goal as a third concept, distinct from both Purpose and Responsibility - rejected: the goals this section's own examples state ("optimize for communal living," "minimize per-unit construction cost") are what the described systems are for, which is Purpose in [System → Key Properties](./system.md#system) terms.
- A framework's goal as a Responsibility of the framework itself - rejected: [When Is a Responsibility Coherent?](./system.md#when-is-a-responsibility-coherent) asks whether a part has an independent behavioral boundary and lifecycle, and a goal stated in a description is put to no such test; the framework's own processes are bound by the consistency requirement this section already states, not by a Responsibility.
- Ruling on whether a realized framework's goal is its own Purpose rather than the described system's - not taken as a separate claim: the case is Memar, where the stated goal is a capability of Memar itself and the aim of systems built within it, so the body states the coincidence rather than choosing between the two readings.
- Restating System's Purpose and Responsibility definitions inline - rejected: [System](./system.md#system) holds both, and a restatement would duplicate them.

---

### The event-taxonomy cluster's link repaired after the question it names was answered
- Time: 2026-10-04T18:55:00Z
- Type: Fixed
- Propagates to:
  - framework.audit.001.md: Done — mechanical link repair; the frozen record's findings, participants, and status are unchanged (Action: None).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — applied

#### What changed
- The `A-07` event-taxonomy cluster in [Framework Changelog - the Go-group claim corpus audited against the documents](./framework.changelog.md#the-go-group-claim-corpus-audited-against-the-documents-and-its-residue-recorded-here) linked to the entry that cluster became in `process.handoff.md`. That entry has since been answered by [Event → What an Event Is](./protocols/process/event.md#what-an-event-is) and removed, so the research's link named an anchor that no longer existed; it now names the section that answers it. The cluster's own claim — that a durable fact, a contract message between components, and a runtime signal are three different things sharing one word in ordinary use — is unchanged.
- A frozen research accepts a mechanical repair without reopening the record.

#### Considered and not done
- **Reinstating a heading in `process.handoff.md` to preserve the old anchor (rejected)**: an empty heading is barred, and a heading invented to keep a link resolvable would put a section in a handoff that records no open state.
- **Rewriting the cluster's prose to say the question is closed (rejected)**: that is the superseding-research mechanism, and a research this narrow does not warrant one; the link alone needed repair.

---

### The framework states its boundary on authentication, session, and authorization
- Time: 2026-10-05T09:07:04Z
- Type: Changed
- Propagates to:
  - framework.handoff.md: Done — the open question "Does Memar need authentication, session, and authorization protocols?" is removed; [What the Framework Does Not Specify](./framework.md#what-the-framework-does-not-specify) now states what holds.
  - framework.audit.001.md: Done — cluster `A-16` now names [Framework → What the Framework Does Not Specify](./framework.md#what-the-framework-does-not-specify); the frozen record's findings, participants, and status are unchanged (Action: None).
  - protocols/modules/sdk.handoff.md: Done — the entry "Revocation and integrity of a delegated credential" names the same section in its `Next:` and its `State:` now records that the credential's vocabulary and revocation mechanism belong to the system that owns them, with the question kept open and its substance intact.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [framework.md](./framework.md) gains *What the Framework Does Not Specify*, stating that authentication, session, and authorization are three protocols the framework leaves to the system that needs them and the project that builds it — each with its own subject, its own conformance rules, and its own path of evolution — and that Memar's architecture-level vocabulary carries neither a `user` nor a `group` concept. What the guarantee layer needs is a principal a privilege boundary can attach to, with no resemblance to a person, a service, or a device assumed on its behalf; the section points at [OS → Identity: principals, not users](./protocols/computer/os.md#identity-principals-not-users) for that statement rather than repeating it.
- `framework.handoff.md`: that open question is removed. It carried a large amount of recovered owner reasoning — that the three are separate concerns and a session is not authentication, that a project should use what the lower layers already provide rather than invent a per-request scheme, that machine-to-machine trust is a certificate from the domain's own authority, that a dependency is trusted whole or not at all, and that the owner's own platform direction was a structure with no administrator — none of which is lost, because the ruling disposes of the question those positions were gathered against: specifying the mechanisms is not the framework's work. The subject remains available to whichever project does specify them.

#### Considered and not done
- **Write authentication, session, and authorization as framework protocol documents (rejected)**: each carries detail that only the system deciding to authenticate, to hold a session, or to admit an action can settle, and a specification written above that decision would freeze one project's answer into a constraint on every system built within Memar. The framework's contribution is the boundary that keeps the three apart, which is what the body now states.
- **Introduce a `user` or `group` concept at architecture level so the three subjects have something to attach to (rejected)**: `user` names an assembly of independent concerns — a name, a home directory, a login shell, a credential — made by one tradition, and adopting the word would carry that assembly's answers into every design conversation that used it. The guarantee side needs only something a privilege boundary can attach to, and [OS → Identity: principals, not users](./protocols/computer/os.md#identity-principals-not-users) already states what that is without the label.
- **Carry the security sense of *token* into the framework (rejected)**: the collision the removed handoff entry recorded against [Token → What a Token Is](./protocols/token.md#what-a-token-is) mattered only if a credential vocabulary were introduced here. With the mechanisms left to their owners, no such vocabulary is introduced, so nothing collides and the term stays with the document that owns it.
- **Naming the `organization` repository in the body (rejected)**: the boundary is a statement about what the framework specifies, not about which project first exercises it; naming a consumer project's path would tie the framework's own subject to one consumer's structure.

---

### The aspect reading already keeps a framework outside the System it shapes
- Time: 2026-10-05T11:52:00Z
- Type: Changed
- Cited:
  - [System](./system.md) - Consumed definitions: Structure (the set of capabilities and limitations a System exposes and enforces) and Structure Is Not the Arrangement of Parts, plus the Meta-Principle's statement that a description characterizing a System is not itself inside it.
- Propagates to:
  - framework.handoff.md: Done - the open question on relabeling the Framework-as-Aspect edge is removed; the answer is the body's.
  - system.md: Pending - [System → Framework as Aspect, and Framework Considered as a System](./system.md#framework-as-aspect-and-framework-considered-as-a-system) still calls the choice between the aspect reading and constraining-from-outside an open question the Framework document leaves for future revision, and points its reader at framework.handoff.md#open-questions for it; that sentence needs to name the section that settles it.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Explicit and Implicit Frameworks](./framework.md#explicit-and-implicit-frameworks) states what a framework contributes to a System: a share of that System's Structure — the capabilities and constraints the System inherited rather than chose for itself — and Structure is a description of capabilities and constraints, not the arrangement of a system's parts. An aspect of a description is therefore not a part placed inside the System it describes: the framework stays outside, and what enters is the share of Structure its description accounts for.
- `framework.handoff.md` no longer carries the entry "Relabeling the Framework-as-Aspect edge". Its other entries, including the questions about separate edge types for Purpose Space and Constraint Space, a labeled framework property on `constrained_by`, and a Framework-to-Model edge, are untouched.

#### Considered and not done
- **Introducing a distinct `constrains` edge type in place of the aspect relation (rejected)**: the concern the removed entry raised was that "is an aspect of" might be read as placing the framework inside the System. Structure is a description of capabilities and constraints and not an arrangement of parts, so the aspect is already a share of a description rather than a part inside a system; a second edge name would name the same fact a second time, in a document that would then carry two labels for one relationship.
- **Moving the ruling into system.md instead of the Framework document (rejected)**: the edge type belongs to [System's conceptual graph](./system.md#edge-types-what-kinds-of-relationships-exist), which that document owns, and the Framework document is where the entry placed the question. The sentence in System that still calls it open is recorded above as a pending propagation rather than edited from outside its owner's file.
- **Settling the adjacent edge-type questions in the same pass (not taken)**: nothing in this resolution decides whether Purpose Space and Constraint Space deserve two edges, whether `constrained_by` needs a framework/sub-framework label, or whether Framework-to-Model belongs in the graph. Those turn on whether a reader misreads the graph as it stands, and [System's own position](./system.md#edge-types-what-kinds-of-relationships-exist) is that the edge taxonomy is a working one, sufficient to prevent the most common misreadings and not yet a complete formalism.

---

### The specificity requirement scoped to one level, and the ground for leaving three mechanisms unlisted
- Time: 2026-10-05T12:20:00Z
- Type: Changed
- Cited:
  - [Protocol](./protocol.md) - Consumed definitions: Who Defines a Protocol (a protocol is meaningful at the level of the system that offers it; each definer's account is decidable where it is offered; plurality of definers is what makes convergence on the real requirement objective rather than hypothetical).
  - [System](./system.md) - Consumed definitions: Boundary (an organization's own draw is its own Boundary) and Key Properties.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Goal-Oriented Frameworks and Purpose Space](./framework.md#goal-oriented-frameworks-and-purpose-space) gains a paragraph after the goal-specificity requirement: "The specificity requirement is about one level: readers disagreeing about what a framework's own goals mean is the failure it exists to prevent. Different organizations developing different models and protocols for the same subject matter is not that failure. Each such answer is stated at the level of the organization that develops it and is internally coherent there ([Protocol → Who Defines a Protocol](./protocol.md#who-defines-a-protocol)), and their plurality is what makes the concept they are each modelling identifiable rather than assumed — a goal specific enough to bind readers of one framework does not and cannot bind what other frameworks decide to model."
- [What the Framework Does Not Specify](./framework.md#what-the-framework-does-not-specify) closes its first paragraph with the ground the subject-distinctness argument does not reach: "Each is left because the level at which it is meaningful is the level of the organization that offers it ([Protocol → Who Defines a Protocol](./protocol.md#who-defines-a-protocol)), and Memar is not that level for any of them."

#### Deliberation
- Both passages were identified in an earlier read-only pass of this session by the same participant now applying them, which surveyed `docs/` for passages that a reader of the rulings would have to reconcile against; the rulings those passages now cite were made elsewhere in this session, and the second of them was applied to this same document earlier in the wave.
- The specificity requirement was read as stated for one framework's readers rather than for all readers of all frameworks. Read universally it forbids the divergence the plurality ruling endorses, and it forbids it in the one place a framework most needs the latitude — its own goals, which the section's residential-building example already shows two frameworks satisfying incompatibly.
- The clause added to *What the Framework Does Not Specify* names the organizational level rather than the three subjects' distinctness, because subject-distinctness was already argued from and does not by itself explain why the framework declines to specify them: a distinct subject with a specified answer would still not be the framework's to specify. The paragraph says neither that authentication is unlike other protocols nor that it is like them; it says where the decision to specify one belongs.
- The word *hypothetical* was deliberately avoided in both sentences. [The Nature of Framework](./framework.md#the-nature-of-framework) defines it as "assumed before realization," explicitly not "imaginary or unrealizable," and Protocol's topic uses it in the everyday sense. Writing "objective rather than hypothetical" here would have put two senses of a defined term in one document, so the sentence says "identifiable rather than assumed" instead.
- Neither handoff entry was removed. "Formalizing framework goals as a named section" asks whether the goals need a section of their own, and "Conflicting framework goals" asks how a framework resolves goals pulling against each other; a paragraph saying which level the specificity requirement binds does not answer either, and the second is a question this document's residential-building example already makes sharp rather than settles.

---

---

### A consistency claim needs a public failure statement
- Time: 2026-10-07T03:45:00Z
- Type: Changed
- Cited:
  - [Documentation — Comparison → Hindsight](./comparisons/hindsight.001.md) - Evidence: Hindsight publishes its own failure catalog; a development framework without a maintained record of where its goals are not applied has an unfalsifiable consistency claim.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [Goal-Oriented Frameworks and Purpose Space](./framework.md#goal-oriented-frameworks-and-purpose-space) gains a paragraph: the consistency requirement binds the framework's public self-report, and a maintained statement of where it applies its goals — and where it does not, including tried-and-abandoned disciplines — is anticipated work recorded here as a requirement, not a report. [README → Where Memar Stops](../README.md#where-memar-stops-and-where-work-continues) carries the one-line pointer to it.

#### Considered and not done
- **Writing the failure statement itself now (deferred)**: the honest record cannot be produced in this session without performative narrative; the requirement is stated, and the statement is anticipated work rather than prose.

---

### The Go-group claim corpus audited against the documents, and its residue recorded here
- Time: 2026-10-07T06:20:00Z
- Type: Added
- Propagates to:
  - framework.handoff.md: Reference - the authentication, session, and authorization question the audit raised is recorded there, not here.
  - protocols/gui/gui.handoff.md, protocols/identifier/media-type.handoff.md, protocols/process/error.handoff.md, process.handoff.md, protocols/memory/memory.handoff.md, protocols/net/networking.handoff.md, protocols/computer/runtime.handoff.md, protocols/time/time.handoff.md, protocols/modules/sdk.handoff.md: Reference - the remaining eleven uncarried claims are open questions in these handoffs, each carrying the owner's reasoning in the vocabulary of the artifact that owns it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - questioner, goal-setter
  - [OpenCode](../CONTRIBUTORS.md#opencode) - researcher

#### What changed
- No text of `framework.md` changed except the authentication question's landing, which the earlier entry records. What this entry adds is the audit's own residue, which had no home while it sat in a file that claimed to be a research: the corpus it examined, the negative result of the examination, and the claims it declined to carry.
- The audit covered twenty-six claim clusters the owner stated in three Go-community message extracts (2023-2025), checked row by row against the current document set. Twelve were already carried by the documents in the documents' own words, one was carried except for a decision an existing handoff already held, and eleven were absent or carried only in part. Every uncarried claim became an open question in the handoff of the artifact that owns its subject, and two handoff files were created for artifacts whose contested vocabulary had none. The raw exports, the preservation plan, and the earlier cluster manifest were then deleted, so no claim depends on a line reference into a file that no longer exists.

#### Surveyed
- **Model before storage, API, and structure** (`A-01`) - carried by [Modeling → The Model as the Primary Artifact](./modeling.md#the-model-as-the-primary-artifact) and System's statement that implementations are projections of the model. No new text; a second statement would be a copy that drifts.
- **A Module is a conceptual boundary, not a deployment unit** (`A-02`) - carried by [Modularity → Module](./modularity.md).
- **Independent identities for routing, service, operation, and request** (`A-03`) - carried by [sRPC → Independent identities](./protocols/net/sRPC.md#independent-identities); its open half is already [SDK Handoff → What the declaration artifact is](./protocols/modules/sdk.handoff.md#what-the-declaration-artifact-is).
- **Acquired facts, derived views, and caches differ in authority** (`A-04`) - carried by [Modeling → Acquired Data vs. Discovered Data](./modeling.md#acquired-data-vs-discovered-data), the shortcut-edge rule, and Memory's shadow-tier rule; when a discovered value may be persisted is already a [Modeling Handoff](./modeling.handoff.md) question.
- **Error, Log, and Bug as three entities** (`A-08`, partly) - carried by [Error → Boundary discipline](./protocols/process/error.md#boundary-discipline); the panic half was recovered into [Control Flow Handoff](./protocols/process/control-flow.handoff.md) on 2026-09-17.
- **Operation semantics, not a universal context object** (`A-09`) - [Process → Data carriage between layers](./process.md#data-carriage-between-layers) already refuses context as a cross-layer carrier, which is the position the sources take; the plan's `OperationContext` proposal contradicted the document and was not carried.
- **Channels and buffers are different things; execution units are pooled** - carried by [Concurrency → Channels are signals, not stores](./protocols/computer/concurrency.md#channels-are-signals-not-stores) and [Concurrency → Execution units are pooled, not spawned](./protocols/computer/concurrency.md#execution-units-are-pooled-not-spawned).
- **Ownership, copy, and lifetime are contract members; allocation claims are measurement claims** (`A-21`, `A-22`) - carried by [Memory → Copy and ownership semantics are contract members](./protocols/memory/memory.md#copy-and-ownership-semantics-are-contract-members) and [Memory → Allocation claims are measurement claims](./protocols/memory/memory.md#allocation-claims-are-measurement-claims); no benchmark number from the sources was carried with them, which is the correct outcome - the documents record the discipline, not one ecosystem's measurements.
- **The GUI does not speak the network; one routing authority; validation generated once** (`A-14`, `A-15` in part) - carried by [GUI → Position on GUI Architecture](./protocols/gui/gui.md), whose changelog already attributes the claims to the owner.
- **Logical routing and link-layer carriage are different owners** (`A-18`) - carried by [GP → Routing architecture](./protocols/net/giti.md#routing-architecture) and [Chapar → Scope and terminology](./protocols/net/chapar.md).
- **HTTP is a guest surface, and its URL is not the routing model** (`A-19`) - carried by [HTTP → Memar's Stance on the HTTP Protocol Surface](./protocols/net/http.md#memars-stance-on-the-http-protocol-surface).
- **Dependency and version management is the repository's own mechanism** - carried by [Dependency and Version Management](./protocols/modules/dependency-management.md), including the counter-arguments.
- **Encapsulation, closure-as-implicit-capsule, and concepts outliving rejected names** (`A-23`) - carried by Khayyam's two protocol texts and [Type → Concepts Outlive Their Labels](./type.md#concepts-outlive-their-labels).
- **Communication channels produce knowledge that must be extracted and preserved** (`A-25`) - carried by [Knowledge → Communication Channels Produce Knowledge but Are Not Knowledge Repositories](./knowledge.md). The audit was that principle being carried out, and this entry is its output.
- **Uncarried claims that became questions elsewhere** (`A-05`, `A-06`, `A-07`, `A-08`, `A-10`, `A-11`, `A-12`, `A-15`, `A-16`, `A-17`, `A-20`) - each is an open question in the handoff of the artifact that owns its subject, linked from the audit's own record and now from this entry's `Propagates to`. The largest is `A-16`: authentication, session, and authorization appear in the corpus only as an example of bundled protocols, and no document, handoff, or vocabulary owns the subject.

#### Examined and not adopted
- **Measurements and observations about one ecosystem** - goroutine and buffer costs, timer accuracy, escape-analysis weakness, allocator-count folklore, a self-reported halving of binary size, an unrigorous "userspace TCP cannot improve throughput" result. Memory's measurement discipline already governs claims of this kind; a number from one runtime with no corpus, version, or platform attached is not an architectural fact, and would become one by being written down.
- **A goroutine pool described as wasteful, against the settled worker-pool default** - [Concurrency → Execution units are pooled, not spawned](./protocols/computer/concurrency.md#execution-units-are-pooled-not-spawned) states the pool as the framework's default, and the objections in the sources are scoped to a language whose per-unit cost is unusually low. Re-opening a settled position needs new evidence, not a restatement.
- **The fixed-width character-encoding argument, the server-rendered-versus-client-rendered document question, and forwarded data-governance material** (`A-24`) - the encoding question has an owner and an open list ([Characters Codec → Still considering](./protocols/codec/characters-codec.md)), where a fixed-width proposal belongs if ever adopted; the rendering question has no selected requirement to attach to; the governance material is visibly forwarded from a named other author, which is evidence of transmission only, not authorship.
- **The build, security, and working-tree snapshot of the archived `memar-go` repository** (`A-26`) - every path in it belongs to a different repository whose current state this checkout cannot confirm. Its one durable residue is carried correctly: [Networking Handoff → The userspace transport realization's scope](./protocols/net/networking.handoff.md#the-userspace-transport-realizations-scope) cites the archived goals as unratified here.
- **Personal, epistemological, and life-advice material, and paradigm comparisons treated as open questions** (`A-23`, `A-25`) - carried by their governing principles, not as claims.

#### Deliberation
- Three rules governed the examination, and they are the method: a claim a governing document already carries gets no new text; a claim that is correct but undecided becomes an open question in the owning artifact's handoff rather than body text, because writing an unratified claim into a governing document makes a conversation look like a decision; a claim that is neither carried nor undecided is recorded as not carried, with its reason, and nowhere else.
- One attribution limit governed every item above, and it is why nothing here is attributed more strongly than "stated by the owner in those groups": the extracts are owner-targeted rather than owner-only, a block without a sender name inherits the previous one, dates could not be recovered, and a forwarded quotation inside a block is evidence of transmission, not authorship.
- Five further claims the end-to-end read surfaced had no artifact to own them, and they are named in the handoffs that took them: a value whose validity is a window must not be measured against a correctable civil clock ([Time Handoff](./protocols/time/time.handoff.md#what-protects-a-time-limited-value-from-a-clock-that-moves)); the GUI's half of the shared validation shape ([GUI Handoff](./protocols/gui/gui.handoff.md#the-guis-half-of-the-shared-validation-shape)); the framework as a managed product, held beside [Framework Handoff → Formalizing framework goals as a named section](./framework.handoff.md#formalizing-framework-goals-as-a-named-section) rather than merged into it; a dependency is trusted whole or not at all, which is an owner decision beside [Dependency and Version Management](./protocols/modules/dependency-management.md); and a service whose many inputs each produce an error signals a broken architecture, which belongs with [SDK Handoff → What the declaration artifact is](./protocols/modules/sdk.handoff.md#what-the-declaration-artifact-is). Two further owner positions were left unstated by choice: the criterion that everything is possible in software and only costs differ, which is a way of arguing rather than a doctrine, and the claim that a panic at any line is a defect in reasoning, which is stronger than the question Control Flow's handoff already carries and would have quietly strengthened it.

#### Considered and not done
- **Keeping the audit as its own numbered record** (rejected on review): it was written as a Research while consulting only this repository's own documents, which the Research facet's criterion now excludes, and re-filing it as an audit invented a second artifact kind for three instances. Its residue belongs in the ledger it always belonged to, which is why the entry above has the sections it has.


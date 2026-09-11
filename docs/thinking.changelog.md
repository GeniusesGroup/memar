# Thinking Changelog

## Changelog

### Created the Thinking document, absorbing the always-active instruction rules
- Time: 2026-09-01T07:55:46Z
- Type: Added
- Cited:
  - [4E cognition](https://en.wikipedia.org/wiki/4E_cognition) — Evidence: grounds the document's claim that external artifacts (models, repositories, documents) are genuine constituents of a thinking system, not merely its outputs; the project's documentation discipline is treated as a discipline of thinking on that basis. Context-only at this revision — embodied, embedded, and enacted claims are recorded without being operationalized.
- Propagates to:
  - `.agents/skills/main/` (SKILL.md, README.md): Done — the collaboration/reasoning rules that previously lived in this always-active skill were absorbed into the base document's Discourse Norms topic and the skill directory was deleted. The always-availability role was taken over by the `memar` skill, which now directs agents to this document before reasoning-heavy work.
  - `others/memar-instructions.md`: Done — flagged as historical archive; its Part I/II/IV rules were the field-tested source this document absorbed and derived from. File retained unmodified as provenance.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- The project's collaboration and reasoning rules — previously a list of behavioral prescriptions in an always-active agent skill (`.agents/skills/main/SKILL.md`) and before that in instruction files — were replaced by a model-first document: what thinking is, which modes it has, how a conversation is two thinking systems joined by a medium, and which discourse norms follow from that model (evaluate claims on merits; definitions outrank terminology; do not assume the other participant correct or incorrect; criticism proportional to the model criticized; ask rather than assume; resist defaults arriving with the medium; prefer long-term clarity).
- Cognitive-science grounding (4E cognition) was added.
- Rules specific to modeling or documentation remain owned by their specialized documents; this document owns the rules governing thinking material as it travels between any two thinking systems.
- The rules were extracted from the retired skill and the archived instruction file, the discourse norms derived from the conversation model, and the document drafted per the Explanation facet specification (Super Z).

#### Deliberation
- The retirement of the always-active instruction skill, rather than its duplication, was directed (Omid Hekayati).
- The name `thinking.md` was chosen so the document can grow beyond critical thinking into systems, creative, and adaptive thinking as cognitive-science grounding deepens (Omid Hekayati).
- 4E cognition grounding and the two-thinking-systems conversation model were required from the start (Omid Hekayati).
- The conversation model treating exchange between any two thinking systems (human, AI, organizational) symmetrically, never as AI-specific etiquette, was directed (Omid Hekayati).
- The first draft was reviewed and the base document directed to state only the "why" — historical provenance of the rules belongs here, not in the explanatory document (Omid Hekayati).

#### Considered and not done
- **Keep the rules as an always-active skill and merely expand it (rejected by the owner)**: the skill form had no derivation behind its rules, framed general norms as AI-specific instructions, and duplicated rules already owned by terminology, modeling, and documentation documents.
- **Keep the retired skill as a thin pointer to this document (rejected by the owner)**: the owner preferred deleting it entirely and strengthening the existing `memar` skill — the skill that accompanies essentially every project adopting Memar's approach — to direct agents to project documentation including this document, avoiding a second near-always-active mechanism with a single line of content.

---

### Mode list expanded; historical narration moved out of the base document
- Time: 2026-09-01T09:10:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### What changed
- Modes of Thinking expanded from four named modes to thirteen, organized into five functional groups: Evaluative (critical, analytical, evaluative decision), Structural (abstract, concrete, systems, sequential), Generative (creative, divergent, analogical, hypothetical), and Corrective (adaptive, reflective).
- The grouping-by-function structure was introduced so the open-ended family stays navigable.
- Abstract thinking was added explicitly.
- The group structure and every mode beyond the original four are this revision's contribution — the owner's original four survive unchanged as members of their groups.
- In the base document, the Motivation was rewritten to state the costs of the rules having no authoritative home (no derivation, scoping drift, no growth path) rather than narrating where the rules used to live; the Methodology was reduced to stating what the drafting presupposed, not the chain of custody from retired files; and a Rationale entry in the Discourse Norms topic was generalized the same way.
- The moved provenance lives in this entry and the entry above.

#### Deliberation
- The first draft's mode list (critical, systems, creative, adaptive) merely mirrored the owner's own examples back instead of completing the family — abstract thinking was missing outright, flagged by the owner (Omid Hekayati — argued).
- The base document was directed to state only the "why" of its content, with all history of how it came to be written moved into this changelog (Omid Hekayati — decided).

#### Considered and not done
- **Keep the mode list at the owner's original four (rejected)**: the list was explicitly offered as incomplete by the owner — it was a starting seed, not a ceiling, and the document's own membership criterion (a named function in thinking) already justified the additions.
- **Keep the historical narration in the base document (rejected)**: the Explanation facet's own principle — a reader of the base artifact needs its current state, not its provenance — applies to the narration of where content came from, not only to front-matter provenance; the owner directed that this rule be applied to the prose as well.

---

### Created thinking.practice.md; absorbed and retired the architectural-critique practice
- Time: 2026-09-01T14:40:00Z
- Type: Added
- Propagates to:
  - `documentation-critique.practice.md`: Done — absorbed and deleted. Its critique procedure (understand-before-critiquing, the conceptual stack, the quality standards, the proportional-strength table, the output format, and the anti-patterns) moved into the new practice file, with its normative claims re-anchored as operationalizations of this document's discourse norms rather than freestanding rules.
  - `documentation-explanation.practice.md`: Done — step 4 of its document-writing procedure gained a note that critical examination of one's own claims is a component of writing applied while drafting, with a pointer to the new practice for when critique is the dominant activity.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- `thinking.practice.md` was created as the Practice-facet companion to this document, operationalizing its modes — chiefly critical thinking — into a followable procedure.
- The file absorbed the content of the retired `documentation-critique.practice.md` (the critique practice had been mis-homed under the documentation prefix: its content is about exercising a thinking mode, not about producing documents), with three changes: (1) its rules were re-anchored as operationalizations of this document's discourse norms rather than freestanding instructions, eliminating a second copy of the proportional-criticism and definitions-over-terminology rules; (2) a "Where Critique Sits" section was added stating the owner's position — critique is a component of writing and of modeling work, exercised alongside the generative and structural modes, and becomes the subject of this practice only when it is the dominant activity; (3) its "Relation to Other Practices" cross-references were updated to the surviving artifacts.
- A pointer to the new practice was added to `documentation-explanation.practice.md`'s writing step, marking the component-versus-activity boundary.
- The practice file was drafted and the absorbed content distributed (Super Z).

#### Deliberation
- Creating a thinking practice document as the absorption target for the critique practice was proposed (Omid Hekayati).
- The direction that documentation work must not be framed as if critique were its whole posture — critical examination is one component of writing a document (one mode among the family), even when starting from scratch — was given (Omid Hekayati).
- The review of where each part of the critique practice's content belonged best was directed (Omid Hekayati).
- The placement was agreed after the alternatives were reviewed (Super Z).

#### Considered and not done
- **Absorb the critique content into `documentation-explanation.practice.md` instead (rejected)**: would couple a thinking-mode procedure to the document-production procedure, implying critique is documentation-specific; critique applies to proposals, models, and designs that never become documents.
- **Create a separate `documentation.practice.md` holding a "critique as part of writing" note (rejected)**: the note is one sentence — a whole file for it would be structure without a reader; the same note placed in `documentation-explanation.practice.md`'s writing step reaches exactly the contributor who needs it, at the moment they need it.
- **Keep `documentation-critique.practice.md` as-is (rejected)**: its name and placement claimed documentation ownership of a thinking-mode practice, and its rules duplicated this document's discourse norms without linking to them — two sources of truth for the same norms, guaranteeing drift.

---

### Knowledge Management link retargeted after the rename
- Time: 2026-09-05T11:30:00Z
- Type: Changed
- Contributors:
  - [Qwen](../CONTRIBUTORS.md#qwen) (Qwen3.8-Flash) — rewrote

#### What changed
- The 4E-grounding topic's reference was retargeted from `knowledge-management.md` to [Knowledge](./knowledge.md) after that document was renamed and re-scoped to the concept.
- No change to this document's content or claims.
- The retarget was mechanical, following the rename and re-scope decided in knowledge.changelog.md.

---

### Added the conceptual-root norm and extended the abstract-thinking entry
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- New discourse norm: receive criticism at its conceptual root, not only its instance — discover the general concern an example evidences, ask when scope is ambiguous, repair in generals, and treat any root beyond the giver's own argument as the receiver's extension (Omid Hekayati — claimed).
- The norm was added to Discourse Norms with the failure modes enumerated: instance-patching, answering narrower than intended, over-generalizing an instance-local critique (Super Z).
- The receiver-side boundary was added — discovering the root does not manufacture a stronger critique than the giver argued, so an extension beyond the giver's claim is recorded as the receiver's own and judged by the evidence standard (Super Z).
- The Abstract thinking mode entry was extended, naming the instance-to-generality move as criticism's mechanism — the mechanism behind the norm (Super Z).

#### Deliberation
- The norm was distilled from a working session's observed failure: a reviewer raised a criticism against one concrete instance (a tool name in one section) and the receiving agent repaired only that instance, then needed the same criticism repeated for a second instance before generalizing (Omid Hekayati).
- The rule was stated — the receiver must discover the criticism's conceptual root, ask when scope is ambiguous, and repair in generals, not merely the cited instance — and its recording in this document directed, noting the agent had not applied this document despite it being loaded (Omid Hekayati — argued).

---

### Documentation-method migration completed: Discussion wrappers, Rationale, Prior art, Unresolved questions, Future possibilities dissolved per the finalized method
- Time: 2026-09-07T00:00:00Z
- Type: refactor
- Propagates to:
  - thinking.handoff.md: Created - open questions and future possibilities moved there.
- Contributors:
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- The document-level `Drawbacks`, `Rationale and alternatives`, and `Prior art` content preserved below; `Unresolved questions` and `Future possibilities` moved to the paired handoff (Super Z).
- The cognitive-science compatibility note (premise evidence for the definition) folded inline into the definition topic (Super Z).

Dissolved every `#### Discussion` wrapper (the definition topic, Modes of Thinking, the 4E-grounding topic, the conversation-model topic, Discourse Norms) and the document-level `## Discussion`; the 4E-contested-theory drawback folded into its topic as inline content; all other content relocated below without loss. (Super Z)

#### Considered and not done
- **Leave "thinking" undefined and regulate only behavior (rejected; migrated from the definition topic's retired `Rationale and alternatives`)**: an undefined central term would import the reader's colloquial sense — for AI-era readers, often "the internal reasoning phase of a language model" — which is one implementation of thinking, not the concept. Memar's terminology governance ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, in thinking.md, and letting documents reference that definition.
- **Name this document "critique" or "discourse" (rejected; migrated from the definition topic's retired `Rationale and alternatives`)**: both name one product or one setting of thinking. The rules Memar needs cover more than critique (systems thinking, creative exploration) and more settings than discourse (solitary analysis). Naming the document after the broader concept keeps its scope honest; the narrower subjects can become their own documents if they earn one.
- **A closed taxonomy of thinking modes (rejected; migrated from the Modes topic's retired `Rationale and alternatives`)**: would replicate the taxonomy-before-definition failure Memar's [classification principles](./classification-principles.md) warn against. Modes are named only for functions the project's actual work depends on.
- **A flat list without grouping (considered, not chosen; migrated from the Modes topic's retired `Rationale and alternatives`)**: simpler at today's scale of thirteen modes, but each added mode would linearly grow the section without revealing which modes are siblings of which; the functional grouping carries that structure at negligible cost.
- **Treat modes as separate "skills" an agent or person either has or lacks (rejected; migrated from the Modes topic's retired `Rationale and alternatives`)**: conflates the description of a practice with a capability — the same conflation [`.agents/skills/README.md`](../.agents/skills/README.md) corrects for the word "skill". A mode is a way of operating, available to be exercised deliberately regardless of the thinker's current proficiency.
- **Regulate conversations as etiquette between unequals (rejected; migrated from the conversation-model topic's retired `Rationale and alternatives`)**: the asymmetry framing — "the human directs, the AI obeys" or the inverse — produces different rule sets per direction, which then drift apart and cannot be transferred to human-human or AI-AI exchanges. Memar's agent documents ([`.agents/README.md`](../.agents/README.md)) already commit to agent-generic phrasing; the conversation model is the conceptual version of that commitment.
- **Model conversation as protocol-governed process (considered, not chosen; migrated from the conversation-model topic's retired `Rationale and alternatives`)**: Memar does define Process and Protocol formally ([Process](./process.md), [Protocol](./protocol.md)), and a conversation does satisfy them. But treating the protocol layer as the primary frame would foreground turn-taking and format — the aspects least specific to thinking — while the norms that matter concern how claims are evaluated, which the protocol frame does not address. The thinking-systems frame is the one the norms actually follow from.
- **Keep the discourse norms distributed across the specialized documents that overlap them (rejected for the general rules; migrated from the Discourse-Norms topic's retired `Rationale and alternatives`)**: the modeling-specific and documentation-specific rules genuinely do live in their specialized documents. But the general evaluation norms have no natural specialized owner — they apply everywhere and are owned by no domain. Leaving them ownerless reproduces the scattering problem under a different name; thinking.md is their single home.
- **A document per mode (critical-thinking.md, systems-thinking.md, ...) (considered, not chosen; migrated from the document-level retired `Rationale and alternatives`)**: the modes share their foundation — what a thinker is, how material travels between thinkers — and splitting would force either duplication of that foundation or a dependency web among siblings. One document with open-ended mode coverage matches the project's current scale; a mode that outgrows its section can graduate to its own document following the project's progressive-migration pattern.
- **Ground the document in AI-agent research rather than cognitive science (rejected; migrated from the document-level retired `Rationale and alternatives`)**: agent frameworks describe current AI products' behavior, which changes on product timescales; cognitive science describes thinking itself, which is the stable referent the norms need. This follows the project's general preference for scientific-layer terminology ([Terminology → Scientific Terms](./terminology.md#scientific-terms)).

#### Considered and not done (topic-level drawbacks relocated per owner ruling)
- **The 4E framing is a research program, not a settled theory;** its variants disagree about how strong each claim is, and "cognition is extended" in particular remains contested, so building project rules on it risks inheriting its controversies. The mitigation the document applies: only the extended claim is operationalized, and only to the extent of grounding what Memar already does (external models as primary artifacts); the contested stronger readings are not relied on. (Migrated from the 4E-grounding topic)

#### Considered and not done (from the removed document-level Drawbacks section)
- **Deriving norms from a model of thinking makes this document a single point of dependency: a defect in the model (for example, a wrong assumption in the conversation model) propagates into every norm derived from it. A list of ungrounded rules fails differently — locally and visibly.** Accepted deliberately: the derivability is what makes the norms checkable rather than arbitrary.
- **The document deliberately overlaps its neighbors (terminology, modeling, documentation practices) at their edges; the overlap is bounded by the ownership rule stated in Discourse Norms, but boundaries erode without maintenance.** Accepted; the ownership rule is the maintenance.

#### Related work
- Taxonomies of thinking skills and dispositions are established in educational psychology and cognitive science — Bloom's taxonomy of educational objectives, dual-process accounts of cognition, and the critical-thinking and metacognition literatures among them. Those taxonomies classify for instructional assessment; this document names modes for the narrower purpose of grounding this project's own discourse norms, and adopts no taxonomic scheme wholesale. (Migrated from the Modes topic's retired `Prior art`)
- 4E cognition (embodied, embedded, enacted, extended) emerged across philosophy of mind and cognitive science from the 1990s onward, against classical computationalist and brain-bound pictures of cognition. Related antecedents include distributed cognition (Hutchins) and activity theory. (Migrated from the 4E-grounding topic's retired `Prior art`)
- Critical-thinking literature (informal logic, argumentation theory) supplies the evaluation criteria referenced by the first norm. Systems-thinking literature (systems theory, cybernetics) underlies both the systems-thinking mode and Memar's [System](./system.md) document. The 4E cognition framing is prior art for the grounding topic and is discussed there. Dialogical models of reasoning (e.g. argumentation as a two-party activity rather than a monologue) anticipate this document's conversation model. (Migrated from the document-level retired `Prior art`)

---

### Added the confirm-before-large-scope-changes norm
- Time: 2026-09-10T11:32:04Z
- Type: Added
- Propagates to:
  - `.agents/skills/memar/SKILL.md`: Done — an intake rule added to Working rules, mirroring the existing Ask-rather-than-assume intake rule.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, decided
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, rewrote

#### What changed
- New discourse norm: confirm before large-scope changes — when a proposed change reaches beyond the instance under discussion (a definition other documents consume, a structure other sections depend on, an edit spanning several documents), propose before applying: state the proposed content and the files it will touch, so the counterpart can shape the change before it exists rather than review it after the fact.
- The norm was placed beside *Ask rather than assume*, its sibling intake norm — both prevent material that was never agreed from propagating into decisions; that one governs the scale of assumptions, this one the scale of changes.

#### Deliberation
- The norm was distilled from a working session's observed failure: an agent had recorded that "ecosystem" carried no Memar definition, and in a later session began a document-set-wide treatment of the word without presenting the plan first — the ambiguity rule was loaded but not applied at change scale (Omid Hekayati — argued).
- Recording the norm in this document and operationalizing it at intake in the `memar` skill, following the existing pattern, was directed (Omid Hekayati — decided).
- The owner's note that this document is not finalized was recorded: the norm's placement beside its sibling is current state, and regrouping the norms by the thinking mode that chiefly exercises each remains open for a future revision (Omid Hekayati).

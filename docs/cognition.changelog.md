# Cognition Changelog

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
- Modes of Thinking expanded from four named modes to thirteen, organized into four functional groups: Evaluative (critical, analytical, evaluative decision), Structural (abstract, concrete, systems, sequential), Generative (creative, divergent, analogical, hypothetical), and Corrective (adaptive, reflective). (The count error — "five" — is corrected by the 2026-09-14 entry.)
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
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

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
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — moved

#### What changed
- The body's fixed top-level sections are now `Abstract`, `Introduction`, `Explanation`, `Results` only (Super Z - applied the finalized documentation method).
- The document-level `Drawbacks`, `Rationale and alternatives`, and `Prior art` content preserved below; `Unresolved questions` and `Future possibilities` moved to the paired handoff (Super Z).
- The cognitive-science compatibility note (premise evidence for the definition) folded inline into the definition topic (Super Z).

Dissolved every `#### Discussion` wrapper (the definition topic, Modes of Thinking, the 4E-grounding topic, the conversation-model topic, Discourse Norms) and the document-level `## Discussion`; the 4E-contested-theory drawback folded into its topic as inline content; all other content relocated below without loss. (Super Z)

#### Considered and not done
- **Leave "thinking" undefined and regulate only behavior (rejected; migrated from the definition topic's retired `Rationale and alternatives`)**: an undefined central term would import the reader's colloquial sense — for AI-era readers, often "the internal reasoning phase of a language model" — which is one implementation of thinking, not the concept. Memar's terminology governance ([Terminology → Terminology Authority and Governance](./terminology.md#terminology-authority-and-governance)) requires defining a load-bearing term once, in thinking.md, and letting documents reference that definition.
- **Name this document "critique" or "discourse" (rejected; migrated from the definition topic's retired `Rationale and alternatives`)**: both name one product or one setting of thinking. The rules Memar needs cover more than critique (systems thinking, creative exploration) and more settings than discourse (solitary analysis). Naming the document after the broader concept keeps its scope honest; the narrower subjects can become their own documents if they earn one.
- **A closed taxonomy of thinking modes (rejected; migrated from the Modes topic's retired `Rationale and alternatives`)**: would replicate the taxonomy-before-definition failure Memar's [classification principles](./modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) warn against. Modes are named only for functions the project's actual work depends on.
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

---

### Added the Convergent mode and the prospective-search extension to Analogical thinking; Comparative Thinking rejected as a mode
- Time: 2026-09-14T18:39:28Z
- Type: Added
- Cited:
  - [Sternberg's triarchic theory of intelligence](https://en.wikipedia.org/wiki/Triarchic_theory_of_intelligence) — Evidence: the two-tier componential structure — executive *metacomponents* for planning, monitoring, and evaluating versus *performance components* that carry out the actions, including "perceiving relations between objects, and applying relations to another set of terms" (the analogical mapping operation) — grounds the document's later claim that an awareness layer and an operations layer exist under the named modes.
  - [Guilford's Structure of Intellect](https://en.wikipedia.org/wiki/J._P._Guilford) — Evidence: convergent production is Guilford's own named operation — "The ability to deduce a single solution to a problem" — the counterpart of divergent production in the operations dimension; convergent thinking enters the mode list as a named function with an established scientific owner, not a coinage.
  - [Miyake et al. 2000, unity and diversity of executive functions](https://en.wikipedia.org/wiki/Executive_functions) — Evidence: latent-variable analysis decomposing executive control into three correlated-but-separable factors (updating, inhibition, shifting) with a common unity factor — converging evidence that even the control layer decomposes into elementary operations; supports the primitives-layer direction recorded in the paired handoff.
  - [Gentner's structure-mapping theory of analogy](https://en.wikipedia.org/wiki/Analogy) — Evidence: "analogy depends on the mapping or alignment of the elements of source and target. The mapping takes place not only between objects, but also between relations of objects and between relations of relations" — cross-domain comparison is a structured mapping operation over relations, not a free association; the double-edge guardrail in the base document governs its products.
  - [Moseley et al. 2005, systematic review of thinking-skills frameworks](https://bera-journals.onlinelibrary.wiley.com/doi/abs/10.1080/01411920500082219) — Evidence: the review "identify and evaluate 35 frameworks and identifies three that appear to be particularly useful in the context of lifelong learning" — the named-mode vocabularies across the field's frameworks disagree while the underlying functions repeat; supports the base document's position that mode names are a navigation aid over functions, and the owner's position that the names can mislead.
  - [Gick & Holyoak 1983, schema induction and analogical transfer](https://doi.org/10.1016/0010-0285(83)90002-6) — Evidence (address-verified; quantitative pattern not independently re-verified this round): spontaneous transfer of an available analogy to an unsolved problem is empirically weak, and comparing two analogous cases induces the abstract schema that transfers — the warrant for the extension's closing move, that deliberately searching for analogs outperforms waiting to notice one.
- Propagates to: none — no live document references the mode list or its count (verified by search before the change).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (the prospective-search gap and the mode's session value), argued (the foundational-principles question), decided (apply the set; the primitives rebuild rides the upgrade session)
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — argued (the rejection case), drafted, verified sources

#### What changed
- **Convergent thinking** entered the Generative group as the counterpart of divergent thinking, with the diverge/converge cycle stated as one cycle, the candidate-testing practice named as its exercised form ([System](./system.md)'s definition reached by candidate testing is the worked example), and the boundary against evaluative decision thinking drawn: a decision selects among options already on the table; convergence narrows a field the cycle itself produced.
- **Analogical thinking** gained the prospective-search extension: the mode is exercised prospectively — before treating a problem as open, deliberately search other domains for a solved version of it — with biomimicry as the standing example (a termite mound's passive self-cooling, a sponge's lattice dispersing current forces on a tall form), the double-edge guardrail extended to the borrowed answer, and the closing contrast: spontaneously noticing the resemblance is the weak path; searching for it is the exercise the mode owes its users.
- The proposal that prompted the round — a new mode named Comparative Thinking — was rejected as a mode and resolved into its owned parts; the rationale is preserved under Considered and not done below, together with the other named candidates the round examined and rejected.
- The round's second outcome — the owner's proposal for a primitives layer under the modes — is recorded as the target architecture for this document's already-scheduled upgrade session; the reasoning and its scientific support live in the paired [handoff](./thinking.handoff.md), keeping this entry to the change that actually landed.
- The 2026-09-01 mode-list entry's count error is corrected in place: it says "five functional groups" while listing four.

#### Deliberation
- The round began from the owner's proposal: a missing mode named Comparative Thinking was claimed to be heavily load-bearing in every session's mental-model building, quoting an internet definition ("placing options, cases, or patterns side by side and asking what truly differs") and the biomimicry of wind-resistant tall structures as the standing example (Omid Hekayati — claimed).
- The proposal was decomposed into three functions, each with an existing owner: cross-domain structure transfer is Analogical thinking verbatim; disciplined side-by-side comparison is the mechanism several modes already run; and only the search policy — look in other domains for the solved version before treating a problem as open — was ownerless, which is the sentence the Analogical extension now carries (Omid Hekayati, Super Z — argued).
- The strongest defense available for Comparative-as-mode — understanding through deliberate contrast as a Structural mode — was tested and failed: the Abstract entry's essential/incidental separation is performed *by* comparison (what persists across compared cases is the essential), so the claimed function is an existing mode's mechanism, not a missing mode (Super Z — argued).
- The owner then raised the deeper question: are some modes foundational with the rest built on them, or should the document name elementary principles of thinking instead, with each mode stating which it uses — offering the encapsulation/OOP misclassification as the error class (naming a principle as part of a package). The foundational-modes tier was rejected (inter-mode dependencies are circular — critical needs criteria that abstract produces while abstract is tested against concrete cases; the document's own "a cycle, not a ladder"), and the two-kind primitives layer (operations + awareness disciplines) accepted as the target architecture for the upgrade session; the vocabulary decision — whether the layer is named "principles," "primitives," or otherwise — is the owner's to make there (Omid Hekayati — argued, decided; Super Z — argued).
- The owner's position that mode names are themselves misleading — his example: prominent critical-thinking educators suggest replacing the name with "پرسشگری سنجش‌گرایانه" (evaluative questioning) precisely because the name misroutes — was recorded as the standing motivation the primitives layer answers (Omid Hekayati — argued).
- Applying the set without waiting for a dedicated primary-source pass was directed: the verified secondary sources suffice; a primary-source pass can follow when the sources are at hand (Omid Hekayati — decided).
- The quote's source page was searched across six engines and not found; the quote is therefore used as provenance of the proposal only, and nothing from it enters the document (Super Z — verified).

#### Considered and not done
- **Add Comparative Thinking as a fourteenth mode (the owner's proposal; rejected)**: the proposal's three functions each have an owner — the transfer is Analogical verbatim, the disciplined comparison is the mechanism several modes already run (and is scheduled to become a named primitive in the upgrade), and the search policy is carried by the Analogical extension. A standalone mode would re-house a mechanism as a mode — the same error class the owner's own encapsulation/OOP analogy names: the principle is real, but it lives under the package, not as a sibling package.
- **Abstract's essential/incidental sentence as a new comparison mode (considered, not chosen)**: the separation the sentence performs *is* comparison, and the operation belongs inside the modes that run it; promoting the mechanism to a mode now would pre-empt the upgrade session's architecture decision. The sentence stays inside the Abstract entry pending the primitives layer.
- **Lateral thinking (rejected)**: its function — escaping established patterns to reach candidates by indirect routes — is covered by the Creative + Divergent pair; the remainder of its usage names a puzzle's surprise, not a mode function.
- **First-principles thinking (rejected)**: its content is Memar's own backbone — definitions precede artifacts, [Framework](./framework.md) — and its operational form (dismantle to foundations, rebuild) is the Analytical + Abstract pair; adding it as a mode would import a name for something the project already does and names elsewhere.
- **Design thinking (rejected)**: a process package (empathize, define, ideate, prototype, test), not a mode — a sequence over several modes; the document names modes by function, not packages by provenance. The same reasoning covers rejecting the family of packaged "X thinking" process brands.
- **Spatial/visual thinking (rejected)**: names the *substrate* material is held in (images, layouts, arrangements), not a function on material; the document distinguishes modes "by what they do to thinking material, not by which part of a brain or system performs them" — substrate names fail that criterion from the other side.
- **Integrative thinking (rejected)**: its function — holding two opposing models and crafting a synthesis superior to either — is the Creative + Adaptive pair applied to models; Memar's absorption practice (retired documents' content merged into owners) is this function exercised, and it needs no separate mode.
- **Probabilistic thinking (deferred, not rejected)**: the judgment of evidence quality and strength-of-claim is owned by the Critical entry ("evaluating claims: … evidence"); the stability judgments in the paired practice's procedure and its proportional-strength table operationalize it. Admitted as a mode only if a future document depends on the *quantitative* form it names; the handoff carries the question.
- **Add the further modes the round named (rejected as a batch)**: each fails the membership criterion individually; batching them would grow the list without a function the project's work depends on.

#### Related work
- Componential theories of intelligence (Sternberg's triarchic theory; Guilford's Structure of Intellect) model thinking as a small set of named elementary operations under higher-order executive control — the scientific tradition the upgrade session's primitives layer continues; Guilford's convergent/divergent production pair is the direct scientific antecedent of this entry's mode pairing. Structure-mapping theory (Gentner) models cross-domain analogy as structured alignment over relations; the schema-induction experiments of Gick and Holyoak established both the weakness of spontaneous analogical transfer and the power of deliberate comparison, grounding the prospective-search extension. Moseley et al.'s systematic review of 35 thinking-skills frameworks found the field's vocabularies diverging over recurring functions — the published form of the owner's names-can-mislead position. The Facione consensus model (cognitive skills + dispositions, the skills/awareness two-type distinction) and Miyake et al.'s decomposition of executive functions (unity-and-diversity of updating, inhibition, shifting) are further componential evidence; they are cited in the paired handoff's architecture record rather than this entry, where they support a change that has not yet landed.
---

### The primitives rebuild: elementary operations and awareness disciplines beneath the modes; thinking defined as a process; named errors recorded; practice companion reshaped
- Time: 2026-09-14T20:30:00Z
- Type: Changed
- Cited:
  - Sternberg, R. J. (1985). *Beyond IQ: A Triarchic Theory of Human Intelligence* (local copy: `chats-context/thinking/`) — Evidence: the two-tier structure the operations/disciplines layer continues — "I have identified seven metacomponents" (executive processes: deciding the problem, selecting lower-order components, selecting a representation, selecting a strategy) over performance components, with the analogical-reasoning set enumerated as "encoding and response components … and inference, mapping, application, comparison, and justification components"; mapping defined as forming the higher-order relation between the two halves of an analogy. The document's mapping operation and awareness-disciplines class are the Memar-form counterparts; no component name was imported.
  - Guilford, J. P. (1967). *The Nature of Human Intelligence* (local copy: `chats-context/thinking/`) — Evidence: convergent production "is in the area of logical deductions … the prevailing function when the input information is sufficient to determine a unique answer" (the convergent mode's entry, verified at primary source this round); and "evaluation is defined as a process of comparing a product of information with known information according to logical criteria" — comparison under criteria is Guilford's own definition of evaluation, grounding the criterion-application operation.
  - Gick, M. L., & Holyoak, K. J. (1980). "Analogical Problem Solving." *Cognitive Psychology*, 12 — Evidence (primary-source numbers, closing this entry's predecessor's open qualifier): spontaneous transfer of a memorized analogous story, without a hint, occurred for 43% of subjects (20% with distractor stories in recall) versus 76% eventually succeeding once a hint was given; Duncker's own subjects produced the dispersion solution 2 of 42 times. The warrant for the analogical mode's closing contrast — deliberate search outperforms waiting to notice — now rests on verified numbers.
  - Miyake, A., Friedman, N. P., Emerson, M. J., Witzki, A. H., Howerter, A., & Wager, T. D. (2000). "The unity and diversity of executive functions." *Cognitive Psychology*, 41 (local copy: `chats-context/thinking/`) — Evidence: the latent-variable decomposition into Shifting, Updating, and Inhibition under a common unity factor — the control layer itself decomposes into separable elementary functions, which is the operations layer's claim about thinking's control side.
  - Facione, P. (1990). *Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction* (the APA Delphi Report; local copy: `chats-context/thinking/`) — Evidence (primary source, closing the predecessor's partial verification): the panel's conceptualization "in terms of two dimensions: cognitive skills and affective dispositions"; a 61% majority held the dispositions part of critical thinking's very meaning; Table 5's dispositions carry 83% consensus. The skills/dispositions distinction is the field-side counterpart of the operations/disciplines two-kind layer.
  - Moseley, D., Elliott, J., Gregson, G., Higgins, S., Miller, N., & Newton, D. (2005). "Thinking skills frameworks for use in education and training." *British Educational Research Journal*, 31(8) (local copy: `chats-context/thinking/`) — Evidence: the systematic review evaluated 35 frameworks (55 identified), organized by "identifying common features as well as differences between frameworks" — the field's vocabularies diverge over recurring functions, the published form of the mode-names-mislead motivation.
  - Gentner, D. (1983). "Structure-Mapping: A Theoretical Framework for Analogy." *Cognitive Science*, 7 (local copies: `chats-context/thinking/`) — Evidence: analogy's interpretation as implicit rules mapping knowledge about a base domain into a target, over relations rather than surface attributes — the structure-mapping tradition the mapping operation continues.
- Propagates to:
  - thinking.practice.md: Done — reshaped in the same session (the owner ruled the practice redesign belongs here, not in the separate upgrade session): the purpose line and front-matter description now name the operations layer; a new "Working With the Operations Layer" section operationalizes the Runs-on clauses (work at operation level when the mode name is insufficient, name the operation to make a critique checkable, switch to discipline level when drifting); a new "Named-Error Checks" section carries the sender-side bias signatures, the receiver-side fallacy forms, the both-paths به غلط rule, and the grow-per-project-not-from-generic-catalogs guidance — the named-error catalog work the body assigns to the practice layer.
  - thinking.handoff.md: Done — settled items left the handoff per its open-state-only rule (the mode-concept question, resolved by the operations layer, and the definition-naming record among them); the intra-system question was re-scoped with the biases/fallacies vocabulary; the TizFekri vocabulary survey item and the Runs-on reader test were added.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (the named-errors proposal with the به غلط dual framing; the thinking-as-process redefinition; the practice redesign in-session; Runs-on for all modes), argued (the layer vocabulary), decided (approve the rebuild with the three extensions)
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, verified sources (all eight primary works verified from the local copies this round)

#### What changed
- **Definition rewritten:** thinking is *the process* of a cognitive system manipulating representations toward some end — with *process* carrying its defined Memar meaning ([Process → Definition](./process.md#definition)) — and thinking positioned as one of a cognitive system's processes, the thinker/thinking relationship named as the System/Process relationship. A new boundary clarification records that thinking characteristically recruits the system's learning process: as a process open to feedback, an episode of thinking typically leaves the cognitive system changed (synaptic change, updated weights, a written note), so a thinker's artifacts are simultaneously outputs, consumed inputs, and possible learning-retained representations.
- **New topic — Elementary Operations and Awareness Disciplines:** nine elementary operations (comparison, mapping, decomposition, generation, instantiation, ordering, criterion application, discrepancy noticing, commitment), a four-member disciplines class (awareness of assumptions, of goal, of the medium, of self), and the modes-as-combinations statement — a mode is a stable combination of operations governed by disciplines; overlaps become predicted (shared operations) rather than tolerated. Instantiation resolves the abstract/concrete cycle from beneath (the two modes are the two directions of one operation's use); reflective thinking resolves as re-targeting the same operations onto the thinker's own material under awareness of self. The strategy/disposition/phase alternatives from the handoff's open question are dissolved: a strategy is a chosen sequence over operations, a disposition a tendency to exercise a mode, a phase a stage of a process emphasizing some operations.
- **Runs-on clauses:** every mode entry in the list now states which operations it runs on and under which disciplines — all fourteen modes, per the owner's ruling that leaving any mode without its clause would preserve exactly the ambiguity the rebuild exists to remove.
- **New topic — Named Errors: Biases and Fallacies:** the two classes of named error as the negative space of the layers above — cognitive biases (به غلط افتادن, falling into error oneself: the named failure modes of the operations layer, guarded by the awareness disciplines) and fallacies (به غلط انداختن, leading another into error: the named failure modes of the inter-system side of the conversation model), with the boundary between them recorded as real but porous (one act can be a bias in the speaker and a fallacy in the exchange; both corrupt regardless of intent), the sender-awareness axis inside the fallacy class named in Persian as سفسطه (sophistry — fallacy deployed knowingly; the axis changes the sender's responsibility, not the corruption's kind), and the enumeration of individual errors assigned to the practice layer, not the body.
- **Abstract and Modes-intro sentences:** the Abstract now names the operations/disciplines layer and the two named-error classes; the Modes topic's introduction points readers to the Runs-on clauses; the Grouping Notes gained the a-mode's-name-is-not-its-definition sentence.
- The predecessor entry's Gick & Holyoak citation qualifier ("quantitative pattern not independently re-verified") is discharged by this entry's primary-source verification.

#### Deliberation
- The owner asked why, after all the research, the primitives had landed only in the handoff; the honest answer recorded: the split followed his own apply-the-set/primitives-ride-the-upgrade-session decision and the confirm-before-large-scope-changes norm, but the primary-source pass that would have justified starting the rebuild was blocked on sources he then supplied — all eight works, downloaded to `chats-context/thinking/` — after which he converted this session into the rebuild session (Omid Hekayati — argued, decided).
- Every Evidence citation was re-verified against the local primary texts this round, replacing the secondary-source links where the primary copy exists; the two gaps the secondary round left open — Gick & Holyoak's quantitative pattern and Facione's dispositions attribution — both closed at primary source (Super Z — verified).
- The thinking-as-process redefinition was proposed by the owner as a consequence of the named-errors framing: with errors defined, thinking can be seen as a system's process — and he noted the learning coupling as a likely designed-in characteristic of cognitive systems generally, offering an AI agent's mid-reasoning memory construction as the instance. The redefinition conforms the reused term *process* to its governing definition ([Process](./process.md)) and records the coupling as an observed characteristic, not a designed requirement (Omid Hekayati — claimed; Super Z — drafted).
- The named-errors proposal arrived with the owner's dual framing — both Persian definitions built on به غلط, marking that both classes derail the path of thinking and of dialogue alike — and with his own reservation that the errors might not sit at the same rank as the awareness disciplines; the reservation was sustained: errors are not disciplines but the negative space of both layers, a third content class, with the intra-system/inter-system split mapping onto the conversation model's two sides (Omid Hekayati — claimed, argued).
- The owner then asked whether the error classes are really only two — noting that Persian reserves سفسطه for fallacy *committed on purpose*. The question was tested against the layer's own partition and resolved inside the fallacy class: the classes are partitioned by where the corruption occurs (the thinker's own operations versus material in transit), and the sender's awareness is an axis *within* the inter-system class — سفسطه names its knowing end, مغالطه remains the class name for the corrupted pattern itself — because the corruption travels identically whether willed or fallen into; the axis changes the sender's responsibility, not the corruption's kind (Omid Hekayati — argued; Super Z — argued, drafted).
- The practice redesign was ruled into this session — the owner judged that with the rebuilt document in context, deciding what the practice must change is this session's work, not the separate upgrade session's (Omid Hekayati — decided).
- The layer's name: "principles" was considered and set aside — the word carries normative-statement weight elsewhere in this repository; the topic landed as Elementary Operations and Awareness Disciplines (Omid Hekayati — argued; Super Z — drafted).
- The TizFekri institute's practice vocabulary — پرورش مهارت‌های اجرایی, پرسشگری/استدلال‌ورزی/تصمیم‌گیری نقادانه, رایج‌ترین مغالطه‌های محاوره‌ای, دلیل آوردن و نقد دلایل — was recorded as live field evidence that practice-facing education renames the named modes toward functions and folds fallacies into the practice layer; the educator behind the پرسشگری سنجش‌گرایانه renaming recorded in the 2026-09-14 Convergent entry is Dr. Hamed Safaeipour, head of TizFekri (tizfekri.com), named here per the owner's identification; a vocabulary-survey item rides the handoff (Omid Hekayati — argued).

#### Considered and not done
- **Define thinking as an activity of the system rather than a process (rejected):** the owner's redefinition direction — with the named-errors and learning-coupling framings in place, the process reading is both the more precise Memar-native statement and the one [Process](./process.md)'s feedback and System/Process topics directly support; "activity" carried no defined meaning.
- **Add biases and fallacies as awareness disciplines or as modes (rejected):** a discipline governs how operations run; an error is a way an operation or an exchange fails — different rank, recorded as the negative space of both layers instead. The owner's own reservation that the errors might not sit at the disciplines' rank was the seed of this resolution.
- **A third error class for سفسطه (rejected):** the classes are partitioned by where the corruption occurs, and sophistry does not name a third place — it names the knowing end of the awareness axis inside the fallacy class. A third class would partition on two different criteria at once (locus and intent), which the classification principles warn against.
- **Partition the fallacy class by intent into مغالطه/سفسطه subclasses (considered, not chosen):** the axis is real and Persian names it, but a subclass split would suggest the corruption differs by intent when it does not — the same corrupted pattern travels either way; the body therefore records the axis and its name without subclassing.
- **Enumerate individual biases and fallacies in the body (rejected):** catalog work, not concept work — the body records the two kinds and their homes; the per-project catalog grows in the practice layer from observed errors, never imported wholesale from a generic catalog.
- **Record the learning coupling as a designed requirement of cognitive systems (considered, not chosen):** the owner proposed it as a probable designed-in characteristic ("احتمالا … طراحی شده"); the body records it as an observed characteristic of thinking in cognitive systems, pending evidence that would justify the stronger claim.
- **Runs-on clauses for load-bearing modes only (rejected by the owner):** a partial application would leave the non-load-bearing modes' ambiguity unresolved and force every reader to reconstruct the missing combinations — the clause is applied to all fourteen modes.

#### Related work
- The componential tradition in the psychology of intelligence is the direct scientific antecedent of the operations layer: Sternberg's metacomponents and performance components (the executive tier and the operational tier; the analogical set naming mapping), Guilford's Structure of Intellect operations dimension (convergent production defined as deducing the unique answer; evaluation defined as comparison under logical criteria), and Miyake et al.'s latent-variable separation of executive functions. The skills/dispositions two-dimension consensus (Facione's Delphi panel) is the field-side form of the operations/disciplines distinction. Gentner's structure-mapping theory supplies the mapping operation's scientific base, and the Gick–Holyoak transfer experiments supply the analogical mode's prospective-search extension with verified numbers. Moseley et al.'s 35-framework systematic review is the published form of this round's standing motivation: named-mode vocabularies diverge over recurring functions. The Persian practice vocabulary of the TizFekri institute (Dr. Hamed Safaeipour) independently renames named modes toward functions and treats مغالطه‌ها as practice-layer content — converging field evidence from the owner's identified source.
---

### Renamed from Thinking to Cognition and restructured around the cognition frame
- Time: 2026-09-15T10:05:00Z
- Type: Changed
- Cited:
  - [Cognition](https://en.wikipedia.org/wiki/Cognition) — Evidence: the scientific layer's own account of the concept this document is renamed for: "Cognition encompasses mental processes that deal with knowledge. It includes psychological activities that acquire, store, retrieve, transform, or apply information," categorized by function into perception, attention, memory, and thinking — "psychological activities in which concepts, ideas, and mental representations are considered and manipulated" — the layer itself names thinking as one member of a cognitive family, which is the frame structure this entry adds; the document's working definition follows this usage per the scientific-terms policy.
- Propagates to:
  - `docs/framework.md`, `docs/knowledge.md`, `docs/knowledge.practice.md`, `docs/documentation-handoff.md`, `docs/documentation-explanation.practice.md`, `.agents/skills/memar/SKILL.md`: Done — live references retargeted to the cognition paths and the retitled conversation-model anchor. Historical changelog prose mentioning `thinking.md` is left untouched as provenance.
  - `README.md`: Done in the working tree only — the purpose-chain link is retargeted, but the file carries the plugin-distribution round's uncommitted changes and was deliberately excluded from this commit's staging set per the commit-scope rule; the edit rides that round's staging.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (the rename question), decided (cognition; restructure in this session; references repointed last; history preserved by committing the rebuild before the rename)
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, repointed, verified sources

#### What changed
- **New opening topic, What Cognition Is:** cognition defined as the activity of a cognitive system — a system whose internal states stand for aspects of its world and whose behavior is mediated by those states — with *thinker* introduced as shorthand for a cognitive system engaged in thinking, the System/Process relationship stated as the frame's first structural fact, and the family of coupled cognitive processes named: perception, attention, memory, learning, thinking — thinking declared this document's center, the others named so later work finds its home under this concept rather than inside thinking's topics.
- **What Thinking Is narrowed to thinking:** the definition keeps its process sense, now reading one layer below the frame; the thinker-is-a-system clarification and the scientific-terminology sentence moved to the cognition topic, where both were always about; the content-store bullet's "activity" wording follows the definition to "process"; the boundary-clarification count ("Three"), which the rebuild had left stale at four bullets, is accurate again once the relocated bullet joins the frame above.
- **The conversation model recast at its true level:** its participants are cognitive systems throughout — the topic title, the model paragraph, the asymmetry-in-implementation/symmetry-in-role consequence, the norms' derivability sentence, the definitions norm's failure tag, and the norms' closing ownership boundary — while what travels between them stays *thinking material*: the rename widens the frame, it does not relabel the cargo.
- **The 4E extended claim** now says external artifacts are part of the cognitive system, which is where a framing about embodied, embedded, enacted, and extended cognition was always pointing.
- **Abstract, Motivation, and Methodology reframed:** the foundational concept named is cognition with thinking at its center; the growth-path sentence attaches rules to cognition while crediting thinking as the exercised process; the first modeling move reads "two cognitive systems."
- **Family retargeted:** Title and H1 to Cognition; companion headers (`# Cognition Changelog`, `# Cognition Handoff`, `# Cognition Practice`), the practice's front-matter name and purpose line, the handoff's reference lines, and every internal link to `cognition.md` with its anchors (the conversation-model anchor retitled accordingly); the handoff gains an open question on whether the other cognitive processes earn their own treatment.
- The rename itself shipped as the immediately preceding pure-rename commit (git `b7e65f3`, four files, zero content change), so file history survives both moves — the sequencing was the owner's ruling: commit the rebuild, rename in isolation, then restructure content and repoint references.
- The name verification demanded by the owner's agent→agency warning is recorded under Considered and not done below.

#### Deliberation
- The owner raised the rename question the day after the definition moved: if thinking is one process of a cognitive system alongside perception, learning, and memory, why is the document named for a single member of the family it just opened? He ruled the rename the right remedy and asked once more that the choice not repeat the agent→agency sequence — in which the narrower, more famous name (agent) was adopted first and only later gave way to the encompassing one (agency) (Omid Hekayati — claimed, decided).
- The verification came out before execution, on four counts. The stem *cognit-* already carries the document's load-bearing terms — cognitive system, cognitive biases, cognitive science — sixteen uses without ownership; the scientific layer's standard account defines cognition as exactly the process family the frame now names, with thinking as one member (cited above); the 4E topic is a framing of cognition housed under a thinking title; and the precedent's shape is exact — agency is named for the capacity, not the actor, and the same inversion is live here. Cognition wins on all four together (Super Z — argued).
- "Cognition" was checked against the neighbor's subject: the document names the family but models only thinking — perception, attention, memory, and learning stay pointers, not content — so the wider title does not annex their governance; [System](./system.md) and [Knowledge](./knowledge.md) keep their homes.
- The owner's sequencing ruling — rebuild commit, then pure rename commit, then content restructure with the repoints — was adopted so the rename is never buried inside content changes, mirroring the relocation-first practice already recorded in this repository's history (Omid Hekayati — decided; executed as three commits).
- The practice companion's purpose line was reworded to "the thinking modes of Cognition" rather than relabeling the modes as cognition's — the modes, operations, disciplines, and errors are thinking's content; the rename widens the frame, not the list of topics (Super Z — drafted).
- The historical references were separated from the live ones before repointing: only live links and cross-document sentences move; every historical changelog mention of `thinking.md`, including inside this document's own changelog, stays as provenance of what was written when (Super Z — applied; Omid Hekayati — directed the last-stage sequencing).
- The README retarget was applied to the working tree but held out of the commit: the file already carries the plugin round's uncommitted changes, and committing it here would smuggle that round's work into this one's scope.

#### Considered and not done
- **Keep the name `thinking.md` and define cognition inside it (rejected):** it would place the governing concept under the file of one of its members — the exact governance inversion the agent→agency rename corrected, where AI Agent was one manifestation of Agency, not its definition; and the sixteen stem-uses would keep pointing from the narrower file at the wider subject.
- **`cognitive-system.md` (considered, not chosen):** names the entity rather than the activity, but the document's content is cognition's structure and the exchanges between thinking systems; entityhood itself is governed by [System](./system.md), and the title should not quietly annex a neighbor's concept.
- **`mind.md` (rejected):** carries philosophical and colloquial weight — the hard problem, mind–body, "theory of mind" — that this document neither inherits nor needs; the scientific layer it grounds itself in names its subject cognition, and the scientific-terms policy follows that layer.
- **Splitting into `cognition.md` and a narrower `thinking.md` (considered, not chosen):** the document is one model with one derivation line — frame, modes, operations, disciplines, errors, conversation, norms — and a split would duplicate the frame to serve a title. A process in the named family may later earn its own document under the project's progressive-migration pattern; the handoff carries that question.
- **Relabeling the modes as "modes of cognition" (rejected):** the modes manipulate representations toward ends, which is this document's definition of *thinking*; attention and memory are not modes in this sense, and broadening the label would re-open exactly the misrouting the rename exists to close.

#### Related work
- The agent→agency rename is the repository's precedent and its citation here is by shape, not subject: a document named for the narrower, more famous member gets retired for the encompassing concept once the encompassing concept is the one doing the governing. This document reached the same posture the week its own definition introduced it: thinking defined as one process of a cognitive system.
- The scientific standard accounts of cognition — the process family of perception, attention, memory, learning, and thinking — are the structure the new opening topic states at working-definition level and cites above; they are a frame for this document, not a claim that this document models the family.
- The TizFekri practice vocabulary — cultivable thinking skills, "اندیشیدن آموختنی است", the نقادانه triad of questioning, reasoning, and decision — names a teachability claim about thinking specifically, one member of this family; mapping it against this document's modes stays the separate open item recorded in the handoff.

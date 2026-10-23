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
- The 4E-grounding topic's reference was retargeted from `knowledge-management.md` to [Knowledge](../modules/knowledge/knowledge.md) after that document was renamed and re-scoped to the concept.
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
- The norm was distilled from a working chat's observed failure: a reviewer raised a criticism against one concrete instance (a tool name in one section) and the receiving agent repaired only that instance, then needed the same criticism repeated for a second instance before generalizing (Omid Hekayati).
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
- **Model conversation as protocol-governed process (considered, not chosen; migrated from the conversation-model topic's retired `Rationale and alternatives`)**: Memar does define Process and Protocol formally ([Process](../modules/process/process.md), [Protocol](./protocol.md)), and a conversation does satisfy them. But treating the protocol layer as the primary frame would foreground turn-taking and format — the aspects least specific to thinking — while the norms that matter concern how claims are evaluated, which the protocol frame does not address. The thinking-systems frame is the one the norms actually follow from.
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
- The norm was distilled from a working chat's observed failure: an agent had recorded that "ecosystem" carried no Memar definition, and in a later chat began a document-set-wide treatment of the word without presenting the plan first — the ambiguity rule was loaded but not applied at change scale (Omid Hekayati — argued).
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
- The round's second outcome — the owner's proposal for a primitives layer under the modes — is recorded as the target architecture for this document's already-scheduled upgrade session; the reasoning and its scientific support live in the paired [handoff](./cognition.handoff.md), keeping this entry to the change that actually landed.
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
  - Sternberg, R. J. (1985). *Beyond IQ: A Triarchic Theory of Human Intelligence* — Evidence: the two-tier structure the operations/disciplines layer continues — "I have identified seven metacomponents" (executive processes: deciding the problem, selecting lower-order components, selecting a representation, selecting a strategy) over performance components, with the analogical-reasoning set enumerated as "encoding and response components … and inference, mapping, application, comparison, and justification components"; mapping defined as forming the higher-order relation between the two halves of an analogy. The document's mapping operation and awareness-disciplines class are the Memar-form counterparts; no component name was imported.
  - Guilford, J. P. (1967). *The Nature of Human Intelligence* — Evidence: convergent production "is in the area of logical deductions … the prevailing function when the input information is sufficient to determine a unique answer" (the convergent mode's entry, verified at primary source this round); and "evaluation is defined as a process of comparing a product of information with known information according to logical criteria" — comparison under criteria is Guilford's own definition of evaluation, grounding the criterion-application operation.
  - Gick, M. L., & Holyoak, K. J. (1980). "Analogical Problem Solving." *Cognitive Psychology*, 12 — Evidence (primary-source numbers, closing this entry's predecessor's open qualifier): spontaneous transfer of a memorized analogous story, without a hint, occurred for 43% of subjects (20% with distractor stories in recall) versus 76% eventually succeeding once a hint was given; Duncker's own subjects produced the dispersion solution 2 of 42 times. The warrant for the analogical mode's closing contrast — deliberate search outperforms waiting to notice — now rests on verified numbers.
  - Miyake, A., Friedman, N. P., Emerson, M. J., Witzki, A. H., Howerter, A., & Wager, T. D. (2000). "The unity and diversity of executive functions." *Cognitive Psychology*, 41 — Evidence: the latent-variable decomposition into Shifting, Updating, and Inhibition under a common unity factor — the control layer itself decomposes into separable elementary functions, which is the operations layer's claim about thinking's control side.
  - Facione, P. (1990). *Critical Thinking: A Statement of Expert Consensus for Purposes of Educational Assessment and Instruction* (the APA Delphi Report) — Evidence (primary source, closing the predecessor's partial verification): the panel's conceptualization "in terms of two dimensions: cognitive skills and affective dispositions"; a 61% majority held the dispositions part of critical thinking's very meaning; Table 5's dispositions carry 83% consensus. The skills/dispositions distinction is the field-side counterpart of the operations/disciplines two-kind layer.
  - Moseley, D., Elliott, J., Gregson, G., Higgins, S., Miller, N., & Newton, D. (2005). "Thinking skills frameworks for use in education and training." *British Educational Research Journal*, 31(8) — Evidence: the systematic review evaluated 35 frameworks (55 identified), organized by "identifying common features as well as differences between frameworks" — the field's vocabularies diverge over recurring functions, the published form of the mode-names-mislead motivation.
  - Gentner, D. (1983). "Structure-Mapping: A Theoretical Framework for Analogy." *Cognitive Science*, 7 — Evidence: analogy's interpretation as implicit rules mapping knowledge about a base domain into a target, over relations rather than surface attributes — the structure-mapping tradition the mapping operation continues.
- Propagates to:
  - thinking.practice.md: Done — reshaped in the same chat (the owner ruled the practice redesign belongs here, not in the separate upgrade session): the purpose line and front-matter description now name the operations layer; a new "Working With the Operations Layer" section operationalizes the Runs-on clauses (work at operation level when the mode name is insufficient, name the operation to make a critique checkable, switch to discipline level when drifting); a new "Named-Error Checks" section carries the sender-side bias signatures, the receiver-side fallacy forms, the both-paths به غلط rule, and the grow-per-project-not-from-generic-catalogs guidance — the named-error catalog work the body assigns to the practice layer.
  - thinking.handoff.md: Done — settled items left the handoff per its open-state-only rule (the mode-concept question, resolved by the operations layer, and the definition-naming record among them); the intra-system question was re-scoped with the biases/fallacies vocabulary; the TizFekri vocabulary survey item and the Runs-on reader test were added.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (the named-errors proposal with the به غلط dual framing; the thinking-as-process redefinition; the practice redesign in-chat; Runs-on for all modes), argued (the layer vocabulary), decided (approve the rebuild with the three extensions)
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, verified sources (all eight primary works verified from the local copies this round)

#### What changed
- **Definition rewritten:** thinking is *the process* of a cognitive system manipulating representations toward some end — with *process* carrying its defined Memar meaning ([Process → Definition](../modules/process/process.md#definition)) — and thinking positioned as one of a cognitive system's processes, the thinker/thinking relationship named as the System/Process relationship. A new boundary clarification records that thinking characteristically recruits the system's learning process: as a process open to feedback, an episode of thinking typically leaves the cognitive system changed (synaptic change, updated weights, a written note), so a thinker's artifacts are simultaneously outputs, consumed inputs, and possible learning-retained representations.
- **New topic — Elementary Operations and Awareness Disciplines:** nine elementary operations (comparison, mapping, decomposition, generation, instantiation, ordering, criterion application, discrepancy noticing, commitment), a four-member disciplines class (awareness of assumptions, of goal, of the medium, of self), and the modes-as-combinations statement — a mode is a stable combination of operations governed by disciplines; overlaps become predicted (shared operations) rather than tolerated. Instantiation resolves the abstract/concrete cycle from beneath (the two modes are the two directions of one operation's use); reflective thinking resolves as re-targeting the same operations onto the thinker's own material under awareness of self. The strategy/disposition/phase alternatives from the handoff's open question are dissolved: a strategy is a chosen sequence over operations, a disposition a tendency to exercise a mode, a phase a stage of a process emphasizing some operations.
- **Runs-on clauses:** every mode entry in the list now states which operations it runs on and under which disciplines — all fourteen modes, per the owner's ruling that leaving any mode without its clause would preserve exactly the ambiguity the rebuild exists to remove.
- **New topic — Named Errors: Biases and Fallacies:** the two classes of named error as the negative space of the layers above — cognitive biases (به غلط افتادن, falling into error oneself: the named failure modes of the operations layer, guarded by the awareness disciplines) and fallacies (به غلط انداختن, leading another into error: the named failure modes of the inter-system side of the conversation model), with the boundary between them recorded as real but porous (one act can be a bias in the speaker and a fallacy in the exchange; both corrupt regardless of intent), the sender-awareness axis inside the fallacy class named in Persian as سفسطه (sophistry — fallacy deployed knowingly; the axis changes the sender's responsibility, not the corruption's kind), and the enumeration of individual errors assigned to the practice layer, not the body.
- **Abstract and Modes-intro sentences:** the Abstract now names the operations/disciplines layer and the two named-error classes; the Modes topic's introduction points readers to the Runs-on clauses; the Grouping Notes gained the a-mode's-name-is-not-its-definition sentence.
- The predecessor entry's Gick & Holyoak citation qualifier ("quantitative pattern not independently re-verified") is discharged by this entry's primary-source verification.

#### Deliberation
- The owner asked why, after all the research, the primitives had landed only in the handoff; the honest answer recorded: the split followed his own apply-the-set/primitives-ride-the-upgrade-session decision and the confirm-before-large-scope-changes norm, but the primary-source pass that would have justified starting the rebuild was blocked on sources he then supplied — all eight works, downloaded by the owner and read from that copy — after which he converted this chat into the rebuild session (Omid Hekayati — argued, decided).
- Every Evidence citation was re-verified against the local primary texts this round, replacing the secondary-source links where the primary copy exists; the two gaps the secondary round left open — Gick & Holyoak's quantitative pattern and Facione's dispositions attribution — both closed at primary source (Super Z — verified).
- The thinking-as-process redefinition was proposed by the owner as a consequence of the named-errors framing: with errors defined, thinking can be seen as a system's process — and he noted the learning coupling as a likely designed-in characteristic of cognitive systems generally, offering an AI agent's mid-reasoning memory construction as the instance. The redefinition conforms the reused term *process* to its governing definition ([Process](../modules/process/process.md)) and records the coupling as an observed characteristic, not a designed requirement (Omid Hekayati — claimed; Super Z — drafted).
- The named-errors proposal arrived with the owner's dual framing — both Persian definitions built on به غلط, marking that both classes derail the path of thinking and of dialogue alike — and with his own reservation that the errors might not sit at the same rank as the awareness disciplines; the reservation was sustained: errors are not disciplines but the negative space of both layers, a third content class, with the intra-system/inter-system split mapping onto the conversation model's two sides (Omid Hekayati — claimed, argued).
- The owner then asked whether the error classes are really only two — noting that Persian reserves سفسطه for fallacy *committed on purpose*. The question was tested against the layer's own partition and resolved inside the fallacy class: the classes are partitioned by where the corruption occurs (the thinker's own operations versus material in transit), and the sender's awareness is an axis *within* the inter-system class — سفسطه names its knowing end, مغالطه remains the class name for the corrupted pattern itself — because the corruption travels identically whether willed or fallen into; the axis changes the sender's responsibility, not the corruption's kind (Omid Hekayati — argued; Super Z — argued, drafted).
- The practice redesign was ruled into this chat — the owner judged that with the rebuilt document in context, deciding what the practice must change is this chat's work, not the separate upgrade session's (Omid Hekayati — decided).
- The layer's name: "principles" was considered and set aside — the word carries normative-statement weight elsewhere in this repository; the topic landed as Elementary Operations and Awareness Disciplines (Omid Hekayati — argued; Super Z — drafted).
- The TizFekri institute's practice vocabulary — پرورش مهارت‌های اجرایی, پرسشگری/استدلال‌ورزی/تصمیم‌گیری نقادانه, رایج‌ترین مغالطه‌های محاوره‌ای, دلیل آوردن و نقد دلایل — was recorded as live field evidence that practice-facing education renames the named modes toward functions and folds fallacies into the practice layer; the educator behind the پرسشگری سنجش‌گرایانه renaming recorded in the 2026-09-14 Convergent entry is Dr. Hamed Safaeipour, head of TizFekri (tizfekri.com), named here per the owner's identification; a vocabulary-survey item rides the handoff (Omid Hekayati — argued).

#### Considered and not done
- **Define thinking as an activity of the system rather than a process (rejected):** the owner's redefinition direction — with the named-errors and learning-coupling framings in place, the process reading is both the more precise Memar-native statement and the one [Process](../modules/process/process.md)'s feedback and System/Process topics directly support; "activity" carried no defined meaning.
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (the rename question), decided (cognition; restructure in this chat; references repointed last; history preserved by committing the rebuild before the rename)
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
- "Cognition" was checked against the neighbor's subject: the document names the family but models only thinking — perception, attention, memory, and learning stay pointers, not content — so the wider title does not annex their governance; [System](./system.md) and [Knowledge](../modules/knowledge/knowledge.md) keep their homes.
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

---

### Error-reduction upgrade: sharpened norms, asymmetry obligations, multi-system consultation
- Time: 2026-09-15T13:45:00Z
- Type: Changed
- Propagates to:
  - `cognition.practice.md`: Done — Norm Application Points section added; operations use-threshold restated; named-error checks gained source-deference and structural-fallacy wording; critique procedure gained reported/inferred/confirmed provenance; proportional-strength table tied to inspectable material and the no-silence reverse guard.
  - `cognition.handoff.md`: Done — duplicate functional-groups entry removed; conflation question settled with the sharper seam; open questions updated for what this upgrade closed and left open; anticipated-work duplicates collapsed.
  - `.agents/skills/memar/SKILL.md`: Done — stale "Thinking's" intake pointers retargeted to "Cognition's" only; no new skill rules added (norms stay in this document).
  - `.agents/.codex-plugin/plugin.json`: Done — "read Thinking" retargeted to "read Cognition".
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed (consult-other-cognitive-systems; skill needs no new rules), decided (apply the multi-model set plus the consultation norm; keep norms in the base)
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5 via [Cursor](../CONTRIBUTORS.md#cursor)) — claimed, argued (independent critique package)
  - [ChatGPT](../CONTRIBUTORS.md#chatgpt) (GPT-5.6-terra via [Cursor](../CONTRIBUTORS.md#cursor)) — claimed, argued (independent critique package)
  - [Composer](../CONTRIBUTORS.md#composer) (Composer via [Cursor](../CONTRIBUTORS.md#cursor)) — rewrote

#### What changed
- **Abstract and Methodology wording:** the over-strong "derivable from a model of cognition itself" claim was narrowed to grounding chiefly in the conversation model, with honesty that not every norm is a pure derivation from that model alone (ChatGPT claimed the overreach; Claude claimed the live seam is conversation-plus-norms vs modes/operations reference layer).
- **Status and Use:** Draft + always-loaded tension resolved — norms are current working constraints, provisional not optional; specialized documents outrank on their domains; contradictions are reported through the changelog (ChatGPT claimed).
- **Learning coupling qualified:** producing or storing an artifact is not itself learning; do not read artifacts as proof of retention or weight update (ChatGPT claimed).
- **Modes use threshold:** begin from the material's missing operation, not mode-label matching (ChatGPT claimed; Claude claimed modes layer is inert at decision time).
- **4E extended boundaries:** collaboration-extended vs private retention; artifact participation ≠ automatic membership in one thinker's boundary (ChatGPT claimed).
- **Conversation model — symmetry qualified:** reciprocal epistemic standing for claim evaluation; not interchangeable authority, responsibility, or decision rights (ChatGPT claimed).
- **New topic — What Implementation Asymmetry Obliges:** no self-citation as established fact; declare unverified reading and context limits; externalize session state into shared artifacts (Claude claimed).
- **Discourse norms sharpened or added:**
  - Evaluate on merits — source as neither authority nor disqualifier; source may be defeasible context (ChatGPT claimed).
  - Definitions — verify load-bearing terms before building on them (Claude claimed).
  - Conceptual-root — reported / inferred / confirmed provenance; no receiver-manufactured scope attributed to the giver (ChatGPT claimed; Claude reinforced).
  - Proportional criticism — inspectable-material strength; reverse guard against critique-suppression (Claude claimed the suppression failure; ChatGPT claimed inspectable strength).
  - **Report absence rather than supplying it** (Claude claimed).
  - **Treat shared artifacts as claims, not absolute authority** (Claude claimed).
  - **Consult other cognitive systems when conceptual depth warrants it** — AI-to-other-models or human-to-human review meeting; generative+evaluative; merits still govern; depth and availability jointly trigger (Omid Hekayati claimed; form generalized beyond AI).
  - Prefer long-term clarity — explicit speed request does not cancel large-scope confirmation or definitional verification (Claude claimed the collision with Confirm).
  - **Precedence when norms collide** — intake Ask/Confirm first; then definitions/absence; then evaluation norms; then long-term clarity (Claude claimed).
  - Norms bind at intake, stated in the norms topic (Claude claimed the missing application-point problem).
- **Named errors:** source-deference / agreement pressure added as a bias with this project's own mirroring-draft instance (Claude claimed); fallacy redefined as defective inferential support whether solitary or exchanged (ChatGPT claimed).
- Practice and propagation as listed under Propagates to.

#### Deliberation
- Independent critiques were solicited from Claude (Opus-5) and ChatGPT (GPT-5.6-terra) before drafting, as a live exercise of what became the consultation norm (Omid Hekayati — directed the review; Cursor/Composer — ran both).
- Claude claimed the document's headline derivation overreaches because norms follow from the conversation model, not from the modes/operations taxonomy; ChatGPT claimed several norms (confirm-large-scope, prefer-clarity) are change-governance or framework values, not pure conversation-model derivations — the body now states both honestly rather than forcing a single derivation story (Claude, ChatGPT — claimed; Cursor/Composer — drafted).
- Omid Hekayati claimed the multi-system consultation obligation, insisted it is not AI-only (a human convening other humans is the same norm), asked whether the skill needed new text, and decided it does not — Cognition remains the single home; skill only keeps intake pointers (Omid Hekayati — claimed, decided).
- Applying the fuller set of High and Medium proposals from both critiques, not only the first shortlist, was directed (Omid Hekayati — decided).
- Moving norms out of the base into practice was rejected by both critiques and by the owner — derivation and single home stay; practice gains application checkpoints only (Claude, ChatGPT — argued; Omid Hekayati — decided).

#### Considered and not done
- **Rewrite the memar skill with duplicated norm text (rejected by the owner):** would recreate the second-home drift the document exists to prevent; intake pointers already present, only retargeted from Thinking to Cognition.
- **Re-scope cognition.practice.md from critique-first to a full per-norm compliance manual now (deferred):** Norm Application Points close the immediate gap; a full re-scope waits until critique procedures outgrow the file (Claude claimed the re-scope; not forced this round).
- **Graduate modes/operations out of the always-loaded base now (deferred):** Claude claimed zero normative loss if they graduate; kept here pending the Runs-on reader test (handoff).
- **Add inductive/deductive/probabilistic modes or operationalize embodied/enacted (rejected both critiques):** no demonstrated dependence; growth rule holds.
- **Formalize conversation as Protocol now (rejected both critiques):** no demonstrated failure from its absence.
- **Enumerate a bias/fallacy catalogue in the body (rejected):** only source-deference earned a named mention by a recorded project instance; further enumeration stays practice-layer and per-project.
- **Regroup discourse norms by mode for navigation (deferred):** precedence addresses collision; mode-grouped navigation remains an open readability question (handoff).

---

### Working representation separated from medium language
- Time: 2026-09-19T15:26:00Z
- Type: Added
- Propagates to:
  - `cognition.practice.md`: Done — intake checkpoint for medium-language vs working-representation separation.
  - `.agents/skills/memar/SKILL.md`: Rejected — Cognition remains the single home; skill already directs workers to load this document before reasoning-heavy work; no duplicated rule text.
  - `documentation.md`: Rejected — Documentation Language already separates the durable English record from conversation; this change links to that rule rather than restating it.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Composer](../CONTRIBUTORS.md#composer) (via [Cursor](../CONTRIBUTORS.md#cursor)) — argued, rewrote

#### What changed
- **Abstract claim (1)** now states that the medium's language is not identical with the representation in which a cognitive system does its best thinking.
- **Awareness of the medium** names collapsing medium language into working representation as a medium-shaped failure of that discipline.
- **Conversation model** records that natural-language media invite matching the medium language for internal operations even when it is not the system's strongest working representation.
- **What Implementation Asymmetry Obliges** gains: operate in the system's strongest working representation; return through the medium in a form the counterpart can use — receive, transform, ask on translation ambiguity, return counterpart-usable (conversation language for replies; project documentation language for durable records).
- Practice intake checkpoint added under Norm Application Points.

#### Deliberation
- The owner observed that addressing the agent in Persian pulled the model's thinking into Persian and degraded depth, and that other agents (e.g. OpenCode, GLM) that translate into a stronger working language then report back in the user's language produce markedly better output (Omid Hekayati — claimed).
- The same chat re-demonstrated the failure after the prescription was already stated: a reply that accepted the diagnosis still reasoned in Persian — evidence the failure is sticky enough to earn a standing obligation, not a one-off tip (Omid Hekayati — claimed).
- Framing as AI etiquette ("always think in English") was rejected in favor of the general form: each cognitive system operates in its strongest working representation and returns through the medium in counterpart-usable form (Composer — argued; Omid Hekayati — decided the full plan: awareness extension, asymmetry obligation, practice checkpoint, changelog, abstract).
- Output policy chosen: think in the stronger representation; write the conversational report in the user's language; keep durable documentation in English per the existing Documentation Language rule (Omid Hekayati — approved; Composer — recommended).

#### Considered and not done
- **Hard-code "always think in English" as the rule (rejected):** would name one current implementation's strength as the concept; the obligation is about strongest working representation, which varies by cognitive system.
- **Add a separate discourse norm in addition to the asymmetry obligation (rejected for this round):** the failure is an implementation-asymmetry obligation under awareness of the medium; a bidirectional evaluation norm would restate without adding checkable content. Practice operationalizes the obligation at intake.
- **Duplicate the rule into the memar skill (rejected):** same second-home drift rejected in the 2026-09-15 upgrade.

---

### A lookup that finds nothing is a fact about the lookup
- Time: 2026-10-04T04:22:01Z
- Type: Changed
- Cited:
  - [Knowledge Research 001](../modules/knowledge/knowledge.research.001.md) — **Reference**: the inquiry whose repeated reporting of an absence as a discovery prompted this. Four occasions in one session, each concluding that a rule did not exist, each later found to be stated already.
- Propagates to:
  - [cognition.practice.md](./cognition.practice.md): Done — the same failure added to [Anti-Patterns](./cognition.practice.md#anti-patterns) as the checklist row a reviewer can catch it with, and a checkpoint added to [Norm Application Points](./cognition.practice.md#norm-application-points) for the case where a lookup matches nothing.
  - [knowledge.practice.md](../modules/knowledge/knowledge.practice.md): Done — one link now names the norm it applies rather than the set, which the section split made possible.
  - [.agents/skills/memar/SKILL.md](../.agents/skills/memar/SKILL.md): Prepared and held back — the tool-dependent half, since what a search returns is bounded by the terms given to it. Deferred to its own commit, where it can link the norm by its own anchor rather than name it in prose. That file carries no changelog of its own.
  - [content.md](../modules/knowledge/content/content.md), [knowledge.md](../modules/knowledge/knowledge.md): None needed — neither change rests on a claim about absence.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — directed, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — drafted

#### What changed
- [Discourse Norms Derived From This Model](./cognition.md#discourse-norms-derived-from-this-model) no longer holds its norms as a list of bolded bullets inside one paragraph. Each norm is a section of its own, named by the norm, so a document that needs one norm can address that norm instead of the whole set. The motivation is visible in this repository rather than argued: [cognition.practice.md → Norm Application Points](./cognition.practice.md#norm-application-points) wrote eight checkpoints that each named a norm and linked the section, because a bullet in a list has no anchor to link to. Two trailing passages that were never norms — the precedence order and the boundaries of what the topic owns — become sections of their own under titles that say so, and the topic's opening now says that they are not norms.
- [Report absence rather than supplying it](./cognition.md#report-absence-rather-than-supplying-it) now distinguishes two things the norm previously ran together: material that is absent from the shared medium, and a lookup that found no match for the terms it was given. The first is a fact about the project; the second is a fact about the query, bounded by the terms searched and the places reached. The silence of a lookup licenses the statement that this query matched nothing and never the statement that the project holds no such rule — the rule may be stated in other words, in another document, or under a name nobody thought to search for.
- The norm now states the procedure the distinction implies: before reporting that something is missing, read the documents that own the subject. A rule that already reaches the case is not a gap, and the cheapest explanation for a rule that appears absent is that the case was never read beside it.
- The failure it prevents is extended past the original one. The norm already named material that looks like support but supports nothing; it now also names an empty result reported as a discovery about the project, and the compounding form — a chain of such reports in which each round takes the previous round's unverified absence as established, which is what turns one missed lookup into a session's worth of wrong findings.

#### Considered and not done
- **A new discourse norm rather than an extension of an existing one**: not taken. [Report absence rather than supplying it](./cognition.md#report-absence-rather-than-supplying-it) already owns the case, and a second norm on the neighbouring subject would split one rule into two that a reader must hold together.
- **Repointing every reference to the set at a single norm**: not taken, and the distinction is which reference means what. A checkpoint that applies one norm now links that norm; a passage about the norms as a body — this record's precedence paragraph, [Knowledge → Write for the Structure of the Subject](../modules/knowledge/knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits)'s reference to Cognition's preference for long-term clarity, [Process → Defect Resolution as an Inquiry](../modules/process/process.md)'s reference to the norms generally — keeps the section, because narrowing it would claim one norm holds the whole of what a general reference holds.
- **Renaming the norms so their anchors read cleanly**: not taken. The names are referenced by name in more than two dozen places across twelve documents, and a mangled anchor is a smaller cost than a renamed concept. Two of the twelve carry punctuation that survives slugging as a double hyphen.
- **A rule requiring a search to be reported with its terms**: partially taken. The norm requires naming what was searched in substance, and the practice's checklist row carries it as the reviewable form; a fixed format for reporting a search was not added, because the requirement is one clause of an existing norm and not a procedure of its own.
- **Rewriting the research record's findings that were produced this way**: not taken. [Knowledge Research 001](../modules/knowledge/knowledge.research.001.md) carries one finding that a primary source later contradicted, that correction is recorded in the record itself, and the remaining findings were each checked against the documents they cite. This entry fixes the method that produced the discarded ones rather than editing the ones that survived.

---

### A deferral budget, and the hard rule separated from the ranking
- Time: 2026-10-04T05:35:11Z
- Type: Changed
- Cited:
  - [Comparison: Memar and GitHub Spec Kit](./comparisons/spec-kit.001.md) - **Reference**: the comparison whose adoption filter produced this change. GitHub Spec Kit's `/specify` bounds its clarification markers at three and orders them by impact; its `/clarify` caps the session at five questions and states a recommendation with its reason. Both were read against this document's norms, and the piece worth taking turned out to be the half the source project does not emphasize.
  - [Framework → Goal-Oriented Frameworks and Purpose Space](./framework.md#goal-oriented-frameworks-and-purpose-space) - **Extends by**: the consistency requirement the project README's new section now answers.
- Propagates to:
  - [cognition.practice.md](./cognition.practice.md): Done - three changes, all recorded here because a practice companion is not an independent artifact whose history stands apart: the deferral checkpoint under Norm Application Points, the hard-rule-versus-ranking paragraph under Quality Standards, and the interactive-reply checkpoint the comparison's Adapt filter produced. A practice companion is not an independent artifact whose history stands apart, so both changes are recorded here rather than in a ledger of their own.
  - [README.md](../README.md): Done - a new section stating where Memar stops and where the work continues, which is the disclosure instance of the consistency requirement this entry's second change concerns. That file carries no changelog of its own.
  - [framework.md](./framework.md): None needed - the consistency requirement already states what the README section answers; the answer is not a new claim about the framework.
  - [.agents/skills/memar/SKILL.md](../.agents/skills/memar/SKILL.md): None needed - the skill's intake rules are stated as pointers into this document and inherit the norm's new shape without naming it.
  - [.agents/scripts/memar-documentation.py](../modules/knowledge/content/content.py), [.agents/scripts/README.md](../.agents/scripts/README.md): None needed - nothing in this change alters a document's written surface, and the check that reports open work is recorded in the [Documentation Changelog](../modules/knowledge/documentation/changelog/changelog.md).
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - directed, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - drafted

#### What changed
- [Ask rather than assume](./cognition.md#ask-rather-than-assume) is now two clauses rather than one, and they govern different things. Asking carries no budget: no cap on the number of questions turns the norm into a licence to proceed on an unstated premise, which is the failure it exists to prevent, and a question whose answer the material already implies is not diligence. Deferral carries one. Where an ambiguity is set aside rather than asked — the answer is not yet reachable, the counterpart is unavailable, the exchange must proceed — that deferral is a fact about the work, and it is recorded where it can be found again: the paired handoff's open questions, each naming the ambiguity it is rather than the topic it sits near, so that a reader six sessions later meets the unresolved question and not the subject it neighbours. The deferred set is ordered, so that what was set aside can be read in the order it will cost: an ambiguity that changes what the work *is* outranks one that changes how a part of it is done, and one that touches a premise the model rests on outranks one that touches a detail.
- The norm's failure clause gains the failure the second half prevents. An unrecorded deferral is the original failure wearing the appearance of having been deliberate, which is the more dangerous form: a reader who finds it cannot tell it from a decision.
- [Cognition Practice → Norm Application Points](./cognition.practice.md#norm-application-points) gains the checkpoint that case needs, stating both that recording a deferral is not resolving it and that a deferral may not be reported as an answer.
- [Cognition Practice → Quality Standards](./cognition.practice.md#quality-standards) gains a paragraph separating the two instruments that a contribution surface tends to blur into one. A firm requirement — a written expectation before the work, a definition verified before it is built on, a proposal confirmed before it is applied — is met or unmet, with no partial credit and no average across dimensions standing in for it. Dimensions to weigh are prioritization: they say what to attend to first, and a proposal that scores well on most and badly on the one that matters is not thereby acceptable. Neither instrument is promoted into the other, and neither is demoted: a dimension is not a threshold because it is measurable, and a threshold is not a dimension because it is inconvenient.
- The project [README](../README.md) gains a section stating where Memar stops: every change whatever its size; the finished delivery of a structure Memar names, which is Enterprise work rather than a limit of coverage; and subjects no Memar document governs, where silence is a claim in neither direction. The framework holds that a development framework's goals must be achievable by its own development processes as well as by the systems developed within it; kept only as a principle, that requirement is kept by nobody, and a maintained statement is what makes it checkable rather than asserted. The section is placed where a reader arrives looking for what the project is for, and it separates two things an earlier draft of it ran together: Memar states the path and every project that follows the documentation arrives at the structure a generated system would have had, while producing that system is what [Enterprise](https://github.com/GeniusesGroup/memar/blob/dc3d1433/README.md#enterprise) sells.

- [Cognition Practice → Norm Application Points](./cognition.practice.md#norm-application-points) gains a checkpoint for the interactive case the asymmetry obligation already covers. When the counterpart must answer and the exchange is interactive, the answer's shape is constrained as well as its content, because narrowing what has to be understood lowers the cost of understanding it, which is the asymmetry the norm is about. The checkpoint states the limit in the same breath: a question that resolves into fixed options has offered a decision the counterpart may not have held, and narrowing a question until one answer survives is the same failure as assuming one by a longer road. Where the options do not cover the answer, that is the finding, and the next question asks for the missing option rather than choosing among the offered ones. It is written as a checkpoint under an existing norm rather than as a norm of its own, which is what keeps it from becoming the funnel it is meant to avoid.

#### Considered and not done
- **A cap on the number of questions (rejected):** it is the shape the source project uses, and it is the opposite of what this norm is for. A ceiling on questions is a licence to assume. The deferral clause is the same discipline applied to the one place a ceiling is safe, and it keeps the norm's force where the failure actually lives.
- **A fixed number of permitted deferrals (rejected):** the same argument one level down. A project under pressure to stay inside a budget of open questions has an incentive to close them by guessing, which is the assumption the norm forbids wearing one more layer.
- **Restating the deferral rule in the Memar skill (rejected):** the same second-home drift rejected in the 2026-09-15 and 2026-10-04 upgrades. The skill routes into this document; it does not carry a copy.
- **Naming the source project in the norm's text (rejected):** the norm states what holds, and a comparative essay is where the comparison lives. A governing document that cited a neighbor for each of its clauses would make the neighbor load-bearing for the rule's meaning.
- **Extending the README section to cover every document set that has not reached `Final` (rejected):** that is a coverage measure, and the section is an answer to a question about the framework's own practice. Where the framework has not settled something, the section says the question is open; where it has settled nothing at all, [Report absence](./cognition.md#report-absence-rather-than-supplying-it) is the norm that applies.

---

### A large change has a second moment, after it exists
- Time: 2026-10-04T00:00:00Z
- Cited:
  - [Practice facet](../modules/knowledge/documentation/practice/practice.md) - Reference: the split this entry follows, where an obligation lives beside the facet and only the runtime-dependent fact stays in the agent's own configuration
- Propagates to:
  - ../.agents/skills/memar/SKILL.md: Done - the clause this norm now carries was removed from the skill's large-scope rule, which had been its only home
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed

#### What changed
- *Confirm before large-scope changes* now states the moment after the change exists: hold the applied result open for the counterpart's review and apply the feedback it carries, and that approval of a plan is not review of its outcome. Its failure-prevented clause gained the second failure alongside the first.
- The clause was removed from the memar skill, which had been its only home, so that the skill points at the norm rather than carrying one of its two halves.

#### Considered and not done
- The second moment was not stated as a separate norm (Space Bunny Alpha - argued). It governs the same act at the same altitude and splitting it would let a session satisfy one half and ignore the other, which is the failure the clause now names.
- The post-application obligation was not extended to the other discourse norms (Space Bunny Alpha - argued). Whether each norm has a second moment is a question this entry does not answer, and answering it for one norm by analogy would be the same over-reach the entry corrects.

---

### Four open questions retired to sections that already answer them
- Time: 2026-10-04T18:18:05Z
- Type: Fixed
- Propagates to:
  - cognition.handoff.md: Done - four open-question entries removed; the answers already stand in `cognition.md` (handoff: no entry of its own).
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, applied

#### What changed
- *Are the four functional groups the right partition?* left the handoff; `Grouping Notes` already holds the answer — the groups are a navigation aid, revised when they stop being useful.
- *The 4E grounding's adoption depth* left the handoff; [Grounding: Cognition and the 4E Framing](./cognition.md#grounding-cognition-and-the-4e-framing) already holds it — the extended claim is what Memar depends on, and the embodied, embedded, and enacted claims are recorded as context, not yet operationalized.
- *The other cognitive processes* left the handoff; [What Cognition Is](./cognition.md#what-cognition-is) already names perception, attention, memory, and learning as coupled processes and states that the others are named here so that later work on them finds its home under this concept.
- *The medium's role as its own topic* left the handoff; [A Conversation as Two Cognitive Systems Connected Through a Medium](./cognition.md#a-conversation-as-two-cognitive-systems-connected-through-a-medium) already states that medium properties do not belong in the document beyond their recognition and the obligations they trigger.

#### Considered and not done
- *Which further modes belong here* stays open. No section of `cognition.md` states a criterion for admitting a further mode; the growth rule the question depends on is the changelog argument rule, and nothing in the document has yet earned its application.
- The handoff's `## Anticipated Work` lines were left untouched; none of them scheduled only these four questions.

---

### The mode list's current verdict recorded against the criterion the body already states

- Time: 2026-10-05T10:12:46Z
- Type: Changed
- Propagates to:
  - cognition.handoff.md: Done - the *Which further modes belong here* entry left Open Questions. The criterion that answers it was already in the body; what was missing was the criterion applied to the entry's own candidates, which is what this change records.
- Contributors:
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) - argued, drafted, applied

#### What changed
- `Grouping Notes` now carries the membership criterion's current verdict rather than only the criterion: no further mode earns a place at present, because the ecosystem's named inferential types decompose into stable combinations of the elementary operations named beneath them rather than adding a function none of them serves, and the judgment of evidence quality and strength of claim is already the Critical mode's.

#### Considered and not done
- **Continuing to leave *Which further modes belong here* open (rejected)**: the 2026-10-04 entry *Four open questions retired to sections that already answer them* left this question open on the stated ground that no section of the document states a criterion for admitting a further mode. That ground no longer holds: the 2026-09-15 operations layer named the membership criterion at both layers and stated that the document does not grow by adopting every named "X thinking" the ecosystem produces, so the criterion exists and the entry's own candidates can be tested against it.
- **Writing the verdict as a standing rule rather than a current one (rejected)**: the same paragraph holds that the membership criterion is fixed while the boundary drawing is not, and that the groups are revised when they stop being useful. A verdict stated for the modes as they stand keeps that revisability; a permanent rule would contradict the paragraph it sits in.
- **Adding an entry for probabilistic thinking's quantitative form (rejected)**: the entry's own test was a document depending on explicit probabilities, calibration, or expected-value trade-offs, and no document in the set yet does. An entry would claim a function no work exercises, which is the named failure mode this layer was built to remove.
- **Regrouping the discourse norms by mode in the same pass (rejected)**: it is a separate open question with its own costs, and folding it in would have coupled a navigation decision to a membership decision the body settles on different grounds.

---

### Keep reading and concluding separate
- Time: 2026-10-07T03:45:00Z
- Type: Changed
- Cited:
  - [Documentation — Comparison → Hindsight](./comparisons/hindsight.001.md) - Evidence: Hindsight's disposition traits shaping reflect without touching recall; a participant's mission must govern its answers, never its evidence.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- [What Implementation Asymmetry Obliges](./cognition.md#what-implementation-asymmetry-obliges) gains an obligation: standing instructions, dispositions, and the current task shape what may be concluded, never what the material is; the counterpart that reads back must receive the material that was read.

#### Considered and not done
- **Phrase it as a new discourse norm rather than an asymmetry obligation** (rejected): the failure — reporting wanted material as read material — is precisely an asymmetry failure; norms bind at intake, while this binds every read.

---

### Adding a record is not a large-scope change
- Time: 2026-10-10T14:30:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - An AI agent (via [Cursor](../CONTRIBUTORS.md#cursor)) — drafted, applied

#### What changed
- [Confirm before large-scope changes](./cognition.md#confirm-before-large-scope-changes) gains its boundary: adding a rule, a note, or an open question to the document that owns its subject waits for no one; removing text is a change the norm covers, because removal is what loses information. The rule itself lives in [Documentation → Recording Is Not Gated; Removal Is](../modules/knowledge/documentation/documentation.md#recording-is-not-gated-removal-is).

#### Considered and not done
- **Stating the whole rule here** (rejected): one home per rule; this norm needed only the sentence that keeps it from being read as gating additions spread across several documents.

---

### Thinking modeled by its components; named kinds read as compositions
- Time: 2026-10-12T07:45:14Z
- Type: Changed
- Cited:
  - Richard Paul and Linda Elder, *The Miniature Guide to Critical Thinking: Concepts and Tools* (Foundation for Critical Thinking) — Evidence: the nine universal intellectual standards (clarity, accuracy, precision, relevance, depth, breadth, logic, significance, fairness; sufficiency is among the further standards in their *Thinker's Guide to Intellectual Standards*), adopted standard by standard under this document's membership criterion and stripped of the word *critical*; the elements of thought it pairs them with are recorded as an open question in the handoff, not adopted.
- Propagates to:
  - cognition.practice.md: Done — *Working With the Operations Layer* became [Working With the Components](./cognition.practice.md#working-with-the-components): clarity first on input and output, named kinds translated into components, the operation and the standard named in a judgment; *Where Critique Sits* and the front matter no longer describe critique as a mode.
  - cognition.handoff.md: Done — *Whether discourse norms should regroup by mode* left Open Questions (regrouping by a false taxonomy would rebuild it); two questions added (questioning as an operation; elements of thought as a component class); the Anticipated Work items on the mode list, the Runs-on reader test, the survey, and graduation now speak of components.
  - modeling.md: Done — [False Taxonomies Hide Shared Structure](./modeling.md#false-taxonomies-hide-shared-structure) is the concept's new home; see modeling.changelog.md.
  - agency.md: Done — its *False Taxonomies* section narrowed to [Professional Categories as False Taxonomies](./agency.md#professional-categories-as-false-taxonomies); see agency.changelog.md.
  - documentation-explanation.practice.md: Done — the writing step holds the draft to the [standards of thinking](./cognition.md#standards-of-cognitive-material) instead of "exercising the thinking modes."
  - `.agents/skills/memar/SKILL.md`: Done — the sections read before a step that reasons, critiques, asks, or delegates now include a link to [Standards of Thinking](./cognition.md#standards-of-cognitive-material); nothing of the section is copied into the skill.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- The Abstract no longer names any kind of thinking. It names the component classes thinking is modeled by — elementary operations, standards, awareness disciplines, named errors — listing only the standards' members, and states that the field's named kinds of thinking are compositions of the components and, read as a division of thinking, a false taxonomy.
- *Modes of Thinking*, its four functional groups, and *Grouping Notes* are replaced by [The Components of Thinking](./cognition.md#the-components-of-thinking), which states the owner's claim — named kinds credit shared components to single kinds, so each is imprecise without the components filed under another — and the four component classes.
- A new class, [Standards of Thinking](./cognition.md#standards-of-cognitive-material): clarity, accuracy, precision, relevance, depth, breadth, consistency, significance, fairness, sufficiency — each a criterion held wherever material appears (input, process, output), owned by no kind and dropped by none. Only clarity is ranked, because every other standard is judged on a clear statement; the boundaries between consistency and sufficiency, accuracy and sufficiency, and depth and breadth are stated; the body names what differs from Paul and Elder's nine (logic named consistency; sufficiency added).
- A new operation, **inference** (deduction, induction, abduction as its forms), distinguished from commitment (inference derives what follows; commitment closes the field). The 2026-10-05 verdict that the named inferential types decompose into the existing operations did not hold: their forms lean on comparison and generation, but the carrying-over of support to a conclusion is none of the existing operations, and almost every act that concludes depends on it; the removed handoff question had already anticipated inference becoming an operation.
- Content the mode entries carried that was not mere labeling moved to the component it belongs to: prospective analogy and the biomimicry example to *mapping*; the abstract/concrete cycle and receiving a criticism at its root to *instantiation*; the whole-document claim-then-rationale method to *decomposition*; the revision mechanisms to *discrepancy noticing*; the diverge/converge cycle, rejected alternatives as evidence of the widening, and deferred judgment in supposition to [How the Components Combine](./cognition.md#how-the-components-combine), which also keeps the strategy/disposition/phase answer; Systems' pointer to Modeling and System to its table row. Illustrative lines (architecture as a decision's or a supposition's output, a definition as abstraction's product) were not carried.
- [Named Kinds of Thinking Are Compositions](./cognition.md#named-kinds-of-thinking-are-compositions) keeps the names only to translate, with a use rule (begin from what the material lacks — the operation it needs, the standard it fails) and a table whose first rows are carried over from the retired mode list; its columns show emphasis only, and every discipline and standard binds every row. Decision and convergence share their operations and differ only in where their field comes from, which the section states as the table's lesson.
- Review: a newly started reviewer (Claude Sonnet, not the drafting session) returned *approve with changes* — three must-fix (kind names still in the Abstract; the table's claim that critical components "recur in nearly every other row" contradicted by its own cells; open questions missing from the handoff) and twelve should-fix or optional findings. All were applied except three: the handoff one, which concerns another session's uncommitted removal of those questions, not this change; the optional suggestion to name only the classes in the Abstract, taken in part (operation names dropped, standards kept, since the owner's point was that clarity binds every session); and the optional note that mechanical steps skip the standards' read in the skill, which needed no change; the report is kept in task 20261012-T073912Z-21576.
- Methodology, the *consult other cognitive systems* norm, and *Named Errors* now speak of components rather than modes; each named error is an operation failing a standard.

#### Considered and not done
- **Keeping the mode list after the components (rejected; owner's decision)**: still loads the names as if they were the model's division, which is the false taxonomy the change removes.
- **Deleting the names with no table (rejected; owner's decision)**: material keeps arriving in those words; without a translation the reader re-derives the mapping each time.
- **Deriving standards only from what Memar's own work has recorded (rejected; owner's decision)**: clarity, accuracy, consistency, and sufficiency are already exercised implicitly by the norms; a recognized set reviewed member by member gives the class a complete first version without importing it wholesale.
- **Coining *false classification* for the owner's term (rejected; owner's decision)**: Memar already held the concept as *false taxonomy*, with the same "useful, not wrong" sense; the concept was moved to its proper home rather than given a second name.
- **Copying the standards into the skill (rejected; owner's decision)**: a copy is a cache that must be invalidated whenever the section changes; the skill links the section.
- **Adding questioning as an operation now (deferred)**: plausible, but not yet shown distinct from generation aimed at a gap; recorded in the handoff.

---

### Cognition's own components separated from thinking's
- Time: 2026-10-12T09:46:32Z
- Type: Changed
- Propagates to:
  - cognition.practice.md: Done — *Working With the Components* and *Quality Standards* link the standards at their new anchor and name material and disciplines as cognition's; the named-error check speaks of cognitive processes.
  - cognition.handoff.md: Done — *thinking material* renamed *cognitive material*.
  - documentation-explanation.practice.md: Done — link repointed to [Standards of Cognitive Material](./cognition.md#standards-of-cognitive-material).
  - documentation-handoff.md: Done — *thinking material* renamed *cognitive material*.
  - `.agents/skills/memar/SKILL.md`: Done — the link to the standards follows the renamed section; nothing copied.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- The owner's claim: this document is about cognition, not only thinking, and some of what the previous entry filed under thinking belongs to cognition — the concept of an assumption is cognition's, while finding assumptions in material received is an act of thinking.
- The model now has two levels. At the level of cognition: a new topic [Cognitive Material](./cognition.md#cognitive-material) (the representations every process works on, with **assumption** defined there as material, not as an act); [Standards of Cognitive Material](./cognition.md#standards-of-cognitive-material) (formerly *Standards of Thinking*), held by every process — what was read, what is recalled, what is reasoned; [Awareness Disciplines](./cognition.md#awareness-disciplines), now stated as attention held on something while other processes run; and cognitive biases, which any process can fall into (availability bias added as memory's example). At the level of thinking: [The Components of Thinking](./cognition.md#the-components-of-thinking) keeps only the operations, with **finding assumptions** named explicitly as decomposition joined to backward inference, and fallacies as thinking's own named errors.
- *What Thinking Is* moved after the cognition-level topics; *What Cognition Is* and the Abstract no longer call thinking the document's center — thinking is the process it develops furthest.
- *Thinking material* is renamed *cognitive material* throughout this document and the two live documents that used it; changelog history keeps the old term.

#### Considered and not done
- **Keeping the disciplines under thinking (rejected; owner's decision)**: a discipline produces no material and accompanies perception and recall as much as reasoning; holding something in view is what attention does.
- **Keeping the term *thinking material* with a widened definition (rejected; owner's decision)**: the word itself carried the impression that the material is thinking's.
- **A named operation *finding assumptions* (not done)**: it is decomposition joined to backward inference, so it is named as that combination inside decomposition rather than as an atom that would duplicate two others.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:46:32Z
- Type: Changed
- Contributors:
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — reviewed, revised

#### What changed
- Reviewed the changes other sessions left uncommitted in this family, beside the two entries above.
- The removal of five open questions from cognition.handoff.md is sound: four are recorded by *Four open questions retired to sections that already answer them* and one by *The mode list's current verdict recorded against the criterion the body already states*.
- *Adding a record is not a large-scope change* is sound; its body sentence and the documentation rule it points at both exist.
- Fixed: the 2026-09-05 entry *Knowledge Management link retargeted after the rename* had been deleted from this changelog with no record. It was restored verbatim from HEAD, since a changelog is history.

---

### What an agent settles itself, and what reaches the owner
- Time: 2026-10-12T16:02:36Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Claude](../CONTRIBUTORS.md#claude) (Opus-5.5) — drafted, applied

#### What changed
- [Norm Application Points](./cognition.practice.md#norm-application-points) gained the escalation checkpoint: an agent settles what the owning material and a second opinion from another model settle, recorded Tentative with the opinion as its reasoning; a definition other documents consume, a change that removes meaning, a change beyond the instance, and a premise the model rests on reach the owner however well they seem settled, as decisions needed gathered into one digest ([Queued Work and Its Hand-Back](../modules/knowledge/documentation/handoff/handoff.practice.md#queued-work-and-its-hand-back)).
- Observed: the owner was in the path of questions an agent could answer at some token cost; the owner's ruling (2026-10-12) keeps the owner for the decisive ones only.

---

### The escalation checkpoint points at the handoff entry
- Time: 2026-10-13T10:55:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - decided the direction
  - [Claude](../CONTRIBUTORS.md#claude) (Sonnet 5.5) - applied

#### What changed
- In [Norm Application Points](./cognition.practice.md#norm-application-points), the checkpoint for a question that reaches the owner now says the agent writes each of the four kinds as an entry in the handoff ([Questions Found During a Task](../modules/knowledge/documentation/handoff/handoff.practice.md#questions-found-during-a-task)), and that an agent with no owner to ask ends with a one-line pointer to the entry under decisions needed, not the question held only in its report.
- Why: the same ruling as the entry of this date in [documentation-handoff.changelog.md](../modules/knowledge/documentation/handoff/handoff.changelog.md); task `20261013-T103110Z-17584`.

---

### Practice description states when and what not
- Time: 2026-10-15T11:58:47Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — allowed the fix
  - [Claude](../CONTRIBUTORS.md#claude) (Opus 5.5) — revised

#### What changed
- `cognition.practice.md`'s `description` now states when it is used — the cases of its *When to Critique* section, intake, and debriefing a run — and what it is not: the norms and components themselves, the critique a modeling chat runs, and the self-examination that is part of drafting, which Documentation — Practice → Description quality criteria requires.
- Why: the study of task 20261015-T061908Z-9468 (report.md, Result 5) found the defect, and the owner allowed it fixed on 2026-10-15; a Practice's `description` is printed as the header an agent reads above its passages, so a description that misleads or states no boundary misleads every agent that reads it.
- Made in task 20261015-T110002Z-23000.

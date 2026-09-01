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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: directed that the always-active instruction skill be retired rather than duplicated; chose the name `thinking.md` so the document can grow beyond critical thinking into systems, creative, and adaptive thinking as cognitive-science grounding deepens; required 4E cognition grounding and the two-thinking-systems conversation model from the start; directed that the conversation model treat exchange between any two thinking systems (human, AI, organizational) symmetrically, never as AI-specific etiquette; reviewed the first draft and directed that the base document state only the "why" — historical provenance of the rules belongs here, not in the explanatory document.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: extracted the rules from the retired skill and the archived instruction file, derived the discourse norms from the conversation model, and drafted the document per the Explanation facet specification.

#### Summary
The project's collaboration and reasoning rules — previously a list of behavioral prescriptions in an always-active agent skill (`.agents/skills/main/SKILL.md`) and before that in instruction files — were replaced by a model-first document: what thinking is, which modes it has, how a conversation is two thinking systems joined by a medium, and which discourse norms follow from that model (evaluate claims on merits; definitions outrank terminology; do not assume the other participant correct or incorrect; criticism proportional to the model criticized; ask rather than assume; resist defaults arriving with the medium; prefer long-term clarity). Cognitive-science grounding (4E cognition) was added per the owner's direction. Rules specific to modeling or documentation remain owned by their specialized documents; this document owns the rules governing thinking material as it travels between any two thinking systems.

#### Rationale and alternatives
- **Keep the rules as an always-active skill and merely expand it (rejected by the owner)**: the skill form had no derivation behind its rules, framed general norms as AI-specific instructions, and duplicated rules already owned by terminology, modeling, and documentation documents.
- **Keep the retired skill as a thin pointer to this document (rejected by the owner)**: the owner preferred deleting it entirely and strengthening the existing `memar` skill — the skill that accompanies essentially every project adopting Memar's approach — to direct agents to project documentation including this document, avoiding a second near-always-active mechanism with a single line of content.

---

### Mode list expanded; historical narration moved out of the base document
- Time: 2026-09-01T09:10:00Z
- Type: Changed
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — argued, decided: the first draft's mode list (critical, systems, creative, adaptive) merely mirrored his own examples back instead of completing the family — abstract thinking was missing outright; directed that the base document state only the "why" of its content, with all history of how it came to be written moved into this changelog.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote.

#### Summary
Expanded Modes of Thinking from four named modes to thirteen, organized into five functional groups: Evaluative (critical, analytical, evaluative decision), Structural (abstract, concrete, systems, sequential), Generative (creative, divergent, analogical, hypothetical), and Corrective (adaptive, reflective). The grouping-by-function structure was introduced so the open-ended family stays navigable; abstract thinking was added explicitly after the owner flagged its absence. The group structure and every mode beyond the original four are this revision's contribution — the owner's original four survive unchanged as members of their groups. In the base document, the Motivation was rewritten to state the costs of the rules having no authoritative home (no derivation, scoping drift, no growth path) rather than narrating where the rules used to live; the Methodology was reduced to stating what the drafting presupposed, not the chain of custody from retired files; and a Rationale entry in the Discourse Norms topic was generalized the same way. The moved provenance lives in this entry and the entry above.

#### Rationale and alternatives
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
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided: proposed creating a thinking practice document as the absorption target for the critique practice; directed that documentation work must not be framed as if critique were its whole posture — critical examination is one component of writing a document (one mode among the family), even when starting from scratch; directed the review of where each part of the critique practice's content belonged best.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote: agreed with the placement after reviewing the alternatives, drafted the practice file, and distributed the absorbed content.

#### Summary
Created `thinking.practice.md` as the Practice-facet companion to this document, operationalizing its modes — chiefly critical thinking — into a followable procedure. The file absorbed the content of the retired `documentation-critique.practice.md` (the critique practice had been mis-homed under the documentation prefix: its content is about exercising a thinking mode, not about producing documents), with three changes: (1) its rules were re-anchored as operationalizations of this document's discourse norms rather than freestanding instructions, eliminating a second copy of the proportional-criticism and definitions-over-terminology rules; (2) a "Where Critique Sits" section was added stating the owner's position — critique is a component of writing and of modeling work, exercised alongside the generative and structural modes, and becomes the subject of this practice only when it is the dominant activity; (3) its "Relation to Other Practices" cross-references were updated to the surviving artifacts. A pointer to the new practice was added to `documentation-explanation.practice.md`'s writing step, marking the component-versus-activity boundary the owner required.

#### Rationale and alternatives
- **Absorb the critique content into `documentation-explanation.practice.md` instead (rejected)**: would couple a thinking-mode procedure to the document-production procedure, implying critique is documentation-specific; critique applies to proposals, models, and designs that never become documents.
- **Create a separate `documentation.practice.md` holding a "critique as part of writing" note (rejected)**: the note is one sentence — a whole file for it would be structure without a reader; the same note placed in `documentation-explanation.practice.md`'s writing step reaches exactly the contributor who needs it, at the moment they need it.
- **Keep `documentation-critique.practice.md` as-is (rejected)**: its name and placement claimed documentation ownership of a thinking-mode practice, and its rules duplicated this document's discourse norms without linking to them — two sources of truth for the same norms, guaranteeing drift.

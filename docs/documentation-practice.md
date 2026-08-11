---
Title: "Documentation — Practice"
Status: Proposed
Start Date: 2026-07-25
ID: 495821
---

# Documentation — Practice
This document specifies the Practice facet: content meant to be followed step by step to accomplish something, as opposed to studied to understand something. See [Documentation](./documentation.md) for what a facet is and why Practice is governed separately from Explanation.

## Abstract
A Practice-facet document (a **Skill file**, named `SKILL.md`) is a short, imperative, self-contained procedure. Its front matter is exactly `name` and `description` — no other fields — and its body stays under roughly 500 lines, with anything longer split into companion files loaded only when needed. This is not this project's own invention: it is the schema three independently-maintained AI ecosystems (Anthropic, OpenAI, Microsoft — see [documentation-practice.changelog.md](./documentation-practice.changelog.md) for citations) converged on without coordinating with each other, adopted here rather than replaced with something new.

## Introduction
### Motivation
An earlier draft tried to govern Skill files with the same schema as Explanation-facet documents (identity, citations, contributor attribution, a topic-first body). That schema is wrong for this facet: a Skill file is read by an agent mid-task, under real context-budget pressure, and every field that isn't the procedure itself is pure cost. The three real ecosystems examined here reached that same conclusion independently, which is stronger evidence than reasoning it out from scratch would have been.

## Explanation

### Frontmatter
Exactly two fields, both required:
- **name**: the skill's name, lowercase with hyphens (e.g. `write-a-document`).
- **description**: what the skill does and, critically, when to use it — this is the only thing an agent sees before the skill triggers, so trigger conditions belong here, never only in the body.

No other fields. All three cited conventions agree on this independently; Anthropic's and OpenAI's both state it as an explicit rule, not an informal habit.

#### Discussion
##### Prior art
Microsoft's own convention layers substantial additional structure on top of this same core (a fixed section order, mandatory callout blocks, a categorization/symlink system) — but explicitly scopes that additional structure to one narrow sub-case (Azure SDK skills specifically), noting elsewhere that "for domain skills, use your judgment to organize logically." The two-field frontmatter rule itself, unlike the rest of Microsoft's structure, is not qualified this way — it applies universally in all three conventions examined.

### Progressive disclosure
A Skill file loads in three levels, each larger and rarer than the last:
1. **Metadata** (`name` + `description`, roughly 100 words) — always in context.
2. **Body** (under ~500 lines) — loaded once the skill triggers.
3. **Bundled resources** (`scripts/`, `references/`, `assets/` — unlimited) — loaded only as needed, and in the case of scripts, sometimes executed without being loaded into context at all.

Keep the body itself lean: move anything that only applies to a specific variant, sub-case, or advanced use into a separate reference file, linked from the body, loaded only when that specific case actually applies.

### Bundled resources
- **`scripts/`**: executable code for anything that would otherwise be rewritten identically each time, or that needs deterministic reliability.
- **`references/`**: documentation meant to be read into context only when needed — schemas, detailed variant-specific patterns, API documentation.
- **`assets/`**: files used in the output itself (templates, images, boilerplate), not read into context at all.

### What not to include
Do not add a `README.md`, `CHANGELOG.md`, or any other auxiliary documentation file inside a Skill folder. A Skill file is consumed by an agent mid-task; meta-documentation about the skill's own history or creation process is pure overhead to that agent and belongs nowhere near it. (This specification, and `documentation.md`, are exactly that kind of meta-documentation — which is precisely why they live outside `.agents/skills/`, not inside any individual skill's folder.) Provenance for a Skill file — citations, contributor attribution, propagation tracking — lives in the paired `<base>.changelog.md` file at the Skill's parent level, not inside the Skill folder itself.

### Description quality criteria
The `description` field is the only thing an agent sees before deciding whether to trigger the skill. Two qualities make it work:

- **Trigger precision.** State the conditions under which the skill applies, not only what it does. A description that says "generates charts" is less useful than one that says "generates charts and diagrams (bar, line, pie, flowchart, mind map) as standalone image files or embedded in reports" — the second tells the agent both *what* and *when*.
- **Boundary clarity.** State what the skill does *not* do, or what it delegates to other skills. If a skill generates charts but does not create PDF reports, say so — this prevents the agent from triggering the wrong skill.

Bad: "A skill for making documents."
Good: "Creates formal Explanation-facet documents (.md) following the documentation-explanation.md specification. Use when producing specifications, analyses, design decisions, or any document meant to be studied rather than followed."

### When to split vs. extend
A single Skill file should do one coherent thing. Split into a separate Skill file when:
- A distinct, independently-triggerable use case emerges (e.g. "create a new document" vs. "revise an existing document" are separate triggers with separate procedures).
- The body would exceed ~500 lines even after moving variant-specific content into reference files.

Extend an existing Skill file (adding a new section or variant) when:
- The new content is a sub-case of the same trigger condition, not a new trigger.
- The new content is short enough that the body stays well under the 500-line limit.

The 500-line guideline is not a hard ceiling — it is a signal that the file is trying to do too much and should be examined for a natural split point.

### Body structure
No fixed section order is imposed (the three cited ecosystems disagree on this, and this specification defers to the author's judgment). A common and effective pattern, applicable to most Skill files:

1. **Overview** (1–3 sentences): what the skill produces and what the agent should have ready before starting.
2. **Steps**: the procedure itself, numbered or in a clear sequence.
3. **Edge cases and failure modes**: what to do when something goes wrong or when the input does not fit the expected pattern.

If the skill has no meaningful edge cases and the steps are self-evident, skip the overview and go straight to the steps. Structure serves the reader, not the other way around.

### Reference file naming
When the body references a companion file in `references/`, name it for what it contains, not for the skill it belongs to: `naming-conventions.md`, not `write-a-document-references-01.md`. The file's placement inside the skill's own `references/` folder already establishes the ownership relationship.

### Writing style
Imperative and concise. Assume the agent reading this is already capable — write only what it doesn't already know. Every sentence should earn its token cost; prefer a short example over a paragraph of explanation wherever both would work.

## Results
Insufficient time has passed since this specification was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Rationale and alternatives
- **Design a new, project-specific schema for Skill files (rejected)**: would produce a fourth, incompatible convention where three independently-converged ones already exist and already work with real tooling (including the very AI systems, such as Claude, that this project already relies on to author and use these files).
- **Require Skill files to cite an Explanation-facet document via a `Citations` field when one exists (considered, not chosen)**: `Citations` is provenance machinery that used to live in an Explanation-facet document's front matter and now lives in its paired Changelog-facet file; requiring it inside a Skill file would reintroduce exactly the apparatus this facet is supposed to avoid. A Skill file's body may still mention a related Explanation-facet document by name in plain prose, without any structured citation field. Provenance for the Skill file itself, if needed, lives in the Skill's paired Changelog-facet file (`<base>.changelog.md`), not inside the Skill folder.

### Unresolved questions
Whether this project will ever need Skill-file conventions beyond what the three cited examples already establish — this project has not yet produced enough Skill files to know.

- Add `Workflow`, `Rules`, ... optional sections.

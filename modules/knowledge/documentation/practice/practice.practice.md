---
name: documentation-practice
description: Use when creating a new formal practice document (.practice.md) for a Memar base document - the paired step-by-step procedure file. Not for creating Explanation-facet documents (use documentation-explanation), changelog files, or handoff files.
---

## Practice Document Creator
Produces the paired Practice-facet companion (`<base>.practice.md`) for a base document that already exists. A practice is meant to be *followed* to accomplish something - it carries the procedure the base specification deliberately omits.

## Steps
1. **Confirm the base document exists.** A practice is always a companion to a base artifact; its front matter is the two fields below and none of the Explanation facet's (no `Status`, `Start Date`, `ID`), and it has no independent identity - its filename derives from the base: `<base-slug>.practice.md`.
2. **Write the frontmatter.** Exactly two fields, both required per [practice.md - Frontmatter](./practice.md#frontmatter):
   - `name`: the skill's name, lowercase with hyphens.
   - `description`: what the skill does *and when to use it* - trigger conditions belong here, never only in the body. See [Description quality criteria](./practice.md#description-quality-criteria) for the precision and boundary-clarity rules.
3. **Extract the procedure from the base specification.** Read the base document and identify what a contributor must *do* to produce a compliant artifact - the base document states structure, not procedure; the practice states procedure, not structure. If the base document already contains step-by-step content, that content migrates here.
4. **Write the body.** Number the steps in a clear sequence; each step earns its token cost - imperative and concise, per the [writing style](./practice.md#writing-style). Add an edge-cases section only where real failure modes exist; skip it if the steps are self-evident. Use the [body structure](./practice.md#body-structure) guidance without treating it as a fixed template.
5. **Verify against the base specification.** Every rule the procedure states must trace back to the base document; every rule in the base document that requires action must appear in the procedure. A mismatch in either direction is a defect in one of the two files.
6. **Record the change in the base artifact's changelog.** A practice companion never receives a changelog of its own - see [changelog.md - Changelog scope](../changelog/changelog.md#changelog-scope).

## Edge cases
- **The base document changes after the practice exists.** Bring the practice in line at that edit - see the base specification's Progressive migration topic; the two files must stay consistent.
- **The procedure is too small to justify a separate file.** If the base document's procedure is one or two sentences, keep it in the base body; a practice file for a trivial procedure is structural overhead.
- **Multiple practices for one base document.** The one-file-per-base convention holds; if the procedures genuinely diverge in audience or trigger conditions, that is a signal the base document should be split, not that the practice file should multiply.

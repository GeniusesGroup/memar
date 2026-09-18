---
name: documentation
description: procedures for writing and revising Memar documentation under documentation.md — written surface, results routing, and where companion records go; use whenever drafting or editing any document in docs/
---
# Documentation Practice
> **Purpose:** Followable procedures that [documentation.md](./documentation.md) presupposes but does not itself contain. Facet schemas, naming, and language rules live in that document and in each facet's governing specification — this file does not restate them.

## Written surface
Apply [documentation.md → Written surface](./documentation.md#written-surface) on every edit:
1. Put the first line of a section's body on the line immediately under the section title — no blank line after the title.
2. Use a single blank line between blocks inside a section only when paragraph separation is needed; never two or more consecutive blank lines.
3. Write normative rules as sentences or numbered steps under section titles. Do not put load-bearing rules in grid layouts or diagram blocks that only work when rendered as graphics; short non-normative lookup grids are allowed.
4. When no prior durable snapshot of the document is available to the reader, state findings as present content — do not narrate "revised" or "formerly" against text the reader cannot open.

## Results and companions
When work produces something durable, route it by type — do not invent a side note:
1. Anticipated claim of a document → that document's Abstract ([Results routing](./documentation.md#results-routing)).
2. Derived consequences of adopting a design → Implications (optional section on the Explanation facet).
3. Observed change to an artifact → append one entry at end-of-file to the paired `.changelog.md` (oldest-first; use `memar-doc.py changelog-append`, do not preload the whole changelog to find the insertion point). Same-session undone mistakes with no lasting design change get **no** entry ([Trivial changes](./documentation-changelog.md#trivial-changes)).
4. Open questions and anticipated work → the paired `.handoff.md`.
5. A deliberate inquiry (including a negative result) → a `.research.<NNN>.md` companion.

## Creating or revising by facet
- New or revised Explanation document → [documentation-explanation.practice.md](./documentation-explanation.practice.md).
- New Practice companion (`.practice.md`) → [documentation-practice.practice.md](./documentation-practice.practice.md).
- Handoff produce/consume → [documentation-handoff.practice.md](./documentation-handoff.practice.md).

## No derivative inventories
Do not add membership indexes of directories, script sets, or comparison folders to READMEs or other pointer files. Point at the collection; let the reader list it ([Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance)).

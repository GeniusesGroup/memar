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
4. State the current rule in the body as what holds. Do not narrate "revised," "formerly," "retired," "withdrawn," or "is not the rule" against a formulation the edit replaced — that sentence belongs in the paired changelog (`What changed` for the outcome, `Considered and not done` for a rejected alternative). This applies whether or not a prior snapshot exists. The snapshot only changes whether a reader could open the old text; it does not license leaving the removed formulation in the body as a negation.

## Rejected positions
A position the owner has rejected is not a record, and the work it generates is bounded by three steps:
1. Delete the entry, section, or sentence whose claim is that position. Do not annotate it, hedge it, or keep it as history for a later reader.
2. Give the alternative that was genuinely examined and not taken its one home: one `Considered and not done` line in the surviving entry, phrased as that alternative and why it was not taken ([Considered and not done](./documentation-changelog.md#considered-and-not-done)).
3. State the decision affirmatively in the document that holds the claim; the changelog records the outcome of the change, never the position it replaced ([Written surface](./documentation.md#written-surface)).

## Results and companions
When work produces something durable, route it by type — do not invent a side note:
1. Anticipated claim of a document → that document's Abstract ([Results routing](./documentation.md#results-routing)).
2. Derived consequences of adopting a design → Implications (optional section on the Explanation facet).
3. Observed change to an artifact → one entry on the paired `.changelog.md` for the whole session, not one entry per edit ([Session consolidation](./documentation-changelog.md#session-consolidation)). Append at end-of-file, oldest-first; use `memar-documentation.py changelog-append` (at `../.agents/scripts/memar-documentation.py`), do not preload the whole changelog to find the insertion point. If this session already has an entry on that file, extend it. Same-session undone mistakes with no lasting design change get **no** entry ([Trivial changes](./documentation-changelog.md#trivial-changes)).
4. Open questions and anticipated work → the paired `.handoff.md`.
5. A deliberate inquiry (including a negative result) → a `.research.<NNN>.md` companion.

## Creating or revising by facet
- New or revised Explanation document → [documentation-explanation.practice.md](./documentation-explanation.practice.md).
- New Practice companion (`.practice.md`) → [documentation-practice.practice.md](./documentation-practice.practice.md).
- Handoff produce/consume → [documentation-handoff.practice.md](./documentation-handoff.practice.md).

## Which file the doer reads
When the task is to carry out work a practice already covers:
1. Read that practice and follow it.
2. Open the paired explanation only if a step names a section to check, or the task is to change the explanation.
3. Do not re-derive the procedure from the explanation when the practice states the steps.

## No derivative inventories
Do not add membership indexes of directories, script sets, or comparison folders to READMEs or other pointer files. Point at the collection; let the reader list it ([Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance)).

## Folder READMEs
A folder that has a main document beside it takes its `README.md` as a symbolic link to that document. A folder with no main document keeps a real `README.md` carrying content of its own. Apply this on every README a change creates, moves, or rewrites:
1. Settle which kind of folder this is. A main document is the one that states what the folder is for; a reader who wants to know what the folder is for arrives at that document. A folder of peers, of companions to documents held elsewhere, or of code has no main document, and its README is written as a real file.
2. For a folder that has one, move into the main document everything the README says that belongs to it — what the folder is for, and the criterion for what belongs in the folder — before replacing the file, so nothing leaves with it. Leave behind what the main document does not own: where a reader goes next, and a note about the folder that no single document holds.
3. Replace the README with a symbolic link whose target is the main document's file name, resolved from the README's own folder. Git records such a link as file mode `120000`, and the link's content is that target path. A README that is a text file naming its target is a text file that points at a sibling, not a link, whatever it says inside.
4. Where the filesystem will not create the link, record it in the index instead of on disk. Write the target path as the file's content with no trailing newline, then set the mode:
   ```
   git add <readme>
   git update-index --add --cacheinfo 120000,$(git hash-object <readme>),<readme>
   ```
   Confirm with `git ls-files -s -- <readme>`, which must report `120000`; a mode of `100644` means the file is a text file and the link was never recorded. The same procedure works where symlinks are supported, and is the one to use on a host that refuses them.
5. For a folder with no main document, write the README as a real file carrying real content: what the folder is for and what belongs in it, stated without restating what the files already say ([No derivative inventories](#no-derivative-inventories)).

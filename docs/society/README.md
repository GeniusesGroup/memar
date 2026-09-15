# Society — Requirement Knowledge Base
This directory holds the design knowledge for livable human settlements: one document per requirement, and inside each document every proposed answer to that requirement, side by side, argued and conflicting. A requirement here is a question the society must answer — "on which plane does each flow travel?", "who judges disputes?" — never smuggled into a favored solution; if a page's title already picks an answer, that is a defect to report, not a hint to follow.

**What you are reading.** Each `####` section under *Approaches* is one proposal (historically one "idea"): what it is, how it works, what it demands, what conventional practice it attacks, and — where the audit has reached it — its fit against existing fabric, its cognitive anchor, and its hook. Rivals and complements are deliberately kept in view together, because the value of the corpus is the comparison, not any single answer.

**Who uses it.** Builders and planners consult it as a decision checklist: before a block is built, the requirements its design touches should each show a recorded verdict in their changelog. Writers and analysts (human or AI) use the pages as they stand — they must read complete on their own; media work, business plans and task-management schemas are downstream readers of this corpus, never its authors' lens. Agents editing these files must first follow `.agents` instructions and load the Memar skill.

**What to watch for.**
- *Status of an answer.* An approach is proposed, not adopted, until a changelog records otherwise. `status: rejected` stays visible with its reason — nothing is deleted from this corpus; history is the asset.
- *Authorship.* Owner claims appear plain; reviewer-authored analytical fields are named in each page's changelog entry, and every open owner-decision question lives in the paired `.handoff.md` until the owner answers it. Do not answer an owner's question as if it were yours.
- *Provenance.* Source file names and quoted local terms stay in their original language on purpose — they are citations, not untranslated leftovers. `legacy-ref (unresolved)` marks a reference inherited from the pre-migration ledger that no label could identify; its changelog entry lists them per page.
- *Direction of dependency.* Network pages (energy, water, data, roads) state abstract rules and name no consumer; consumer pages declare their needs toward the network. A patch that inverts this arrow is wrong even when it reads well.
- *Stable handles.* Approach headings carry a strippable section-id suffix — the ledger mapping of these ids lives in each page's changelog; do not renumber, rename away, or reuse them.

The full operating rules of this corpus are the conventions each page already follows — requirement as question, changelog as ledger, handoff as the owner's open-decision queue, nothing deleted ever. Migration history lives page by page in the changelogs; there is no external operations file to keep in sync.

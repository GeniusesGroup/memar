---
Title: "Scripts Rule — Normative References"
Status: Draft
Start Date: 2026-10-16
ID: "497823"
---

# Scripts Rule — Normative References
This is the rule for what an act reads before it starts: for each kind of act, the sections of Memar's documents it cannot be carried out without having read, listed in this folder one list per kind beside one list every act reads. It is a rule of Memar's scripts, whose `task` concern declares the kinds of act ([`task_kind.py`](../../services/task_kind.py); `memar content context --help` names them), and it lives in the scripts' `rules/` folder as [Where Rules Live](../../../../docs/rule.md#where-rules-live-rules-beside-protocol) says; it moves to the `rules/` folder of the scripts' `task` module when the scripts become modules (session 20261015-T123046Z-17544), since its subject is the kinds that module declares ([Which Module a Rule Belongs To](../../../../docs/rule.md#which-module-a-rule-belongs-to)).

## The rule
Before an act starts, the agent doing it reads, in its own context, every section named by the entries of `normative_references-every_act.md` and of the list of each kind its act is.

The normative claim is stated here; no other Memar document states it. The Memar skill instructs the agent to read what its act requires ([Consult the governing document before each act](../../../skills/memar/SKILL.md#consult-the-governing-document-before-each-act)), and that instruction is the agent's runtime form of this claim, not a second owner of it ([Normative Claim and Executable Form](../../../../docs/rule.md#normative-claim-and-executable-form) lets the claim move with the Rule while the other place links back).

## Why it exists
What an act reads is one owner's selection across many documents, and a selection of that kind has no natural home in any of the documents it selects from. Kept apart, in a folder of its own, it is reviewed whole, it can be kept or dropped per project, and each entry carries the hash of its section as it read when the entry was last reviewed, so a section whose meaning moved under its entry is found by a check instead of going stale silently. Before this rule the selection was written in the code that composes an act's context, where nothing could tell when a passage it named had changed.

## Normative and informative
*Normative* and *informative* are taken in their established sense in standardization, not narrowed: in the ISO/IEC Directives, Part 2 (its clause "Normative references") and in the IETF's RFCs alike, a normative reference is a cited document, or part of one, indispensable for applying the citing document, and an informative reference helps understanding and binds nothing. The lists here are normative references of an act; what a search returns about the act's subject is informative.

## A list and its entries
A list is a file `normative_references-<word>.md` in a declared place, `<word>` being a kind's word or `every_act`. It holds a level-1 title, one sentence on why its act reads these sections, and its entries; it has no front matter a program reads.

An entry is one line at column 0, outside a fenced block: a list item whose text begins with a link to the section, then ` — ` and one sentence saying why the act reads it, then, last on the line, the review mark — a code span holding `reviewed` and the hash `memar content section FILE '#anchor' --hash` prints for that section. For illustration:

```
- [Modeling Practice → The Modeling Workflow](../../../../docs/modeling.practice.md#the-modeling-workflow) — a design ends in a module's contract, and its eighth step is the gate. `reviewed c8900bbbb4cb`
```

- **The link** is relative, to a Markdown file of the place's repository, with an anchor for a section or none for a whole document; in a project's list it may instead be a passage of Memar named by Memar's published URL, which is read and hashed from Memar's checkout. It is never root-relative (`/docs/...`), which in a project's list could mean the project's root or Memar's.
- **The why** is the entry's comment: a reason kept beside the fact it explains, not a second statement of the fact.
- **The mark** says the section was reviewed for this act as it reads now. A section that changes since has to be read again and its entry's mark updated; a section that was split gets an entry for each part the act must read.
- **A drop** — an entry in a project's list beginning `- Not read here: ` before its link — removes one of Memar's passages from that project's acts; its why is its reason, and it carries no mark.
- Any other text of a list, a link in its sentence included, is not an entry: the shape is the declaration.

The entries are the one statement of what an act reads, and no document restates them. The why sentences carry the selection's judgment, so a list is not a derivative inventory ([No Fabricated or Redundant Provenance](../../../../modules/content/documentation/documentation.md#content-rule-no-fabricated-or-redundant-provenance)).

## Declared places
A list is read only where lists are declared to live, so that a fixture or an illustrative example saved under a list's name binds nobody.

- **In Memar**, this folder, a constant in the code that reads it. It is not a preference, because Memar's lists bind every project and are found the same way from every one.
- **In a project**, the folders the `normative_references` key of the project's `.agents/memar/preferences.md` front matter names: one or more paths relative to the project's top folder, separated by commas, each a folder inside the project and none the top folder itself. Only the lists directly in each folder are read, not below it; a named folder that does not exist is reported, not read as an empty list. Empty or absent, the project has no lists of its own and its sessions read Memar's alone.
- **Anywhere else**, a file named like a list is never read, and `memar content check` warns of it.

## Enforcement
- **Resolver behaviour**: the composer behind `memar session start` and `memar content context` prints, for an act's kinds, the every-act sections and then each kind's, each section once, reading the lists and the sections from the live files on every call; a section changed since its mark is printed as it reads now, marked so.
- **Governance report**: `memar content check` reports an entry whose link or anchor resolves to nothing, whose mark is missing or differs from its section's current hash, a list whose word names no kind, and a drop that drops nothing, has no reason, or names an every-act section.

The composer reads this folder and a project's declared places, and `task_kind.py` names no section (sessions 20261016-T135247Z-13740 and 20261016-T135247Z-15984). A project's drop is printed in the context where the passage stood and counted on its first line and in `memar content check`'s summary line; a declared folder that does not exist is said on the first line.

## Scope
Memar's checkout, whose lists bind the acts of every project's sessions, software or not; and each project's declared places, whose lists add to Memar's or drop from them for that project's sessions only.

## Keep it or drop it
A project keeps Memar's lists as they are, adds sections of its own or passages of Memar the lists omit, or drops one of Memar's passages with its reason. The sections of `normative_references-every_act.md` are the exception: the owner rules (2026-10-16) that no project may drop them, and the composer prints them whatever a project's lists say. When what a passage governs leaves Memar for another repository — git and file-system details for an organization's own — the entries naming it move between lists, and nothing in the governed document changes.

## The format, and when it changes
The lists are Markdown, provisionally. [A Fact in Code Is Written Once](../../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once) presumes a fact is code, and in Memar that code is Khayyam; a list is code by that section's questions 1 and 3, and is written in Markdown for three reasons, each a fact about today: nothing that reads the lists parses Khayyam, so a Khayyam list would be a source no tool takes; an entry is a link into a Markdown document, which in Markdown renders, is counted by `memar content backlinks` and is checked by the anchor check with no new parser; and a person reviews a list on the published repository, where Markdown renders. The format changes:
1. when the Khayyam toolchain parses declarations the scripts or the Memar server read, so a list can be a Khayyam declaration the same tools take as a source — which removes the first reason, and with it the override;
2. when the Memar server keeps the lists as edges of its graph, from an act to a section, so the file becomes an export of what the server holds rather than its source;
3. when an entry needs more fields than one line carries, such as a scope, a condition or a date.

## What this rule does not claim
- It does not claim that the lists hold everything that governs a step: the governing documents of a step's subject are still found by searching for its terms, as the Memar skill says.
- It does not claim that a section a list omits binds nothing; it claims only that the sections it names bind before the act.
- It does not define the kinds of act or their words; `task_kind.py` does.
- It does not claim the every-act sections are derived from Cognition's model; they stand by the owner's ruling, stated in their list with its reason.

## Names are provisional
Every name this rule introduces — `normative_references`, `every_act`, the list file names, the preference key — is provisional by the owner's ruling (2026-10-16) that choosing a name is never finished and improving one is a standing task; session 20261016-T135248Z-22376 studies and decides them, and leaves the `TODO` that [A Name an Agent Doubts](../../../../docs/terminology.md#a-name-an-agent-doubts) asks for beside each name it keeps in doubt.

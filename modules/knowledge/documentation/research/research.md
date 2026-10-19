---
Title: "Documentation — Research"
Status: Draft
Start Date: 2026-09-08
ID: 496903
---

# Documentation — Research
This document specifies the Research artifact: a numbered companion file, named `<base-filename>.research.<NNN>.md`, that records a deliberate inquiry into a stated question — what was asked and why, who took part and in what roles, how it was conducted, and what it found — so the inquiry's outcome, including a negative or inconclusive one, survives as an examinable record. See [Documentation](../documentation.md) for what a Facet is, and [Documentation — Changelog](../changelog/changelog.md) and [Documentation — Handoff](../handoff/handoff.md) for the companion-file conventions this specification follows.

## Abstract
A Research-facet document is a numbered companion artifact (`<base>.research.<NNN>.md`) recording one deliberate inquiry: its governing questions and goals with their explicit standing, its participants and roles, its methodology and findings, and its conclusion — including negative and inconclusive outcomes, which have no other home in this documentation system. It is neither current understanding (that is [Explanation](../explanation/explanation.md#reader-relationship)), a change history ([Changelog](../changelog/changelog.md#reader-relationship)), nor resumable discussion state ([Handoff](../handoff/handoff.md#reader-relationship)): those three facets carry a subject's settled truth, its change history, and its live discussion state; the Research facet carries the trail of a question deliberately pursued. A research is mutable while Active and frozen once Complete or Withdrawn; a correction to a frozen research is a newer, superseding research, never a rewrite of the record.

## Introduction

### Motivation
A question raised in this project's discussions has three possible destinations today, and none of them is a research: it can be answered inside the discussion and written into the governing document as settled truth; it can remain open and live in the paired [handoff](../handoff/handoff.md) while the discussion is live; or it can be dropped. What the system lacks is the deliberate middle case: a question worth a bounded investigation, whose investigation itself — its goals, its method, its evidence, its participants, and possibly its negative or inconclusive result — deserves to survive even though it changed nothing. A negative result recorded nowhere is a question destined to be re-investigated at full cost; findings recorded without their participants and method cannot be audited, only believed; and an inquiry's standing assumed rather than stated cannot distinguish "answered" from "nobody has looked yet."

The Changelog facet's scope makes the gap precise: it records why and how an artifact *changed*. An investigation that concludes "no change is warranted" produces no changelog entry, so the system loses exactly the record that would have prevented repeating the work. The Explanation facet's [relevance discipline](../explanation/explanation.md#relevance-discipline) excludes open questions and process narrative from document bodies — by design — and the Handoff facet is mutable state that retires when the discussion ends. The need recurs; this facet names it.

### Methodology
Unlike the Changelog and Handoff facets — each of which consolidated a practice that had already accumulated informally across working sessions — this specification was drafted ahead of accumulation: the need was identified and the requirements stated by Omid Hekayati in a working session on 2026-09-08, and the specification was designed directly against the established companion-file pattern (the dot-keyed pairing of the Changelog and Handoff facets) and the attribution conventions the Changelog facet already defines ([CONTRIBUTORS.md](../../../../CONTRIBUTORS.md) identity, role tags, inline claim attribution). The requirement set — the governing questions and goals stated at the file's opening with their standing explicit, the participants and their roles including the review outcome, a mandatory methodology, a table of contents for files expected to grow long, and stick-to-base naming — came from that session and its owner review, which also named the method section `Methodology` after the Explanation facet's section; the structural treatment (controlled status vocabularies, freeze-on-completion, supersession, the graduation paths into the other facets) is this specification's design response to those requirements, argued in the paired [changelog](./research.changelog.md) and [handoff](./research.handoff.md).

## Explanation

### What a Research Is
A **research** is a deliberate, bounded inquiry into a stated question, conducted with material from outside this project. **Deliberate** — it is opened on purpose to answer the question, as distinct from the incidental exploration every discussion performs; **bounded** — its scope is stated with it, so a reader can tell whether their question falls inside this research or outside it; **conducted with material from outside this project** — see [What Qualifies as an Inquiry Worth This Facet](#what-qualifies-as-an-inquiry-worth-this-facet), which is the criterion a session checks before opening one, and which three common near-misses fail.

Two boundary statements sharpen the definition:

- **A research is not a draft of the governing document.** When an inquiry settles something, the settled content graduates into the governing Explanation-facet document through that document's own revision process and changelog; the research remains as the record of how the answer was reached — the evidence and method trail a changelog entry can cite. A research whose content has graduated is Complete, not retired: unlike a handoff, it persists.
- **A research is not a discussion transcript.** It records the inquiry's distilled state — questions, goals, method, findings, conclusion — not the conversation that produced them; the same analysis-not-transcription discipline the [Handoff facet](../handoff/handoff.md#analysis-not-transcription) names applies here.

### Reader relationship
A research is **examined to evaluate an inquiry** — what was asked, why it mattered, who took part and in what role, how it was conducted, what it found, and how firm the outcome stands. That is told apart from the reader relationship of each other facet by what the reader is expected to do, which each of [Explanation](../explanation/explanation.md#reader-relationship), [Changelog](../changelog/changelog.md#reader-relationship) and [Handoff](../handoff/handoff.md#reader-relationship) states for itself. A document kind that needs a reader relationship none of them answers is the case [Extensibility](../documentation.md#extensibility) covers, and it enters by its own specification.

### What Qualifies as an Inquiry Worth This Facet
The facet has a membership criterion, and it is the one thing a session must check before opening a research file, because the wrong turn here is common and produces files that look like inquiry and are not.

**A research brings in something from outside this project's own documents, and its findings are about how that external material bears on the question.** A source outside the project — another framework's specification, a paper, a standard, a practitioner account, a body of prior practice — and a method the project's own vocabulary does not already supply. The test is what the inquiry could not have produced by reading this repository: if every source consulted is a document of this project, the work is an audit of the project's own record, however carefully done, and it is not this facet.

Three things that look like research and are not, each with where it belongs instead:

- **An open question, written up.** A question this project has not answered, recorded as a numbered companion with a status line and an empty Findings section, is a question. It belongs in the base artifact's [handoff](../handoff/handoff.md), where it is visible to the next session as live state; a research file with no findings yet is a handoff entry wearing a research's clothes, and it costs a reader the mandatory sections to learn nothing.
- **An inventory of what the project's own documents already say.** Enumerating the project's requirements, rules, fields, and conventions, and reporting that they hold or do not hold, is an audit. Its findings are claims about the project, so they belong in the changelog entry of the change they produce, or in the handoff while they produce none. Written as a research, such an inventory is filed as scholarship while citing nothing outside the building.
- **A written record of the reasoning that produced a decision already made.** The path by which a conclusion was reached is [decision-shaping context](../changelog/changelog.md), and the changelog entry that made the change is its home. A research that only makes that path examinable duplicates what the changelog facet already requires, in a file that claims to be something it is not.

Where a question may yet deserve a real inquiry, the correct next step is to open the handoff entry and, when the inquiry is actually taken up, name the external source or method it will use. What the facet refuses is the file whose existence implies an inquiry that never happened.

### Relationship to the Other Facets
- **Versus Explanation**: an Explanation-facet document carries its subject's current state and excludes open questions and process narrative from its body ([Explanation → Reader relationship](../explanation/explanation.md#reader-relationship)). A research is the pre-settlement counterpart: it may hold open questions, provisional findings, and method narrative, because examining the inquiry is its reader relationship. When a research settles something, the settled content graduates into the governing document — never by editing the research into a pseudo-document.
- **Versus Changelog**: a changelog records why and how an artifact changed ([Changelog → Reader relationship](../changelog/changelog.md#reader-relationship)); a research records an inquiry that may or may not produce a change. A negative result ("investigated; no change warranted") is recorded here and nowhere else. When a research does produce a change, the base artifact's changelog entry cites the research in its `Cited` field with the `Evidence` relation. An opened research that has produced no change owes its base changelog nothing; the research file itself is the record until there is a change to record.
- **Versus Handoff**: a handoff is mutable state captured so a paused discussion can resume ([Handoff → Reader relationship](../handoff/handoff.md#reader-relationship)), and it retires when nothing open remains; a research is a durable record that persists after completion. The flow between them: an open question in a handoff that warrants deliberate investigation graduates into a research, its origin attributed; questions the research itself leaves open graduate back to the base artifact's handoff when the research completes.

### File Format and Naming
- A research file is named `<base-filename>.research.<NNN>.md`, placed next to its base artifact in the same directory — for example, a research opened against the Lexer protocol (`modules/computer/lexer/lexer.md`) lives at `modules/computer/lexer/lexer.research.001.md`. The base artifact is not necessarily a document, following the same rule the Changelog facet states.
- `NNN` is a zero-padded three-digit ordinal, assigned per base artifact in creation order, starting at `001`. It is identity, not meaning: it records creation order only and implies no priority or importance. It is unrelated to the `ID` numbering Explanation-facet documents carry.
- **The first research is `001`** — there is no bare `<base>.research.md` form. A bare form would force the first file's renaming the moment a second research appears, and renaming breaks the relative references other documents already hold ([documentation.md → URI](../documentation.md#uri)).
- **No parentheses and no descriptive slug in the filename.** The inquiry's description lives in the file's title and Question and Goals section, not in its name: a research's scope commonly shifts as it runs, and a descriptive filename goes stale exactly when the inquiry goes somewhere unexpected, while renaming to fix it breaks inbound references. A stable identity in the name, a current meaning in the title. Discovery is served by the filename scan (`*.research.*.md`), the mandatory question statement (content search), and the base changelog's `Cited` pointers for researches whose outcome was applied.
- **Pairing keys on the dot.** `lexer.research.001.md` is a companion of `lexer.md`; a hyphenated name such as `lexer-research.md` names an independent document that pairs to nothing. This is the same boundary the Changelog facet records ([Changelog scope](../changelog/changelog.md#changelog-scope)).
- The file has no YAML front matter — a plain H1 title, following the companion pattern: `# {Base Document's Title} Research {NNN} — {short inquiry name}` (for example, `# Lexer Research 001 — Tokenization caching`). As with the other companions, a research never reaches a settled "design" of its own; its identity comes from its base file and its ordinal, and its current meaning from its title and question.

### Structure
The body is a mandatory core followed by an open catalog of optional sections. The core is mandatory because a research's identity is its question, its people, its method, and its standing: a file without them is not a research, and an omitted review state reads as approval. The catalog follows the open-catalog pattern the [Explanation](../explanation/explanation.md#optional-sections) and [Handoff](../handoff/handoff.md#optional-sections) facets use: sections are included when they have content and omitted entirely when they do not; an empty header is never left in place; the list may grow as real researches demonstrate the need.

#### Table of Contents (mandatory)
The first section, immediately under the H1: a linked list of the file's `##` sections, in order. Research files are expected to grow long across sessions — findings, questions, and method accumulate — and the table of contents is the one-glance map of what the record holds. It is present unconditionally, including on short researches, so the shape of every research file is dependable without opening it; the cost is a few lines, the benefit is a uniform contract.

#### Status (mandatory)
One line stating the inquiry's overall state, taken from the values [Documentation → Status](../documentation.md#status) names for a research, which the type `Status` holds (`Status.for_kind`). A research has no front matter, so its Status is this section. Specific to a research: `Complete` requires every question to carry a final per-question status, and `Withdrawn` records its reason in the conclusion or notes. A superseded research states `Superseded by: {file}` on the line beneath.

#### Question and Goals (mandatory)
The inquiry's identity, stated at the head of the file:

- **Questions**: each governing question, stated as a question, each with its own status (the type `QuestionStatus`). A research is opened only for a question stated here. Questions added mid-inquiry — by any participant, including a reviewer — are appended here with their attribution and initial `Open` status. An answered question is marked `Answered` even before the conclusion is written; a question's standing is recorded, never assumed.
- **Goals**: what answering the question is for — what the inquiry is expected to deliver or enable. Each goal carries its own status (the type `GoalStatus`). Goals may be refined mid-inquiry; a refinement updates the entry and records what changed, rather than silently substituting.
- **Scope**: a short statement of what the inquiry covers and what it explicitly leaves out.

#### Participants (mandatory)
One entry per participant — a thinking system: person or AI agent — linked to their [CONTRIBUTORS.md](../../../../CONTRIBUTORS.md) identity, with the roles they hold. The role vocabulary is open, seeded with the roles the practice has already demanded: `Questioner` (raised the question), `Goal-setter` (defined the goals), `Researcher` (conducted the inquiry and wrote the record), `Reviewer` (reviewed the writing). One participant may hold several roles, and roles may pass between participants as an inquiry crosses sessions. A reviewer's entry records the review's outcome explicitly — `Approved` | `Not approved` ({reason}) | `Not yet reviewed` — so an unapproved research is visibly unapproved. Roles are recorded here; claims made by participants are attributed inline where they appear, following the Changelog facet's inline-attribution norm, so a role list never grows into a second, drifting copy of the claims.

#### Methodology (mandatory)
How the inquiry is being or was conducted: the sources consulted, the procedure followed, and the limits or known blind spots. Findings without a stated method cannot be audited, only believed — so unlike the [Explanation facet's](../explanation/explanation.md#optional-sections) optional `Methodology`, a research's cannot be omitted. The name matches the Explanation facet's section deliberately: the same kind of content — how the work was actually arrived at — and the same placement freedom applies, wherever it best serves the record. A single-reasoning-pass inquiry records that fact and its sources; even the minimal method is stated, not implied. Citations follow [documentation.md → Citations](../documentation.md#citations); a source supporting a finding is cited at the finding with the `Evidence` relation. A question's origin is recorded without being cited: attributing where a question came from gives that source no standing and lets it carry no conclusion, so a finding the consulted sources do not support is stated as the inquiry's own reasoning rather than as something they establish.

### Optional Sections
A non-exhaustive catalog of sections a research's author may include — nowhere is any of these mandatory, and this list may grow. Sections are included when they have content and omitted entirely when they do not; an empty header is never left in place, so a section's presence always means the content exists. New sections may be added as real researches demonstrate the need, following the same pattern.

#### Findings
What the inquiry has established so far, as claim-shaped statements, each carrying inline attribution where authorship varies and cited evidence where evidence exists. Ordered by question when the research governs several. A finding that is genuinely tentative says so in its own statement — that is content; question-level standing is carried by the question statuses.

Numeric estimates (including percentages and coverage estimates) are not measured data merely because they are expressed as numbers. Without an inspectable method and supporting evidence, they must not be cited as measured results. Qualitative judgments expressed numerically must be identified as estimates, regardless of whether their author is a person or an AI system.

#### Open Questions
Questions raised during the inquiry that it does not answer — including those a reviewer added. While the research is Active they live here; when it completes, each graduates to the base artifact's handoff or is explicitly dropped, so a live question is never buried inside a frozen record.

#### Conclusion
Written when the research reaches `Complete` or `Withdrawn`: the final outcome for each question — the answer, or why the question was withdrawn — and where the outcome landed: the changelog entry or document revision that carries it, or the explicit statement that nothing changed. A recorded negative result is this facet's purpose: it is the trace that prevents the question's re-investigation at full cost.

#### Related Artifacts
Documents, records, or other researches affected by or affecting this inquiry — what relation, what action is needed there.

#### Notes
Anything that does not fit above but may matter later.

### Lifecycle and Integrity
- **Active** researches are mutable working records: findings accumulate, questions and participants are added, statuses are updated as the inquiry moves.
- **Complete and Withdrawn** researches are frozen records. A correction is a newer research that references and supersedes the old one; the superseded record stays in place with its `Superseded by` pointer — a wrong finding and a negative result are equally part of the inquiry's trail. Mechanical repairs (broken links, typos) do not reopen a frozen record.
- A research file receives **no companion changelog and no companion handoff**: its own status fields and participant record are its live state — the same recursion stop the other companion facets apply — and a superseding research is its correction mechanism.

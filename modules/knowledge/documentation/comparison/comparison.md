---
Title: "Documentation — Comparison"
Status: Draft
Start Date: 2026-10-06
ID: 497579
---

# Documentation — Comparison
This document specifies the fair-comparison essay: the method a project follows when it examines a neighbouring project that people offer as its substitute. The method lives here; each consuming project keeps its essays wherever that project's documentation system puts documents of this kind, under the conditions stated below.

## Abstract
A comparison is an essay about other projects conducted under the examining project's own principles: it states the other project's self-definition first, separates layers, judges it against its own purpose before measuring it against the examining project, and writes toward absorbing what is durable into that project's homes. It is not a rejection list, not a scoreboard, and not a place where a principle may live only — whatever an essay concludes about its own project graduates into the documents that own it. [The essay's required shape](#the-essays-required-shape) is fixed; the sections below add obligations to it. Four requirements carry an effective date, because the essays already written do not satisfy them and a rule retrofitted onto the corpus it did not govern would be a claim about work that never ran under it.

## Introduction

### Motivation
Neighbouring projects routinely get offered as substitutes for a framework's own method, and the question "why not just use X?" deserves a written, fair answer rather than an assertion. Two failure modes make such an answer hard to write and harder to keep true. The first is tone: an answer that dismisses a neighbouring project is worthless as evidence and corrodes the reader's trust in every other claim beside it. The second is storage: a method kept as a folder pointer file is invisible to the project's document set, cannot be cited by a governing document, and drifts from the conventions that govern everything else it sits beside.

### Methodology
The method is not designed in the abstract. It accumulated from working comparisons in the folder this document governs, each conducted under the fairness rules below, each feeding what it surfaced back into the documents that own it. Two structural decisions came first. Comparisons are deliberately outside the facet system, because an essay's reader relationship — examining the comparative argument — is none of the reader relationships the facet specifications state, and forcing it into one would give it a changelog and a status ladder it must not have. Those specifications are the subfolders of the [documentation module](../documentation.md), each stating its own reader relationship; an essay needs a relationship of its own rather than one borrowed from them. The four dated requirements at the end came from specific gaps the rules were silent on: claims that no reader could tell from verified ones, a collapsed history mistaken for thin evidence, a count that moved on recount, and a project whose disclosure reached its code but not its own front door.

## Explanation

### What a comparison is
- An essay for humans (and agents) who ask: "Why not just use X instead of this project?"
- A place that may record **negative or partial results**: X is good at Y; X does not replace this project's job.
- Deliberately **outside** the facet system, and therefore bound by this document rather than by a facet specification.

### What a comparison is not
- Not a rejection list or a scoreboard.
- Not a claim that other projects are "bad." Many are strong at what they set out to do.
- Not a substitute for the project's live documentation, and not a place where a rule may live only. An essay is corrected in place with its reasons stated inside; what it concludes about this project belongs in that project's governing documents, and the record of the change belongs in their changelogs.

### What binds an essay
An essay is not an Explanation- or Practice-facet document, so the conventions that govern those facets do not reach it by their own terms. This document extends them: the Content Rule's prohibition on fabricated information, its prohibition on redundant restatement, and [Written surface](../documentation.md#written-surface)'s prohibition on carrying normative logic in grids or diagram blocks apply to an essay as they apply to any document ([Content Rule](../documentation.md#content-rule-no-fabricated-or-redundant-provenance)). So do the cross-cutting requirements this document adds below. What an essay does not get is the facet machinery: no front matter, no companion changelog, no handoff, no status ladder.

### Fairness rules
1. **State the other project's self-definition first** — judge it against its own purpose before measuring it against the examining project. Write toward absorption, not coexistence: place what is durable in the examining project's homes so the neighbouring pack becomes unnecessary inside a session of that project, and treat coexistence of packaging as transitional rather than as the goal.
2. **Separate layers** — a session-workflow pack, a distribution platform, domain knowledge, and a system-development framework are different jobs, and conflating them produces false rivals. The cut to apply is by the job a reader would hire the project for, not by the layer names a stack diagram happens to use ([Framework → Memar's Framework: Design Space Over Implementation Layers](../../../../docs/framework.md)).
3. **Credit strengths without borrowing their packaging** — an idea graduates when it can be stated as a rule the examining project could follow without the neighbouring project's machinery; a harness ritual, a marketplace shape, and a persuasion script are packaging, and packaging does not travel.
4. **Prefer durable claims** — a claim is durable if it stays true as models and tools change; write to that test rather than to the weakness of the current generation of agents ([Knowledge → Write for the structure of the subject](../../knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits)).
5. **Keep load-bearing logic linear** — do not encode norms in grids or diagram blocks; use section titles and linear lists ([Written surface](../documentation.md#written-surface), [Knowledge → Write for the structure of the subject](../../knowledge.md#write-for-the-structure-of-the-subject-not-for-todays-reader-limits)).
6. **A comparison carries no changelog** — the file is its own record and is corrected in place, with its reasons stated inside. What graduates from it into the examining project's model is recorded in that project's changelogs, never here.

### Where a project's comparison essays live
In this repository the essays live in `docs/comparisons/`, whose `README.md` is a real file that states the folder's criterion, because the folder has no main document: this document specifies the method, and the folder holds the essays it governs. The two rules that hold there are the two every project applies to its own folder: an essay is found by listing the directory, never through an index — an index of comparisons is the derivative inventory the Content Rule forbids — and one essay occupies one file, named after the project it examines.

### How an essay is identified over time
An essay examines one project at one inspected revision, so a project examined twice has two essays rather than one revised essay: the first is named `<project>.001.md`, the second `<project>.002.md`, and the ordinal is creation order, carrying no meaning beyond it. The distinction that makes the numbering necessary is between correcting an essay and re-examining a project. A correction — a wrong citation, a count that moved on recount, an unfair sentence — is made in the file that is wrong, because that file is the record of the examination and a corrected record is still that record. A re-examination is a new examination: the upstream project has moved, this project has changed, and the earlier essay's premises no longer hold, so it stays as it was written and the new essay cites it. Writing the second examination over the first would leave the reader unable to tell which state of both projects an argument was made against — the same reason a superseded research is a newer record and not a rewrite ([Documentation — Research → Lifecycle and Integrity](../research/research.md#lifecycle-and-integrity)).

### Standing principles these comparisons assume
Each project states its own standing principles and cites the documents that own them. The ones below apply to this repository's essays, and they are applied rather than re-derived:
- One continuous mental model as internal knowledge — a project carries one, and adapters may multiply but the model must not ([Knowledge → A project carries one continuous mental model](../../knowledge.md#a-project-carries-one-continuous-mental-model)).
- Executable projections where generation belongs in code services — not endless prose recipes for each concrete artifact ([Knowledge → Knowledge and Code](../../knowledge.md#knowledge-and-code)).
- Memar is not distributed as host-tool plugins or marketplace cards; a consuming project installs a pointer ([Using Memar in another project](../../../../README.md#using-memar-in-another-project)).
- Prompt / harness technique sits under Communication, not under Agency's foundation ([Agency → Prompt Engineering and Harness Engineering](../../../../docs/agency.md#prompt-engineering-and-harness-engineering)).

### The essay's required shape
An essay carries the header block that makes its evidence checkable: the compared project with a link to it, the commit or revision inspected, and the method — including what was not executed ([Content Rule → No fabricated information](../documentation.md#content-rule-no-fabricated-or-redundant-provenance)). It then follows the stages of the type `EssayStage`, in that order, as numbered sections; the last, Open for critique, carries the disclosure quota below.

An essay may add sections the case requires — a second-opinion record, a source-status drill-down, a category the case needed that this list does not name — and may name dispositions beyond the four in stage 7 when the case needs them. What it may not do is skip a stage, or merge two of them into one section whose heading claims both.

### Method requirements added by practice
The four requirements below apply to essays written from 2026-10-07. They are part of the method now, not commentary on it, and the essays that predate them are not thereby defective: the corpus is not evidence that the corpus was governed.

1. **A disclosure quota under "Open for critique".** The essay names which of its claims it could not verify from the checkout — a benchmark that resolves off-repo, a version never exercised, a count carried from an earlier pass rather than recounted — and does the same for its own project's claims cited in the essay. When nothing was unverifiable, the essay says that instead of writing the section's absence, because a reader cannot otherwise tell a clean pass from no pass; that statement is content, and a passage saying every claim is checkable is a claim too, on the same footing.
2. **Single-commit checkouts.** When the inspected repository's history is collapsed, the essay says so once, where it states the checkout's status, and treats the missing history as a finding about the source: a project that cannot show why a change happened is a different kind of source than one that can.
3. **A second-opinion pass, by a party that did not draft the essay.** After the first pass, another party re-verifies every count, every file-and-line citation, and every restated normative sentence, and the essay records that the pass happened and what it corrected — a clean pass is recorded as such, or the reader cannot distinguish it from none ([Documentation Changelog → Approval Requires a Reviewer Who Did Not Do the Work](../changelog/changelog.md#approval-requires-a-reviewer-who-did-not-do-the-work) holds the rule that the reviewer did not do the work). The pass checks rather than drafts, which is what makes it affordable enough to always run.
4. **Triple-marked conceptual material.** Where a project labels planned or prototype work, the essay checks for the label in prose, in code comments, and in defaults — enabled and disabled flags, advertised versions — and records which of the three is missing as a finding about that surface. The general rule is that capability a project has not enacted must be marked wherever a reader can reach it, so that no single surface claims more than the project holds; each project then decides which surfaces that means for it. Memar's form of the rule is that material describing owed or planned capability carries the mark in prose, by a quiescent default where code exists, and at the entry point, which is a clause of the Content Rule ([Content Rule → Owed or planned capability](../documentation.md#content-rule-no-fabricated-or-redundant-provenance)).

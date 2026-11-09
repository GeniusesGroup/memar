---
Title: "Documentation — Comparison"
Start Date: 2026-10-06
ID: 497579
---
# Documentation — Comparison
This document specifies the fair-comparison essay: the method a project follows when it examines a neighbouring project that people offer as its substitute. The method lives here; an essay is a content of a task, a template this document governs, and it names no file, directory, path or file name ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)).

## Abstract
A comparison is an essay about other projects conducted under the examining project's own principles: it states the other project's self-definition first, separates layers, judges it against its own purpose before measuring it against the examining project, and writes toward absorbing what is durable into that project's homes. It is not a rejection list, not a scoreboard, and not a place where a principle may live only — whatever an essay concludes about its own project graduates into the documents that own it. [The essay's required shape](#the-essays-required-shape) is fixed; the sections below add obligations to it. Four requirements carry an effective date, because the essays already written do not satisfy them and a rule retrofitted onto the corpus it did not govern would be a claim about work that never ran under it.

## Introduction
### Motivation
Neighbouring projects routinely get offered as substitutes for a framework's own method, and the question "why not just use X?" deserves a written, fair answer rather than an assertion. Two failure modes make such an answer hard to write and harder to keep true. The first is tone: an answer that dismisses a neighbouring project is worthless as evidence and corrodes the reader's trust in every other claim beside it. The second is storage: a method kept outside the project's document set cannot be cited by a governing document, and drifts from the conventions that govern everything else it sits beside.

### Methodology
The method is not designed in the abstract. It accumulated from working comparisons, each conducted under the fairness rules below, each feeding what it surfaced back into the documents that own it. Two structural decisions came first. Comparisons are deliberately outside the facet system, because an essay's reader relationship — examining the comparative argument — is none of the reader relationships the facet specifications state, and forcing it into one would give it a status ladder it must not have. Those specifications are the subfolders of the [documentation module](../documentation.md), each stating its own reader relationship; an essay needs a relationship of its own rather than one borrowed from them. The method requirements arose from specific gaps the rules were silent on: claims that no reader could tell from verified ones, a collapsed history mistaken for thin evidence, a count that moved on recount, and a project whose disclosure reached its code but not its own front door.

## Explanation
### What a comparison is
- An essay for humans (and agents) who ask: "Why not just use X instead of this project?"
- A place that may record **negative or partial results**: X is good at Y; X does not replace this project's job.
- Deliberately **outside** the facet system, and therefore bound by this document rather than by a facet specification.

### What a comparison is not
- Not a rejection list or a scoreboard.
- Not a claim that other projects are "bad." Many are strong at what they set out to do.
- Not a substitute for the project's live documentation, and not a place where a rule may live only. An essay is never edited, and what it concludes about this project belongs in that project's governing documents, where the change is recorded by a changelog content of the task that made it.

### What binds an essay
An essay is not an Explanation- or Practice-facet document, so the conventions that govern those facets do not reach it by their own terms. This document extends them: the Content Rule's prohibition on fabricated information, its prohibition on redundant restatement, and [Written surface](../documentation.md#written-surface)'s prohibition on carrying normative logic in grids or diagram blocks apply to an essay as they apply to any document ([Content Rule](../documentation.md#content-rule-no-fabricated-or-redundant-provenance)). So do the cross-cutting requirements this document adds below. What an essay does not get is the facet machinery: no front matter, no status ladder, and no changelog of its own.

### Fairness rules
An essay follows [Self-definition before comparison](./rules/self-definition-before-comparison/self-definition-before-comparison.md), [Compare by job](./rules/compare-by-job/compare-by-job.md), [Absorb ideas, not packaging](./rules/absorb-ideas-not-packaging/absorb-ideas-not-packaging.md), and [Durable claims](./rules/durable-claims/durable-claims.md). [Written surface](../documentation.md#written-surface) keeps its load-bearing logic linear, and [No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md) governs its immutable task content and any correction or graduated conclusion.

### Where an essay is found
An essay is found by the `comparison` Topic label on the task that holds it, then in that task's timeline content. One essay examines one project, and its task is its only home; [No derivative inventories](../rules/no-derivative-inventory/no-derivative-inventory.md) governs discovery.

### How an essay is identified over time
An essay examines one project at one inspected revision, and that revision is what identifies it: a project examined twice at different revisions has two essays, each naming the revision it inspected, and the later one cites the earlier. The distinction that makes this necessary is between correcting an essay and re-examining a project. A correction — a wrong citation, a count that moved on recount, an unfair sentence — is a new content that replies to the essay and states the reason, because the essay is the record of the examination and is never edited. A re-examination is a new examination: the upstream project has moved, this project has changed, and the earlier essay's premises no longer hold, so the earlier essay stays as it was written and the new essay, a content of a new task, cites it. Writing the second examination over the first would leave the reader unable to tell which state of both projects an argument was made against — the same reason a superseded research is a newer content and not a rewrite ([Documentation — Research](../research/research.md)).

### Standing principles these comparisons assume
Each project states its own standing principles and cites the documents that own them. The ones below apply to this repository's essays, and they are applied rather than re-derived:
- One continuous mental model as internal knowledge — a project carries one, and adapters may multiply but the model must not ([Knowledge → A project carries one continuous mental model](../../../../modules/knowledge/knowledge.md#a-project-carries-one-continuous-mental-model)).
- Executable projections where generation belongs in code services — not endless prose recipes for each concrete artifact ([Knowledge → Knowledge and Code](../../../../modules/knowledge/knowledge.md#knowledge-and-code)).
- Memar is not distributed as host-tool plugins or marketplace cards; a consuming project installs a pointer ([Using Memar in another project](../../../../README.md#using-memar-in-another-project)).
- Prompt / harness technique sits under Communication, not under Agency's foundation ([Agency → Prompt Engineering and Harness Engineering](../../../../modules/management/agency/agency.md#prompt-engineering-and-harness-engineering)).

### The essay's required shape
An essay carries the header block that makes its evidence checkable: the compared project with a link to it, the commit or revision inspected, and the method — including what was not executed ([Content Rule → No fabricated information](../documentation.md#content-rule-no-fabricated-or-redundant-provenance)). It then follows the stages of the type `EssayStage`, in that order, as numbered sections; the last, Open for critique, carries the disclosure quota below.

An essay may add sections the case requires — a second-opinion record, a source-status drill-down, a category the case needed that this list does not name — and may name dispositions beyond the four in stage 7 when the case needs them. What it may not do is skip a stage, or merge two of them into one section whose heading claims both.

### Method requirements added by practice
The method requirements effective from 2026-10-07 are [Disclose unverified claims](./rules/disclose-unverified-claims/disclose-unverified-claims.md), [Report collapsed checkout history](./rules/report-collapsed-checkout-history/report-collapsed-checkout-history.md), and [Independent second opinion](./rules/independent-second-opinion/independent-second-opinion.md). [Content Rule → Owed or planned capability](../documentation.md#content-rule-no-fabricated-or-redundant-provenance) governs the triple-marked conceptual material an essay examines.

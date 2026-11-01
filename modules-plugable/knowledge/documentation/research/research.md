---
Title: "Documentation — Research"
Status: Draft
Start Date: 2026-09-08
ID: 496903
---
# Documentation — Research
This document specifies the Research template: the shape of the content that records one deliberate inquiry into a stated question, placed in the timeline of the task that is the inquiry. It names no file, directory, path or file name: where a content is kept is the store's concern. See [Documentation](../documentation.md) for what a template is.

## Abstract
A research records one deliberate inquiry: its question and goals, how it was conducted, what it found, and its conclusion, including a negative or inconclusive outcome, which has no other home in this documentation system. It is neither current understanding ([Explanation](../explanation/explanation.md#reader-relationship)), a change history ([Changelog](../changelog/changelog.md#reader-relationship)), nor resumable discussion state ([Handoff](../handoff/handoff.md#reader-relationship)): the research carries the trail of a question deliberately pursued. Its parts are declared in code ([primitive](./primitive/), [content_kinds.py](content_kinds.py)), so this specification writes none of them as text. What it states is what a research is, which inquiries qualify, how it relates to the other templates, and the requirements a party that did not write it can decide from a stated input.

## Introduction
### Motivation
A question raised in this project's discussions has three possible destinations, and none of them is a research: it can be answered inside the discussion and written into the governing document as settled truth; it can remain open as a `question` content of a task; or it can be dropped. What the system lacks is the deliberate middle case: a question worth a bounded investigation, whose investigation itself, its goals, method, evidence and possibly its negative or inconclusive result, deserves to survive even though it changed nothing. A negative result recorded nowhere is a question destined to be re-investigated at full cost; findings recorded without their method cannot be audited, only believed.

A change record cannot hold it: it records why and how a thing changed, and an investigation that concludes that no change is warranted produces none. The Explanation template's [relevance discipline](../explanation/explanation.md#relevance-discipline) excludes open questions and process narrative from document bodies by design. The need recurs; this template names it.

### Methodology
This specification was drafted ahead of accumulation: the need was identified and the requirements stated by Omid Hekayati in a working chat on 2026-09-08, and the specification was designed against the Changelog and Handoff templates and the attribution conventions the Changelog template defines. The owner's rulings of 2026-10-31 made the research a template and a Topic label of a task: each research is its own task, the task holds its Status and the placers of its contents, and a question the research leaves open is a `question` content of the task. This document applies them.

## Explanation
### What a Research Is
A **research** is a deliberate, bounded inquiry into a stated question, conducted with material from outside this project. **Deliberate**: it is opened on purpose to answer the question, as distinct from the incidental exploration every discussion performs. **Bounded**: its scope is stated with it, so a reader can tell whether their question falls inside this research or outside it. **Conducted with material from outside this project**: see [What Qualifies as an Inquiry Worth This Template](#what-qualifies-as-an-inquiry-worth-this-template).

Two boundary statements sharpen the definition:

- **A research is not a draft of the governing document.** When an inquiry settles something, the settled content graduates into the governing document through that document's own revision, and the research remains as the record of how the answer was reached, the evidence and method trail a change record can cite.
- **A research is not a discussion transcript.** It records the inquiry's distilled state, questions, goals, method, findings, conclusion, not the conversation that produced them; the [analysis-not-transcription](../handoff/handoff.md#analysis-not-transcription) discipline applies here.

A research is a task labelled with the topic `research` ([labels](./labels/topics.py)). The task holds the Status of the inquiry, changed only by a Request ([Request](../../../../modules/process/request/request.md)), and the placers of its contents; the research repeats neither.

### Reader relationship
A research is **examined to evaluate an inquiry**: what was asked, why it mattered, how it was conducted, what it found, and how firm the outcome stands. That is told apart from the reader relationship of each other template by what the reader is expected to do, which each of [Explanation](../explanation/explanation.md#reader-relationship), [Changelog](../changelog/changelog.md#reader-relationship) and [Handoff](../handoff/handoff.md#reader-relationship) states for itself.

### What Qualifies as an Inquiry Worth This Template
The membership criterion is the one thing to check before opening a research, because the wrong turn here is common and produces contents that look like inquiry and are not.

**A research brings in something from outside this project's own documents, and its findings are about how that external material bears on the question.** A source outside the project, such as another framework's specification, a paper, a standard, a practitioner account or a body of prior practice, and a method the project's own vocabulary does not already supply. The test is what the inquiry could not have produced by reading this repository: if every source consulted is a document of this project, the work is an audit of the project's own record, however carefully done, and it is not this template.

Three things that look like research and are not, each with where it belongs instead:

- **An open question, written up.** A question this project has not answered is a `question` content of a task ([Handoff → The kinds](../handoff/handoff.md#the-kinds)). A research with no findings yet is a question wearing a research's clothes.
- **An inventory of what the project's own documents already say.** Reporting that the project's requirements, rules and conventions hold or do not hold is an audit. Its findings are claims about the project, so they belong in the change record of the change they produce, or in a `question` content while they produce none.
- **A written record of the reasoning that produced a decision already made.** The path by which a conclusion was reached is a `decision` content ([Handoff → The kinds](../handoff/handoff.md#the-kinds)), and the change record that made the change is its home.

Where a question may yet deserve a real inquiry, the next step is the `question` content, naming the external source or method the inquiry will use when it is taken up. What this template refuses is the research whose existence implies an inquiry that never happened.

### Relationship to the Other Templates
- **Versus Explanation**: an Explanation document carries its subject's current state and excludes open questions and process narrative from its body. A research is the pre-settlement counterpart: it may hold provisional findings and method narrative, because examining the inquiry is its reader relationship. When a research settles something, the settled content graduates into the governing document, never by editing the research into a pseudo-document.
- **Versus Changelog**: a change record says why and how a thing changed ([Changelog → Reader relationship](../changelog/changelog.md#reader-relationship)); a research records an inquiry that may or may not produce a change. A negative result ("investigated; no change warranted") is recorded here and nowhere else. When a research does produce a change, the change record cites the research with the `Evidence` relation.
- **Versus Handoff**: a handoff template writes the contents that carry a paused discussion's live state ([Handoff → The kinds](../handoff/handoff.md#the-kinds)). A question that warrants deliberate investigation becomes a research, its origin attributed; the questions a research leaves open are `question` contents of its task, not a section of the research.

### The parts
The parts of a research, their headings, their order and which are mandatory are declared in [primitive](./primitive/), and no writer creates, renames or reorders one. The question and goals, the methodology, the findings, the conclusion, the related contents and the notes are there; so are the words that give a question and a goal each its standing.

Findings are claim-shaped statements, each carrying attribution where authorship varies and cited evidence where evidence exists. A finding that is genuinely tentative says so in its own statement. Numeric estimates, including percentages and coverage estimates, are not measured data merely because they are numbers: without an inspectable method and supporting evidence they must not be cited as measured results, and a qualitative judgment expressed numerically is identified as an estimate, whether its author is a person or an AI system.

The methodology cannot be omitted: findings without a stated method cannot be audited, only believed. A single-reasoning-pass inquiry records that fact and its sources; even the minimal method is stated, not implied. A source supporting a finding is cited at the finding with the `Evidence` relation. A question's origin is recorded without being cited: attributing where a question came from gives that source no standing, so a finding the consulted sources do not support is stated as the inquiry's own reasoning rather than as something they establish.

The conclusion states the final outcome for each question, the answer or why it was withdrawn, and where the outcome landed: the change record or document revision that carries it, or the explicit statement that nothing changed. A recorded negative result is this template's purpose: it is the trace that prevents the question's re-investigation at full cost.

### The requirements
Each requirement is decidable from a stated input by a party that did not write the research. None names a part or a count, because those are the declaration's.

1. **A research is opened only for a stated question**, and its question carries a standing that is recorded, never assumed.
2. **A research cites at least one source from outside this project**, or it is not a research ([What Qualifies](#what-qualifies-as-an-inquiry-worth-this-template)).
3. **A research states its methodology**, and a finding is never stated as established by a source that does not support it.
4. **A research is a content and is never overwritten or removed.** A correction is a later research that replies to the earlier one; a wrong finding and a negative result are equally part of the inquiry's trail.
5. **A research receives no record beside it** ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)).

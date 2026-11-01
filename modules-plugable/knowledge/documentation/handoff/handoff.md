---
Title: "Documentation — Handoff"
Status: Proposed
Start Date: 2026-08-04
ID: 496041
---

# Documentation — Handoff
This document specifies the Handoff concept and its templates: the shapes of the contents of kind `question`, `decision`, `assumption` and `anticipated-work` that carry the state of an ongoing discussion across a session boundary, so the discussion can continue from stable ground instead of restarting. `handoff` is the name of the concept and is not a kind of content; each of the four kinds is a template with fields of its own. The module names no file, directory, path or file name ([No Record Is Written Beside a Document](../rules/no-record-beside-a-document/no-record-beside-a-document.md)). See [Documentation](../documentation.md) for what a template is, and [Cognition → A Conversation as Two Cognitive Systems Connected Through a Medium](../../../../docs/cognition.md#a-conversation-as-two-cognitive-systems-connected-through-a-medium) for the model this specification builds on: a session is one stretch of an exchange between cognitive systems, and the material traveling between sessions degrades unless something carries it.

## Abstract
A handoff is the distilled state of a discussion — what was decided, what remains open, what is being assumed, and what is anticipated — produced by **analysis, not transcription**. It is carried by contents of a task's timeline, one content per question, decision, assumption or anticipated work, and is written with full awareness of its own risks: selection asymmetry (the writer chooses what counts as important), analysis-versus-record confusion (a distilled claim can silently present itself as what was actually said), and invisible premises (the reasoning behind a conclusion can be lost while the conclusion survives). The fields of the templates exist to control exactly those risks — confidence marking, assumption recording, and rationale capture are mandatory structure, not optional polish. Its consumers are agents of any kind: an AI session resuming a thread, a human returning to a discussion after weeks, a colleague joining mid-stream, or an organization handing work between shifts. The `handoff` relationship between two sessions is general — the AI-mediated conversation is one instance of it, not its definition.

## Introduction
### Motivation
Discussions in this project routinely span multiple sessions: a topic is introduced, partially explored, set aside, and resumed days or weeks later. Without a deliberate record, each resumption pays one or more of these costs:

- **Context loss.** The next chat receives only what memory, chat scrollback, or habit happens to preserve — which is less than what the discussion established, and distorted in unknowable ways.
- **Re-litigation.** Settled points are re-argued because no record distinguishes "decided with reasoning" from "merely discussed" — or the record exists but does not say how firm each conclusion was.
- **Resurfaced ambiguity.** An ambiguity that was resolved is rediscovered as if new, because the resolution and the argument that produced it were never carried forward.
- **Re-explanation burden.** A participant must restate background that was already established, paying for every resumption what should have been paid once.

The failure mode is not hypothetical: this project's working directories accumulated ad-hoc context notes, chat extracts, and half-structured summaries precisely where no named template governed the need. Naming the templates and specifying their fields converts that recurring improvisation into a controlled practice.

### Methodology
The concept first emerged as informal convention — a project decision recorded that a handoff must be produced between conversations, and real notes accumulated in the project's working context before the pattern was named. It was first kept as a companion file of a document; moving it into the timeline of the task that holds the discussion made the task the single home of the discussion's state, and left this specification with the shapes alone. The field requirements — confidence marking, assumption tracking, decision-with-rationale — were carried over from the practice documents' field-tested tables, not invented here.

## Explanation
### Reader relationship
Content meant to be *read to resume a paused discussion*: the contents of a timeline that carry a discussion's current state across a session boundary — decisions with their confidence, open questions, assumptions, and anticipated work — so the next chat (an AI system, a returning human, a colleague joining mid-stream) can continue from recovered state instead of re-derivation.

It serves a reader who continues unfinished work, which the [Changelog](../changelog/changelog.md#reader-relationship) does not. That difference is what makes a question, an assumption or an anticipated work state that is open until it is answered, firmed up or dropped. Its central discipline — that the record is an *analysis* of the discussion, not a transcript, with the risks of distillation named and structurally controlled — is [Analysis, Not Transcription](#analysis-not-transcription).

### What a Handoff Is
A **handoff** is the transfer of an ongoing engagement — a discussion, a task, a decision process — from one session (or agent, or person) to another, such that the receiving side can continue without repeating what the sending side already did. The concept is well established outside software: telecommunications defines handover/handoff as transferring an ongoing call or session between channels without losing it ([Handover](https://en.wikipedia.org/wiki/Handover)), and change-of-shift reporting in healthcare and follow-the-sun development in software are the same concept for human work. This document borrows the established word, with the established meaning, and specializes it to documented discussions.

Two boundary statements sharpen the definition:

- **A handoff is a distillation, not a record.** A transcript preserves what was said; a handoff preserves what the discussion *established* — and those are different with different failure modes. This distinction is load-bearing for the whole specification and is developed in [Analysis, Not Transcription](#analysis-not-transcription).
- **A handoff is not the discussion's conclusion made permanent.** Concluding a topic — writing its outcome into the governed documentation — is the job the [Explanation](../explanation/explanation.md) and the [Changelog](../changelog/changelog.md) already serve. A handoff is for discussions that have *not* reached that state. When the discussion concludes, its content graduates into the proper documents and the contents that carried it are answered, not edited. A question that concluded without an answer stays open as a content of its task, or as a task of its own, until it resolves into design or is explicitly dropped by a later content that says so; the Explanation excludes unresolved questions from document bodies (see its [Relevance discipline](../explanation/explanation.md#relevance-discipline)).

### Analysis, Not Transcription
Producing a handoff is an **analysis** of the discussion, not a copy of it. This distinction is the specification's central claim, because every field below exists to control a specific risk that analysis carries. Three risks are named explicitly:

- **Selection asymmetry.** The writer chooses what counts as important, and that choice is invisible to the reader unless the record makes it visible. A task whose timeline holds no question looks identical to one where no questions remained open. *Control: each state category is a kind of its own — question, decision, assumption, anticipated work — so an omission is a decision the writer makes kind by kind, not a blanket habit.*
- **Analysis-versus-record confusion.** A distilled claim ("we decided X") can silently present itself as what was actually said, when it may be the writer's interpretation of what was said. *Control: confidence marking is mandatory — every decision carries its confidence level, so interpretation is labeled as interpretation; where a conclusion had dissenting considerations or a rejected alternative, the options are recorded, which distinguishes "settled with reasoning" from "settled by fatigue."*
- **Invisible premises.** The reasoning behind a conclusion can be lost while the conclusion survives — a future reader inherits "X" with no way to evaluate whether X still holds. A decision without its reasoning cannot be safely revised or defended later. *Control: the decision fields require the options that existed, the reason, and what tipped the balance — the "why" travels with the "what."*

With these controls, the distillation earns its cost: it is short enough to actually be read at the start of a session (unlike a transcript), and structured enough that its selectivity is auditable (unlike an ad-hoc summary). Without them, a handoff is not a neutral convenience — it is a new point of failure, potentially worse than no record because it creates false confidence in an unauditable selection.

### Relationship to the Other Templates
Each governs a different reader relationship, and the boundaries between them are what keep each content honest:

- **Versus Explanation**: an Explanation-facet document carries its subject's current state ([Explanation → Reader relationship](../explanation/explanation.md#reader-relationship)). A handoff records where a discussion currently *stands* — including its unsettled parts. A handoff must never smuggle design claims: if the discussion has actually settled something, the content belongs in the governing document, and the handoff points to it rather than restating it.
- **Versus Changelog**: a changelog records what *changed* and why — it is consulted to audit history ([Changelog → Reader relationship](../changelog/changelog.md#reader-relationship)). A handoff records where a *discussion stands* — it is read to resume work. They can refer to each other, but neither absorbs the other.
- **Versus Plan**: what is to be done next, in order, is a plan of the task; an anticipated work is what no one has committed to.

The handoff relationship between sessions is also what the [Cognition](../../../../docs/cognition.md) document's conversation model predicts is needed: cognitive material degrades crossing a medium, and a session boundary is a medium crossing. The contents are the compensation for that specific degradation — specified here, justified there.

### The kinds
A task holds as many contents of each kind as its discussion produces: a task that asks the owner several questions places several `question` contents, and each answer is a later content that refers to the one it answers. The kinds, and the fields each carries, are declared in `./content_kinds.py` and in the types of [`./primitive/`](./primitive/): the fields of a kind are the types carrying its label (`question-field`, `decision-field`, `assumption-field`, `anticipated-work-field`), and the controlled vocabularies are the types carrying the label `confidence` and `stability`.

- **question** — something undecided that the task cannot settle alone. It stands alone: the test is whether a session with no memory of the task can read it and know what is asked and what each answer would change; a question that fails is rewritten before the task that wrote it ends. It is placed in the task that found it; it becomes a task of its own when the task ends with it unanswered.
- **decision** — what was settled, with its options, its reason and its confidence. A decision may cite the content that approved it (an [approval](../approval/approval.md), such as the comment of a user with the CTO role); the status of the task is not repeated in it.
- **assumption** — what is taken as given meanwhile, with its stability and what would change if it proved wrong.
- **anticipated-work** — extensions, growth paths and follow-up work the discussion anticipates but no one has committed to; distinct from a question (something is undecided) and from a plan (someone is doing it now).

Two writing rules bind every kind:

- **The vocabulary is fixed.** The confidence levels and the stability levels are controlled vocabulary — the receiving session must be able to distinguish firm conclusions from provisional ones without guessing what the writer meant.
- **Specific over general.** "We discussed modeling approaches" is a failed content; "Decided: graph-oriented modeling as primary method — reason: reveals relationships better than table-based approaches" is a passing one. Every content must be understandable by a session that did not participate, without re-reading the discussion it summarizes.

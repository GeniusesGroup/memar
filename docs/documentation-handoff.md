---
Title: "Documentation — Handoff"
Status: Draft
Start Date: 2026-09-01
ID: 496741
---

# Documentation — Handoff
This document specifies the Handoff artifact: a companion file, named `<base-filename>.handoff.md`, that preserves the state of an ongoing discussion between thinking sessions so the discussion can continue from stable ground instead of restarting. See [Documentation](./documentation.md) for what a Facet is, and [Thinking → A Conversation as Two Thinking Systems Connected Through a Medium](./thinking.md#a-conversation-as-two-thinking-systems-connected-through-a-medium) for the model this specification builds on: a session is one stretch of an exchange between thinking systems, and the material traveling between sessions degrades unless something carries it.

## Abstract
A Handoff-facet document is a **companion artifact** (`<base>.handoff.md`) capturing the distilled state of a discussion — what was decided, what was resolved, what remains open, what is being assumed, and what comes next — produced by **analysis, not transcription**. It is written with full awareness of its own risks: selection asymmetry (the writer chooses what counts as important), analysis-versus-record confusion (a distilled claim can silently present itself as what was actually said), and invisible premises (the reasoning behind a conclusion can be lost while the conclusion survives). The artifact's structure exists to control exactly those risks — confidence marking, assumption recording, and rationale capture are mandatory structure, not optional polish. Its consumers are agents of any kind: an AI session resuming a thread, a human returning to a discussion after weeks, a colleague joining mid-stream, or an organization handing work between shifts. The `handoff` relationship between two sessions is general — the AI-mediated conversation is one instance of it, not its definition.

## Introduction

### Motivation
Discussions in this project routinely span multiple sessions: a topic is introduced, partially explored, set aside, and resumed days or weeks later. Without a deliberate artifact, each resumption pays one or more of these costs:

- **Context loss.** The next session receives only what memory, chat scrollback, or habit happens to preserve — which is less than what the discussion established, and distorted in unknowable ways.
- **Re-litigation.** Settled points are re-argued because no record distinguishes "decided with reasoning" from "merely discussed" — or the record exists but does not say how firm each conclusion was.
- **Resurfaced ambiguity.** An ambiguity that was resolved is rediscovered as if new, because the resolution and the argument that produced it were never carried forward.
- **Re-explanation burden.** A participant must restate background that was already established, paying for every resumption what should have been paid once.

The failure mode is not hypothetical: this project's own working directories accumulate ad-hoc context notes, chat extracts, and half-structured summaries precisely where no named artifact governs the need. Naming the artifact and specifying its structure converts that recurring improvisation into a controlled practice.

### Methodology
This specification was not designed in the abstract. The `<base>.handoff.md` pattern follows the path the Changelog facet already paved: the underlying practice first emerged as informal convention — a project decision recorded that handoff files must be produced between conversations, two practice documents were drafted to structure them, and real handoff notes accumulated in the project's working context before the pattern was named as a facet. This document consolidates and formalizes that existing practice, following the same adoption argument the Changelog facet used: once a pattern is applied across multiple artifacts, giving it a governing specification is a smaller conceptual cost than leaving it as implicit convention. The structural requirements — confidence marking, assumption tracking, decision-with-rationale — were carried over from the practice documents' field-tested tables, not invented here.

## Explanation

### What a Handoff Is
A **handoff** is the transfer of an ongoing engagement — a discussion, a task, a decision process — from one session (or agent, or person) to another, such that the receiving side can continue without repeating what the sending side already did. The concept is well established outside software: telecommunications defines handover/handoff as transferring an ongoing call or session between channels without losing it ([Handover](https://en.wikipedia.org/wiki/Handover)), and change-of-shift reporting in healthcare and follow-the-sun development in software are the same concept for human work. This document borrows the established word, with the established meaning, and specializes it to documented discussions.

A **Handoff-facet document** (`<base>.handoff.md`) is the written artifact that makes a handoff possible across time: the distilled, structured state of a discussion, written so that a session that was not present can act as if it had been.

Two boundary statements sharpen the definition:

- **A handoff is a distillation, not a record.** A transcript preserves what was said; a handoff preserves what the discussion *established* — and those are different artifacts with different failure modes. This distinction is load-bearing for the whole specification and is developed in [Analysis, Not Transcription](#analysis-not-transcription).
- **A handoff is not the discussion's conclusion made permanent.** Concluding a topic — writing its outcome into the governed documentation — is the job the [Explanation facet](./documentation-explanation.md) and the [Changelog facet](./documentation-changelog.md) already serve. A handoff is for discussions that have *not* reached that state: the topic is still moving, and the artifact exists so the movement survives the session boundary. When the discussion does conclude, the handoff's content graduates into the proper documents and the handoff retires.

#### Discussion

##### Rationale and alternatives
- **Use the name "continuity note" (rejected)**: describes a hope (that the topic continues) rather than the artifact's function (transferring state across a boundary). "Handoff" names the function, and does so with an established, cross-domain word rather than a coined one — consistent with the project's preference for scientific-layer or established terminology over invented labels ([Terminology → Scientific Terms](./terminology.md#scientific-terms)).
- **Use the name "conversation note" (rejected)**: scopes the artifact to AI chat sessions. The need is agent-generic: a fully human working session — a design review meeting, a pair-modeling session, a shift handover — requires exactly the same state transfer, and this project's agent documents ([`.agents/README.md`](../.agents/README.md)) commit to content that applies to whichever agent is actually reading. The session may be AI-mediated, human, or organizational; the artifact's structure is identical in all three cases.
- **Leave this as convention without a governing specification (rejected)**: the pattern was already repeating across real artifacts (see Methodology). Leaving it unnamed would reproduce the drift the [Documentation](./documentation.md) meta-layer exists to prevent — each future handoff inventing its own structure, with no guarantee the next session knows how to read the previous one's.

##### Prior art
Telecommunications handover: the transfer of an in-progress session between channels or cells without loss — the source of the term and of the requirement that the transfer preserve the session rather than restart it. Change-of-shift report in healthcare: structured transfer of patient state between shifts, with its own documented failure literature when done poorly. Follow-the-sun development: the same transfer across time zones in software work. Meeting minutes and decision logs: the long-established human practice of distilling a discussion into its outcomes — a handoff document is their disciplined descendant, with structure added for the risks minutes historically ignore (confidence, assumptions, invisible premises).

### Analysis, Not Transcription
Producing a handoff is an **analysis** of the discussion, not a copy of it. This distinction is the specification's central claim, because every structural requirement below exists to control a specific risk that analysis carries. Three risks are named explicitly:

- **Selection asymmetry.** The writer chooses what counts as important, and that choice is invisible to the reader unless the artifact makes it visible. A handoff that omits an unresolved question looks identical to one where no questions remained open. *Control: the required structure forces the writer through each state category — decisions, resolutions, open questions, assumptions, next steps — so an omission is a decision the writer makes section by section, not a blanket habit; and the Status field states the topic's overall state so a reader knows how complete the transfer is.*
- **Analysis-versus-record confusion.** A distilled claim ("we decided X") can silently present itself as what was actually said, when it may be the writer's interpretation of what was said. *Control: confidence marking is mandatory — every decision carries its confidence level (Decided / Tentative / Explored-but-unresolved / Deferred), so interpretation is labeled as interpretation; where a conclusion had dissenting considerations or a rejected alternative, the rationale is recorded, which distinguishes "settled with reasoning" from "settled by fatigue."*
- **Invisible premises.** The reasoning behind a conclusion can be lost while the conclusion survives — a future reader inherits "X" with no way to evaluate whether X still holds. A decision without its reasoning cannot be safely revised or defended later. *Control: the decision structure requires capturing what options existed, what criteria were used, and what tipped the balance — the "why" travels with the "what."*

With these controls, the distillation earns its cost: it is short enough to actually be read at the start of a session (unlike a transcript), and structured enough that its selectivity is auditable (unlike an ad-hoc summary). Without them, a handoff is not a neutral convenience — it is a new point of failure, potentially worse than no artifact because it creates false confidence in an unauditable selection.

#### Discussion

##### Drawbacks
The controls cost effort: a disciplined handoff takes noticeably longer to write than a loose summary, and a writer under session-end pressure will be tempted to skip the confidence marking or the rationale capture — exactly the parts that carry the value. The specification accepts this cost deliberately: a fast, unreliable handoff pays its cost later, with interest, when the next session trusts it.

##### Rationale and alternatives
- **Specify a transcript-based handoff (rejected)**: preserves fidelity but fails the purpose — the next session must re-analyze the full exchange, paying again the cost the handoff existed to avoid, and transcript volume discourages the artifact from being written at all.
- **Specify only a free-form summary (rejected)**: minimal effort, but leaves all three risks uncontrolled — selection asymmetry, unlabeled interpretation, and lost premises are precisely what free-form summaries historically suffer from, in this project's own working context as much as anywhere.
- **Use meeting-minutes format as-is (considered, not chosen)**: minutes capture outcomes and action items well, but conventionally omit confidence levels, assumption tracking, and rejected-alternative rationale — the three controls this document makes mandatory. The handoff structure is minutes extended with those controls, not minutes adopted wholesale.

### Relationship to the Other Facets
The Handoff facet does not compete with the existing facets — each governs a different reader relationship, and the boundaries between them are what keep each artifact honest:

- **Versus Explanation**: an Explanation-facet document states what something *is*, at its current state of understanding. A handoff records where a discussion currently *stands* — including its unsettled parts. A handoff must never smuggle design claims: if the discussion has actually settled something, the content belongs in the governing Explanation-facet document (via that document's own revision process), and the handoff points to it rather than restating it.
- **Versus Changelog**: a changelog records what *changed in an artifact* and why — it is consulted to audit history. A handoff records where a *discussion stands* — it is read to resume work. They can reference each other (a handoff may cite the changelog entries a discussion produced; a changelog entry may note the handoff it emerged from), but neither absorbs the other.
- **Versus Practice**: the practice documents governing *how* to produce a handoff live in [the paired practice file](./documentation-handoff.practice.md). The base document defines the artifact's concept and structure; the practice defines the procedure.

The handoff relationship between sessions is also what the [Thinking](./thinking.md) document's conversation model predicts is needed: thinking material degrades crossing a medium, and a session boundary is a medium crossing. The handoff artifact is the compensation for that specific degradation — specified here, justified there.

#### Discussion

##### Unresolved questions
1. Should a concluded handoff be deleted, archived under a different name, or left in place with its Status set to Complete? Deletion loses the trail of how the documentation came to be; retention accumulates files. Not settled here — the practice file carries the current working answer, and this document may adopt it once real usage shows which costs dominate.
2. Can one handoff serve a discussion that spans more than one base topic — or should multi-topic sessions split into one handoff per topic at the boundary? The practice file currently requires one-topic-per-file; whether that survives real multi-topic sessions is untested.

### File Format
A Handoff-facet file is named `<base-filename>.handoff.md`, following the same companion-file convention the Changelog facet established — with the same pairing rule: the base artifact is not necessarily a document (a handoff can carry a discussion about an image, a piece of code, a model), though a discussion document is the overwhelmingly common case.

The file has no YAML front matter — just a plain H1 title, following the Changelog facet's pattern (`# {Base Document's Title} Handoff`). The rationale is the same one the Changelog facet recorded: a handoff never reaches a settled "design" the way an Explanation-facet document does; it is a living state-capture, and its identity comes from its paired base file, which its filename already encodes.

### Structure
The body is a fixed skeleton of state sections — fixed, because the next session's ability to *find* a category of state quickly is the entire point, and a findable structure cannot be left to per-file invention. Sections are included when they have content and omitted entirely when they do not; an empty header is never left in place, so the skeleton's presence always means the state exists:

```markdown
# {Base Document's Title} Handoff

## Topic & Purpose
{What is being discussed and why — one short paragraph. The handoff's only narrative section.}

## Status
{Active | Paused | Blocked | Complete — the topic's overall state.}

## Decisions
{For each decision: what was decided, the reasoning, and its confidence — Decided / Tentative / Explored-but-unresolved / Deferred. Where alternatives were considered and rejected, the rejected alternative and the reason are recorded with the decision.}

## Ambiguities Resolved
{For each: what was unclear, what is now clear, and what evidence or argument resolved it.}

## Open Questions
{For each: the question, why it matters, whether it blocks continuation, and a suggested path toward answering it.}

## Assumptions
{For each: what is being assumed, its stability (Strong / Weak / Unexamined), and what would change if it proved wrong.}

## Key Definitions Established
{Terms defined, refined, or confirmed during the discussion, with the agreed definition — cross-referencing the governing document where the definition has been formally recorded.}

## Proposed Next Steps
{Ordered steps toward continuation, with dependencies.}

## Related Artifacts
{Documents, models, or records affected by or affecting this discussion — what relation, what action is needed there.}

## Notes
{Anything that does not fit above but may matter later.}
```

Two writing rules bind every section:

- **Confidence vocabulary is fixed.** The four levels (Decided, Tentative, Explored-but-unresolved, Deferred) and the three stability levels (Strong, Weak, Unexamined) are the artifact's controlled vocabulary — the receiving session must be able to distinguish firm conclusions from provisional ones without guessing what the writer meant.
- **Specific over general.** "We discussed modeling approaches" is a failed entry; "Decided: graph-oriented modeling as primary method — reason: reveals relationships better than table-based approaches" is a passing one. Every entry must be understandable by a session that did not participate, without re-reading the discussion it summarizes.

#### Discussion

##### Rationale and alternatives
- **Free-form structure (rejected)**: see [Analysis, Not Transcription](#analysis-not-transcription) — the fixed skeleton is the selection-asymmetry control; a free-form handoff cannot be audited for what it omitted.
- **A machine-readable format (YAML/JSON) instead of Markdown (considered, not chosen)**: would make handoffs queryable, but the artifact's primary reader is a session that reads prose, and a structured format raises the writing cost at exactly the point (session end) where the writer has least capacity for it. A structured extraction can be added later as tooling, the way the facet registry question is being handled for the meta-layer.
- **Timestamped entries like a changelog (rejected)**: a handoff's entries are the current state of a discussion, not a history of changes to it — the state is rewritten as the discussion moves, not appended to. If the history of the discussion's own evolution matters, that is what the discussion's eventual Changelog entries will record when its content graduates into governed documents.

## Results
Insufficient time has passed since this specification was adopted to report real, observed outcomes from its use. This section will be filled in once there is such experience to draw on.

## Discussion

### Drawbacks
The facet adds a fourth artifact kind to the documentation system — one more thing a contributor must understand and choose among. It also institutionalizes a writing obligation at session boundaries, where motivation to produce it is lowest; the quality controls in [Analysis, Not Transcription](#analysis-not-transcription) make the obligation heavier than the ad-hoc habit it replaces, by design. And the boundary between "handoff" and "early draft of the real document" is a real risk: a discussion that has effectively concluded should graduate into Explanation- and Changelog-facet documents, not persist as a handoff indefinitely — [Relationship to the Other Facets](#relationship-to-the-other-facets) states the boundary, but enforcing it requires judgment every time.

### Rationale and alternatives
- **Extend the Practice facet instead (a bigger practice document, no new facet) (rejected)**: a practice is meant to be *followed* to accomplish something; the handoff document's primary reader relationship is different — it is *consulted* to resume a discussion's state, and its structure serves a reader reconstructing state, not an agent executing steps. Forcing it into the Practice facet would repeat the schema mismatch the facet system was created to eliminate. The procedure for producing a handoff *is* practice content, and it lives in the paired practice file.
- **Extend the Changelog facet instead (rejected)**: a changelog is append-only history of an artifact's changes; a handoff is a mutable snapshot of a discussion's state. Append-only state-capture would force every refinement of a decision into a new entry, burying the current state under the discussion's own evolution — the reader needing "where do we stand" would have to reconstruct it from the deltas, which is the cost the artifact exists to avoid.
- **Leave the practice unformalized, relying on the existing practice documents only (rejected)**: the two prior practice documents structured the *writing* of handoffs but left the artifact itself with no governing specification, no name in the facet system, and no defined relationship to the other facets — every structural decision they carried (confidence vocabulary, required sections, one-topic-per-file) was informal convention. This document absorbs that content, formalizes it, and gives the pattern the same named, extensible treatment the other facets have.

### Prior art
The telecommunications handover and healthcare change-of-shift literatures are the concept's established homes (see Prior art under [What a Handoff Is](#what-a-handoff-is)). Meeting-minutes and decision-log practice is the closest documentation-side tradition. Within AI-assisted development specifically, handoff/context-summary conventions have begun appearing in ecosystem tooling — evidence of the need, though those conventions are typically free-form and unstructured in exactly the ways [Analysis, Not Transcription](#analysis-not-transcription) warns against.

### Unresolved questions
1. Does a handoff ever warrant its own companion changelog — for example, when a handoff is long-lived across many sessions and its own evolution becomes worth auditing? The Changelog facet's recursion stop applies to `.changelog.md` files themselves; whether it should extend to long-lived `.handoff.md` files is unexamined.
2. Should handoff files live beside their base documents in `docs/`, or in a separate directory — and does the answer change when the base artifact is outside `docs/`? File placement interacts with the repository's naming conventions and is not settled here.

### Future possibilities
- Tooling could validate a handoff against its skeleton (required sections present, confidence vocabulary used correctly) the same way a linter checks document structure — proposed, not designed.
- A handoff whose topic concludes could trigger the documentation-update proposal the Documentation Improvement workflow defines — the graduation path from discussion state to governed documents, made mechanical.

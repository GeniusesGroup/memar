---
name: documentation-handoff
description: defines how a handoff between sessions is produced and consumed
---

# Documentation — Handoff Practice

> **Purpose:** This practice defines how a handoff is produced at the end of a session and how it is consumed at the start of the next one. It is the procedural companion to [documentation-handoff.md](./documentation-handoff.md), which defines what a handoff is, why its structure is what it is, and the risks it controls — that document is assumed reading, and its rules are not restated here.

---

## When This Practice Applies

Produce a handoff when a session ends with any of these true:

- the discussion reached decisions or resolutions worth preserving
- ambiguities were resolved whose reasoning would otherwise be lost
- open questions or assumptions exist that a future session needs to know about
- the topic will continue in a later session, or a different agent may pick it up
- the session's work touched other artifacts in ways those artifacts do not yet reflect

Do not produce a handoff when:

- the exchange was trivial (simple Q&A, quick factual answer)
- nothing was decided, resolved, or opened
- no continuation is anticipated
- everything the session concluded has already graduated into governed documents (see the graduation rule in [documentation-handoff.md → What a Handoff Is](./documentation-handoff.md#what-a-handoff-is))

---

## Producing a Handoff

1. **Inventory the session against the skeleton.** Walk the section list in [documentation-handoff.md → Structure](./documentation-handoff.md#structure) and ask, for each: did this session produce anything in this category? This walk is the selection-asymmetry control — omissions happen section by section, visibly, not by habit.
2. **Mark confidence while it is fresh.** Assign each decision its confidence level (Decided / Tentative / Explored-but-unresolved / Deferred) and each assumption its stability (Strong / Weak / Unexamined) before the session's actual certainty fades — category drift (tentative hardening into decided) is the most common distillation error, and it happens in the minutes after the discussion, not later.
3. **Capture reasoning with every decision.** What options existed, what criteria were used, what tipped the balance. A decision without reasoning cannot be safely revised or defended by the receiving session.
4. **Record dissent and rejected alternatives.** Where a conclusion had competing considerations, they travel with the conclusion — this preserves nuance and prevents future re-litigation of settled issues.
5. **Link artifacts and sources.** Reference the documents, models, chat logs, or transcripts the discussion drew on or affected, with the action needed on each (None / Update / Review / Create).
6. **Apply the file format.** Name it `<base>.handoff.md` (or a dated topic-named file for conversations not tied to one document — see [documentation-handoff.md → File Format](./documentation-handoff.md#file-format) and the placement note below). Write only sections with content; leave no empty headers.
7. **Self-check against the reader who was not there.** Re-read the draft as the next session will: could a session with no memory of this discussion pick up every thread from this file alone? Anything answered "no" goes back to step 3.

### Placement

- Handoffs paired with a governed base document live beside it (`<base>.handoff.md` next to `<base>.md`).
- Handoffs for discussions not yet tied to a governed document live in the project's conversation-records location (`chats-context/`), named `YYYY-MM-DD-topic-name.md`, one topic per file — a multi-topic discussion is split into one handoff per topic so each can resume, conclude, and retire independently.

---

## Consuming a Handoff

At the start of a session that continues from a handoff:

1. **Read it completely before responding.** A partial read defeats the artifact — the sections are interdependent (an assumption may qualify a decision; an open question may block a next step).
2. **Acknowledge the state before advancing.** State the decisions you are building on and their confidence levels, so misreadings surface at the start rather than mid-work.
3. **Do not re-argue Decided points unless asked or unless new evidence exists.** Tentative points may be revisited — that is what the marker means. Re-arguing without new evidence repeats the cost the handoff was produced to avoid.
4. **Update the handoff as the session moves the state.** New decisions are added with their confidence; resolved questions move to Ambiguities Resolved; a changed direction rewrites the affected sections. The handoff is a living state-capture, not an append-only history — stale state is worse than absent state, because it is trusted.
5. **Graduate conclusions when they stabilize.** When a decision hardens into settled design, propose it into the governing Explanation-facet document, and wait for approval before modifying project documents. A documentation-improvement proposal:
   - identifies the **exact document and section**, and provides **replacement-ready text in English** (the project's documentation language);
   - states **what ambiguity the change resolves** — documentation serves understanding, not volume: an addition that answers no currently-unanswerable question is not an improvement;
   - names its **type**: ambiguity resolution (existing text can be read multiple ways), gap filling (something is missing or incomplete), decision recording (a concluded decision is not yet captured), terminology alignment (the same term carries different meanings across documents), or structural improvement (organization hinders comprehension);
   - keeps proposed text **self-contained, precise, defined** (key terms defined or referenced), and **cross-referenced** (related documents and terms linked, not left for the reader to find).

---

## Quality Checklist

Before closing a handoff, verify:

- [ ] Every decision carries reasoning and a confidence level
- [ ] Every resolved ambiguity records *how* it was resolved, not only the verdict
- [ ] Every open question states why it matters and whether it blocks
- [ ] Every assumption states its stability and the consequence of its failure
- [ ] Rejected alternatives and dissenting considerations are recorded where they existed
- [ ] Next steps are ordered with dependencies
- [ ] The confidence vocabulary is used as defined (no invented levels)
- [ ] A session with no prior participation could resume from this file alone

---

## Relation to Other Artifacts

| Artifact | Connection |
|----------|-----------|
| [documentation-handoff.md](./documentation-handoff.md) | Governing specification — the concept, structure, and rationale this practice follows |
| [documentation-explanation.md](./documentation-explanation.md) | Conclusions that stabilize graduate from a handoff into Explanation-facet documents |
| [documentation-changelog.md](./documentation-changelog.md) | Graduated changes are recorded in the base artifact's changelog; handoffs and changelogs reference each other but do not absorb each other |

---

*This Practice is part of the Memar project collaboration framework. It should evolve as the project's collaboration patterns become clearer.*

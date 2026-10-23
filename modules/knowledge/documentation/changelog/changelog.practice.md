---
name: documentation-changelog
description: procedures for writing a Changelog-facet entry and for obtaining the independent review an `approved` tag requires — how to ask, what a verdict must contain, and how to record the outcome; use whenever a task is about to record an observed change, or is about to write `approved`. Not the field shapes, the state vocabulary, or the approval rule, which changelog.md holds, and not where an unfinished withheld verdict goes, which the documentation-handoff practice says
---
# Documentation Changelog Practice
> **Purpose:** Followable procedures that [changelog.md](./changelog.md) presupposes but does not itself contain — what a verdict is, how one is obtained, and what happens to the entry either way. The field shapes, the state vocabulary, and the approval rule live in that document and are not restated here.

## Recording an approval
The obligation is [Approval Requires a Reviewer Who Did Not Do the Work](./changelog.md#approval-requires-a-reviewer-who-did-not-do-the-work): three conditions, and all three are required. This section is how a task satisfies them.

1. **Decide whether the change is one that can be approved.** Where a command can show the claim false if it were false, an independent verdict earns what it costs. A change the claim is about reading — a wording fix, a broken link, a rename — can still be approved on a verdict that rests on reading, but rarely earns the second party; your own check of it is what decides whether it is right. When it is unclear, ask the reviewer; that question is one of the things the reviewer is for.
2. **Ask a reviewer that did not do the work.** The request carries four things and no more:
   - **the claim** — the one sentence the entry makes about what now holds, quoted from `What changed` rather than paraphrased, since a paraphrase is what the review then cannot check;
   - **the evidence** — where a command can show the claim false if it were false, that command named exactly as it is to be run, including the working directory it needs; where reading decides the claim, the passages the reviewer is to read against it;
   - **the boundaries** — what the reviewer is *not* to consider, so it does not spend the task reviewing a decision you have already made;
   - **the verdict asked for** — permission to write `approved`, or a reason it is withheld.
   A brief that names neither a command nor the passages to read produces an opinion, and an approval resting on an opinion establishes nothing.
3. **Read the verdict as a finding, not as a gate.** Three outcomes, and the third is the most useful:
   - *Permitted* — write `approved` with the reviewer's name, and record in `What changed` what the verdict examined and what it found, including any command it ran and what came back, so a later reader weighs the same evidence and reaches the verdict in its own mind rather than trusting this one.
   - *Withheld, with a reason* — write no `approved`; carry the reason into the entry, under `Considered and not done` if the reason is that a position was rejected, or into the paired handoff's open questions if the work is unfinished. An entry left unapproved is the correct state for unchecked work, not a gap to tidy.
   - *Withheld, because the evidence itself was wrong* — the command named does not exist, does not run, or passes for a reason unrelated to the claim. That is a defect in the change, and it is the outcome worth having: it was found before the entry was written rather than by whoever reads it next.
4. **Do not re-ask the same reviewer after changing the work.** A reviewer that has already seen the claim has a model of it, which is the thing the separation exists to avoid. Where the work changed materially, the review is a new review by a party that has not seen the earlier version.

## Choosing who reviews
The rule requires independence from the work, not a roster. In this project's practice that is a sub-agent given the four things above, because a sub-agent starts without the task's context and therefore without the task's model of what it meant. Two consequences follow and both are worth stating:

- **The reviewer is a second cognitive system, not a second pass by the first.** Re-reading your own work carefully is not review; it is the same reader with the same model, and it will find what it expected. Where a runtime offers no second system, the honest outcome is no `approved`.
- **A smaller or cheaper model is usually the right reviewer** for a bounded claim with named evidence, because the review is a comparison against a stated expectation rather than a design judgment, and independence matters more here than depth.
- **The same four-part request serves an in-task second opinion even when no `approved` tag is sought.** Claim, evidence, boundaries, verdict asked for — the verdict is then recorded into the handoff or the decision's reasoning rather than into a changelog entry.

## What this is not
This procedure produces an audit by a party that did not do the work, over evidence it gathered and weighed itself. That is the strongest scrutiny available inside one collaboration, and [Terminology → On Independent Verification, Today](../../../../docs/terminology.md#on-independent-verification-today) states what it is worth against an outside institution. An `approved` tag records that a second party checked. It does not record that the work is correct, and no reader should treat it as more than the first of those two statements.

## Relation to Other Artifacts
| Artifact | Connection |
|----------|-----------|
| [changelog.md](./changelog.md) | Governing specification — the field shapes, the state vocabulary, and the approval rule this procedure carries out |
| [handoff.practice.md](../handoff/handoff.practice.md) | Where a withheld verdict goes when the work is unfinished rather than rejected |
| [documentation.md → Results routing](../documentation.md#results-routing) | Which home a given durable result takes, decided by its type |

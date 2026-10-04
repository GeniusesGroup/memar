---
name: documentation-changelog
description: procedures for writing a Changelog-facet entry and for obtaining the independent review an `approved` tag requires — how to ask, what a verdict must contain, and how to record the outcome; use whenever a session is about to record an observed change, or is about to write `approved`
---
# Documentation Changelog Practice
> **Purpose:** Followable procedures that [documentation-changelog.md](./documentation-changelog.md) presupposes but does not itself contain — what a verdict is, how one is obtained, and what happens to the entry either way. The field shapes, the state vocabulary, and the approval rule live in that document and are not restated here.

## Recording an approval
The obligation is [Approval Requires a Reviewer Who Did Not Do the Work](./documentation-changelog.md#approval-requires-a-reviewer-who-did-not-do-the-work): three conditions, and all three are required. This section is how a session satisfies them.

1. **Decide whether the change is one that can be approved.** A change whose correctness is a matter of reading — a wording fix, a broken link, a rename — is not improved by a review that has to judge what the words were trying to say. A change whose claim is that something now behaves in a stated way is. When it is unclear, ask the reviewer; that question is one of the things the reviewer is for.
2. **Ask a reviewer that did not do the work.** The request carries four things and no more:
   - **the claim** — the one sentence the entry makes about what now holds, quoted from `What changed` rather than paraphrased, since a paraphrase is what the review then cannot check;
   - **the evidence** — the command whose output would show the claim false if it were false, named exactly as it is to be run, including the working directory it needs;
   - **the boundaries** — what the reviewer is *not* to consider, so it does not spend the session reviewing a decision you have already made;
   - **the verdict asked for** — permission to write `approved`, or a reason it is withheld.
   A brief that omits the evidence produces an opinion, and an approval resting on an opinion establishes nothing.
3. **Read the verdict as a finding, not as a gate.** Three outcomes, and the third is the most useful:
   - *Permitted* — write `approved` with the reviewer's name, and record in `What changed` what it ran and what came back, so a later reader can re-run it rather than trust it.
   - *Withheld, with a reason* — write no `approved`; carry the reason into the entry, under `Considered and not done` if the reason is that a position was rejected, or into the paired handoff's open questions if the work is unfinished. An entry left unapproved is the correct state for unchecked work, not a gap to tidy.
   - *Withheld, because the evidence itself was wrong* — the command named does not exist, does not run, or passes for a reason unrelated to the claim. That is a defect in the change, and it is the outcome worth having: it was found before the entry was written rather than by whoever reads it next.
4. **Do not re-ask the same reviewer after changing the work.** A reviewer that has already seen the claim has a model of it, which is the thing the separation exists to avoid. Where the work changed materially, the review is a new review by a party that has not seen the earlier version.

## Choosing who reviews
The rule requires independence from the work, not a roster. In this project's practice that is a sub-agent given the four things above, because a sub-agent starts without the session's context and therefore without the session's model of what it meant. Two consequences follow and both are worth stating:

- **The reviewer is a second cognitive system, not a second pass by the first.** Re-reading your own work carefully is not review; it is the same reader with the same model, and it will find what it expected. Where a runtime offers no second system, the honest outcome is no `approved`.
- **A smaller or cheaper model is usually the right reviewer** for a bounded claim with named evidence, because the review is a comparison against a stated expectation rather than a design judgment, and independence matters more here than depth.

## What this is not
This procedure produces an audit by a party that did not do the work, using evidence it ran itself. That is the strongest scrutiny available inside one collaboration, and [Terminology → On Independent Verification, Today](./terminology.md#on-independent-verification-today) states what it is worth against an outside institution. An `approved` tag records that a second party checked. It does not record that the work is correct, and no reader should treat it as more than the first of those two statements.

## Relation to Other Artifacts
| Artifact | Connection |
|----------|-----------|
| [documentation-changelog.md](./documentation-changelog.md) | Governing specification — the field shapes, the state vocabulary, and the approval rule this procedure carries out |
| [documentation-handoff.practice.md](./documentation-handoff.practice.md) | Where a withheld verdict goes when the work is unfinished rather than rejected |
| [documentation.md → Results routing](./documentation.md#results-routing) | Which home a given durable result takes, decided by its type |

---
Title: "Documentation — Approval"
Status: Proposed
Start Date: 2026-10-31
ID: 502810
---

# Documentation — Approval
This document specifies the Approval template: the shape of a content of kind `approval` placed in the timeline of a task, in which a reviewer who did not do the work gives a verdict on another content of the timeline. It names no file, directory, path or file name. An approval is its own kind and not a part of the content it judges: it is a judgement about that content's correctness, made by another party at another time, and the content it judges is never edited to carry it.

## Abstract
An approval content names the content it judges, the reviewer's verdict, and what the reviewer examined and found. The reviewer is the placer of the approval. Three conditions bind it, and all three are required: the reviewer did not do the work, the reviewer returns a verdict and not an impression, and without a verdict there is no approval.

## Explanation
### Reader relationship
Content meant to be *consulted* by a reader who needs to know whether a second party checked a claim, who that party was, and on what. The reader is given the verdict and its evidence, not the work.

### Template
| Field | Holds |
|---|---|
| Judges | The placement (number) of the content in this timeline, or the reference to the content in another, that the verdict is about |
| Verdict | `approved` or `withheld` |
| Examined | What the reviewer compared against what, and what it found; the command and what it returned where a command can show the claim false |
| Reason | Required when the verdict is `withheld`: why permission is refused |

The reviewer is the placer. A person's approval is a content placed by that person; a comment by a user with the CTO role that approves a decision is an approval in this sense, and a `decision` may cite it ([Handoff](../handoff/handoff.md)).

### Approval Requires a Reviewer Who Did Not Do the Work
`approved` is a **judgement about a content's own correctness**, and it is separated from the rest for the same reason Test → What a Passing Suite Establishes (`modules/process/test/test.md#what-a-passing-suite-establishes`) separates what a green run proves from the claim that the work is finished: the party that performed the work cannot judge it, because it holds the model of what it meant to do and reads its own output as that model.

1. **The reviewer did not do the work.** An agent that authored, edited, or drafted the change may not approve it. Where the work was done by one cognitive system, the reviewer is another — in this project's practice, a sub-agent given the claim to assess and the evidence to assess it from. That is the internal-audit half of how certification actually works: the body that performs the work is not the body that audits it.
2. **The reviewer returns a verdict, not an impression.** A verdict is the reviewer's own comparison of what now holds against what the content claims, and it names what it examined and what it found; where a command can show the claim false if it were false, the verdict names that command and what it returned. A verdict may rest on reading alone where reading decides the claim, but an opinion naming nothing examined has established nothing, and an approval resting on it is the unverified claim wearing a verified one's name. What keeps the approval from becoming self-certification is the first condition, not the presence of a command.
3. **No verdict, no `approved`.** Where the reviewer withholds permission, the approval carries `withheld` and the reason. A content left without an approval is the correct state for work that has not been checked, and is not a defect to be tidied away.

This is not a certificate. An audit by a party that did not do the work, over evidence it gathered and weighed itself, is the strongest form of scrutiny available inside one collaboration, and [Terminology → On Independent Verification, Today](../../../../docs/terminology.md#on-independent-verification-today) states plainly what that is worth against an outside institution. The approval records that a second party checked; it does not record that the work is correct in general.

---
Title: "Approval Rule — A Review Request Has Four Parts"
Start Date: 2026-11-01
---
# Approval Rule — A Review Request Has Four Parts
A rule of this repository, held for [Approval](../../approval.md), which owns the claim in [Approval Requires a Reviewer Who Did Not Do the Work](../../approval.md#approval-requires-a-reviewer-who-did-not-do-the-work). This rule states what a request to a reviewer carries.

## The rule
A request for a verdict carries four things and no more:
- **The claim.** The one sentence the content makes about what now holds, quoted from the content and not paraphrased, because a paraphrase is what the review then cannot check.
- **The evidence.** Where a command can show the claim false if it were false, that command named exactly as it is to be run, with the working directory it needs; where reading decides the claim, the passages the reviewer is to read against it.
- **The boundaries.** What the reviewer is not to consider, so it does not spend the review on a decision already made.
- **The verdict asked for.** Permission to approve, or a reason it is withheld.

The same four parts serve a second opinion asked for inside a task when no approval is sought. The verdict is then recorded in the reasons of a `decision` content, or as a `question` or `assumption` content, and not in an approval.

## Why it exists
A request that names neither a command nor the passages to read produces an opinion, and an approval resting on an opinion establishes nothing. The review of a bounded claim with named evidence is a comparison against a stated expectation and not a design judgment, so independence matters more there than depth, and [the model follows the need](../../../../../management/task/rules/model-follows-need/model-follows-need.md): a lower level is usually enough.

## Keep it or drop it
An organization may let a request say "please review this". It then gets what each reviewer chooses to examine, and cannot tell a verdict on the claim from a verdict on something nearby.

## What this rule does not claim
- It does not fix a form for the request; the four parts may be a message or a plan.
- It does not say how large the request is beyond "no more": a fifth part, such as the history of the work, hands the reviewer the model the separation exists to avoid.

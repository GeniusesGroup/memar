---
Title: "Approval Rule — A Verdict Is a Finding, Not a Gate"
Start Date: 2026-11-01
---
# Approval Rule — A Verdict Is a Finding, Not a Gate
A rule of this repository, held for [Approval](../../approval.md), which owns the claim in [Approval Requires a Reviewer Who Did Not Do the Work](../../approval.md#approval-requires-a-reviewer-who-did-not-do-the-work). This rule states how a task reads and records the verdict it receives.

## The rule
A verdict has one of three outcomes, and the task records each in the way below.
- **Permitted.** The approval is placed with the reviewer as its placer, and its Examined field states what the verdict examined and what it found, including each command run and what came back, so a later reader weighs the same evidence and reaches the verdict in its own mind and does not trust this one.
- **Withheld, with a reason.** The approval carries `withheld` and the reason. Where the reason is that the work is unfinished, the task places a `question` or `anticipated-work` content for it; where a position was rejected, the rejected alternative goes to the Options of a `decision` content. A content left without an approval is the correct state for unchecked work and not a gap to tidy.
- **Withheld because the evidence itself was wrong.** The command named does not exist, does not run, or passes for a reason unrelated to the claim. That is a defect in the change found before anyone else met it, and it is the most useful outcome.

## Why it exists
A verdict read as a gate is pursued until it opens, and the reviewer's reasons are dropped when it does. Read as a finding, each outcome tells the task something it did not know.

## Keep it or drop it
An organization may treat a withheld verdict as an obstacle and ask again until one permits. It then collects approvals that say only that someone, once, did not object.

## What this rule does not claim
- It does not say which outcome a given claim should get; that is the reviewer's comparison.
- It does not say when a withheld content is answered; a later content that refers to it does ([Changelog → Never edited, corrected by a new record](../../../changelog/changelog.md#never-edited-corrected-by-a-new-record)).

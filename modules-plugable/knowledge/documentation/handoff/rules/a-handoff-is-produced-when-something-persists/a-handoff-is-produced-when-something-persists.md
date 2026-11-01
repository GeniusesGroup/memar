---
Title: "Handoff Rule — A Handoff Is Produced When Something Persists"
Start Date: 2026-11-01
---
# Handoff Rule — A Handoff Is Produced When Something Persists
A rule of this repository, held for [Handoff](../../handoff.md), which owns the claim in [What a Handoff Is](../../handoff.md#what-a-handoff-is). This rule states when a task places the contents that carry a discussion's state.

## The rule
- **A conversation ends when the person who started it declares the work finished,** not when one reply or one task is complete; until then its state is kept. A task is narrower than a conversation and ends when its check passes or it stops.
- **When a task or a conversation ends with any of these true, its state is placed as `question`, `decision`, `assumption` and `anticipated-work` contents:**
  - the discussion reached decisions or resolutions worth preserving;
  - ambiguities were resolved whose reasoning would otherwise be lost;
  - open questions or assumptions exist that a future task needs to know about;
  - the topic will continue in a later task, or a different agent may pick it up;
  - the work touched other artifacts in ways those artifacts do not yet reflect.
- **None is placed when** the exchange was trivial, nothing was decided, resolved or opened, no continuation is anticipated, or everything the task concluded has already graduated into governed documents.

## Why it exists
A handoff costs the writer a distillation and the reader a reading. Where nothing persists it costs both and carries nothing; where something does, its absence costs the next task the context, the settled points and the ambiguities already resolved.

## Keep it or drop it
An organization may place the contents at the end of every task. It then fills the timeline with contents that decide nothing, and the contents that do are harder to find.

## What this rule does not claim
- It does not say what a tangent found mid-task becomes; that is not decided here.
- It does not make an empty result an artifact: a task with nothing to hand over places nothing ([Written surface](../../../documentation.md#written-surface)).

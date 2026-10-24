---
Title: "Forked Sub-Agent"
Status: Draft
Start Date: 2026-10-15
ID: 497795
---

# Forked Sub-Agent

## Abstract
This document states Memar's position on one capability of an agent runtime that Memar does not own: a **sub-agent started as a fork of its parent's context at a chosen point**, rather than as a cold start. The runtime is outside Memar's authority, so the document records an expectation and the conditions on which a task Memar governs may rely on it, not a requirement Memar can enforce. The expectation has five parts: the parent marks a point in its context and starts K children (say 10) that each begin with exactly the context up to that point and then a short task of their own; the shared part is paid for once and read by every child at the cheaper read price; each child works apart from the parent and returns only its answer, which the parent appends to its own context; from any earlier marked point the parent may start another wave while earlier children run on unaffected; and parent and children, of every wave, share the prefix up to their fork point. The reason is cost and quality: a cold child pays again, at the write price, for the skill and the documents the parent already read, which pushes work into few large tasks, and a brief cannot carry the rules the parent has read. The document carries the open questions about the mechanism that Memar cannot answer from outside, and states what Memar does until the capability is offered. Nothing here is a claim that any runtime offers it.

## Introduction

### Motivation
Memar's operating practice asks every agent to load the Memar skill and the governing documents of each step before acting, and asks a delegating task to hand a sub-agent only a brief while the whole task is written in the sub-agent's plan (`memar task ensure --help`). A sub-agent therefore starts cold: it knows what its brief and plan say, and it pays to load the skill and the documents again. Two failures follow, and both are failures of the runtime's shape, not of the agents.

1. **The same material is paid for once per child.** The prefix a cold child reads is the same tens of kilobytes every time, yet a prefix cache reuses only a prefix that is unchanged, and a child's brief comes first and differs from child to child. The material that follows the brief cannot be a hit across children, so each child pays the full write price for what the parent has already paid for. The cost of loading, set against the size of the task, then decides how work is cut: tasks are made few and large to amortize the load, and a small, well-isolated task costs more to start than to do.
2. **A brief restates, and a cold child can still miss.** What a sub-agent knows is what the delegator wrote down for it ([Agency → Context](../../../docs/agency.md#context)). The rules the parent has read are not in a cold child's context unless the brief repeats them, and a brief that repeats them is a second copy to keep consistent with the first.

### Methodology
The document consumes [Agency](../../../docs/agency.md) and [Cognition](../../../docs/cognition.md) and adds no definition to either. It was modeled as [Modeling Practice](../../../docs/modeling.practice.md#the-modeling-workflow) asks, before it states anything: the concepts are listed under [Concepts](#concepts), each treated as provisional; the responsibility boundary between Memar and the runtime is drawn under [What Memar Owns and What the Runtime Owns](#what-memar-owns-and-what-the-runtime-owns); and the questions the modeling raised are in the paired [handoff](./forked-subagent.handoff.md). The cost reasoning is stated under [Cost](#cost) in terms of prices, not of any vendor's figures, since a figure is a runtime's to publish and changes.

## Explanation

### Position
A runtime that offers it makes a sub-agent available in two relations to its parent's context, not one.

- **A cold start**: the child's context is its brief. Everything the child needs is written for it.
- **A fork**: the child's context is the parent's context up to a marked point, followed by the child's own task.

Both are [delegation](../../../docs/agency.md#delegation) of a responsibility to an Agent; they differ in what [Context](../../../docs/agency.md#context) the delegator hands over, and neither changes who stays accountable. Memar's position is that an agent runtime serving Memar's work should offer the fork, because the work Memar describes — many independent checks, reviews, searches, and per-file edits from one prepared context — is the case the fork serves, and because the cold start remains right where the child must *not* inherit the parent's context.

### Concepts
Each is provisional until the open questions in the handoff that touch it are settled.

- **Parent.** The agent whose context is forked. It loads what the work and all its sub-agents need, then marks.
- **Fork point.** A marked position in the parent's context. It is a position, not a copy: what lies before it is shared by everything started from it.
- **Child.** A sub-agent started at a fork point. Its context is the shared prefix plus its own task, and it grows apart from the parent's thereafter.
- **Wave.** The K children started from one fork point together. A parent may start any number of waves, each from a fork point of its own choosing, including one marked earlier.
- **Answer.** What a child returns. It is the child's whole contribution to the parent's context; the child's working is not.
- **Shared prefix.** The context from the start up to a fork point, common to the parent and to every child of every wave started at or after that point.

### The Expectation
A runtime serving Memar's work is expected to meet each of these. They are stated so that whether a runtime meets them can be decided by a party that did not write them, from what the runtime does.

1. **Fork from a point.** The parent can mark a point in its context and start K children from it. Each begins with exactly the parent's context up to the point, then a task of its own, and K may be at least 10.
2. **One shared prefix in the cache.** The shared prefix is written to the cache once and read by every child, within the cache's life, at the read price. A child's task comes after the shared prefix, never before it.
3. **Children work independently and answer.** A child's working stays in the child. Only its answer returns to the parent, and the parent appends the answers to its own context.
4. **Fork again from any earlier point.** From a marked point the parent can start another wave without disturbing children still running from an earlier one. A running child continues on its own context, unaffected by later forks and by the parent's later turns.
5. **Everything shares the common part.** The parent and the children of every wave share the prefix up to their fork point.

What the expectation does not say: how a point is marked, how many children may run at once, whether a child may itself fork, or what the answer's shape is. Those are the runtime's, and where Memar's work needs one of them it is a question in the handoff.

### What Memar Owns and What the Runtime Owns
The runtime owns the mechanism: the cache, the marking, the starting, and the price. Memar owns two things and states them so the runtime's choices do not decide them by default.

- **What is loaded before the point.** The parent loads, before the point, what the work and *all* its sub-agents need and nothing a single child needs, since the shared prefix is shared by all. What belongs there is the work's own skill and governing documents, as [Consult the governing document before each act](../../../.agents/skills/memar/SKILL.md#consult-the-governing-document-before-each-act) gives them; a child's own governing documents, beyond the common ones, are read by the child after the point, at the price of its own context.
- **Whose accountability the child's answer carries.** A fork changes what the child knows, not who is accountable. The delegating task reads a child's answer as a claim, as it reads a cold child's report ([Treat shared artifacts as claims](../../../docs/cognition.md#treat-shared-artifacts-as-claims-under-the-same-evaluation-not-as-absolute-authority)): what the child inherited is the parent's reading, which is unverified for the child's step until the child reads the governing passage itself ([What Implementation Asymmetry Obliges](../../../docs/cognition.md#what-implementation-asymmetry-obliges)).

The fork also moves a risk the cold start did not carry: a child that inherits the parent's context inherits the parent's errors and assumptions with it. A reviewer asked to critique the work must not be a fork of the task that did the work ([choosing who reviews](../../knowledge/documentation/changelog/changelog.practice.md#choosing-who-reviews)); a fork is for work whose independence from the parent's reasoning is not what is wanted.

### Cost
Let the shared prefix be of size S, the price of writing a token to the cache be W, the price of reading a cached token be R, with R less than W, and let K children be started within the cache's life.

- **Cold starts.** Each child loads the skill and documents itself, behind a brief that differs from the others'. The shared material is not a prefix hit across children, so it is paid at W by each: about K · S · W.
- **A fork.** The prefix is written once and read by the K children: about S · W + K · S · R.

The difference, (K − 1) · S · (W − R), grows with K, with S, and with the gap between the two prices, and it is what the load of the skill and documents costs a design that must start many children. Three consequences, each conditional on the figures a runtime publishes and on the open questions below:

- **The pressure toward few large tasks weakens.** Today the cost of loading is amortized by making a task big. If the load is paid once for many children, a task can be as small as its own check, which is what [Sizing a Task and Recording Follow-Ups](../../knowledge/documentation/handoff/handoff.practice.md#sizing-a-task-and-recording-follow-ups) already prefers on other grounds.
- **A failed child is cheap to redo.** It is discarded and started again from the same point at the read price; the parent's context is not touched by the child's working.
- **The advantage has a lifetime.** The saving holds for children started within the cache's life; a wave started after the prefix has expired pays the write price again. The lifetime is therefore part of the cost, and is the first open question.

The reasoning is the cost of a step over the whole work, rework included, as [Task and plan](../../../.agents/skills/memar/SKILL.md#task-and-plan) states it, not the tokens of one task. It does not argue that a fork is always cheaper: a task whose child needs little of the shared prefix pays to read what it does not use, and a prefix grown large by loading what only some children need is a cost to all of them.

### What Memar Does Until a Runtime Offers It
Memar sizes a task by the cost of loading the skill against the size of the task, and batches related tasks into one agent where they share what they read. This is a workaround for the missing capability, not a position on how work should be cut, and it is the part of Memar's practice that the capability would make unnecessary for the read-heavy case. Where a runtime offers a fork, nothing in Memar's documents forbids using it; the delegating task still opens each child's task, writes its task, and reads its answer as a claim.

### Relationship to Other Concepts
- [Agency](../../../docs/agency.md): the fork is a delegation whose handed Context is the delegator's own, up to a point.
- [Cognition](../../../docs/cognition.md): the parent's context is a budget, and the answers a parent appends are what grows it; a fork keeps the children's working out of it.
- [Modeling](../../../docs/modeling.md): this document records an expectation about a surface outside Memar and does not model a module of Memar's, which is why it is here and not in a category of [Modules](../../../modules/README.md).

### Open Questions
The questions Memar cannot answer from outside are carried in the paired [handoff](./forked-subagent.handoff.md), where they are revised as they are answered: whether a fork's shared prefix is a cache hit for every child started within the cache's life and what that life is; what happens to a running child when the parent's context is compacted; whether a child can be told that it is a fork and must not fork further; and whether a `fork` agent type that some builds' tool descriptions mention is this capability.

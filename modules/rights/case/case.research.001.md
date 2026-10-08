# Case Research 001 — One UUID as case, group, and task

## Table of Contents

- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
- [Open Questions](#open-questions)

## Status

Active

## Question and Goals

- **Questions**
  - Is one UUID at once a case, a group, and a task? Status: `Open`. Omid Hekayati stated this on 2026-09-27 as a premise: the case UUID is a group so it can be a timeline, and a task so a judge can assign an expert. It is not a settled type identity.
- **Goals**
  - Record the premise and what would falsify it. Status: `Met`. Adopting the type identity is outside this research.
- **Scope**: the type identity of one case UUID. Human-language reasons are already decided to be timeline texts on the case; this research does not reopen that. Arbitration versus adjudication is out of scope.

## Participants

- [Omid Hekayati](../../../CONTRIBUTORS.md) — Questioner. Reviewer: Not yet reviewed.
- [Grok](../../../CONTRIBUTORS.md) — Researcher, 2026-09-27. Reviewer: Not yet reviewed.

## Methodology

One reasoning pass. Sources are his premise of 2026-09-27 and the recorded group, task, and timeline models: a group is a user type by `(user)-[:group]`, an organization is a user type by `(user)-[:organization]`, task is recorded as an additive entity over a group and also as content, and a timeline is recorded as `(group)-[:---]->(timeline)`, usable as a channel id for texts in time order. The timeline handoff still asks whether a timeline is an independent entity and whether a task decomposes into group, content, relation, state, and permission. No source was asked to confirm the premise. A falsifier below is a test, not a verdict.

## Findings

The premise stands until one of the following is shown. None of them is shown by this pass.

- Case, group, and task already have different recorded jobs. A case is the dispute that carries parties, votes, and a ruling. A group carries membership. A task is a piece of work assigned against skill, and the group record calls task additive over a group rather than identical with the group. The premise fails if one UUID must accept a group operation or a task operation that a case must not undergo, including breaking the assigned team at the end of the task, or a parent-group deletion, while the dispute, its votes, and its ruling remain.
- The recorded timeline edge runs from a group to a timeline. The timeline may be named by a UUID and used as the channel for texts in time order. The premise fails if the human-language reasons live on that timeline node and the case UUID is only the group at the other end, or if a case can carry those texts without being a group.
- The timeline handoff leaves open whether a task is a composition of a group plus content, relation, state, and permission. The premise fails if assigning an expert is that composition and the case UUID is only one part of it.
- The same handoff leaves open whether a timeline is an independent entity. The premise fails if the texts do not need the case to be a group, a task, or a timeline node.

## Open Questions

- Is one UUID at once a case, a group, and a task? Status remains `Open`. Graduation into the case explanation waits on a verdict this research does not give.

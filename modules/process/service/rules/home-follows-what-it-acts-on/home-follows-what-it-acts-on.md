---
Title: "Service Rule — A Service's Home Is the Domain of What It Acts On"
Labels: Draft
Start Date: 2026-11-05
---
# Service Rule — A Service's Home Is the Domain of What It Acts On
A rule of this repository, held for [Service](../../service.md). Owner (2026-11-05, task 20261105-T064658Z-1260), from the move of the filesystem services; it is the first step of [Modularity Rule — A Refactor Moves in Order](../../../../knowledge/modularity/rules/refactor/refactor.md).

## The rule
- **Before a service is declared, moved or rewritten, one question decides its home: what does it act on?** The service belongs to the module whose subject that is. Exact-text replacement acts on a text, so it is the text domain's, and it reaches a file only through the file adapter.
- **The home is not the folder the service stands in, the library it calls, or the tool it was first written for.** A service is not put in a domain because it was found there or because it calls that domain's code.
- **The module and its contract are stated before code,** and the owner of each concept and role the service plays is searched and imported, as [One Owner](../../../../knowledge/modularity/rules/one-owner/one-owner.md) says; the report says what was searched ([Modeling Practice → The Modeling Workflow](../../../../../docs/modeling.practice.md#the-modeling-workflow), eighth step).
- **A service that would join another domain's answers is a widget's work,** not its own ([Widget Aggregates](../../../../computer/ui/rules/widget-aggregates/widget-aggregates.md)); a missing abstraction of the owner is a task queued for the owner, not a local stand-in ([One Owner](../../../../knowledge/modularity/rules/one-owner/one-owner.md)).
- **What the service acts on is reached through the owner's port, not through a path.** When the service is rewritten it also leaves the filesystem ([A Rewritten Service Leaves the Filesystem](../rewrite-uses-memory-adapter/rewrite-uses-memory-adapter.md)).

## Why it exists
`content_edit` and `content_write` were moved into the filesystem domain because they stood in the filesystem folder, not because they act on files; they act on text. The move had to be done again (task 20261105-T064701Z-1260, decision 8 of timeline 20261101-T060800Z-24804). The question asked first costs one sentence; the wrong home costs a second move and a second repointing of every importer.

## Keep it or drop it
An organization may place services by the library they wrap and remain conformant to Memar's concepts, at the cost that a change of library moves the service and every caller of it.

## What this rule does not claim
- It does not name the domain of any service; each is decided by the question, from the service's code.
- It does not say how a service that acts on two subjects is split; that is a decomposition question ([Modeling Practice → The Modeling Workflow](../../../../../docs/modeling.practice.md#the-modeling-workflow)).
- It does not move a service by itself: the order of a move is [the refactor rule's](../../../../knowledge/modularity/rules/refactor/refactor.md).

---
Title: "Placements"
Status: Draft
Start Date: 2026-10-17
ID: 496333
---

# Placements
## Abstract
This document states how a module of any project built with Memar is placed: by which of three tests it stands under `modules/`, `modules-plugable/` or `bundles/`, and which [categories](../label/labels/category.md), any number, it is browsed under. The tests are the labels [Kernel](./labels/kernel.md), [Pluggable](./labels/pluggable.md) and [Bundle](./labels/bundle.md), each defined once in [`labels/`](./labels/), beside [Guest](./labels/guest.md), which a module of either of the first two may also carry. Every project that uses Memar follows these placements; a repository that places modules differently owes the reason in its own documents and cites this module for the difference. The `organization` repository, where the placements were first worked out, refers here for why its modules are placed as they are. The placements belong to [Modularity](./modularity.md) because they are its principles applied to a repository: a module that is optional for a system is pluggable for it, and a module the foundations cannot lose is kernel.

## Why placement is stated here
Where a module lives is a claim about what it is, and a claim about what a thing is belongs to the model, not to a repository's habit. Memar's own modules were once placed by transfer and by reading, with no argument recorded anywhere, and two answers to one question grew side by side: a shelf for modules that are not Memar's, and a placement for optional capabilities. This document holds the one answer, so that every document that places a module cites it instead of restating it. The meaning of each label is not kept here: a label is defined by the module that owns the claim it makes ([Label](../label/label.md)), and the placement labels are the claims of Modularity.

## The placements
| Placement | Where | The test |
| --- | --- | --- |
| [Kernel](./labels/kernel.md) | `modules/<path>/<module>/` | Removing it would force a foundational abstraction to be fabricated, or another to be distorted |
| [Pluggable](./labels/pluggable.md) | `modules-plugable/<path of the module it attaches to>/<capability>/`, or the category's own pluggable folder for a capability of the whole category | An optional capability that attaches through an explicit relationship and can be removed whole |
| [Bundle](./labels/bundle.md) | `bundles/<name>/` | Runs or aggregates modules, and states no responsibility of its own |

A module has exactly one placement. The placements are tests on the module's subject and are not a ranking: a pluggable module is not lesser than a kernel one, only optional for the system it attaches to ([Modularity → Core Structure and Optional Modules](./modularity.md#core-structure-and-optional-modules)).

A placement and a category are labels of different kinds, and they combine without nesting: a module that is `kernel` and `computer` is two true statements about it, which is why the same categories stand under both roots, at the same paths ([A Folder Is a Label](../label/rules/folder-label/folder-label.md)). A module's other labels, `guest` first, are written in its manifest ([Label → A module's labels](../label/label.md#a-modules-labels)).

## Rules
The rules this document's placements are checked against, one per directory under [`rules/`](./rules/README.md):
- [Placement](./rules/placement/placement.md) — what a module's place is checked against.
- [Kernel Neutrality](./rules/kernel-neutrality/kernel-neutrality.md) — a kernel module fixes no choice another organization may make otherwise.

The rule for how many levels a category may have, and for the mirror a pluggable module's path follows, is Label's, since a category is a label ([Category Depth](../label/rules/category-depth/category-depth.md)).

## What this document does not state
- **What a module is.** [Modularity](./modularity.md) defines it; this document only places one.
- **Where a module's files sit inside it.** That is the module layer's own account of role folders ([Modules → The kinds of folder here](../../README.md#the-kinds-of-folder-here)).
- **What a name or a label is.** That is [Label](../label/label.md)'s.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Modularity](./modularity.md) | Depends_on — module, optional module, pluggable behavior and foundational status | None (read) |
| [`modules/README.md`](../../README.md) | Reference — the layer these placements apply to | None (read) |
| [Label](../label/label.md) | Depends_on — what a label is, and the labels a module's manifest carries | None (read) |
| [`placements.handoff.md`](./placements.handoff.md) | Base — this document's open state | Follows this document |

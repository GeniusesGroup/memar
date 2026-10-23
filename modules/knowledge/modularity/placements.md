---
Title: "Classification"
Status: Draft
Start Date: 2026-10-17
ID: 497842
---

# Classification
## Abstract
This module states how a module of any project built with Memar is classified: where it is placed, in which namespace it is browsed, and which labels it carries. A module is placed by one of three tests — [Kernel](./primitive/kernel.md), [Pluggable](./primitive/pluggable.md), [Bundle](./primitive/bundle.md) — browsed under a one-level [Category](./primitive/category.md), and further classified by labels in its manifest, the first of which is [Guest](./primitive/guest.md). Every project that uses Memar follows these placements; a repository that places modules differently owes the reason in its own documents and cites this module for the difference. The `organization` repository, where the placements were first worked out, refers here for why its modules are placed as they are.

## Why classification is a module
Where a module lives is a claim about what it is, and a claim about what a thing is belongs to the model, not to a repository's habit. Memar's own modules were once placed by transfer and by reading, with no argument recorded anywhere, and two answers to one question grew side by side: a shelf for modules that are not Memar's, and a placement for optional capabilities. This module holds the one answer, so that every document that places a module cites it instead of restating it.

## The placements
| Placement | Where | The test |
| --- | --- | --- |
| [Kernel](./primitive/kernel.md) | `modules/<category>/<module>/` | Removing it would force a foundational abstraction to be fabricated, or another to be distorted |
| [Pluggable](./primitive/pluggable.md) | `modules-plugable/<category>/<capability>/` | An optional capability that attaches through an explicit relationship and can be removed whole |
| [Bundle](./primitive/bundle.md) | `bundles/<name>/` | Runs or aggregates modules, and states no responsibility of its own |

A module has exactly one placement. The placements are tests on the module's subject and are not a ranking: a pluggable module is not lesser than a kernel one, only optional for the system it attaches to ([Modularity → Core Structure and Optional Modules](../../../docs/modularity.md#core-structure-and-optional-modules)).

## Labels
A placement says where a module is. A **label** says something more about it, and a module carries as many labels as are true of it: a label is attached to a module the way a name is attached to content ([Label](../label/label.md)), and no label replaces the placement. Labels are written in the module's manifest, `<module>.manifest.yaml` beside its main document, in a `labels` field:

```yaml
labels:
  - guest
```

The manifest's other fields are not yet decided ([Open Questions](./classification.handoff.md#the-module-manifest-fields-beyond-labels)); `labels` is the one this module relies on. A label's meaning is a primitive of this module, one document per label. `guest` is the first; a label is added when a recurring claim about modules needs to be searched for, and a claim that is true of one module only is stated in that module's document.

## Rules
The rules this module holds work on, one per directory under [`rules/`](./rules/README.md):
- [Placement](./rules/placement/placement.md) — what a module's place is checked against.
- [Category Depth](./rules/category-depth/category-depth.md) — categories are one level.
- [Kernel Neutrality](./rules/kernel-neutrality/kernel-neutrality.md) — a kernel module fixes no choice another organization may make otherwise.

## What this module does not state
- **What a module is.** [Modularity](../../../docs/modularity.md) defines it; this module only places one.
- **Where a module's files sit inside it.** That is the module layer's own account of role folders ([Modules → The kinds of folder here](../../README.md#the-kinds-of-folder-here)).
- **What a name looks like.** A name is a label, and the rules for names are [Label](../label/label.md)'s.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Modularity](../../../docs/modularity.md) | Depends_on — module, optional module, pluggable behavior and foundational status | None (read) |
| [`modules/README.md`](../../README.md) | Reference — the layer these placements apply to | None (read) |
| [Label](../label/label.md) | Depends_on — what a label is | None (read) |
| [`classification.handoff.md`](./classification.handoff.md) | Base — this module's open state | Follows this document |

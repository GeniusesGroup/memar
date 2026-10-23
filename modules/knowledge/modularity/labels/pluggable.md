---
Title: "Pluggable"
Status: Draft
Start Date: 2026-10-17
ID: 496333
---

# Pluggable
## Abstract
**Pluggable** is the placement of a module that is an optional capability: it attaches to a kernel module, or to another pluggable one, through an explicit relationship, owns its complete capability, and can be installed and removed as a whole while the module it attaches to stays whole. A pluggable module sits at `modules-plugable/<category>/<capability>/`. The word describes an architectural relationship and not a plugin mechanism ([Modularity → Pluggable Does Not Mean Plugin](../modularity.md#pluggable-does-not-mean-plugin)): a pluggable module may be compiled into the same artifact and live in the same repository as the module it attaches to.

## The test
A module is pluggable when both answers are yes:
- **Does it attach through an explicit relationship?** The module to which it attaches exposes that relationship ([Modularity → Pluggable Behavior](../modularity.md#pluggable-behavior)), and the pluggable module carries its own concepts, rules and behavior, so the module it attaches to gains no field or branch for it.
- **Would removing it leave the module it attaches to whole?** If the attaching module would lose part of its own responsibility, the capability is not optional and the candidate is [Kernel](./kernel.md).

The grounds are [Modeling → Extensible Behavior Belongs to Pluggable Modules](../../../../docs/modeling.md#extensible-behavior-belongs-to-pluggable-modules) and [Modularity → Core Structure and Optional Modules](../modularity.md#core-structure-and-optional-modules). The distinction is relative to the system and its purpose: a module is not optional in isolation, only optional for a stated system.

## Operational rules
- **A pluggable module owns its capability whole.** The relationship and its processing sit in one module and are never split across modules.
- **A capability is filed under the category of the module through which it is instantiated**, even when it affects several. Where a capability could start from two modules, the category follows the one that instantiates it.
- **A pluggable module carries a capability name, or the name of the kernel module whose optional parts it holds.** `modules-plugable/<category>/<kernel-module-name>/` is allowed only for the module that holds that kernel module's optional parts — `modules-plugable/rights/law/` holds law's labels, rules and the laws it introduces — and it never restates the kernel type nor stands as a second version of it. A guest module keeps a foreign name, because the foreign name is the capability's own ([Guest](./guest.md)). Owner's ruling, 2026-10-20 ([Modules Research 001](../../../modules.research.001.md#6-owner-decisions-needed), D1).
- **A difference in parameters is configuration inside one module;** a difference in processing semantics may be a distinct module.
- **Analytics is never kernel.** It produces discovered, removable data from acquired data ([Modeling → Acquired Data vs. Discovered Data](../../../../docs/modeling.md#acquired-data-vs-discovered-data)); a query with its own types, events, storage and processing is itself a pluggable module.

## Examples
- A calendar that serves one family of requirements — the Mars calendar — attaches to the time modules and is removable without any other time module changing: pluggable.
- A foreign protocol Memar realizes — HTTP — attaches to the networking Memar owns and is removable without networking changing: pluggable, labelled [Guest](./guest.md).
- An invoice discount attaches to the invoice through an explicit relationship; the invoice never branches for it ([Modularity → Example: Pricing and Invoice Behavior](../modularity.md#example-pricing-and-invoice-behavior)).

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Modularity](../modularity.md) | Depends_on — the principle and its limits | None (read) |
| [Kernel](./kernel.md) | Reference — the placement it is distinguished from | None (read) |
| [Placements](../placements.md) | Base — the module that defines the placements | None (read) |

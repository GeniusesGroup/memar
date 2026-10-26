---
Title: "Modularity Rule — Placement"
Status: Draft
Start Date: 2026-10-17
ID: 496333
---

# Modularity Rule — Placement
Modularity's rules live one rule per directory under [`modules/knowledge/modularity/rules/`](../README.md), and this is the rule for a module's placement: that it has one, that its place does not lie about what it is, and that what it may depend on follows from where it is. It is a governance rule of this repository, held for the placements [Kernel](../../labels/kernel.md), [Pluggable](../../labels/pluggable.md) and [Bundle](../../labels/bundle.md).

## The rule
- **A module has exactly one placement.** It stands under `modules/`, under `modules-plugable/`, or under `bundles/`, never under two, and a subject Memar owns has no second address in another placement.
- **Dependence runs from the optional toward the foundation and from a composition toward its parts, never back.** A kernel module names no address under `modules-plugable/` or `bundles/`; a pluggable module may name the kernel module it attaches to and other pluggable modules it declares it depends on, and names nothing under `bundles/`; a bundle may name any module. A back edge is a module that has become foundational, or a composition that has become a part, without saying so.
- **A pluggable module carries a capability name, or the name of the kernel module whose optional parts it holds.** The path is the mirror of the kernel module's path ([Category Depth](../../../label/rules/category-depth/category-depth.md)). The name is the capability's, except for the one pluggable module that holds a kernel module's optional parts, which carries that kernel module's name and restates nothing of its type ([Pluggable → Operational rules](../../labels/pluggable.md#operational-rules)). Any other name shared with a kernel module at the same path is a duplicate of one subject, and it is recorded as an open question where it exists rather than kept silently.
- **The label `guest` follows the authority test.** A module carries it only when changing its contract would need the agreement of someone outside this project ([Guest → The test](../../labels/guest.md#the-test)), and a module that passes that test carries it.

## Why it exists
A placement is a claim about a module, and a claim held only by habit drifts. Memar's own tree held a shelf for foreign modules whose path made the claim, and the shelf's rule against mirroring a Memar module was broken by the shelf's own contents; the cost was a second address for one subject. Stating the dependence direction once makes each placement checkable from the module's own `in` addresses, which no reader has to decide by judgment.

## How a check would run
Reading the `in` addresses of a module's declarations, and the manifest's `labels`, is enough to decide the second and fourth items; the first and third need a walk of the repository's top-level places. Of these, this repository checks only the second item and only for its Python: the module-graph test, [`module_graph.py`](../../../../../bundles/memar/tests/module_graph.py), fails on an import from a module under `modules/` into `modules-plugable/` or `bundles/` that no dated allowance names ([Kernel Neutrality → How a check runs](../kernel-neutrality/kernel-neutrality.md#how-a-check-runs)). The rest is stated for the checker that will.

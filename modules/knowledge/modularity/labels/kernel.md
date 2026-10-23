---
Title: "Kernel"
Status: Draft
Start Date: 2026-10-17
ID: 496333
---

# Kernel
## Abstract
**Kernel** is the placement of a module that Memar's foundational set cannot lose: a module whose removal would force a foundational abstraction to be fabricated or another to be distorted. A kernel module sits at `modules/<category>/<module>/`, and the category is only a browsing namespace ([Category](../../label/labels/category.md)). Kernel is one of the three placements of [Placements](../placements.md); the others are [Pluggable](./pluggable.md) and [Bundle](./bundle.md).

## The test
The test is the one [Modularity → What Earns Foundational Status](../modularity.md#what-earns-foundational-status) states, applied to a module: attempt to express, through the remaining modules, the part of reality the candidate covers. If the result forces a new foundational abstraction, or bends an existing one, the candidate is kernel. If an independently modeled capability attaching to existing modules can fill the gap, the candidate is pluggable, however central it feels.

Importance is not the test. A module can dominate how a system is used and still be fully expressible through the foundations; a quietly load-bearing abstraction may be irreplaceable. Two guards keep the test honest, both from the same section: the fabrication must land inside the foundational set, so inconvenience is not evidence; and the test runs against requirements that exist, not anticipated ones.

## What follows
- **Kernel stays small.** The expectation that foundational concepts remain few ([Modularity → Foundational Concepts Should Remain Few](../modularity.md#foundational-concepts-should-remain-few)) is why a new candidate is first read as a capability over what exists, and only demonstrably unexpressible ones are examined as kernel.
- **A kernel module does not reference a pluggable one.** Dependence runs from a pluggable module toward the module it attaches to, never back; a kernel module that names a pluggable module has made that module foundational without saying so.
- **A kernel module fixes no choice an organization may make otherwise.** [Kernel Neutrality](../rules/kernel-neutrality/kernel-neutrality.md) states the rule and its test.
- **A kernel module's category is where it is browsed, not what it is.** A module moves between categories when its subject is better served by another namespace; the placement does not change.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Modularity](../modularity.md) | Depends_on — the test and its guards | None (read) |
| [Placements](../placements.md) | Base — the module that defines the placements | None (read) |

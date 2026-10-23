---
Title: "Bundle"
Status: Draft
Start Date: 2026-10-17
ID: 496333
---

# Bundle
## Abstract
**Bundle** is the placement of a named composition that runs or aggregates several modules toward a requirement no single module states. A bundle sits at `bundles/<name>/`. Its parts are modules, and what the bundle adds is the composition: which modules it brings together, how they are started and reached, and what it ships. The test and what a bundle may own are stated once, in [`bundles/README.md`](../../../../bundles/README.md); this document only places the bundle among the three placements of [Placements](../placements.md).

## What distinguishes it
- A [Kernel](./kernel.md) or [Pluggable](./pluggable.md) module states a responsibility of its own; a bundle states none and composes the responsibilities of others.
- Dependence runs from a bundle into modules and never back: no module includes anything under `bundles/`. A place another module has to reach into is a module, whatever runs it today.
- A part that serves only one bundle stays inside it, laid out with the role folders a module uses; once a second bundle or project needs it, it is a reusable module and moves out.

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [`bundles/README.md`](../../../../bundles/README.md) | Depends_on — the test and the ownership rule | None (read) |
| [Placements](../placements.md) | Base — the module that defines the placements | None (read) |

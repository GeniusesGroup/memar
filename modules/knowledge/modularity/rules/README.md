# Modularity Rules (`modules/knowledge/modularity/rules/`)
Rules for the conditions this repository holds a module's placement to: where it is, and what it may fix or depend on by that place. The concepts they check are the placement labels of [Modularity](../modularity.md) ([Placements](../placements.md)); a Rule here states what an owner requires when checking work against them, and does not restate the placements. The general concept of Rule is [`modules/process/rule/rule.md`](../../../process/rule/rule.md).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Placement](./placement/placement.md) | A module's placement and what its place lets it depend on | Governance | One placement per module; dependence runs from pluggable to kernel and from a bundle to modules, never back |
| [Kernel Neutrality](./kernel-neutrality/kernel-neutrality.md) | What a kernel module may fix | Governance | A kernel module states its subject and fixes no choice another organization may make otherwise |
| [One Owner](./one-owner/one-owner.md) | Where a concept is declared | Governance | A concept is declared once, with its storage, retrieval, validation and display, in the module whose subject it is; others import it |
| [Module Replacement](./module-replacement/module-replacement.md) | How a module is replaced while data written under its contract exists | Governance | A generation is a new module with a new `Type_UUID` and the same name; the old one is `EndOfLife`, data names its writer, and an adapter, a conversion service and an error serve the generation before; no mode flag and no version in a name |

The rule for the levels of a category is [Label's](../../label/rules/category-depth/category-depth.md), since a category is a label.

One part of these Rules is checked: the module-graph test, [`module_graph.py`](../../../../bundles/memar/tests/module_graph.py), fails on an import from a kernel module into a pluggable module or a bundle. The rest is enforced by no check this repository runs today.

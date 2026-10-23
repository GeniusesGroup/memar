# Modularity Rules (`modules/knowledge/modularity/rules/`)
Rules for the conditions this repository holds a module's placement to: where it is, and what it may fix or depend on by that place. The concepts they check are the placement labels of [Modularity](../modularity.md) ([Placements](../placements.md)); a Rule here states what an owner requires when checking work against them, and does not restate the placements. The general concept of Rule is [`modules/process/rule/rule.md`](../../../process/rule/rule.md).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Placement](./placement/placement.md) | A module's placement and what its place lets it depend on | Governance | One placement per module; dependence runs from pluggable to kernel and from a bundle to modules, never back |
| [Kernel Neutrality](./kernel-neutrality/kernel-neutrality.md) | What a kernel module may fix | Governance | A kernel module states its subject and fixes no choice another organization may make otherwise |

The rule for the levels of a category is [Label's](../../label/rules/category-depth/category-depth.md), since a category is a label.

One part of these Rules is checked: the module-graph test, [`module_graph.py`](../../../../bundles/memar/tests/module_graph.py), fails on an import from a kernel module into a pluggable module or a bundle. The rest is enforced by no check this repository runs today.

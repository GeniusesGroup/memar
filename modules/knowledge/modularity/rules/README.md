# Classification Rules (`modules/knowledge/classification/rules/`)
Rules for the conditions this repository holds a module's placement to: where it is, in which namespace, and what it may depend on by that place. The concepts they check are the primitives of [Classification](../classification.md); a Rule here states what an owner requires when checking work against them, and does not restate the placements. The general concept of Rule is [`modules/process/rule/rule.md`](../../../process/rule/rule.md).

| Rule | Subject | Tier | What it is |
| --- | --- | --- | --- |
| [Placement](./placement/placement.md) | A module's placement and what its place lets it depend on | Governance | One placement per module; dependence runs from pluggable to kernel and from a bundle to modules, never back |
| [Category Depth](./category-depth/category-depth.md) | The levels between a placement and a module | Governance | A category is one level, and a facet is part of its module, not a sibling |
| [Kernel Neutrality](./kernel-neutrality/kernel-neutrality.md) | What a kernel module may fix | Governance | A kernel module states its subject and fixes no choice another organization may make otherwise |

One part of these Rules is checked: the module-graph test, [`module_graph.py`](../../../../.agents/scripts/tests/module_graph.py), fails on an import from a kernel module into a pluggable module or a bundle. The rest is enforced by no check this repository runs today.

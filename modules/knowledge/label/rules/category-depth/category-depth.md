---
Title: "Classification Rule — Category Depth"
Status: Draft
Start Date: 2026-10-17
ID: 497842
---

# Classification Rule — Category Depth
Classification's rules live one rule per directory under [`modules/knowledge/classification/rules/`](../README.md), and this is the rule for how many levels stand between a placement and a module. It is a governance rule of this repository, held for [Category](../../primitive/category.md).

## The rule
- **Between a placement and a module there is one level, the category.** The path of a kernel or pluggable module is its placement, one category, and the module; a place with another level in it is either a module that holds facets or a category that should not exist.
- **A module that holds modules holds its own facets or parts.** The documentation module holds its facets (changelog, comparison, plan and the rest) because each is a part of what documentation is. A part is never a sibling of its module, and a module whose parts could stand alone in another module's work is not holding parts but a category by another name.
- **A category is not created for a handful of modules.** A subject too small to hold several modules with a reason to grow is a module of the category it serves.

## Why it exists
Every added level is another place for two modelers to disagree about where a module goes, and a deeper tree does not make a model more accurate; it makes the path longer and the disagreement more likely. The owner's ruling on this repository's first reorganization (2026-10-17) was to avoid categories inside categories, and in particular not to subdivide `time` further, whose modules are few and will stay few.

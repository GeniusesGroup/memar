---
Title: "Category"
Status: Draft
Start Date: 2026-10-17
ID: 497843
---

# Category
## Abstract
A **category** is a browsing namespace for [kernel](../../modularity/labels/kernel.md) and [pluggable](../../modularity/labels/pluggable.md) modules: the first level under `modules/` and under `modules-plugable/`. It says where a reader looks for a module, and it is not an ontological parent: a module does not inherit meaning from its category, and the same category names are used on both sides so that a pluggable module is found beside the kernel module it attaches to.

## The rules
- **A category is one level.** A category holds modules and nothing between: no category inside a category. A module may hold modules that are its own facets or parts (documentation holds its facets), because a module is itself a bounded responsibility ([Modularity → Module as a System](../../modularity/modularity.md#module-as-a-system)); a facet is a part of the module and is not a sibling of it.
- **A category that would hold few modules is not created.** A group of a handful of modules, with no sign of growing, is a reason to place them in the category they serve, not a new namespace: every added category is another place two modelers can disagree about.
- **A category names a subject, not a mechanism or an implementation.** A concept with no independent identity belongs to the category it is a part of: hardware, codecs, cryptography and memory are parts of the computer, and an identifier is a part of how a computer names things.
- **The categories are not final.** A category is merged, split or renamed when its subject is better served another way, and a category in this repository is not assumed to be right because another repository uses it.
- **No complete inventory of modules is kept in a category's document.** A category's document may name modules as examples of its subject, and the list of what it holds is what the category holds ([Documentation → No derivative inventories](../../../../modules-plugable/knowledge/documentation/documentation.md)).

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Placements](../../modularity/placements.md) | Base — the module that defines the placements | None (read) |
| [Kernel](../../modularity/labels/kernel.md), [Pluggable](../../modularity/labels/pluggable.md) | Reference — the placements a category holds | None (read) |

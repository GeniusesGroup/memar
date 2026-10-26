---
Title: "Category"
Status: Draft
Start Date: 2026-10-17
ID: 497843
---

# Category
## Abstract
A **category** is a browsing namespace for [kernel](../../modularity/labels/kernel.md) and [pluggable](../../modularity/labels/pluggable.md) modules: a folder under `modules/` or under `modules-plugable/` that holds modules, or other categories, and holds no contract of its own. It says where a reader looks for a module, and it is not an ontological parent: a module does not inherit meaning from its category. The categories of the two roots correspond: a category stands at the same path under both, so that a pluggable module is found beside the kernel module it attaches to.

## The rules
- **A category may hold categories.** The path of a module is its placement, zero or more categories, and the module (`modules-plugable/computer/memory/store/record`, where `memory` is a category). There is no numeric ceiling: each level earns itself by the rules below, and a level that does not is dissolved. The owner ruled on 2026-10-24 that "a category is one level" was a bad rule; the level it limited was an accident of the first reorganization, not a property of browsing ([Category Depth](../rules/category-depth/category-depth.md)).
- **A folder is a module or a category, never both.** A module holds a contract of its own: a structural kind (`protocol/`, `edges/`, `edges-loop/`, `edges-shortcut/`, `status/`, `labels/`), code, or a main document named for the folder that defines one concept or states what the folder requires; the last is how a module not yet developed is told from a category (compiler, lexer, os). A category holds its children and a document that says what its subject is and names modules as examples, and nothing a party could be held to: no `protocol/`, no code, no `services/` or `errors/`. A folder that would be both is a category whose contract was never divided into modules, and the contract is divided: a category that offers a `protocol/` folder collects every concept nobody modelled into the category's protocol, and the category stops being a place to browse. A category is therefore not a module, and the sentence that said it was is withdrawn.
- **A module does not hold modules.** What a module holds beside its role folders are its facets, the parts of the one concept it is, and a child that could stand alone in another module's work is not a facet ([Category Depth](../rules/category-depth/category-depth.md)).
- **A mirror folder is the one exception, on the pluggable side only.** It is the path of a kernel module under `modules-plugable/`, holds only the pluggable modules that attach to that kernel module, and holds no contract of its own; the kernel module's existence earns it, so the few-members test does not apply to it. The pluggable module that holds that kernel module's optional parts ([Pluggable → Operational rules](../../modularity/labels/pluggable.md#operational-rules)) is a module and stands at that path itself only when the kernel module has no other capability.
- **A category and its counterpart correspond.** A category stands at the same path and with the same name under `modules/` and under `modules-plugable/`; a category with members on one side only stands on that side only, and each such category is reviewed on its own. The pluggable side does not invent a category its kernel side lacks, or the reverse, without a reason written in the category's document.
- **A category that would hold few modules is not created,** at any level. A group of a handful of modules, with no sign of growing, is a reason to place them in the category they serve, not a new namespace: every added category is another place two modelers can disagree.
- **A category names a subject, not a mechanism or an implementation.** A concept with no independent identity belongs to the category it is a part of: hardware, codecs, cryptography and memory are parts of the computer, and an identifier is a part of how a computer names things.
- **The categories are not final.** A category is merged, split, nested, dissolved or renamed when its subject is better served another way, and a category in this repository is not assumed to be right because another repository uses it. The review of this repository's categories is in [Modules Handoff](../../../modules.handoff.md#re-reading-this-repositorys-categories).
- **A role folder's name is never a category's or a module's.** `services`, `tests`, `docs`, `rules`, `errors`, `protocol`, `primitive` and `temp` are read as roles at any depth by the tools that walk the tree ([Module skeleton](../../../modules.md#module-skeleton)).
- **No complete inventory of modules is kept in a category's document.** A category's document may name modules as examples of its subject, and the list of what it holds is what the category holds ([Documentation → No derivative inventories](../../../../modules-plugable/knowledge/documentation/documentation.md)).

## Related artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [Placements](../../modularity/placements.md) | Base — the module that defines the placements | None (read) |
| [Category Depth](../rules/category-depth/category-depth.md) | Reference — the levels a category may have and the mirror | None (read) |
| [Kernel](../../modularity/labels/kernel.md), [Pluggable](../../modularity/labels/pluggable.md) | Reference — the placements a category holds | None (read) |

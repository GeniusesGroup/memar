---
Title: "Memar Fs"
Labels: Draft
Start Date: 2026-11-02
---
# Memar Fs
## Abstract
This bundle offers the acts on files and folders that an agent or a tool reaches for as verbs, each with the constraint that keeps a text or a path from being lost: make a directory link, list a tree, say whether a copy has fallen behind, and put a path in the recycle bin and never delete it. It is a bundle, where an outside system is met: the operating system's files are not a Memar concept outside the filesystem ([Filesystem Rule: No File Concept Outside the Filesystem](../../modules-plugable/computer/memory/filesystem/rules/no-file-concept/no-file-concept.md)), and the bundle, which no module depends on, is where its words (file, folder, path, link, recycle bin) may appear. The abstraction is in [`services/`](./services/) and [`errors/`](./errors/); this document says what the bundle is, why, and what it costs. The code of the four acts lives in [`services/`](./services/), moved from the filesystem module, and its tests are in [`tests/`](./tests/).

## Why a bundle
- **The verbs are the filesystem's leaf services, not its subject.** The filesystem module keeps what it needs to be itself: the per-file lock, the trash it relies on, the checkout and the scratch folders it names. The four verbs here are acts a caller performs through the Memar server, and a module states what its subject is and requires ([Kernel Neutrality](../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). A bundle is a composition that may name any module and any outside system, and no module names a bundle ([Placement](../../modules/knowledge/modularity/rules/placement/placement.md#the-rule)), so the dependence runs from the composition to its parts.
- **The explanation lives in the tool.** Every command verb (all but Copy) carries its constraint in its own help, and the listing of the command verbs reaches an agent with MCP as tools and an agent without it as a `commands` listing. No skill, project instruction or document needs to explain these acts in prose, or to name the path of a script.

## The verbs and what each refuses
The verbs, their parameters, their refusals and their errors are declared in [`services/`](./services/) and [`errors/`](./errors/). A failure that is not the caller's call to change is an error of its own, never a refusal.

A refusal changes nothing, except that Trash goes path by path and the paths before the refused one are already done.

## What it holds and what it leaves
It holds the four acts and the listing, and the services they stand on: the lock a daily job or a run takes (`fs_lock`), the adapters of the text domain's edit port to a real folder (`text_edit_store`, `text_edit_lock`) and the wiring of `memar content edit` and `memar content write` to the text domain's edit service (`text_edit_command`, reached from `content_text_edit` and `content_text_write`), the trash mechanism the verbs call (`fs_trash`), the storage the files adapter of the store stands on (`storage`), and the helpers they share (`_fs_common`). What a Memar repository is (`bundles/memar/services/location/repository.py`), the folders a copy never carries (`bundles/memar/services/machine/copy_excluded.py`), the target folder of a run and the lock of one install at a time (`bundles/memar/services/install/services/target.py` and `lock.py`) are of the Memar bundle, which asks them of the machine and not of this bundle. The filesystem module keeps only its Khayyam abstractions, documents, manifest and rules.

**Copy is a library service, not a command.** It has no command line and no help of its own; its only importer is the editor-extension code of [`bundles/memar`](../memar/) (`bundles/memar/services/machine/editor_extension.py`) and no module imports it, and the command tree, the MCP tools and the `commands` listing carry the other five verbs.

## Words of the operating system, and a debt
The bundle names files, folders, paths, links and a recycle bin, which the [no-file-concept rule](../../modules-plugable/computer/memory/filesystem/rules/no-file-concept/no-file-concept.md) lets only the filesystem name. The decision recorded here, for the owner to confirm: these verbs are the operating system's own interface, so the bundle names those things as the system's own words. This is the case the rule's "Keep it or drop it" allows, recorded as a debt under the rule's "Existing mentions are debts": each text of the bundle is rewritten the day the files go.

## Trade-offs
- **One face, not two.** The three command verbs and the two text verbs join the Memar server's single command tree and its MCP tools; a standalone entry point is a thin addition later.

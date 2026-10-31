---
Title: "Memory View"
Status: Draft
Start Date: 2026-10-23
ID: 497993
---

# Memory View

## Abstract
A memory view is a read-only folder built from the committed state of one class of nodes, for a person's editor and eyes, through the [record contract](../record/record.md) and nothing else. It is a function of the store's state and the project's preferences, it is never committed and never edited, and no verb reads it. The layout inside the folder is each domain's own presentation of its nodes, so that work records can be shown in the shape they had before they moved into the store; the project chooses only the class shown and the root folder. The builder, its presentation registry and its answers are Khayyam, [`protocol/view.kh`](protocol/view.kh) and the `view-*.kh` files beside it, with its refusals in [`errors/errors.kh`](errors/errors.kh); [`view.py`](view.py) realizes them, and the verb that runs it, `memar view refresh`, is `bundles/memar/services/view/services/refresh.py`.

## Explanation

### Placement
The owner ruled on 2026-10-24 that the adapters of the memory contract are modules of their own and not parts of `record`, and the model of task `20261024-T052936Z-22844` places this one, a consumer of the `record` capsule, at `modules-plugable/computer/memory/store/view/` after the division of the contract into modules (task `20261026-T120259Z-16244`), beside the capsules it reads; it stands there since task `20261024-T160310Z-25344`.

The view is a consumer of the capsule and a capability it can do without, so it is a pluggable module of its own and the record document holds none of its rules. It needs the presentation each domain declares for its nodes, because the path of a content and the text it points to are domain knowledge the capsule must not have ([Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). An adapter that can build a view faster may offer its own behind the same verb.

### What a view is
- **A function of two things.** The view is determined by the store's committed state and the preferences that select it. Building it twice with no change in between rewrites no file, and building it after the folder is deleted gives the same bytes. That is what makes it safe to delete and to leave stale.
- **Never committed, never edited.** The view's folder is ignored by version control, the builder refuses to build into a folder that is not, the files are made read-only by the operating system, and a file found changed is rewritten from the store and counted as drift. An edit goes through a verb. No verb reads the view, so an agent that reads it risks stale text and is told so; the check that no verb reads it is a scan of names, so a read through a path typed by hand is beyond it.
- **Built on demand.** The view is built when a person asks, with one verb. Neither a service nor an agent builds one of its own accord.
- **Selected by preferences.** The key `view` is written `class=folder` and names the class shown and the folder it is built in, in the `memar:` block of the manifest; it holds nothing else, and its name is this module's, as an adapter's keys are its own ([Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). The form is the one the preferences module declares once for every key of a class ([`preferences.py`](../../../../../modules/process/project/services/preferences.py)). A domain registers its presentation with this module when the entry point of Memar's tooling starts; a project defines at most one view. The verb opens the class through `open` of `bundles/memar` and hands the builder the `record` it returns, so the builder reaches the store through the contract alone.
- **A folder in use is never cleaned.** The builder records the files it wrote in a list inside the folder, with the token of each file's bytes, touches only those, and refuses a folder that holds a file it did not write. It reads every node from one committed state and decides every refusal before it writes anything, so a refused build leaves the folder as it was.
- **The task folder waits for the migration.** The folder of `.agents/tasks` is given to the view only when the migration has removed the old folders and the task logs that still lie there, and the same change adds the folder to the ignore list of version control.

### The cases
They are code, in [`tests/view.py`](tests/view.py) and, for the verb, `bundles/memar/services/view/tests/refresh.py`; each runs the builder over `volatile` and over `git-store` with a test presentation, because the presentation of a Task is the task module's, built by a later task.

---
Title: "Memory View"
Status: Draft
Start Date: 2026-10-23
ID: 497993
---

# Memory View

## Abstract
A memory view is a read-only folder built from the committed state of one class of nodes, for a person's editor and eyes, through the [record contract](../record/record.md) and nothing else. It is a function of the store's state and the project's preferences, it is never committed and never edited, and no verb reads it. The layout inside the folder is each domain's own presentation of its nodes, so that work records can be shown in the shape they had before they moved into the store; the project chooses only the class shown and the root folder.

## Explanation

### Placement
The owner ruled on 2026-10-24 that the adapters of the memory contract are modules of their own and not parts of `record`, and the model of task `20261024-T052936Z-22844` places this one, a consumer of the `record` capsule, at `modules-plugable/computer/memory/store/view/` after the division of the contract into modules (task `20261026-T120259Z-16244`), beside the capsules it reads; it stands there since task `20261024-T160310Z-25344`.

The view is a consumer of the port and a capability the port can do without, so it is a pluggable module of its own and the port document holds none of its rules. It reads nodes through `get`, `parts`, `list` and `scan`, and it needs the presentation each domain declares for its nodes, because the path of a content and the text it points to are domain knowledge the port must not have ([Kernel Neutrality](../../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). An adapter that can build a view faster may offer its own behind the same verb.

### What a view is
- **A function of two things.** The view is determined by the store's committed state and the preferences that select it. Building it twice with no change in between rewrites no file, and building it after the folder is deleted gives the same bytes.
- **Never committed, never edited.** The view's folder is ignored by version control, the builder refuses to build into a folder that is not, the files are made read-only by the operating system, and a file found changed is rewritten from the store and counted as drift. An edit goes through a verb. No verb reads the view, so an agent that reads it risks stale text and is told so.
- **Built on demand.** The view is built when a person asks, with one verb. Neither a service nor an agent builds one of its own accord.
- **Selected by preferences.** The key `view`, declared by this module, is written `class=folder` and names the class shown and the folder it is built in, in the `memar:` block of the manifest; it holds nothing else. A domain registers its presentation, a function from a node to the relative paths and bytes it shows, with this module when the entry point of Memar's tooling starts, for the class its services use; the task module's names a Task's folder by its legacy id and its files by the content names the `timeline` part points to, and a content's name is its path relative to the Task's folder. A project defines at most one view, and builds it with the verb `memar view refresh`. The builder records the files it wrote in a list inside the folder, touches only those, and refuses a folder that holds a file it did not write, so a folder in use for something else is never cleaned. The folder of `.agents/tasks` is given to the view only when the migration has removed the old folders and the task logs that still lie there, and the same change adds the folder to the ignore list of version control.

### The cases
Each case runs against the builder over `volatile` and over `git-store`, with a test presentation of the nodes (the presentation of a Task is the task module's, built by a later task). The tests are written by the task that builds the view, each pending case carrying `owed:memory.view` in its title, and when they run this list is replaced by a pointer to them.

Owed: memory.view

- `view-is-deterministic`: two builds with no change in between leave every file's bytes and modification time as they were.
- `view-rebuild-identical`: a build after the folder is deleted gives the same set of paths and bytes.
- `view-changed-node-rewrites-only-its-files`: after one node changes, exactly the files that show it are rewritten.
- `view-refuses-unignored-folder`: in a working tree under version control, a folder that version control does not ignore is refused and nothing is written.
- `view-files-read-only`: every file the builder wrote carries the operating system's read-only attribute.
- `view-drift-is-rewritten-and-counted`: a file changed by hand is restored by the next build, which reports one drift.
- `view-refuses-foreign-files`: a folder holding a file the builder did not write is refused and nothing is written or removed.
- `view-never-read-by-verbs`: a scan of the verbs' source finds no read of the view's folder.

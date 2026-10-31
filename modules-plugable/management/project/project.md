# Project
A project is a task that carries the label `project`: the upstream task of a body of work, active until the work ends, which other tasks refer to. Developing Memar, an organization or a product is such a task. A project is not a type of its own, and no module declares an abstraction of one (owner, 2026-10-31).

## Model
- `(task)-[:---]->(project)`: a task refers to the project task it belongs to.
- The label `project` is declared with the task domain's labels ([topics.py](../task/labels/topics.py)).

## What a project uses, and whose it is
- Its name and aliases are titles of the task, the [title](../../uri/title/title.md) module's.
- The label is the [label](../../../modules/knowledge/label/label.md) module's mechanism.
- What an application states in its manifest for Memar's tools belongs to [software's manifest](../../../modules/computer/software/edges/manifest/manifest.md) until a better owner is found.
- A file, a folder or a path is named only by the [filesystem](../../computer/memory/filesystem/rules/no-file-concept/no-file-concept.md).

# Project
A project is a task that carries the label `project`: the upstream task of a body of work, active until the work ends, which other tasks refer to. Developing Memar, an organization or a product is such a task. A project is not a type of its own, and no module declares an abstraction of one (owner, 2026-10-31).

## Model
- A project is only the label `project` on a task, plus the task-to-task relation of kind `project` from a member task to that project task (the same family as `part_of`, `blocks`, and the other kinds [task-relations](../task/rules/task-relations/task-relations.md) names). There is no `ProjectUUID` and no project type.
- The label `project` is declared with the task domain's labels ([project.py](../task/labels/project.py)).

## What a project uses, and whose it is
- Its name and aliases are titles of the task, the [title](../../uri/title/title.md) module's.
- The label is the [label](../../../modules/knowledge/label/label.md) module's mechanism.
- What an application states in its manifest for Memar's tools belongs to [software's manifest](../../../modules/computer/software/edges/manifest/manifest.md) until a better owner is found.
- A file, a folder or a path is named only by the [filesystem](../../computer/memory/filesystem/rules/no-file-concept/no-file-concept.md).
- `protocol/dt-uuid.kh` (`Field_ProjectUUID`) is **EndOfLife for new facts**: it declared a project id type the model forbids. Stores that still key by it are owed a rekey to the project task's address; new task facts use the `project` relation kind instead.

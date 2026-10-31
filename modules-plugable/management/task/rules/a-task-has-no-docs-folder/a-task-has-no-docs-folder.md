# Task Rule — A task has no docs folder
Status: Draft

## The rule
- **What a task writes for a reader is a content of its timeline, never a file in a `docs` folder of the task.** A research note, a design, a ruling of the owner and a table are each posted with `memar conversation post --timeline ID --kind KIND`, and are never edited.
- **A task folder holds `task.yaml`, its numbered contents, its claim, and `services`, `tests` and `temp`.** No service makes a `docs` folder, and no document, plan or help text tells an agent to write in one.
- **A tool is not a note.** A script a task writes is code; it belongs in the module that owns its subject, with a test, and not in the task's folder.

## Why it exists
The owner's ruling of 2026-10-31. An agent wrote the owner's rulings in a `docs` file of a task instead of its timeline, where the next task cannot find them by the task, and another wrote a service in a task's folder. A file in `docs` is a text beside the timeline, which the new way of keeping a record exists to end.

## How a check would run
A task folder with a `docs` folder, or a document that names one as the place to write, breaks the rule. The statement is the owner's (2026-10-31); this repository runs no automatic check of it today. The files that stand in `docs` folders are moved into their task's timeline by the queued tasks that move them (see the plan of the task that carries this rule) before the folders are removed.

# Task Rule — A task writes a record where it will live and appends to no file another task writes
Status: Draft

## The rule
- **A task folder holds one folder for each domain the task acts on, and each record the task makes about a domain is a file of its own in that domain's folder.** The folder path is the domain's path in the repository, the file's name is its number on the Task's timeline and a short slug, and the file is one handoff entry or one changelog record, in a records folder named `@handoff` or `@changelog`.
- **A record is moved to its home and is not rewritten.** What moves it is a rule on the path and the name, and it needs no reading of the text: the record's file is placed beside the document it concerns, under a name made of its instant, the task and the slug; the number stays in its front matter.
- **A task appends to no file that another task also writes.** The shared handoff and changelog of a document are views assembled from the records, not files an agent edits, except the head of a handoff (its topic and status), which is a state of the document and open for the owner.
- **A record that is a state, such as an open question, is answered by a reply and is not edited into an answer.**

## Why it exists
1294 changelog entries sit in 221 files and the handoffs in 256 more, and every task appends to the file of each document it touches, so two writers race over one file and a file grows past what one reading can take. Records that are separate files, named by where they go, can be moved by a script, and several tasks can write at once.

## How a check would run
List the files a task wrote outside its own folder before its end: a handoff or a changelog is one only if the move that places it was done by the script. The statement is the owner's, recorded in [the Task handoff](../../../../../modules/management/task/task.handoff.md#critique-as-a-content-on-the-timeline-2026-10-30-tentative); this repository runs no automatic check of it today.

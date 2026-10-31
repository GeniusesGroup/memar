# Task Rule — A text of a task is added, never replaced
Status: Draft

## The rule
- **A text of a task is a content placed in its timeline, and is added and never written over ([A placement is added, never written over](../../../../../modules/management/timeline/rules/a-placement-is-added-never-written-over/a-placement-is-added-never-written-over.md)).** The task domain adds none itself: it has no view of a content.
- **A conversion of the structure of a text is not a replacement.** It keeps the text's meaning and its place, gives it a new representation with an edge to the earlier one, and keeps the earlier representation reachable; it is made by the conversion service of the module that replaced the earlier one ([Module Replacement](../../../../../modules/knowledge/modularity/rules/module-replacement/module-replacement.md)). A change of meaning is never a conversion.
- **A fact of a task (its status, priority, labels, what it depends on) is changed through its store**, one fact at a time, and a service that changes it opens no file.
- **Until the timeline holds the contents, the interim realization is the file adapter's alone:** a content is a numbered file written once and made read-only, the facts of the task are one YAML file, and no document or Khayyam names that layout.
- **The same holds in Python:** a service core opens no file, and a service touched for any reason is brought to this shape by the agent that touches it.

## Why it exists
An agent replaced a task's `plan.md` and the owner's critique in it was lost on 2026-10-30; the task folders are not under git, so nothing else kept it. A message whose meaning is edited can change the course of the whole task, which is why a fork from a middle content, not an edit, is the remedy to be added later.

## How a check would run
A verb or an agent that writes over a content, or a service that opens a file of a task, breaks the rule. The statement is the owner's (2026-10-31); the design is in task 20261030-T160219Z-30104; this repository runs no automatic check of it today.

---
Title: "Memar Git"
Labels: Draft
Start Date: 2026-11-01
---
# Memar Git
## Abstract
This bundle offers the acts a working tree shared by several tasks needs from git, each with the constraint that keeps work from being lost: commit only the named paths, take a commit back, finish an interrupted commit, stop tracking without deleting, rename, move many files matching a pattern keeping their history, discard only when confirmed, set work aside, and bring a deleted path back. It is a bundle, where an outside system is met: git is not a Memar concept, so no module states it ([Filesystem Rule: No File Concept Outside the Filesystem](../../modules-plugable/computer/memory/filesystem/rules/no-file-concept/no-file-concept.md)), and the bundle, which no module depends on, is where its words (repository, path, index) may appear. The abstraction is in [`services/`](./services/) and [`errors/`](./errors/); this document says what the bundle is, why, and what it costs.

## Why a bundle
- **Git is met in a bundle.** A module states what its subject is and requires ([Kernel Neutrality](../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)); git is one organization's choice of how a repository is kept, and a second organization would keep it otherwise. A bundle is a composition that may name any module and any outside system, and no module names a bundle ([Placement](../../modules/knowledge/modularity/rules/placement/placement.md#the-rule)), so the dependence runs from the composition to its parts.
- **The explanation lives in the tool.** Every verb carries its constraint in its own help, and the listing of the verbs reaches an agent with MCP as tools and an agent without it as a `commands` listing, the way the Memar server's commands are listed. No skill, project instruction or document needs to explain git acts in prose, or to name the path of a script.

## How it reaches tasks
A commit names the tasks it carries out. The bundle does not import the task domain and does not read a task store: it asks the Memar server whether each cited task exists, through the verb the server offers, with the repository as the project. A change of how tasks are kept therefore does not reach the bundle, and a server that cannot be asked is an error of its own, never an answer that the tasks exist. The present check cannot tell an unreachable server from a task not found; the abstraction is deliberately stricter and tells them apart, for the code step to realize.

## What it holds and what it leaves
It holds the nine acts, the listing, and the helpers the acts share (finding the repository and resolving a path in it, running git, waiting out another process's lock under one deadline, a private index, the single write that gives the shared index a commit's entries, and the accounting of staged moves and of changes staged by another).

## Words of git, and a debt
The bundle names paths, folders, files and a recycle bin, which the [no-file-concept rule](../../modules-plugable/computer/memory/filesystem/rules/no-file-concept/no-file-concept.md) lets only the filesystem name. The decision recorded here: git's own interface is paths (pathspecs, a replacement given as PATH=FILE), so the bundle names them as git's own words, and its verbs take their paths as git's pathspecs and not as the Memar filesystem's. This is the case the rule's "Keep it or drop it" allows, and it is recorded as a debt under the rule's "Existing mentions are debts": each text of the bundle is rewritten the day the files go. The recycle bin is the same kind of mention, a service of the machine reached for safety, not a concept of the bundle.

## Services of other domains held for now, a debt
By the owner's ruling of 2026-11-07 the whole of the former `modules-plugable/computer/git` moved here at once, so the bundle holds, for now, services that are not git's own: the records branch of tasks (`archive_task_records`, `show_task_records`, `sweep_idle_task_folders`, `trash_task_folder`, `task_store`, `branch`), and `keep`. They still import the task domain, which the section [How it reaches tasks](#how-it-reaches-tasks) forbids. The debt is repaid by placing each in the domain of what it acts on, the day the task-records rework lands, and until then the test `tests/tasks.py` leaves those six files out of its check (the name `KNOWN_DEBT` in it). An agent that meets this need not report it, and one that places a service in its domain removes its file from `KNOWN_DEBT`.

## Trade-offs
- **One face, not two.** The verbs join the Memar server's single command tree and its MCP tools; a standalone `memar_git` entry point is a thin addition later. The cost is that a person without the Memar server installed has no listing until the entry point exists.
- **The task check depends on a running server.** A commit cannot be made while the server is unreachable, unless it declares that it carries out no task; the alternative, reading the task store directly, would make the bundle follow the task domain's every change.
- **The git rules live here and nowhere else.** The alternative is to keep them in a module or in the agent's skill, as they are today; the cost of that is a module in the kernel's neighbourhood that teaches every reader a foreign concept, and a skill that explains in prose what the tool should say. The cost of this choice is that a document which wants to speak of a git act can only point at the verb.

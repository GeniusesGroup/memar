---
Title: "Modularity Rule — A Refactor Moves in Order"
Labels: Draft
Start Date: 2026-11-05
---
# Modularity Rule — A Refactor Moves in Order
A rule of this repository, held for [Modularity](../../modularity.md). It applies to every refactor: a move or rewrite of an existing file, service, type, folder or module that is meant to keep what the thing does. It is the one place where the order of a refactor is stated; the clauses that other rules own are linked here and stated there. Owner (2026-11-05, task 20261105-T064658Z-1260), from the move of the filesystem services (tasks 20261102-T134025Z-8232, 20261103-T072532Z-15212, 20261105-T054954Z-15064).

## The rule
- **The home is decided first.** For a service the question is what it acts on ([A Service's Home Is the Domain of What It Acts On](../../../../process/service/rules/home-follows-what-it-acts-on/home-follows-what-it-acts-on.md)); for any other thing it is the module whose subject it is ([One Owner](../one-owner/one-owner.md)). Nothing is moved to a place it will leave again. A catch-all folder invented while cleaning another file (for example `archive/` for leftover foreign source) is not a home.
- **A move changes nothing else.** It is committed as a pure move ([Task Rule — Commits Are Few and Readable](../../../../../modules-plugable/management/task/rules/commits-are-few-and-readable/commits-are-few-and-readable.md)); the edits the new place needs and every change of behavior come in later steps.
- **The importers are found before the first one is repointed.** They are found by searching the old path as a string and the ways files reach each other (module names, loader calls, relative parents, documents and manifests that name the file), and their count is stated in the plan. A search that was not made is not an empty result.
- **The importers are repointed in one batch, by folder,** the system's entry point last. The old path stays alive until the last importer is repointed, and the system is run once after each batch to see that it still works: a break found late stops every session. Only then are the old files removed, with the removal verb of the git tool.
- **Only the unit tests of the changed service run until the task's last step** ([Test Rule — Tests First and Scoped](../../../../process/test/rules/tests-first-and-scoped/tests-first-and-scoped.md)).
- **A refactor that rewrites a service leaves the filesystem,** its storage isolated in one method until then ([A Rewritten Service Leaves the Filesystem](../../../../process/service/rules/rewrite-uses-memory-adapter/rewrite-uses-memory-adapter.md)); this rule's own claim is that the rewrite is a step after the move, not part of it.
- **No other document states a procedure of refactoring.** A document, a skill or a help text that needs one links here, and says nothing the rules above do not.

## Why it exists
The refactor of the filesystem services put `content_edit` in the wrong domain, ran 78 importer test files while services were still to be moved, and mixed edits into a move, which loses the file's history. Each of these was a judgment made again by each agent; the order in which they are asked decides the cost of the whole refactor, because the home decides the move, the move decides the importers, and the importers decide what a test run has to cover.

## Keep it or drop it
An organization may refactor with its editor's own tooling and mix a move with its edits in one commit, and remain conformant to Memar's concepts, at the cost of a history that cannot follow a file and of a break found by the first user.

## What this rule does not claim
- It does not give the commands: moving, removing and committing are described by the help of the tools `git_rename`, `git_remove`, `git_history-move-glob` and `git_commit`.
- It does not replace a module: a change to the stored shape or the protocol is a generation ([A Module Is Replaced, Not Versioned](../module-replacement/module-replacement.md)), and a rename of a declaration is the language's own rule's ([Khayyam — Declaration Rename](../../../../../bundles/khayyam/rules/declaration-rename/declaration-rename.md)).
- It does not claim a tool finds all importers; no tool does so today, and the search stays the agent's, stated in its report.
- It is enforced by no check this repository runs today.

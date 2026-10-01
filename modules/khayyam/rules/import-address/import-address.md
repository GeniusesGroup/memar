---
Title: "Khayyam Rule — Import Address"
Status: Draft
Start Date: 2026-09-26
ID: "497331"
---

# Khayyam Rule — Import Address
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the form of the URI an `in` declaration carries. It is a rule of this toolchain, not a statement of the language: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) states that the value is a URI — the file URI system is the source of truth, and which file URI resolves to which version is a build/tooling-layer concern — and where a named file is found is a resolver's business.

## The rule
The value an `in` declaration carries is a **URI**, the language fixes no scheme for it, and which scheme a project writes its URIs in is dependency management's choice. This toolchain does not grade a URI's shape: it accepts a URI carrying no extension, a URI carrying a foreign extension, and a URI carrying no path separator at all, and it refuses only a URI it cannot account for. The one thing it insists on is that the URI resolve, and it refuses with `unresolved-import` when nothing accounts for it.

**By default the base a URI is resolved from is the manifest of the module that wrote it** — not a repository root, not the folder a client has open, and not the directory the file happens to sit in. That is the owner's ruling of 2026-09-29 and it is stated here as a *default* on purpose, because the earlier version of this rule stated it as a fact and this toolchain read that fact as permission for a day: a rule that says a default is a default says what a reader may assume, and what a reader may not assume is the part that was missing. A project may resolve from somewhere else — a directory convention, a build-time path table, a service — and this rule does not forbid it. What no project may do is resolve from something and not say so, because a program's declarations then mean different things in two directories with nothing on the screen telling a reader which.

A module's manifest is what a base is read through, and how a module claims an address and how one reaches it is [dependency management's subject, not this rule's](../../../../docs/protocols/modules/dependency-management.md). This rule requires one thing about it and states no more: a reader of a URI must be able to say who answers for it. The corpus still writes path-shaped URIs (`modules/process/error/error.kh`) and this rule does not require them to change. **What would falsify this reading:** a project whose modules are claimed by nothing and whose URIs still resolve, which would mean the claim is optional and the base is something else.

## Why it exists
A name and a location are two different things, and a tool that conflates them makes a program's declarations depend on a resolver's configuration. An organization whose files are named `boolean.kh` and an organization whose resolver maps the stem `boolean` onto a versioned artifact are both writing `in` declarations; the toolchain that reads one of them has no business refusing the other's spelling. Stating that as a rule is what keeps the choice explicit — the earlier state of this toolchain was the opposite, a check that required the extension because the grammar had been made to require it, and the grammar no longer says so.

The base is the second half of the same claim. A repository that holds a hundred modules holds a hundred manifests, and there is no one place they all resolve from, so an address cannot be written from "the root" — it is written from the module that wrote it. The earlier version of this rule named the repository root, and the toolchain implemented it with a walk up for a version-control directory, which made the storage engine a fact of the model: whether a reader's window sat inside a `.git` decided what their file meant. Version control is not this project's method of managing knowledge, and a resolver that reads its answers out of a `.git` directory is answering from the representation and calling it the represented.

## Keep it or drop it
An organization may keep this rule, replace it with a stricter one, or drop it. A stricter rule is a rule an organization may hold: requiring the full file name, requiring a path-shaped URI, or supplying a default extension when a URI carries none is a decision about a file's name that belongs to whoever owns the files. This repository's choice is the permissive one, and it is the one its own corpus already follows — 660 of the 663 `in` paths under `modules/**/*.kh` carry `.kh` because the files are named that way, not because the toolchain insists. **A rule that this repository might have got wrong is the point of the form:** everything above is a default this repository holds, and an organization that resolves from a directory convention instead has not broken anything, because the rule says the choice is the organization's and only that it must be declared.

## What this rule does not claim
- It does not claim the language requires, forbids, or supplies an extension. The language states that the value is a URI; what the file it addresses is called is settled by [Khayyam → File Extension](../../../../docs/khayyam/khayyam.md#file-extension) and by the organization that owns the file.
- It does not claim the language fixes a scheme, or that a project resolves URIs as this one does. Several schemes exist — a repository-root-relative path, a name under a module's claim, a UUID — and which one a project writes is dependency management's choice, not the grammar's.
- It does not claim the language fixes the base a URI is resolved from. The default above is this rule's, and a project's may differ; what no project may do is resolve from something undeclared. What a module's manifest says, what it claims, and how one reaches it belong to [dependency management](../../../../docs/protocols/modules/dependency-management.md), and this rule does not restate them.
- It does not claim anything about what a program means. Two URIs that resolve to one file are a resolution policy, and resolution policy is the framework layer's to vary.
- It does not change what the toolchain does. The toolchain does not yet consult a manifest, because where one is looked for is undecided; what it does is refuse with a sentence naming what is missing, and the sentence names a manifest rather than a file.

## Open questions
This rule's own open state — including whether a URI may carry more than a name, and what a resolver may complete — lives in its [handoff](./import-address.handoff.md).

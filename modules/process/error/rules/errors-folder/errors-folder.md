---
Title: "Error Rule — Errors Folder"
Status: Draft
Start Date: 2026-10-30
---

# Error Rule — Errors Folder
A rule of this repository, held for [The Error](../../error.md). It applies only to software modules that declare errors. It is held here because the module that would change if what an error is changed is this one, and the folder is where that declaration is read. Where a module's errors are declared is a layout question: [Modules → the kinds of folder](../../../../README.md) names `errors/` among the role folders, and this rule states what that role holds.

## The rule
- **The errors of a module are declared in its `errors` folder, as Khayyam, and nowhere else:** not in `protocol`, not in a service's file, not in a realization.
- **A realization raises, returns or matches an error only by the declaration that folder holds** and makes no error type of its own, in any language.
- **Each error is a type with the [`detail.kh`](../../../../computer/type/protocol/detail.kh) methods.** An error the realization needs and the folder lacks is declared there first, before the code that needs it.
- **A module with no errors has no `errors` folder.**
- The shape follows modules that already declare theirs, for example [`errors.kh` of `index`](../../../../../modules-plugable/computer/memory/store/index/errors/errors.kh).

## Why it exists
An error is part of what a module says of itself; one placed in `protocol` or in a Python file cannot be found where a reader and a tool look for it, and its `detail.kh` methods are not written. The memory-layer task (20261023-T074642Z-5420) put `Unavailability` in `protocol/store.py`.

## Keep it or drop it
An organization may place its errors by another layout and remain conformant to [The Error](../../error.md); what it may not do is use the name `errors` for a folder that holds something else.

## What this rule does not claim
- It does not claim what an error is composed of; [The Error](../../error.md) states that.
- It does not claim how a failure is carried or accounted for; that is the [Disregarded Error rule](../disregarded-error/disregarded-error.md).
- It is enforced by no check this repository runs today.

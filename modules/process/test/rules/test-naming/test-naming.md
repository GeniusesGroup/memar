---
Title: "Test Rule — Test Naming"
Status: Draft
Start Date: "2026-09-30"
ID: "497433"
---

# Test Rule — Test Naming
A rule of this repository, held for the [Test](../../../../../docs/protocols/process/test.md) protocol. [Test Placement](../test-placement/test-placement.md) decides where a Test lives; this rule decides what its own artifacts are called, and follows from that placement: a Test inside a `tests/` folder needs no marker in its name, because the folder is the marker. It is a governance rule of this repository, not part of the Test protocol, for the reason [test-placement.md → Keep it or drop it](../test-placement/test-placement.md#keep-it-or-drop-it) states.

## The rule
- **No Test artifact carries a marker in its name.** A file inside a module's `tests/` folder is a Test by its location, so its name says what it tests and nothing more. No `test_` prefix, no `_test` suffix, no `.test.` infix, no `.spec.` extension.
- **A Test file is named for the Process it names, in the repository's own form.** Where the tested unit is a file, the name matches the file's own base name; where the tested unit is a Process that no single file realizes, the name is the Process's name. The subject is therefore visible in the name, which is what a reader of the folder listing is looking for.
- **The subject is also stated inside the Test.** The name is for the reader scanning the tree; the statement inside is what the [Test](../../../../../docs/protocols/process/test.md) protocol actually requires, per [Test → A Test's Subject Is a Named Process](../../../../../docs/protocols/process/test.md#a-tests-subject-is-a-named-process). A Test that names its subject only in its file name has not satisfied the protocol, and renaming the folder or the file does not change that.
- **Test support that is not itself a Test is named for what it supports.** A fixture, a helper, or a shared arrangement used by several Tests in the folder is a Test-support artifact; it says so rather than borrowing a Test's subject, because a reader scanning the folder is looking for subjects and would otherwise find one twice.

## Why this exists
This repository's naming practice already distinguishes a file that is another angle on the same subject from a file that is a different subject, and it does it with a separator rather than with an adjective. `documentation.md → File Naming` gives the rule for documents — the dot carries a companion's facet key, the hyphen carries the boundary between a category and a topic — and the module tree already uses the same form for the same reason, with `<base>.observers.kh` and `<base>.locale.<lang>.kh` beside the base they belong to. A `*_test.kh` beside its subject is a third thing: neither an angle on the same subject nor a different subject, but the *checking of* the same subject, stated in the name of a file that is not the subject.

The argument against the marker is not that it is uninformative but that it duplicates what the folder already says, and duplication is where two things drift. A repository with both arrangements states twice, in two mechanisms, where a Test is; a repository that later moves to one arrangement must find and remove every marker in the other. The `tests/` folder states it once, structurally, so a reader's inference is sound without knowing any convention, and a runner that scans the folder needs no naming rule at all.

## Keep it or drop it
An organization that keeps a Test beside what it tests will find this Rule unusable, and should adopt [Test Placement](../test-placement/test-placement.md#keep-it-or-drop-it)'s relaxation together with a marker convention instead. The two Rules are a pair for that reason: a marker in the name is a reasonable substitute for a folder and an unreasonable addition to one, and adopting one without the other leaves the location of a Test stated in two places or in none.

## What this rule does not claim
- It does not claim the [Test](../../../../../docs/protocols/process/test.md) protocol requires any naming. It states no structural rule, and the protocol states none.
- It does not claim the marker is a language feature. It is a convention of this repository's source tree; a language whose own tools reserve a suffix for Test artifacts would constrain naming for reasons outside this document.
- It does not claim a Test's name is its subject statement. The statement inside the Test is the obligation; the name is the reader's shortcut to it.
- It does not claim anything about naming for a Test in a language other than the one this repository's modules are written in, where a runtime may require a discovery convention the repository does not control.

## Open questions
This rule's own open state lives in its [handoff](./test-naming.handoff.md).

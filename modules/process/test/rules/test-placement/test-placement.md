---
Title: "Test Rule — Test Placement"
Status: Draft
Start Date: "2026-09-30"
ID: "497432"
---

# Test Rule — Test Placement
A rule of this repository, held for the [Test](../../../../../docs/protocols/process/test.md) protocol. A Test is a standing part of the system that owes it, and this rule states where that part lives: in a `tests/` folder inside the module whose Process the Test names. It is a governance rule of this repository, not part of the Test protocol — an organization that organizes its tests differently conforms to the protocol without adopting this rule, which is what [rule.md → Who Owns and Introduces Rules](../../../../../docs/rule.md#who-owns-and-introduces-rules) requires of any Rule.

## The rule
- **A Test lives in the `tests/` folder of the module that owns the Process it names.** A module folder is a responsibility boundary, per [`modules/README.md`]](../../../../README.md); the folder carrying that module's Tests is a second kind of responsibility within the same boundary, not a scattering of Test artifacts through the module's own surface.
- **The folder is named `tests/`, plural.** It holds many Tests, one per named Process, so the name counts its contents; a folder holding one thing of its kind is named for that kind alone, as `protocol/` is. The reasoning, and what it does not settle about the repository's other role folders, is under [Why this exists](#why-this-exists).
- **A module with no decidable expectation has no `tests/` folder.** An empty folder asserts an obligation the module does not have, and the emptiness will otherwise be read as work not done rather than as work not required.
- **A Test never leaves the module that owns its subject's Process.** A Test placed elsewhere splits the standing the protocol states: the obligation is owed by the system, and a system that keeps its evidence outside itself has an unrealized surface per [Test → A Test Is Part of the System That Owes It](../../../../../docs/protocols/process/test.md#a-test-is-part-of-the-system-that-owes-it).

## Why this exists
A module folder in this repository is read as the unit of a responsibility — what it owns, what it exposes, what it requires. Interleaving Test artifacts through that folder makes the module's own surface harder to read, and the cost is not proportional to the number of Tests: a reader opening a module to learn what it does must now distinguish, by name alone, the file that implements a concern from the file that checks it.

The alternative arrangement, a Test artifact beside each thing it tests, is the ecosystem's ordinary choice and it makes the tested unit findable by proximity. What it costs is the module's readability, and that cost is paid on every read rather than on every failure. The `tests/` folder accepts the cost instead at the point of writing, where the rule is checkable against a tree, and it buys three things the sibling arrangement does not give: the module's own files are all production files, so a reader's inference is sound without knowing any naming convention; a module's Tests are one addressable thing, so running them requires naming the module and nothing else; and a Test's subject is stated by the folder it is in, which is what makes the coverage question in the protocol answerable by looking at the tree.

The plural is a direct consequence of the same reasoning applied to the name. This repository's role folders are singular when they hold one thing of their kind and plural when they hold many: `protocol/` holds a module's one protocol however many files its declaration needs, while `errors/`, `rules/`, and `services____/` hold one folder or file per instance of a many-valued kind. A `tests/` folder holds one Test per named Process, so it takes the plural. The two role folders this repository's Khayyam toolchain carries are singular, and whether that is a third case or a drift is not settled here; the question is recorded in the protocol document's [handoff](../../../../../docs/protocols/process/test.handoff.md).

## Keep it or drop it
An organization may keep a Test beside what it tests, gather all Tests at the repository's root, or place them per package, and remain conformant to [test.md](../../../../../docs/protocols/process/test.md) while doing so. What an organization may not do under this rule's subject is drop the folder while keeping the name, because the name is what tells a reader which files are the module's production surface; a repository that adopts neither this rule nor a replacement has left the inference unsound rather than merely unconventional.

## What this rule does not claim
- It does not claim the [Test](../../../../../docs/protocols/process/test.md) protocol requires a folder, a `tests/` folder, or any layout. The protocol states no structural rule and points here instead; see [Test → What a Test Is Not](../../../../../docs/protocols/process/test.md#what-a-test-is-not).
- It does not claim the name of a module's `tests/` folder is settled for the repository as a whole. It settles the name for the folders this rule governs.
- It does not claim a folder is where a Test is *found* by a runner. Discovery is a mechanism's business, per [Test → Test, Check, and Runner](../../../../../docs/protocols/process/test.md#test-check-and-runner); a runner that ignores this folder is free to do so, at the cost of not running the Tests.
- It does not claim a Test may be absent because a module's implementation is small, new, or believed correct. Absence is decided by whether the module's surface has decidable expectations, per [Test → A Test Is Part of the System That Owes It](../../../../../docs/protocols/process/test.md#a-test-is-part-of-the-system-that-owes-it).
- It does not claim the module folder itself is a module's unit of ownership in the abstract sense; that is [Modularity](../../../../../docs/modularity.md), and this rule follows the representation this repository uses.

## Open questions
This rule's own open state lives in its [handoff](./test-placement.handoff.md).

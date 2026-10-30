---
Title: "Software Rule — Abstraction First"
Status: Draft
Start Date: 2026-10-30
---

# Software Rule — Abstraction First
A rule of this repository, held for [Software](../../software.md). It applies only to work whose product is software; Memar is also used for systems that are not, and the rule says nothing about them. It states the order in which a software requirement is developed: its abstraction first, in Khayyam, approved, and only then any code of it. Step 8 of the workflow accepts a protocol, an abstraction or the document that owns the subject; the narrowing to Khayyam is [Framework → Khayyam and Other Languages](../../../../../docs/framework.md#khayyam-and-other-languages)'s. The claim it applies is [Modeling Practice → The Modeling Workflow](../../../../../docs/modeling.practice.md#the-modeling-workflow), whose eighth step makes a module's contract stand before code is committed to the module, and [Test → The Expectation Is Written Before the Work](../../../../process/test/test.md#the-expectation-is-written-before-the-work), which puts the abstraction before the Test.

## The rule
- **The abstraction of a software requirement is written in Khayyam before any code of it.** It is the skeleton: the types, each with the methods of [`detail.kh`](../../../../computer/type/protocol/detail.kh) that say what the type says of itself; the services, as [`service.kh`](../../../../process/service/protocol/service.kh) and [`services.kh`](../../../../process/services/protocol/services.kh) declare a service and a group of services; and the errors, in the module's `errors` folder ([Errors Folder](../../../../process/error/rules/errors-folder/errors-folder.md)). A protocol or an abstraction is not written in Python and is not a Markdown document: a realization in any language is of an abstraction already stated, and a name first made while coding is a fault ([Framework → Khayyam and Other Languages](../../../../../docs/framework.md#khayyam-and-other-languages)).
- **A fresh agent that did not do the work approves it, and the owner too where the existing rules send the decision to the owner.** The approval is a record in the changelog of the module's document.
- **No code of the requirement is committed to a module before that approval.** A commit whose abstraction was not approved first breaks the rule, even when its tests are green.
- **Where the abstraction needed is missing from Memar,** it is written in Khayyam as part of the first step, or the gap is recorded in the handoff of the document it concerns and the work stops.
- **Then the order is** the abstraction in Khayyam, its approval, the tests ([Test → The Expectation Is Written Before the Work](../../../../process/test/test.md#the-expectation-is-written-before-the-work)), then the code.
- **The exception the workflow bounds stays bounded:** code whose subject is a language's own ability to compile and run may precede a contract, and only the owner accepts that a piece of work is that.

## Why it exists
The owner found the memory-layer task (20261023-T074642Z-5420) built against Memar's own principles: its contract was written as a Python protocol and described in a Markdown document, and the Khayyam that should have stated it was not written. Python is used because it compiles and runs today, not because it is wanted; an abstraction fixed in a realization is a second design nobody reviewed.

## Keep it or drop it
An organization may develop its software from the code up and remain conformant to Memar's concepts, at the cost the workflow names: errors of understanding become invisible to every check.

## What this rule does not claim
- It does not claim the abstraction is final forever: a later requirement may move a boundary ([System → What Architecture Is Not](../../../../../docs/system.md#what-architecture-is-not)).
- It does not claim how an approval is recorded beyond the changelog; that is [Changelog Practice](../../../../../modules-plugable/knowledge/documentation/changelog/changelog.practice.md).
- It is enforced by no check this repository runs today; a reviewer finds, for each commit of code, the `.kh` files and the approval that precede it.

---
Title: "Modularity Rule — A Concept Has One Owner Module"
Status: Draft
Start Date: 2026-10-30
---

# Modularity Rule — A Concept Has One Owner Module
A rule of this repository, held for [Modularity](../../modularity.md). It applies wherever an abstraction, a service or a widget is declared, in every language.

## The rule
- **A concept is declared once, in the module whose subject it is, with everything that belongs to it:** its abstraction, how it is stored and retrieved, how it is validated, how it is shown, and the errors of its refusals. A title is the title module's; a priority, the task's; a label, the label module's; a project and its name, the project module's.
- **Another module imports the owner's declaration and declares none of its own.** It does not wrap the concept in a type of its own, does not write again a member the owner declares (a field embeds the owner's `Field_` abstraction), and does not write again the check, the display or the refusal of the owner.
- **Before declaring anything, search for its owner** (`memar content search`, `memar content find`, and the folders of `modules` and `modules-plugable`), by the term and by what it is. A thing found is imported.
- **A missing abstraction of an owner is the owner's gap.** It is recorded as a task for the owner's module and waits there; the module that needed it does not fill it with a copy.
- **What is left to a module is what is its own subject,** and the widgets that compose its own services with its neighbours' abstractions.

## Why it exists
The design of the making of a task (task 20261030-T094103Z-28324) declared a title, a priority, labels, a project name, the texts a task holds and their views in the task domain, and repeated their members in a request, after three reviews that asked only whether the files were correct. The owner found it: a copy has no owner who stores, retrieves and validates it, and every copy drifts.

## Keep it or drop it
An organization may declare what it uses in the module that uses it and remain conformant to Memar's concepts, at the cost that each copy is validated, stored and shown by its own code.

## What this rule does not claim
- It does not claim a module cannot define a type for a role a concept plays in it; a role with its own subject is its own concept.
- It is enforced by no check this repository runs today; a reviewer asks of each declaration, "whose subject is this?".

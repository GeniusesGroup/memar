---
Title: "Modularity Rule — Kernel Neutrality"
Status: Draft
Start Date: 2026-10-20
ID: 496333
---

# Modularity Rule — Kernel Neutrality
Modularity's rules live one rule per directory under [`modules/knowledge/modularity/rules/`](../README.md), and this is the rule for what a kernel module may fix: its subject, and no choice another organization may make otherwise. It is held for the placements [Kernel](../../labels/kernel.md) and [Pluggable](../../labels/pluggable.md), and it is to modules what [Khayyam → Minimal Legislation](../../../../../docs/khayyam/khayyam.md#minimal-legislation-a-principle) is to the grammar.

## The rule
- **A kernel module states what its subject is and requires, and fixes no choice an organization may make otherwise.** A taxonomy, a list of names (folder roles, categories, label or status words), a vocabulary, a policy or a workflow is a choice when a second organization could make it differently and the module's subject would mean the same. A choice is a pluggable module attached to the kernel module, or the composition's (a bundle, a project's `memar:` preferences), and the kernel module reaches it only through an abstraction it owns.
- **The test is two questions, in order.** Could a second organization choose this differently? Would choosing it differently change what the subject means? Yes and no: it is a choice, and it leaves the kernel module. Otherwise it is the subject, and it stays.
- **A domain may be partly kernel and partly pluggable, and each part is judged on its own.** The kernel is the domain's core function, without which the function does not exist; the test is put to each part with care, case by case, and never answered for a whole domain by a list decided in advance. The domain's optional parts sit in a pluggable module that may carry the domain's name ([Pluggable → Operational rules](../../labels/pluggable.md#operational-rules)).
- **A value the subject needs is a parameter, not a choice the module makes.** The module exposes it; the value an organization picks is set where the organization configures ([Pluggable → Operational rules](../../labels/pluggable.md#operational-rules): a difference in parameters is configuration).
- **A choice is written once, in the module that owns it.** No kernel module, tool or document keeps a copy of it ([Documentation → A Fact in Code Is Written Once](../../../documentation/documentation.md#a-fact-in-code-is-written-once)).
- **Placing anything in a kernel module asks three questions, in this order:** is it the subject or a choice (this rule); is it kernel or pluggable ([Pluggable → The test](../../labels/pluggable.md#the-test)); does every dependence run toward the foundation ([Placement → The rule](../placement/placement.md#the-rule)).

## Why it exists
Memar's modules are meant to be taken by organizations that are not their author. A kernel module that fixes a choice leaves each of them two options, take the choice or fork the kernel, and Memar already refuses that for its language, its rules and its protocols ([Rule → Who Owns and Introduces Rules](../../../../process/rule/rule.md#who-owns-and-introduces-rules); [Protocol → Who Defines a Protocol](../../../../../docs/protocol.md#who-defines-a-protocol)). The case that made the rule necessary was the role-folder list fixed in a kernel module's enum, which every session folder and every module folder inherited ([Modules Categories Research 001](../../../../../.agents/tasks/20261019-T191746Z-16420/docs/modules.categories.research.001.md)).

## How a check runs
The direction is checked by the module-graph test, [`module_graph.py`](../../../../../bundles/memar/tests/module_graph.py): an import from a module under `modules/` into `modules-plugable/` or `bundles/`, by an `import` statement or by `import_module` with the module's dotted path, fails unless an allowance names it with the owner's date and the condition that ends it. Whether something is a choice is decided by the test above, which an agent reads before a design or an implementation, because no program can decide what another organization might choose.

## Keep it or drop it
An organization may keep or drop this rule for its own kernel. Dropping it is coherent for an organization whose kernel no other organization takes; Memar keeps it because Memar's is taken.

## What this rule does not claim
- It does not claim a kernel module holds no names: the names of its own types, fields and methods are its subject.
- It does not make a folder's name its meaning. A name carries meaning as a label, refined over time and retired when its concept changes ([Label](../../../label/label.md)); the kinds behind the names — a contract, the edge kinds, status, the kinds of work — carry the structure (the owner's ruling of 2026-10-20 on [Modules Categories Research 001](../../../../../.agents/tasks/20261019-T191746Z-16420/docs/modules.categories.research.001.md#7-owner-decisions-needed), C2).
- It does not make the categories under `modules/` profile data; [Category](../../../label/labels/category.md) governs them.

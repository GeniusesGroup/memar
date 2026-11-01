---
Title: "Type Rule — One Type per File"
Status: Draft
Start Date: 2026-10-31
---

# Type Rule — One Type per File
A rule of this repository, held for [Type](../../type.md), whose identity is what a type says of itself ([No Comments in Code](../no-comments-in-code/no-comments-in-code.md)). It applies to code in every language this repository's code is written in. It is held by Type because what a file declares is a type's, and the file is the type's address.

## The rule
- **A file declares one type, and is named for it.** The type's definition, its members' meanings and the text it says of itself are in that file and nowhere else ([A Fact in Code Is Written Once](../../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
- **A catalog whose members each carry a definition of their own is a set of types, one file each.** A member that is only a name and a line of purpose is a member of its type; a member that has a definition, a use, a distinction from its neighbours or a reason is a type, and its file holds them.
- **A file that lists the types of a set holds no definition.** It imports them and nothing more; the list is read from the folder when the language allows.
- **A new or changed file follows the rule;** older files are split when a task changes them, not in a sweep that touches files for no other reason.

## Why it exists
The owner's ruling of 2026-10-31: a large file such as `optional_section.py` makes the reader scan every member to find one, and its members' definitions could not grow into code without turning one file into a document. One type per file lets the specification hold the reason only, and the type hold the rest.

## Keep it or drop it
An organization may keep many types in one file and remain conformant to Memar's concepts; it then keeps a file that grows with every member and a document that restates what the file cannot hold.

## What this rule does not claim
- It does not decide how a type's members are expressed; that is the type's own design.
- It is enforced by no check this repository runs today.

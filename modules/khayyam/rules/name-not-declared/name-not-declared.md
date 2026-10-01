---
Title: "Khayyam Rule — Name Not Declared"
Status: Draft
Start Date: 2026-09-26
ID: "497333"
---

# Khayyam Rule — Name Not Declared
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the second of the four import-resolution rules. It is a compiler-gate rule of this toolchain, not a statement of the language: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) gives the `in` declaration a name and a path, and what a tool does when the named file does not declare that name is the tool's own condition.

## The rule
An `in` declaration naming an entity the target file does not declare refuses the unit, with the implementation label `name-not-declared`. [core/src/frontend.ts](../../core/src/frontend.ts) looks the name up among the target's own declarations — a file includes by name, and what it does not declare it does not have.

**The label says "declared" because that is the word the language uses, and this rule was renamed to say so.** It was `name-not-exported` until 2026-09-30, and a reader of the resulting fault took it to mean the target file was fine and had withheld the name — that is, that it exported something else and left this one out. The label named a mechanism the language does not have: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) gives a declaration a name and a path and says nothing about a surface, a publication step, or anything being hidden. A label that borrows another language's vocabulary sends the reader looking for that language's mechanism, and the repair — which is a one-word change in five source files — is cheaper than the hour it cost to explain a fault that was correct. `declaration` is the language's own word for what a `tp` or a `vr` writes, and this rule's subject is exactly one of those being absent.

## Why it exists
Inclusion is by named entity, not by file wholesale, so the importing file's claim is about one declaration. If the target does not make it, the name in the importing file names something no reading of the sources can satisfy, and the failure would otherwise surface much later as an unbound name with no indication of which file was supposed to supply it. Refusing at the inclusion site keeps the report next to the claim that made it.

## Keep it or drop it
An organization may keep this rule or drop it, and the way to drop it is to make the target declare what the importer needs — a file that declares the names others use, a generated list of declarations, or a rule that rewrites the inclusion to where the declaration really is. A tool that simply stopped checking would be accepting imports that name nothing, which is the same position the [unresolved import rule](../unresolved-import/unresolved-import.md) refuses.

## What this rule does not claim
- It does not claim the language refuses an import of an undeclared name. The language states what `in` means; what a tool does about a name that is not there is the tool's own condition.
- It does not claim a file publishes a surface. There is no such concept here, and the old label's error was naming one; how much of a module belongs to it is a module-membership question, and [the dependency-management handoff](../../../../docs/protocols/modules/dependency-management.handoff.md) is where that is being worked out.
- It does not claim a diagnostic message, a code, or a recovery behavior; the diagnostics contract is deferred and the label is an implementation label — though a label that a reader has to ask about is a label that has failed at the one job it has.

## Open questions
This rule's own open state lives in its [handoff](./name-not-declared.handoff.md).

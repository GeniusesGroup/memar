---
Title: "Khayyam Rule — File Layout"
Status: Draft
Start Date: 2026-09-29
ID: "497402"
---

# Khayyam Rule — File Layout
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for how source files in this repository are sized and ordered. It is a governance rule of this repository, not a grammar requirement: [Khayyam → Import Mechanism (`in`)](../../../../docs/khayyam/khayyam.md#import-mechanism-in) states that `in` includes named entities from other files; it does not legislate file length or declaration order.

## The rule
- **Short files for single responsibility**: each `.kh` file should stay small enough to express one coherent responsibility; the file-as-import-unit model encourages splitting rather than accumulation.
- **Contracts-first order**: a file is meant to be read with `in` inclusions and type declarations before method bodies. Companion tooling may fold declaration blocks and bodies so that order is the default view ([Linter → Tooling may present structure first](../../../../docs/protocols/computer/linter.md#tooling-may-present-structure-first)); that assist is not grammar.
- **One abstraction per protocol file (strong default)**: under `protocol/`, a file that declares more than one abstraction (`tp X ab`) is harder to navigate than one concept per file — each `in` import names a file, so a multi-abstraction file forces readers to open it for one name and absorb others. **Split** when the abstractions are distinct concepts (for example `Empty`, `Nil`, and `Null` in ADT operations). **Keep together** when one abstraction only composes the others tightly, or the declarations form a single cohesive family (for example `Codec`, `Codec_Decoder`, and `Codec_Encoder`; or `Observer_X` / `Mutator_X` families already placed in `<base>.observers.kh` and `<base>.mutators.kh` companion files per the [observer and mutator rule](../../../computer/adt/rules/observer-mutator/observer-mutator.md)). This default is advisory — not mandatory — but is the shape new protocol work should take unless there is a stated reason to bundle.

## Why it exists
Khayyam has no package keyword; the file is the module surface. Long files and body-first layouts make dependencies and contracts harder to see at a glance, which works against the import model the language document describes. A file holding several unrelated abstractions repeats that cost at the contract layer: the import path no longer signals which concept is being pulled in.

## Keep it or drop it
An organization may allow large files, body-first authoring, multi-abstraction protocol files, or generated reordering without review. This repository holds the convention for human-authored sources; generated or ported files may differ until tidied.

## What this rule does not claim
- It does not claim the grammar requires a declaration order or a maximum line count.
- It does not claim tooling must fold or sort declarations.
- It does not claim one file equals one capsule or one abstraction — only that one abstraction per protocol file is the strong default, with the observer/mutator companion-file exception stated above.
- It does not require splitting existing multi-abstraction files that form one tight family; judgment stays with the module owner.

## Open questions
This rule's own open state lives in its [handoff](./file-layout.handoff.md).

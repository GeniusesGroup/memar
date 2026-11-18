---
Title: "Khayyam Rule — File Layout"
Labels: Draft
Start Date: 2026-09-29
ID: "497402"
---
# Khayyam Rule — File Layout
Khayyam's rules live one rule per folder under [`bundles/khayyam/rules/`](../README.md), and this is the rule for how source files in this repository are sized and ordered. It is a governance rule of this repository, not a grammar requirement: [Khayyam → Import Mechanism (`in`)](../../../../modules/computer/khayyam/khayyam.md#import-mechanism-in) states that `in` includes named entities from other files; it does not legislate file length or declaration order.

## The rule
- **Short files for single responsibility**: each `.kh` file should stay small enough to express one coherent responsibility; the file-as-import-unit model encourages splitting rather than accumulation.
- **Contracts-first order**: a file is meant to be read with `in` inclusions and type declarations before method bodies. Companion tooling may fold declaration blocks and bodies so that order is the default view ([Linter → Tooling may present structure first](../../../../modules/computer/linter/linter.md#tooling-may-present-structure-first)); that assist is not grammar.
- **One abstraction per protocol file**: under `protocol/`, a file introduces one abstraction (`tp X ab`). Each `in` import names a file, so a second abstraction in that file forces a reader who asked for one name to absorb another. The owner confirmed this on 2026-11-17 for a collection beside its element: `Group_Identifiers` is `identifiers.kh`, and `identifier.kh` holds only `Group_Identifier`. **Split** when the abstractions are distinct concepts (for example `Empty`, `Nil`, and `Null` in ADT operations, or an element and the collection of it). **Keep together** when the declarations are one observer or mutator family in the companion file `<base>.observers.kh` or `<base>.mutators.kh` ([observer and mutator rule](../../../../modules/computer/adt/rules/observer-mutator/observer-mutator.md)), or when one abstraction only composes the others as a single cohesive family (for example `Codec`, `Codec_Decoder`, and `Codec_Encoder`). A collection is not that family.

## Why it exists
Khayyam has no package keyword; the file is the module surface. Long files and body-first layouts make dependencies and contracts harder to see at a glance, which works against the import model the language document describes. A file holding several unrelated abstractions repeats that cost at the contract layer: the import path no longer signals which concept is being pulled in.

## Keep it or drop it
An organization may allow large files, body-first authoring, multi-abstraction protocol files, or generated reordering without review. This repository holds the convention for human-authored sources; generated or ported files may differ until tidied.

## What this rule does not claim
- It does not claim the grammar requires a declaration order or a maximum line count.
- It does not claim tooling must fold or sort declarations.
- It does not claim the grammar refuses a second abstraction in a file. The one-abstraction shape is this repository's rule for protocol files, with the two exceptions stated above.
- It does not require splitting a file that is one cohesive family under those exceptions. A collection beside its element is not such a family, and it is split.

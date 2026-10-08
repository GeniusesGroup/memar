---
Title: "Khayyam Go Target"
Status: Draft
Start Date: 2026-10-08
ID: 497622
---

# Khayyam Go Target
## Abstract
This document is the Go target of the Khayyam toolchain: what the bridge between the archived Go reference and this repository's Khayyam sources does today, what it reads, what it still owes, and what may sit beside it. The target exists because the owner ruled on 2026-10-05 that Go stays a target of the toolchain — a folder named for the emit output it is to produce, beside [`js/`](../js/target.md), and not a place where the language's design is decided. It is not yet an emit target in the sense the pipeline uses that word: nothing here produces a Go artifact, and no Go artifact exists. What it does produce is Khayyam. [`abstraction_bridge.py`](./abstraction_bridge.py) reads Go sources and writes the declarations that have a Khayyam form; every construct that has none stays in the destination as a residue carrying its original Go text, with the whole Go file kept verbatim as comments at the end of the file it produced; and the three Rules that govern that residue are applied here by `tidy --rule`. What the port did, what it measured, and what it left undecided are recorded in the paired [research](./target.research.001.md).

## Introduction
### Motivation
The bridge is the only path by which the archived `memar-go` reference reached this repository's sources, and 852 of the repository's `.kh` files still end in the residue block it wrote ([`go-clue-residue`](./rules/go-clue-residue/go-clue-residue.md)). A tool whose output is unfinished needs a document that says what it has produced and what it has not, or the residue reads as a design rather than as work in progress. The toolchain's own placement names this folder for an emit output ([Khayyam → Local placement](../../khayyam.md#local-placement)), so the gap between what the folder is named for and what it does is the thing a reader arrives here to have settled.

### Methodology
Each statement below is read from the code it names: the two directions and the five sub-commands from [`abstraction_bridge.py`](./abstraction_bridge.py)'s own usage block, the residue block's marker, seal and license line from [`go_source_block.py`](./go_source_block.py), and the four source-rewrite passes `tidy` applies from [`tidy.py`](./tidy.py). Nothing here describes an emitter that does not exist, and no design for one is proposed.

## Explanation
### What this target owns
The toolchain's pipeline is source → frontend → semantic representation → target → artifact → host ([Khayyam Handoff → Pipeline](../../khayyam.handoff.md#pipeline)). The frontend and the representation under [`core/`](../../core/) are target-independent and are not this target's. This target holds the other side of that seam as it stands for Go: the bridge that reads a Go source and writes a Khayyam one, the readers that give that bridge the Go text and the Khayyam text it works on, and the three Rules that say what the residue must become.

The [research](./target.research.001.md) beside this document is where the port's own record lives — the two archives, where they disagree, which side the sources took, and the subjects with no home. It is a record of one inquiry, not the target's current state; this document is that.

### The bridge
[`abstraction_bridge.py`](./abstraction_bridge.py) is the entry point, and it carries two directions and five sub-commands.

The **Go to Khayyam** direction converts Go interface declarations to Khayyam abstractions and, in the inverse `khayyam-to-go` direction, emits Go interfaces and refuses a construct that has no Go interface form. Mode 1 promotes a referenced non-interface type and mode 2 refuses it; `--only` narrows the Go direction to one interface or one method. This direction is about abstractions alone and is narrower than the residue the transfer leaves behind.

**`transfer`** moves one Go source — a file, a package directory, or with `--recursive` a whole tree — into one Khayyam destination. Unlike the archive re-emit it creates a destination that does not exist and never rewrites one that does: it only inserts, and a result that would lose a line, a declaration or a comment of the destination is not written. Whatever has a Khayyam form is written as a declaration; every other construct stays as a `TODO(go-migrate)` residue with its original Go text; and the whole Go file is appended as comments, so nothing the Go file said is lost. It is dry unless `--write` is given, and a decision the owner has not taken — the integer and float capsules, an unresolved name, a generic instantiation name — is residue with the blocker named rather than a guess ([`transfer.py`](./transfer.py)).

**`reemit`** re-emits the protocol files of the archive from the whole Go corpus, carrying Go doc comments over verbatim and qualifying every declaration by its module. It only rewrites a protocol file that already exists, and never one whose declarations or comments the corpus does not carry: such a file is reported as guarded and left for its owner ([`corpus_port.py`](./corpus_port.py)).

**`observer-names`** and **`bare-names`** rename what the sources already hold — the observer shape and the qualified-names spelling, and then the module prefix where the bare name is unique. Both plan before they apply, and a plan says what each name becomes and, for every name it will not touch, why ([`renames.py`](./renames.py)).

Every command that writes Khayyam asks the frontend first. [`khayyam_frontend.py`](./khayyam_frontend.py) and [`frontend_check.ts`](./frontend_check.ts) run the M1 frontend over the result, with an override standing in for a file not yet on disk, so a write is checked before it happens and nothing the frontend would newly refuse is written.

### The reader for a ported file's residue block
What a ported file ends with is defined in [`go_source_block.py`](./go_source_block.py) and read back in [`khayyam_source.py`](./khayyam_source.py) and [`tidy.py`](./tidy.py). The block opens with a `// TODO(go-migrate):` marker line and then holds the reference's Go text, each line commented out; a block may be sealed by a `// --- go-source: <label> sha256:<digest> ---` line over the bytes it was made from, so what it holds can be checked rather than trusted and a sealed block leaves whole or not at all. The reader finds the block, its label, its seal and its end, and reports where it begins; the front of the file is read at a second, line scale, where each `tp` and the lines it spans are seen the way a source rewrite needs to see them. A file holding one of these blocks is never re-rendered without it — that is the one thing the block and the licence line are, in [`transfer` and `reemit`](./transfer.py) alike.

### The three residue rules it applies
[`tidy`](./tidy.py) applies four source-rewrite rules, and the first three are this target's own — the catalog at [`rules/`](./rules/README.md) holds the conditions on what the port left in these sources:

| Rule | Subject | Applied by |
| --- | --- | --- |
| [`Commented Generic Bindings`](./rules/commented-generic-bindings/commented-generic-bindings.md) | A generic Go interface whose methods stayed in the residue block | `tidy --rule commented-generic-bindings` |
| [`Go Clue Residue`](./rules/go-clue-residue/go-clue-residue.md) | The end-of-file Go clue block a ported file ends with | `tidy --rule go-clue-residue` |
| [`Result Parameter Names`](./rules/result-parameter-names/result-parameter-names.md) | A parameter name the port wrote where the Go signature named nothing | `tidy --rule result-parameter-names` |

The fourth, `method-separation`, is not a residue rule: it is one blank line between two method declarations in a file that carries prose, and it is [the Khayyam catalog's](../../rules/method-separation/method-separation.md). `tidy` applies all four by default and narrows to named ones with `--rule`. Every pass is dry unless `--write` is given, and a second run over the output changes nothing.

### What this target owes: a Go artifact
A target folder is named for the artifact it emits, and this one emits none. There is no Go artifact, no compilation step from a Khayyam representation to a Go one, and no Go runtime this toolchain builds against; the `khayyam-to-go` direction above writes Go interface declarations for a set of abstractions and is not a compiler for a program. What the target owes is that artifact, and no design for it is stated here or anywhere in this folder: what a Go artifact would have to decide — the module layout, the naming, the mapping of every construct the language admits and Go does not — is not a question any document in this repository has answered, and writing a guess into this document would give the guess a standing it has not earned.

The residue rules are kept rather than retired for the same reason they are stated rather than designed around: the port's writer still produces all three subjects afresh for every Go file it transfers, and 852 of the repository's `.kh` files still end in a residue block.

### Membership criterion
A file belongs under `targets/go/` when it is the bridge between Go and Khayyam, or a reader the bridge needs, or a Rule about the residue that bridge leaves:

- **The bridge and its readers** — [`abstraction_bridge.py`](./abstraction_bridge.py) and the modules it is one call into: the Go lexer and parser, the Khayyam reader, the comment reader, the residue block, the naming tables, the frontend check, and their tests.
- **The residue rules** — [`rules/`](./rules/README.md), whose subject is what the port left in a `.kh` file. A Rule whose subject is a Khayyam program is the [language catalog's](../../rules/README.md) whatever tool applies it; enforcement does not decide a Rule's home ([Rule → Which Module a Rule Belongs To](../../../../docs/rule.md#which-module-a-rule-belongs-to)).
- **This folder's own records** — this document and the [research](./target.research.001.md) that carries the port's measurement.

What does **not** belong here:
- **A mechanism whose subject is Khayyam rather than the port** — the declaration-rename service reads Khayyam names and outlives this folder, so it is [`services/rename/`](../../services/rename/), not here.
- **The language's own rules and specification** — [`rules/` at the module root](../../rules/README.md) and [`docs/khayyam/`](../../../../docs/khayyam/README.md).
- **The port's record at large** — what the port measured and what it left undecided is [research](./target.research.001.md), one bounded inquiry beside this document rather than material spread through this one.
- **Anything about the Go language itself** — a condition on a Go source file is Go's to state, not this folder's.

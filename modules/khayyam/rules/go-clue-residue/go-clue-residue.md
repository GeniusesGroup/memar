---
Title: "Khayyam Rule — Go Clue Residue"
Status: Draft
Start Date: 2026-09-28
ID: "497377"
---

# Khayyam Rule — Go Clue Residue
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the Go text the port leaves at the end of a Khayyam file. It rewrites source; it is applied by `abstraction_bridge.py tidy --rule go-clue-residue` in [`targets/go/`](../../targets/go/abstraction_bridge.py).

## The rule
A ported file may end with a Go clue block: a `// TODO(go-migrate):` marker line, then a `/* … */` comment holding the reference's Go text, with every `*/` inside it written `* /`. The block holds what the Khayyam declarations above it have not yet carried. What the Khayyam file already carries leaves the block:

- **The license header** of the Go text, when the Khayyam file opens with its own.
- **A Go method** of an interface, when the Khayyam abstraction that stands for the interface declares the same method: same name, bare or behind the owner's name as the port wrote it (`Start` or `Timer_Start` for `Start` on `Timer`), with as many parameters and as many results. The abstraction that stands for the interface is found the way the [qualified names rule](../qualified-names/qualified-names.md) forms names: `TimerStatus` is `Timer_Status`, and a name may carry its module.
- **A field** of a struct, when the Khayyam capsule that stands for the struct holds a field of that name; **an embedded type or a composition entry**, when the Khayyam declaration composes the declaration that stands for it.
- **A whole interface or struct**, once every member is carried, its own comments are carried, and — for a struct — no Go method is declared on it in the block.
- **The block and its marker**, once nothing is left in it but the package clause, the imports, and comments the Khayyam file already carries.

A Go comment is part of its declaration: a method, field, or type leaves only when every comment attached to it — the lines above it and a comment trailing it — appears as a comment in the Khayyam file. A Go function with a body is never carried, because the port writes no bodies. A block sealed by a `sha256` line leaves whole or not at all, since removing part of it would break its seal. Nothing is removed from the Khayyam side, and a Go declaration that nothing matches stays.

## Why it exists
The block is a clue for the person finishing the port: it says what the Khayyam declarations do not yet say. A block that still quotes what has been carried hides the residue among copies — in the ported corpus most of a typical block was already transcribed. Shrinking it to the residue makes the block's size the measure of the work left, and an empty block's removal the evidence that nothing is left.

## Keep it or drop it
An organization may keep every clue block whole until a person removes it, or drop the blocks entirely. Keeping them whole loses the measure; dropping them loses the clue. This rule is a middle state that exists only while a port is in progress, and it retires with the last block.

## What this rule does not claim
- It does not claim a matched declaration is correct. The match is by name and arity; whether the Khayyam types are right is the port's question, answered elsewhere.
- It does not claim anything about Go that is not in a clue block, or about the Go reference itself.
- It does not claim a removed block means the Go file is fully ported. Whether a Go file is transferred is the port's ledger's to state, from the Go source, not from the block.

## Open questions
This rule's own open state lives in its [handoff](./go-clue-residue.handoff.md).

---
Title: "Khayyam Rule — Result Parameter Names"
Status: Draft
Start Date: 2026-09-28
ID: "497379"
---

# Khayyam Rule — Result Parameter Names
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for a parameter name that no author chose. It rewrites source; it is applied by `abstraction_bridge.py tidy --rule result-parameter-names` in [`targets/go/`](../../targets/go/abstraction_bridge.py).

## The rule
A parameter of a method signature named `resultN` or `argN` — the names the port wrote where the Go signature left a parameter unnamed — is renamed after its type:

1. the first letter of the type's name, lower-cased;
2. if that is taken in the same signature, or is a keyword (`tp`, `vr`, `in`, `cp`, `mt`, `ab`, `sc`), the first two letters;
3. if those are taken too, the two letters with a number, from 1.

The type's name is the last segment of a qualified name, the word that says what the value is: `Timer_Status` gives `s`, `Time` gives `t`, `Error` gives `e`. A name the author chose — `with`, `str`, `err`, `mAdd` — is never renamed, and a method with a body is not touched.

```khayyam
tp Status mt (self Timer) () (s Timer_Status)
tp A mt (self T) (s String) (st Status, st1 Status)
```

## Why it exists
`result0` says only that the Go signature named nothing; it carries no meaning a reader can use and repeats across every signature of the corpus. The type is the one thing known about the value, so its initial is the shortest name that says something, and the same derivation everywhere makes the name predictable ([Method in Khayyam → Method Structure](../../../../docs/khayyam/method.md#method-structure) writes every parameter by name in the two variable groups).

## Keep it or drop it
An organization may require a full word, forbid one-letter names, or leave generated names until an author chooses. The rule replaces one generated name with another that carries more; it does not claim the author's choice.

## What this rule does not claim
- It does not claim a one-letter name is good style. It claims it is better than `result0` and no worse than any other mechanical choice.
- It does not claim the last segment is always the right word; a type whose meaning sits in its module part loses it here.
- It does not claim anything about names an author wrote.

## Open questions
This rule's own open state lives in its [handoff](./result-parameter-names.handoff.md).

---
name: khayyam-syntax-lite
description: Use whenever Khayyam (the programming language, file extension .kh) is mentioned, or when writing, converting, or reviewing Khayyam code — especially direct, mechanical translation of existing code (e.g. from a legacy codebase) into Khayyam syntax. Khayyam is a young, uncommon language not covered by general training data — do not write or reason about Khayyam code from memory or by analogy to Go/Rust/C. Trigger for "write this in Khayyam", "convert this function to Khayyam", "explain Khayyam's syntax", or any .kh file content.
---

# Khayyam Syntax (lite)

Khayyam is a minimalist language (part of the Memar framework ecosystem) that strictly defines *how* code is structured. **File extension:** `.kh`

## Scope of this skill

This skill covers **mechanical syntax only** — how to write valid Khayyam, not how to (re)model a codebase around Memar's domain-modeling conventions. If the person is translating existing code, porting a legacy module, or otherwise wants Khayyam used as a drop-in target language without adopting Memar's broader modeling philosophy, respect that: translate structure-for-structure (functions → methods, structs → capsules, interfaces → abstractions) rather than pushing for renaming, re-decomposition, or restructuring toward domain-driven capsules unless asked. If they *do* want the fuller design-philosophy treatment, point them to the `memar-plugin`/`khayyam-syntax` skill instead of improvising it here.

## ⚠️ Always defer to the live repo for anything beyond this cheat sheet

Use the **`memar-navigator`** skill to fetch `Khayyam.md` (canonical spec) and, if the question needs it, the specific `khayyam-*.md` documents (memory model, error handling, concurrency, etc.) from `github.com/GeniusesGroup/memar`. Don't guess at syntax not covered below.

## Quick reference (mechanically summarized from Khayyam.md — verify against the live file for anything precision-sensitive)

### Top-level keywords
| Keyword | Meaning | Keyword | Meaning |
|---|---|---|---|
| `tp` | type | `in` | include (import) |
| `vr` | variable | `cp` | capsule |
| | | `mt` | method |
| | | `ab` | abstraction |
| | | `sc` | scope |

No `namespace`/`package`; the file system is the source of truth, `in` routes to a file path.

### Import
```khayyam
tp TcpConn in "net/tcp"
vr MaxTimeout in "net/config"
```

### Capsule (struct-equivalent)
```khayyam
tp {name} cp { ___ }
```
One `fieldName fieldType` per line. Fields are never directly accessible from outside — only via methods.

### Method (function-equivalent)
```khayyam
tp {name} mt (self {type_owner}) ({args}...) ({returns}...) { ___ }
```
- All three parentheses always written, even empty.
- Args/returns passed **strictly by reference**; no by-value.
- No `const`/`mut`.
- Body-less = abstraction contract or FFI stub.
- Calls use a single `.`.
- No `self` in signature → static, call via `TypeName.Method()`. `self` present → instance, call via `varName.Method()`.

### Abstraction (interface-equivalent)
```khayyam
tp Reader ab
tp Read mt (self Reader) (data Element) (err Error)
```
No logic/state in the abstraction itself. No generics syntax (`<T>`/`[T]`) — covariant returns + compiler-chosen dispatch replace it.

### Scope
```khayyam
tp {name} sc { ___ }
```
Control-flow (`IF`, `LOOP`, `GOTO`) is library-built, not language keywords. Only valid inside a method body.

### Variable
```khayyam
vr {name} {type}
```
No `=`, no implicit copying. Explicit duplication via a method call: `vr newVar Type` then `newVar.CopyFrom(oldVar)`.

## Translating from other languages (mechanical mapping)

| From (typical) | To (Khayyam) |
|---|---|
| `struct`/`class` fields | `cp` with hidden fields, accessor/mutator methods |
| free function | `mt` with no `self` |
| method on a type | `mt` with `self {type_owner}` |
| `interface`/`trait` | `ab` |
| generic function `f<T>(x T)` | rewrite around required behavior (an `ab`) instead of a type parameter — see `memar-navigator` → `khayyam-polymorphism.md` if the mapping isn't obvious |
| `x = y` / mutation | a method call that explicitly performs the mutation |
| deep/shallow copy | explicit `CopyFrom`-style method, never implicit |

If a construct doesn't map cleanly (closures, macros, generics-heavy code), don't invent syntax — fetch the relevant document via `memar-navigator` (e.g. `khayyam-absence_of_closures.md`, `khayyam-rejection_of_macros.md`) to see the documented replacement pattern before proposing one.

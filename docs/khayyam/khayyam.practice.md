---
name: khayyam-syntax
description: Use whenever Khayyam (the programming language, file extension .kh) is mentioned, discussed, or when writing, reading, reviewing, or explaining Khayyam code. Khayyam is a young, uncommon language not covered by general training data — do not attempt to write or reason about Khayyam code from memory or by analogy to Go/Rust/C. Trigger this skill for requests like "write this in Khayyam", "convert this function to Khayyam", "explain Khayyam's syntax", "how do capsules/abstractions/methods work in Khayyam", or any .kh file content. Part of the Memar framework ecosystem; also trigger if the user mentions "Memar" alongside code/language questions.
---

# Khayyam Language Skill
Khayyam is a minimalist system-modeling language, part of the Memar framework ecosystem. **File extension:** `.kh`

## Scope of this skill: mechanical syntax vs. full modeling philosophy
Two different postures, depending on what the person actually wants:

- **Mechanical translation.** Translating existing code, porting a legacy module, or otherwise using Khayyam as a drop-in target language: translate structure-for-structure (functions → methods, structs → capsules, interfaces → abstractions) — see *Translating from other languages*, below. Don't push renaming, re-decomposition, or restructuring toward domain-driven capsules unless asked.
- **Full design treatment.** The person wants Khayyam written the way Memar intends: apply *Rules worth applying even when not asked*, below, without waiting to be asked.

When unclear which is wanted, default to mechanical translation and mention that a fuller pass is available if wanted.

## ⚠️ Verify against the live repo, not memory
This skill does not bundle the spec. Fetch `khayyam.md` via the **`memar`** skill before writing or explaining any nontrivial code — it evolves independently and a copy here would go stale. For anything this cheat sheet doesn't cover — why a rule exists, a topic not listed below, or anything outside Khayyam itself — use `memar` SKILL rather than guessing or naming a specific document from memory.

## Quick reference (verify against the live file for anything precision-sensitive)

### Top-level keywords
| Keyword | Meaning  | Keyword | Meaning          |
| ------- | -------- | ------- | ---------------- |
| `tp`    | type     | `in`    | include (import) |
| `vr`    | variable | `cp`    | capsule          |
|         |          | `mt`    | method           |
|         |          | `ab`    | abstraction      |
|         |          | `sc`    | scope            |

Everything at the top level is either a **Type** (`tp`) or a **Variable** (`vr`). No `namespace`/`package` — the file system is the source of truth, `in` routes to a file path.

### Import
```khayyam
tp TcpConn in "net/tcp"          // import a type (capsule/abstraction/method)
vr MaxTimeout in "net/config"    // import a variable/constant/singleton
```

### Capsule (encapsulation)
```khayyam
tp {name} cp { ___ }
```
- One `fieldName fieldType` per line.
- Fields are never directly accessible from outside — only via methods. No public fields, ever.

### Method
```khayyam
tp {name} mt (self {type_owner}) ({args}...) ({returns}...) { ___ }
```
- The receiver (`self`) can be attached to any type — a capsule, an abstraction, or another method.
- All three parentheses always written, even when empty.
- Args/returns passed strictly by reference; no by-value.
- No `const`/`mut` — mutation only through an exposed mutating method.
- Body-less method = abstraction specification signature, or FFI stub against an external `.s`/`.o` implementation.
- Calls always use a single `.` — never `::`.
- The signature names the parent type: `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`. The call on that type is `W32.Sum(a, b)(total, err)`. The body does not invoke `self`. A call on a variable of the parent type is `k.Set(value)(err)` for `tp Set mt (self Key) (value String) (err Error)`.
- An influencing position may be a `vr`, an `sc`, or an `mt`. The compiler distinguishes them. A method can implement an abstraction by defining methods on itself, and can present that fact with an intent abstraction such as `abstraction_p.Implements`.
- A method's synchronous or asynchronous nature is an abstraction the method implements by defining methods on itself, never a choice at the call. There is no `go`/`async`/`await` keyword.

### Abstraction (pure behavioral specification)
```khayyam
tp Reader ab
tp Read mt (self Reader) (data Element) (err Error)   // defined independently, body-less
```
- No logic, state, or bodies. Methods fulfilling the specification are defined outside it.
- Compose via a `{}` block at the definition site.
- May only use other abstractions as args/returns — never concrete capsules.
- No generics syntax (`<T>`, `[T]`). Covariant returns + compiler-chosen dispatch replace it.
- Satisfaction is structural — no `implements` keyword.

### Scope
```khayyam
tp {name} sc { ___ }
```
Control-flow (`IF`, `LOOP`, `GOTO`, etc.) is library-built, not language keywords. Only valid inside a method body.

### Variable
```khayyam
vr {name} {type}
```
- A logical reference, never raw data. No `=`, no implicit copying (deep or shallow).
- Explicit duplication: `vr newVar Type` then `newVar.CopyFrom(oldVar)`.

## Translating from other languages (mechanical mapping)
For the mechanical-translation posture — a structural mapping, not a redesign.

| From (typical)               | To (Khayyam)                                                               |
| ---------------------------- | -------------------------------------------------------------------------- |
| `struct`/`class` fields      | `cp` with hidden fields, accessor/mutator methods                          |
| free function                | `mt` whose parent type is in `self`, called on that type: `W32.Sum(a, b)(total, err)` for `tp Sum mt (self W32) (a W32, b W32) (total W32, err Error)`. The body does not invoke `self`. |
| method on a type             | `mt` with `self {type_owner}`, called on a variable of that type: `k.Set(value)(err)` |
| `interface`/`trait`          | `ab`                                                                       |
| generic function `f<T>(x T)` | rewrite around required behavior (an `ab`) instead of a type parameter     |
| `x = y` / mutation           | a method call that explicitly performs the mutation                        |
| deep/shallow copy            | explicit `CopyFrom`-style method, never implicit                           |
| `go`/`async`/`await`         | no equivalent — tag the method itself at its definition, not the call site |

If a construct doesn't map cleanly (closures, macros, generics-heavy code), don't invent syntax — fetch the documented replacement pattern via `memar` SKILL before proposing one.

## Field-shaped values
A value such as `Field_UserUUID` is one type. On that type, write one method that names which other abstractions a code generator implements for it, per [abstraction_p.Implements](../protocols/abstraction-implements.md). The generator writes those methods. This is a generation procedure, not a Khayyam keyword.

## Rules worth applying even when not asked
For the full-design-treatment posture:

- Prefer behavior-based abstractions over type-identity-based designs.
- Wrap primitive values in named capsules; don't use raw `string`/`int`/`bool` for business values (`W32`, not `int`; `UserRegistry`, not `Map<ID, User>`).
- Don't create `Utils`/`Helpers`/`Common` capsules — place responsibility in domain-meaningful capsules.
- No magic numbers, no opaque generic containers — name what a value means.
- One syntactic construct per semantic intent.

These are direction, not exhaustive settled mechanisms — if a concrete case isn't covered above, fetch the relevant document via `memar` SKILL rather than inventing an answer.

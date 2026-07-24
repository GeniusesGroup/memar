---
name: khayyam-syntax
description: Use whenever Khayyam (the programming language, file extension .kh) is mentioned, discussed, or when writing, reading, reviewing, or explaining Khayyam code. Khayyam is a young, uncommon language not covered by general training data — do not attempt to write or reason about Khayyam code from memory or by analogy to Go/Rust/C. Trigger this skill for requests like "write this in Khayyam", "explain Khayyam's syntax", "how do capsules/abstractions/methods work in Khayyam", or any .kh file content. Part of the Memar framework ecosystem; also trigger if the user mentions "Memar" alongside code/language questions.
---

# Khayyam Language Skill
Khayyam is a minimalist, un-opinionated **system-modeling language** (not a traditional feature-collecting language), part of the **Memar framework** ecosystem. Its core philosophy is **Separation of Syntax and Governance**: Khayyam defines strictly *how* code is structured, and deliberately delegates *how* code behaves (memory management, architectural rules, execution policy) to compilers, linters, and organizational frameworks like Memar.

**File extension:** `.kh`

## ⚠️ Always defer to the live repo — do not rely on memory or a static cheat sheet alone
This skill does **not** bundle a copy of the Khayyam spec. Khayyam has 15+ interlinked document files that evolve independently (design changes, new constructs, rejected alternatives) — a copy here would go stale. Use the **`memar-navigator`** skill to fetch the live files from `github.com/GeniusesGroup/memar` before writing or explaining any nontrivial Khayyam code.

**Files most relevant to this skill** (see `memar-navigator` for how to fetch them and how the cross-reference/Citations convention works):
- `Khayyam.md` — canonical syntax spec. Always check this first; it's the source of truth for the quick reference below.
- `khayyam-design_philosophy.md` — rationale (naming, no-generics stance, domain modeling).
- Topic-specific documents, read on demand depending on the question: `khayyam-abstraction.md`, `khayyam-encapsulation.md`, `khayyam-inheritance.md`, `khayyam-polymorphism.md`, `khayyam-variable.md`, `khayyam-memory_model.md`, `khayyam-concurrency.md`, `khayyam-error_handling.md`, `khayyam-function_as_capsule.md`, `khayyam-library_driven_control_flow.md`, `khayyam-naming_driven_package_elimination.md`, `khayyam-dependency_resolution.md`, `khayyam-composition_depth_as_decomposition_signal.md`, `khayyam-absence_of_closures.md`, `khayyam-decorators_rejection.md`, `khayyam-rejection_of_macros.md`, `khayyam-domain_driven_arithmetic.md`
- Tooling documents if the question is about compilation/linting/FFI/migration: `Khayyam-compiler.md`, `Khayyam-linter.md`, `Khayyam-runtime.md`, `Khayyam-migration_guide.md`

If a question depends on something not covered by these (or by `terminology.md` / `protocol.md` / `framework.md` / `modeling.md`, which the Khayyam documents assume as background), fetch those too rather than guessing — `memar-navigator` covers the full topic index.

## Quick reference (mechanically summarized from Khayyam.md at time of writing — verify against the live file for anything precision-sensitive)

### Top-level keywords
| Keyword | Meaning | Keyword | Meaning |
|---|---|---|---|
| `tp` | type | `in` | include (import) |
| `vr` | variable | `cp` | capsule |
| | | `mt` | method |
| | | `ab` | abstraction |
| | | `sc` | scope |

Everything at the top level is either a **Type** (`tp`) or a **Variable** (`vr`). There is no `namespace`/`package` concept — the file system is the source of truth, and `in` routes to a file path.

### Import
```khayyam
tp TcpConn in "net/tcp"          // import a type (capsule/abstraction/method)
vr MaxTimeout in "net/config"    // import a variable/constant/singleton
```

### Capsule (encapsulation)
```khayyam
tp {name} cp { ___ }
```
- Fields: one `fieldName fieldType` per line.
- Fields are **never** directly accessible from outside — only via methods. No public fields, ever.

### Method
```khayyam
tp {name} mt (self {type_owner}) ({args}...) ({returns}...) { ___ }
```
- A method is a callable capsule; the receiver (`self`) can be attached to *any* type, including an abstraction or another method.
- The three parentheses (`type_owner`, args, returns) are **always** written, even when empty.
- All args and returns are passed **strictly by reference**. There is no by-value passing.
- No `const`/`mut` keywords — mutation is only possible if the capsule explicitly exposes a mutating method.
- Body-less methods (`{}` omitted) are valid for: (a) abstraction contract signatures, (b) FFI linking against external `.s`/`.o` implementations.
- Calls always use a single `.` — no `::` or other secondary operator.
- **No `self` in signature → static, called on the type**: `TypeName.Method()`.
- **`self` in signature → instance, called on a variable**: `varName.Method()`.

### Abstraction (pure contract)
```khayyam
tp Reader ab
tp Read mt (self Reader) (data Element) (err Error)   // defined independently, body-less
```
- Abstractions hold no logic/state/bodies. Methods fulfilling the contract are defined outside it.
- Abstractions compose via a `{}` block at the definition site.
- Abstractions may only use other abstractions as args/returns — never concrete capsules.
- **No generics syntax** (no `<T>`, `[T]`). Covariant returns + "Smart Compilation" replace the need for it.

### Scope
```khayyam
tp {name} sc { ___ }
```
Used for control-flow constructs (`IF`, `LOOP`, `GOTO`, etc., built as libraries, not language keywords). Only valid inside a method body.

### Variable
```khayyam
vr {name} {type}
```
- Variables are **logical references**, never raw data. No `=` assignment operator anywhere, and no implicit copying (deep or shallow).
- Explicit duplication requires a method call, e.g. `vr newVar Type` then `newVar.CopyFrom(oldVar)`.

## Design principles worth applying even when not asked explicitly

- **Behavior over type identity** — prefer expressing "what capability is required" over "what concrete type is this." This is why Khayyam has no generics syntax.
- **No primitive obsession** — raw `string`/`int`/`bool` used for business values is discouraged; wrap them in named capsules (e.g. `W32`, not `int`; `UserRegistry`, not `Map<ID, User>`).
- **No utility dumping grounds** — avoid suggesting `Utils`/`Helpers`/`Common` capsules; push responsibilities into domain-meaningful capsules instead.
- **Self-documenting naming is enforced, not stylistic** — magic numbers and opaque generic containers are treated as violations of intent, not just style nits.
- **Syntactic atomicity** — one syntactic construct per semantic intent.

These are philosophy/direction from `khayyam-design_philosophy.md`, not settled mechanisms for every case — if a concrete question depends on a mechanism not covered by the files listed above, fetch the relevant document via `memar-navigator` rather than inventing an answer.

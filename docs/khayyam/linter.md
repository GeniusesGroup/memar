---
Title: "Khayyam Linter & Tooling Rules"
Status: Proposed
Start Date: 2026-06-22
ID: 495025
---

# Khayyam Linter & Tooling Rules
This document is addressed to the developers of a Khayyam linter and its companion tooling (IDE integration, LSP, code generators) — not to the Khayyam language. Nothing here adds to, restricts, or amends Khayyam's syntax or semantics; every rule below is a recommendation about how Khayyam's own thinking — Separation of Syntax and Governance above all — should find concrete manifestation in the tools that enforce governance.

## Abstract
In Khayyam, the linter is a fundamental pillar of the architecture, not an optional quality tool: the language keeps its core syntax minimal and deliberately hands the enforcement of safety, memory rules, and clean architecture to the linter and IDE tooling (see [Separation of Syntax and Governance](./khayyam.md#separation-of-syntax-and-governance-a-principle)). This document states what that handoff requires of the tools' implementers: IDE folding behaviors that keep architecture visible; the Orphan Rule preventing Monkey Patching of external types; generated accessor methods that keep Information Hiding workable; a basket of suggested diagnostics (naming, type suggestions, type-as-argument meaningfulness, `sc`-based analysis) that carry Khayyam's preferences without ever becoming language restrictions. Every rule here constrains a *tool*, never the language: a linter rule can be disabled — that is precisely why the language assigns only governance, never ontology, to this layer.

## Introduction

### Motivation
Khayyam's central architectural move is a handoff: syntax defines what may exist (compiler-enforced), governance defines how well-formed instances flow (linter/framework-enforced). The handoff's destination — the linter — is where most of Khayyam's safety and architectural discipline actually lives, which makes the linter's implementers custodians of more of the system's integrity than their counterparts in most language ecosystems. Yet the language specification, correctly, says almost nothing about how a linter should behave: governance policy is exactly what Khayyam refuses to fix at the language level, since organizations must be able to tune it without forking the language.

That refusal leaves a real gap this document fills: without a statement of the *default* governance posture, each linter team would have to re-derive from the language spec alone which diagnostics matter, which are suggestions versus obligations, and why the language deliberately left each one to tooling. The specific failure the document guards against is the linter quietly becoming a second compiler — a place where rules that feel important get hardened into de-facto language restrictions, undoing by tooling policy what the grammar refuses to do by syntax. Every rule below is written to be relaxable by configuration, and to say so explicitly.

## Explanation

### IDE Behavior & Visual Formatting
- **Auto-Folding:** To manage inclusion bloat and improve readability, IDEs MUST automatically fold continuous blocks of `tp ... in ...` and `vr ... in ...` declarations at the top of files.
- **Structural Overview:** By default, IDEs SHOULD fold all capsule and method bodies (`{}`) when a file is first opened. This forces the reader to see the high-level architecture and contracts before diving into the implementation details.

Aggressive default folding can hide relevant context from a reader who does not yet know where anything is — the "see the architecture first" benefit applies once a reader knows the file's shape, and can disorient on first contact. Fold-state persistence and per-project overrides are therefore not conveniences but mitigations this rule depends on.

### Cross-file Methods — The Orphan Rule (Monkey Patching Prevention)
Since Khayyam does not use explicit `package` boundaries, large capsules or logic blocks can be naturally split across multiple files within a directory. To achieve this, a type can be imported (`in`) into a new file, and new methods (`mt`) can be attached to it there.

Since Khayyam relies entirely on the file system for modularity (without `package` keywords), capsules can be legally split across multiple files in the same directory. Syntactically, Khayyam allows you to attach a method to any imported type. This provides the freedom to split implementations across multiple files cleanly. However, to prevent unintended mutations of third-party libraries (Monkey Patching), Khayyam relies on its strict Linter.

The Linter differentiates between extending a *local directory type* (which is fully permitted for file-splitting) and mutating a *distant/external library type* (which will trigger a strict warning or error by default). This design keeps the core syntax simple while allowing organizations to customize strictness via Linter rules.

- **The Rule:** The Linter MUST strongly warn or throw an error if a developer attempts to attach a new method (`mt`) to a type (`tp`) that was imported from an external library or a different domain directory.
- **Why:** This prevents unpredictable "Monkey Patching" and mutation of third-party behavior. If external extension is needed, the developer must use Composition (wrapping the external capsule in a local one).

The local/distant boundary is directory-based, so legitimate monorepo cases — a shared internal library consumed across nearby directories — fall on the "distant" side and require composition even when the consumer and library are maintained by the same team. The rule also cannot distinguish a *new* method from a *re-definition* of an existing one purely by syntax; the latter needs the linter to resolve the full import graph, which is real implementation cost.

### Boilerplate Generation
- **Getters & Setters:** To strictly enforce Information Hiding, capsules expose no data fields. The Linter MUST assist developers by automatically generating global `get` and `set` methods for internal fields when requested.
- Generating accessors on request keeps the capsule's behavioral contract explicit — every accessor appears in source, is reviewable, and can carry domain rules — rather than synthesizing a public surface the author never wrote. The field-access enforcement this rule pairs with is specified once, below, under [Linters](#linters).

Generated accessors can accumulate into the same wide, meaningless public surface Information Hiding exists to prevent — a capsule whose every field gets a mechanical `get`/`set` pair has, in effect, public fields with extra steps. The generation assist is only faithful to the encapsulation principle when accessors are requested deliberately, which tooling cannot force.

### Suggested Diagnostics
The diagnostics in this section are *suggestions to the implementer* and, through configuration, to organizations — none is a language-level restriction, and each says which side of the [syntax/governance line](./khayyam.md#separation-of-syntax-and-governance-a-principle) it lives on. They are collected here because they share that character, not because they relate to one another mechanically.

A "suggested" tier is inherently softer than the MUST-level rules above it, and its guidance ages differently: because these diagnostics encode *current* thinking about what good Khayyam looks like, they are the most likely content in this document to need revision as the ecosystem matures — a suggested diagnostic that no longer reflects best practice should be revised or retracted here rather than silently kept for compatibility.

#### Linters
- Linters MUST suggest naming e.g. in importing other packages, ...
- Linter MUST provide `Type` suggestion in developing of codes.
- Linter MUST help to generate some useful methods like getter and setter methods. For each capsule field the developer must define explicit `get`/`set` methods; direct field read/write outside the capsule's own methods is a **linter error** (not a compiler error). Direct access is already impossible at the language level because fields are private (see [Sovereign Encapsulation](./encapsulation.md#sovereign-encapsulation)); the linter's role is governance and DX scaffolding, not syntax enforcement.

#### Type-as-Argument for `sc`/`mt` (Suggested Rule)
Khayyam syntax allows an argument position to be satisfied either by a variable (`vr`) of the declared type or, for the sub-types `sc` (code scope) and `mt` (method), by the type itself passed as a type-level argument (e.g., `CF.IF(isValid, ValidScope)` where `ValidScope` is `tp ValidScope sc { ... }`). Whether a name in an argument position denotes a variable or a type is resolved by the compiler from the AST — from the expected type in the callee's signature there is no ambiguity.

- **Suggested linter rule:** Passing a type itself is *meaningful* only for `sc`/`mt`. Other types (capsules, abstractions) should normally be passed via a `vr`; a bare type appearing where a capsule/abstraction value is expected should be flagged as suspicious. Passing an `mt` value in closure style (capturing state as an implicit capsule) is discouraged — see [Closures as Implicit Capsule Syntax](./encapsulation.md#closures-as-implicit-capsule-syntax). These are *suggested* linter diagnostics, not language-level restrictions — an organization may relax them.

#### Compiler Event Abstraction for Analysis (DAA/Linter)
The compiler is an independent application that emits control-flow events (entering/leaving an `sc`, taking/skipping a branch). Analysis libraries such as DAA or the linter subscribe to these events rather than requiring the compiler to recognize a specific library's `IF` by name.

- **Suggested linter rule:** A DAA implementation should treat `sc` as the common denominator across all control-flow libraries, not `IF`/`ELSE` names. Branch exclusivity is learned from `sc` events, not from special-casing a privileged library. See [the compiler-side statement of the same contract](./compiler.md#control-flow-via-sc-and-jump-primitives).

## Results
No observed results are recorded yet. This section will be updated when tooling built against these rules yields evidence that can be distinguished from their intended rationale.

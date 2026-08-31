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

#### Discussion

##### Drawbacks
Aggressive default folding can hide relevant context from a reader who does not yet know where anything is — the "see the architecture first" benefit applies once a reader knows the file's shape, and can disorient on first contact. Fold-state persistence and per-project overrides are therefore not conveniences but mitigations this rule depends on.

##### Rationale and alternatives
- **Leave folding entirely to user preference (rejected as a *default*):** the folded-by-default view is the design's statement of what a file is — contracts and structure first, implementation second. Individual developers may unfold; the default expresses the intended reading order rather than enforcing it.
- **Let the linter warn about over-long import blocks instead (rejected):** warning changes nothing about reading order; folding solves the actual problem (inclusion bloat crowding out architecture) rather than nagging about it.

##### Prior art
Code-folding as a default view for structure-first reading is common in IDEs (Visual Studio's region folding, JetBrains' structural collapse), though rarely as opinionated about *what* the default view should teach. The stronger precedent for "contracts before implementation" is interface-first file organization in Go's idiom of reading a file's declarations top-down; the folding rule makes that reading order mechanical rather than customary.

##### Unresolved questions
Whether fold state should persist per-file, per-project, or reset per session — and whether the SHOULD-level body folding should degrade for very small files — are IDE UX decisions not settled here.

### Cross-file Methods — The Orphan Rule (Monkey Patching Prevention)
Since Khayyam does not use explicit `package` boundaries, large capsules or logic blocks can be naturally split across multiple files within a directory. To achieve this, a type can be imported (`in`) into a new file, and new methods (`mt`) can be attached to it there.

Since Khayyam relies entirely on the file system for modularity (without `package` keywords), capsules can be legally split across multiple files in the same directory. Syntactically, Khayyam allows you to attach a method to any imported type. This provides the freedom to split implementations across multiple files cleanly. However, to prevent unintended mutations of third-party libraries (Monkey Patching), Khayyam relies on its strict Linter.

The Linter differentiates between extending a *local directory type* (which is fully permitted for file-splitting) and mutating a *distant/external library type* (which will trigger a strict warning or error by default). This design keeps the core syntax simple while allowing organizations to customize strictness via Linter rules.

- **The Rule:** The Linter MUST strongly warn or throw an error if a developer attempts to attach a new method (`mt`) to a type (`tp`) that was imported from an external library or a different domain directory.
- **Why:** This prevents unpredictable "Monkey Patching" and mutation of third-party behavior. If external extension is needed, the developer must use Composition (wrapping the external capsule in a local one).

#### Discussion

##### Drawbacks
The local/distant boundary is directory-based, so legitimate monorepo cases — a shared internal library consumed across nearby directories — fall on the "distant" side and require composition even when the consumer and library are maintained by the same team. The rule also cannot distinguish a *new* method from a *re-definition* of an existing one purely by syntax; the latter needs the linter to resolve the full import graph, which is real implementation cost.

##### Rationale and alternatives
- **Language-level restriction (an orphan rule like Rust's, compiler-enforced; rejected):** Khayyam's grammar deliberately allows attaching a method to any imported type; hardening the boundary into syntax would move a governance preference into ontology, and organizations with different extension policies would have no escape hatch.
- **Permit external extension freely (rejected as default):** Monkey Patching breaks the referential trust a reader places in an external library's documented behavior — the same hidden-behavior problem Khayyam's no-magic principles target, arriving through the back door of tooling permissiveness.
- **Linter-enforced with organizational override (chosen):** the default protects the common case; an organization that genuinely owns both sides of the boundary can relax it by configuration, making the policy decision visible in the linter config rather than silently available to everyone.

##### Prior art
Rust's orphan rule is the closest mainstream mechanism, but it is compiler-enforced — a language-level ontology decision Khayyam explicitly declines to make. Go's prohibition on defining methods on types from other packages is similarly structural. C#'s extension methods and Kotlin's extension functions permit external extension as an ordinary, visible-language feature — evidence that extension itself is not inherently unsafe, but that its *governance* is where the design decision belongs. Khayyam takes the middle path: syntactically free, governed by default.

##### Unresolved questions
Whether "local directory" is the right unit for the boundary — as opposed to a repository root, an explicitly declared ownership file, or a linter configuration map — is not settled; the directory heuristic is simple but arbitrary at monorepo scale.

### Boilerplate Generation
- **Getters & Setters:** To strictly enforce Information Hiding, capsules expose no data fields. The Linter MUST assist developers by automatically generating global `get` and `set` methods for internal fields when requested.
- Generating accessors on request keeps the capsule's behavioral contract explicit — every accessor appears in source, is reviewable, and can carry domain rules — rather than synthesizing a public surface the author never wrote. The field-access enforcement this rule pairs with is specified once, below, under [Linters](#linters).

#### Discussion

##### Drawbacks
Generated accessors can accumulate into the same wide, meaningless public surface Information Hiding exists to prevent — a capsule whose every field gets a mechanical `get`/`set` pair has, in effect, public fields with extra steps. The generation assist is only faithful to the encapsulation principle when accessors are requested deliberately, which tooling cannot force.

##### Rationale and alternatives
- **Have the compiler auto-generate accessors for all fields (rejected):** synthesizes a public surface the author never declared, weakening Information Hiding by default; a capsule's contract should contain only behavior its author wrote or explicitly requested.
- **Provide no assist (rejected):** without a generation assist the accessor requirement becomes heavy boilerplate, and boilerplate fatigue is exactly the pressure that produces demands to reopen field exposure — the failure this rule exists to prevent.
- **Linter/IDE-generated on explicit request (chosen):** the assist removes the mechanical cost while keeping every accessor visible and reviewable in source.

##### Prior art
Java's IDE-generated getter/setter convention is the direct precedent, including its well-known failure mode (bean-shaped classes whose encapsulation is nominal). Go's explicit-methods-only culture shows the opposite pole: no generation, maximal ceremony. Khayyam's position is the middle one — generation is available and expected, but each generated method enters the source and the capsule's contract as if hand-written.

##### Unresolved questions
Whether generated setters should default to bare assignment or to routing through a validation hook the capsule declares (e.g., a designated `Set`-guard method) is not settled; the latter preserves domain invariants but adds a convention to be specified.

### Suggested Diagnostics
The diagnostics in this section are *suggestions to the implementer* and, through configuration, to organizations — none is a language-level restriction, and each says which side of the [syntax/governance line](./khayyam.md#separation-of-syntax-and-governance-a-principle) it lives on. They are collected here because they share that character, not because they relate to one another mechanically.

#### Linters
- Linters MUST suggest naming e.g. in importing other packages, ...
- Linter MUST provide `Type` suggestion in developing of codes.
- Linter MUST help to generate some useful methods like getter and setter methods. For each capsule field the developer must define explicit `get`/`set` methods; direct field read/write outside the capsule's own methods is a **linter error** (not a compiler error). Direct access is already impossible at the language level because fields are private (see [Sovereign Encapsulation](./khayyam-encapsulation.md#sovereign-encapsulation)); the linter's role is governance and DX scaffolding, not syntax enforcement.

#### Type-as-Argument for `sc`/`mt` (Suggested Rule)
Khayyam syntax allows an argument position to be satisfied either by a variable (`vr`) of the declared type or, for the sub-types `sc` (code scope) and `mt` (method), by the type itself passed as a type-level argument (e.g., `CF.IF(isValid, ValidScope)` where `ValidScope` is `tp ValidScope sc { ... }`). Whether a name in an argument position denotes a variable or a type is resolved by the compiler from the AST — from the expected type in the callee's signature there is no ambiguity.

- **Suggested linter rule:** Passing a type itself is *meaningful* only for `sc`/`mt`. Other types (capsules, abstractions) should normally be passed via a `vr`; a bare type appearing where a capsule/abstraction value is expected should be flagged as suspicious. Passing an `mt` value in closure style (capturing state as an implicit capsule) is discouraged — see [Closures as Implicit Capsule Syntax](./khayyam-encapsulation.md#closures-as-implicit-capsule-syntax). These are *suggested* linter diagnostics, not language-level restrictions — an organization may relax them.

#### Compiler Event Abstraction for Analysis (DAA/Linter)
The compiler is an independent application that emits control-flow events (entering/leaving an `sc`, taking/skipping a branch). Analysis libraries such as DAA or the linter subscribe to these events rather than requiring the compiler to recognize a specific library's `IF` by name.

- **Suggested linter rule:** A DAA implementation should treat `sc` as the common denominator across all control-flow libraries, not `IF`/`ELSE` names. Branch exclusivity is learned from `sc` events, not from special-casing a privileged library. See [the compiler-side statement of the same contract](./khayyam-compiler.md#control-flow-via-sc-and-jump-primitives).

#### Discussion

##### Drawbacks
A "suggested" tier is inherently softer than the MUST-level rules above it, and its guidance ages differently: because these diagnostics encode *current* thinking about what good Khayyam looks like, they are the most likely content in this document to need revision as the ecosystem matures — a suggested diagnostic that no longer reflects best practice should be revised or retracted here rather than silently kept for compatibility.

##### Rationale and alternatives
- **Promote these diagnostics to language rules (rejected):** each would either deny existence (ontology — the compiler's side of the line) or harden one organization's flow preference into universal law. The type-as-argument case is the concrete example: the language deliberately leaves which types may be passed as type-arguments unrestricted, keeping syntax generic and placing the meaningfulness rule in tooling.
- **Scatter these diagnostics across the construct documents they relate to (rejected):** each construct document states its own language-level semantics; collecting the tooling-side diagnostics in one place keeps the governance layer reviewable as a whole, and keeps the construct documents free of implementation advice that could drift from actual linter behavior.

##### Prior art
Go's `vet` and `staticcheck` occupy the same tier: official-tooling diagnostics that encode community consensus without being language rules. The naming/type-suggestion requirements mirror LSP-based assists in modern IDEs generally. The `sc`-as-common-denominator rule is Khayyam-specific, mirroring the compiler's own event contract (see its Prior art under [Control Flow via `sc` and Jump Primitives](./khayyam-compiler.md#control-flow-via-sc-and-jump-primitives)).

##### Unresolved questions
How a suggested diagnostic is promoted (or demoted) over time — and whether the promotion path runs through organization adoption, a governance RFC, or default-on status in a reference linter — is not settled.

## Results
No observed results are recorded yet. This section will be updated when tooling built against these rules yields evidence that can be distinguished from their intended rationale.

## Discussion

### Drawbacks
Khayyam's architecture concentrates unusual responsibility in its linter: safety disciplines that other languages enforce structurally (error-inspection, memory-rule adherence, encapsulation etiquette) are only as strong as the linter configuration in force. A team running a weak or disabled linter loses those guarantees with no language-level safety net — a cost accepted knowingly under the Separation of Syntax and Governance, but a real one. These rules also speak for tools that do not yet exist; until implementations mature, the document governs by intention rather than by enforced behavior.

### Rationale and alternatives
- **Fold tooling rules into the construct documents ([Khayyam](./khayyam.md), [Encapsulation](./khayyam-encapsulation.md), [Control Flow](./khayyam-control_flow.md), ...)** *(rejected)*: each construct document states what the language does and why; sprinkling IDE and linter behavior through them would blur the syntax/governance line the documents exist to demonstrate, and would couple language-document stability to tooling decisions that change far more often.
- **Keep linter behavior unspecified (rejected):** governance is the linter's entire job under Khayyam's architecture; leaving it undocumented makes each implementation's policy an accident of whichever team built it, and quietly converts "governance is tunable" into "governance is whatever the default build does."
- **A dedicated document per tool (linter.md, ide.md, lsp.md; rejected for now)**: at the current stage the tooling surface is one coherent set of recommendations; splitting it would multiply cross-referencing overhead before there are distinct implementations to govern. Revisit if the IDE and linter concerns genuinely diverge.

### Prior art
Go is the closest structural precedent: a deliberately minimal language paired with official tooling (`gofmt`, `vet`) that carries community standards the grammar does not. The difference is degree — Go's tooling is conventionally important, while Khayyam's linter is architecturally load-bearing by design, holding responsibilities (safety enforcement, orphan governance) that Go's compiler or Rust's compiler own structurally. This inversion is Khayyam's own; the prior art establishes the pattern, not the weight.

### Unresolved questions
1. What is the concretely specified boundary between compiler-enforced and linter-enforced for each diagnostic this document mentions — in particular which diagnostics MUST be on by default in a reference linter, versus opt-in? The [syntax/governance principle](./khayyam.md#separation-of-syntax-and-governance-a-principle) supplies the test ("existence vs. flow"), but per-rule classification needs a settled pass.
2. Should the boundary unit for the [Orphan Rule](#cross-file-methods--the-orphan-rule-monkey-patching-prevention) (directory vs. repository vs. declared ownership) be configurable per organization, and what does the default configuration ship as?

### Future possibilities
- A reference linter configuration, shipped with the first tooling release, encoding the MUST-level rules as defaults and the suggested diagnostics as opt-in sets.
- An extension point for organization-defined diagnostics, so custom governance rules plug into the same machinery rather than living in ad-hoc scripts.
- A conformance suite for linter implementations, mirroring the compiler-side one proposed in [Khayyam Compiler Directives → Future possibilities](./khayyam-compiler.md#discussion).

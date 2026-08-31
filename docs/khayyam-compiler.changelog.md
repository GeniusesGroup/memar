# Khayyam Compiler Changelog

## Changelog

### Correct control-flow and compile-time-function contracts
- Time: 2026-08-27T00:00:00Z
- Type: Fixed
- Cited:
  - [Control Flow in Khayyam](./khayyam-control_flow.md) — Depends_on: `sc` and event abstraction that the compiler exposes
  - [Variable in Khayyam](./khayyam-variable.md) — Reference: domain-driven arithmetic and `FromString` human-readable text concerns
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: clarified that `goto` as a keyword is retired thinking and that the compiler is an independent app emitting events for DAA
  - [Super Z](../CONTRIBUTORS.md#super-z) — rewrote: content below

#### Summary
Replaces `Control Flow via Framework Intrinsics` (which claimed the compiler “treats the framework’s `IF` as an intrinsic” and listed `goto` as the only native branching keyword) with `Control Flow via `sc` and Jump Primitives`: the AST recognizes only `sc` and low-level jump intrinsics (lowered to `goto` at IR, not a source keyword); framework `IF`/`ELSE` are ordinary library code; the compiler emits `sc` entry/exit and jump events to which DAA/linter subscribe. Corrects the `closeIdleSocket` example that inlined `Config.CNF_KeepAlive_Idle()` as an argument to `checkIdlePass` to the statement form with a named `idleDur` variable per the no-expression-chaining rule. Clarifies `Compile-Time Functions`: `W32`/`NanoSecond` are not privileged types; eligibility is a property of an explicitly designated pure/const method whose inputs are constants; the string `"7200"` is human-readable text for a typed variable, not a magic number.

#### Rationale and alternatives
Alternatives for the control-flow wording: (a) keep `goto` as keyword and `IF` as intrinsic (rejected — reintroduces the coupling the design exists to avoid); (b) move branching into syntax (rejected). For compile-time text: (a) treat `W32` as privileged (rejected — violates Zero-Magic), (b) move all work to runtime (rejected — loses pre-compilation guarantee).

---

### Clarify runtime patching vs. Immutable Infrastructure
- Time: 2026-08-27T00:00:00Z
- Type: Changed
- Cited:
  - [Khayyam Runtime Specification](./khayyam-runtime.md) — Reference: the same `unsafe` runtime-patching description
  - [Polymorphism in Khayyam](./khayyam-polymorphism.md) — Reference: the Dynamic Dispatch Reducibility note that expects reducibility under Immutable Infrastructure
- Contributors:
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below

#### Summary
Appends to `Change logic in runtime` a relation note: the default/safe deployment model is Immutable Infrastructure (no runtime capability addition without recompilation); the described `unsafe` WASM-like module replacement is an explicit, opt-in escape hatch, audited and never used for normal evolution, and therefore does not contradict the principle.

---

### Migrate to the Explanation-facet structure
- Time: 2026-08-30T00:00:00Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](./documentation-explanation.md) — Depends_on: the structure this migration follows — YAML front matter, the `Abstract → Introduction → Explanation → Results → Discussion` body, and the per-topic Discussion pattern — is that specification's, applied to this document for the first time.
  - [Khayyam - Programming Language](./khayyam.md) — Reference: *Khayyam Is Not Its Own Compiler or Runtime* and *Separation of Syntax and Governance*, which supply the framing for the new Abstract, Motivation, and Discussion content.
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested: migrate this document (and its two sibling tooling documents) to the latest documentation methodology; clarified the framing constraint that governs the new sections — none of the three tooling documents may impose anything on Khayyam itself, since together they are recommendations to each component's developers about how Khayyam's own thinking should find concrete manifestation.
  - [Super Z](../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote: content below.

#### Summary
This document is now structured per `documentation-explanation.md`: YAML front matter added (Status: Proposed; Start Date and ID assigned retroactively from the file's first commit date, 2026-06-22); Abstract, Motivation, per-topic Discussion sections, Results, and a document-wide Discussion added. The framing thread through every new section is the requested one: this document binds compiler *implementers*, never the language — each directive records how Zero-Magic Core, no-privileged-types, and Separation of Syntax and Governance must manifest in an implementation, and the specific shortcuts that would quietly reintroduce magic (special-casing a framework's `IF`, hardcoding `main`, privileged numeric types, normalized runtime patching). No construct-level content was removed: Control Flow via `sc` and Jump Primitives (with GOTO lowering detail and the commands-break rule), Environment-Agnostic Entry Points (with Delegation/Adaptability bullets), Compile-Time Functions (with the `CNF_KeepAlive_Idle` example and no-privileged-types clarification), and Change Logic in Runtime (with the Immutable Infrastructure relation note) are all preserved, reorganized under Explanation with their new Discussion sections derived from Khayyam's own philosophy documents rather than from new design decisions. New open questions recorded: the compiler event schema needs its own specification; the purity-designation mechanism is unspecified; what `unsafe` gates is unspecified; the "what Khayyam specifies vs. what an implementation provides" boundary remains shared with `khayyam.md`.

#### Rationale and alternatives
Considered writing the new Discussion content as fresh design contributions (e.g., proposing a concrete event schema or designation syntax while at it). Rejected: this migration's purpose is structural, and the document's own framing forbids it from deciding things onto the language — new design belongs in its own session with Omid's review. Also considered assigning an ID at current time instead of retroactively; rejected in favor of the Start-Date-derived hour value per the ID spec's retroactive-numbering provision.

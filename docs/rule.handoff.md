# Rule Handoff
Open work for `rule.md`. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Module framing versus graph-node framing
[Modularity](./modularity.md#rules-as-a-provisional-term) and [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule) describe Rule differently. Are these two views of one concept, or two concepts that need distinct names?

### Shared notation for linter-checkable Rules
[Linter handoff → rule-authorship notation](./protocols/computer/linter.handoff.md#the-rule-authorship-notation) remains open. Should `rule.md` grow a Practice companion once notation settles?

### Are ontology checks Rules at all?
[Rule → What a Rule Is](./rule.md#what-a-rule-is) counts both ontology rules (the compiler gate: what may exist) and governance rules (how admitted instances are kept) as Rules. [Rule → Who Owns and Introduces Rules](./rule.md#who-owns-and-introduces-rules) says a Rule is introduced by an owner and is not part of the language or protocol. A grammar's well-formedness check is part of the language itself, not a replaceable owner's claim. So either ontology checks are not Rules (they are the specification's own definition), or "not part of the language" holds only for governance rules. Which one?

### Rule-engine protocol document
Should `modules/process/rule/` and `modules/process/rules-engine/` gain a protocol-level specification under `docs/protocols/process/`, or remain implementation surfaces cited from `rule.md`?

## Follow-up work: relocate document-level rules
Inventory of normative rule passages still stated at document level (not moved in this session). Each entry: anchor, short quote, proposed `rules/` target. Count: **32** entries.

### `docs/khayyam/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [inheritance.md#compiler-rules](./khayyam/inheritance.md#compiler-rules) → No Implicit Behavior Acquisition | "Embedding a capsule … does not expose the inner capsule's methods … automatically." | `modules/khayyam/rules/no-implicit-behavior-acquisition/` |
| [inheritance.md#compiler-rules](./khayyam/inheritance.md#compiler-rules) → Explicit Delegation Required | "the developer must explicitly define a method on the host capsule and transparently delegate" | `modules/khayyam/rules/explicit-delegation-required/` |
| [inheritance.md#compiler-rules](./khayyam/inheritance.md#compiler-rules) → Abstraction Conformance Is Structural | "influencing-variable types must match exactly … influenced-variable types … covariant return" | `modules/khayyam/rules/abstraction-conformance-structural/` |
| [inheritance.md#compiler-rules](./khayyam/inheritance.md#compiler-rules) → Abstractions Have No Behavior | "An abstraction (`ab`) cannot contain method bodies, state, or default implementations." | `modules/khayyam/rules/abstractions-have-no-behavior/` |
| [inheritance.md#linter-rules](./khayyam/inheritance.md#linter-rules) → Anti-Lazy Inheritance Check | "blocks any patterns … attempting to create implicit method promotion hooks" | `modules/khayyam/rules/anti-lazy-inheritance/` |

### `docs/protocols/process/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [error.md#enforcement-of-the-each-error-is-its-own-type-rule](./protocols/process/error.md#enforcement-of-the-each-error-is-its-own-type-rule) | "`Err` prefix with the remainder in PascalCase" naming convention | `modules/process/error/rules/err-prefix-naming/` |
| [control-flow.md#two-etymologically-distinct-roots-not-base-plus-negation](./protocols/process/control-flow.md#two-etymologically-distinct-roots-not-base-plus-negation) | "prefer two etymologically distinct roots over a base term plus its negation" | `modules/process/control-flow/rules/conditional-pair-naming/` |
| [control-flow.md#library-defined-control-flow](./protocols/process/control-flow.md#library-defined-control-flow) → IF/ELSE pairing | "`ELSE` always takes an explicit reference back to the same condition value it pairs with" | `modules/process/control-flow/rules/else-explicit-condition-reference/` |

### `docs/protocols/computer/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [compiler.md#runtime-mutation-of-the-artifact-is-unsafe](./protocols/computer/compiler.md#runtime-mutation-of-the-artifact-is-unsafe) | "MUST be tagged `unsafe`" for runtime binary patch capability | `modules/computer/compiler/rules/runtime-mutation-unsafe/` |
| [compiler.md#the-compiler-recognizes-language-primitives-not-library-names](./protocols/computer/compiler.md#the-compiler-recognizes-language-primitives-not-library-names) | "does not treat library-provided operations as intrinsics" | `modules/computer/compiler/rules/no-library-intrinsics/` |
| [compiler.md#entry-and-lifecycle-are-not-grammar](./protocols/computer/compiler.md#entry-and-lifecycle-are-not-grammar) | "does not hardcode a syntax-level entry point or lifecycle … into the language" | `modules/computer/compiler/rules/no-grammar-entry-point/` |
| [linter.md#how-a-governance-rule-is-authored](./protocols/computer/linter.md#how-a-governance-rule-is-authored) | Required members: Subject, Tier, Default, Override | `modules/computer/linter/rules/governance-rule-schema/` (meta-rule for rule shape) |

### `docs/protocols/memory/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [memory.md#teardown-is-explicit-and-automation-writes-source](./protocols/memory/memory.md#teardown-is-explicit-and-automation-writes-source) | "every execution path … must invoke … release" | `modules/computer/capsule/rules/explicit-teardown-paths/` |
| [memory.md#safety-enforcement-is-governance](./protocols/memory/memory.md#safety-enforcement-is-governance) | memory-safety checks are linter/compiler governance, relaxable | `modules/computer/capsule/rules/memory-safety-governance/` |
| [memory.md#uninitialized-reads-are-refused](./protocols/memory/memory.md#uninitialized-reads-are-refused) | "A value that has not been definitely assigned is not readable" | `modules/computer/capsule/rules/uninitialized-read-refused/` |
| [memory.md#copy-and-ownership-semantics-are-contract-members](./protocols/memory/memory.md#copy-and-ownership-semantics-are-contract-members) | "contract states whether the caller retains ownership … must be *written*" | `modules/computer/capsule/rules/ownership-contract-members/` |
| [memory.md#the-boundary-copy-convention-stated](./protocols/memory/memory.md#the-boundary-copy-convention-stated) | "producing side prepares a copy the receiving side may retain" | `modules/computer/capsule/rules/boundary-copy-default/` |
| [memory.md#allocation-claims-are-measurement-claims](./protocols/memory/memory.md#allocation-claims-are-measurement-claims) | allocation claims "stated with the measurement that supports them" | `modules/computer/capsule/rules/allocation-claims-measured/` |

### `docs/protocols/net/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (HopCount encoding) | "`0x00` is reserved exclusively as the Broadcast sentinel" | `modules/net/chapar/rules/hopcount-broadcast-sentinel/` |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (Broadcast frame shape) | "BroadCast frame must have all hop port number space with 0-byte data" | `modules/net/chapar/rules/broadcast-frame-shape/` |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (Switching adaptor) | "one of them must be as switching adaptor" | `modules/net/chapar/rules/switching-adaptor-required/` |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (Hop rewrite) | "Switch device must rewrite the received port number" | `modules/net/chapar/rules/hop-port-rewrite/` |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (Next Hop advance) | "forwarding switch advances Next Hop past its own stamped position" | `modules/net/chapar/rules/next-hop-advance/` |
| [chapar.md#rules](./protocols/net/chapar.md#rules) (Terminal drop) | "Unicast frame whose Next Hop points past the last hop-port entry … is dropped" | `modules/net/chapar/rules/terminal-unicast-drop/` |

### `docs/type*.md` and other `docs/` roots
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [type.md#structure-is-fixed-by-definition](./type.md#structure-is-fixed-by-definition) | "no concept introduction … can be minted into a running system" | `modules/computer/datatype/rules/structure-fixed-at-definition/` (ontology-tier; may remain concept-only) |
| [type.md#type-and-rules](./type.md#type-and-rules) | Taxonomy: invariants, constraints, behavioral rules, business rules | Concept framing only — no relocation; informs Rule kinds |
| [modeling.md#constraints-belong-to-the-constraining-concern](./modeling.md#constraints-belong-to-the-constraining-concern) | constraint modeled on constraining concern, not duplicated on resources | Modeling principle — optional `modules/modeling/rules/` if executable checks emerge |
| [terminology.md#architectural-rule](./terminology.md#architectural-rule) | reasoning order: problem → concepts → principles → technologies → tools → products | `organization` repo or `modules/terminology/rules/` — not Khayyam/protocol executable |
| [documentation-explanation.md#conventions](./documentation-explanation.md#conventions) | PascalCase front-matter fields; hyperlink cross-references | `docs/` documentation practice — not Module `rules/` |

### Notes on inventory
- Khayyam docs not listed above already link to `modules/khayyam/rules/` (naming, import, orphan extension, etc.).
- Memory module paths live under `modules/memory/`; capsule lifecycle targets remain under `modules/computer/capsule/` until a rule document states otherwise.
- Protocol documents that are **entirely** rule sets (for example [chapar.md](./protocols/net/chapar.md) wire format) may relocate rule-by-rule or gain a single `modules/net/chapar/rules/README.md` index without moving protocol narrative.

## Memar server defining document
No `docs/` document yet defines the Memar server as a concept. The name appears in [Khayyam execution handoff → Rule model](../modules/khayyam/execution.handoff.md) (diagnostics without target invocation) and [Knowledge → Knowledge and Code](./knowledge.md#knowledge-and-code) (callable generative services / language-server-style tools). Anticipated work on server capabilities is routed to those handoffs until a protocol document exists.

## Follow-up work: classify `modules/khayyam/rules/`
Plan only — read each rule, classify, move nothing. Counts over the 24 rules in the [Khayyam rules index](../modules/khayyam/rules/README.md): **(a) 5**, **(b) 5**, **(c) 15**.

### (a) Not Khayyam-specific — belong in another module's `rules/`
| Rule | Proposed home | Rationale |
| --- | --- | --- |
| [comment-policy](../modules/khayyam/rules/comment-policy/comment-policy.md) | `organization` repository or documentation practice | License header and documentation placement for this repository's `.kh` files — organizational policy, not Khayyam grammar |
| [file-layout](../modules/khayyam/rules/file-layout/file-layout.md) | `organization` repository or a future module-organization rules home | File size, declaration-order, and one-abstraction-per-protocol-file convention for human-authored sources in this repository — classified not Khayyam-specific; candidate to relocate when a module-organization rules home exists (no move yet) |
| [lifecycle-method-names](../modules/khayyam/rules/lifecycle-method-names/lifecycle-method-names.md) | `modules/memory/rules/` or `modules/computer/capsule/rules/` | Conventional `Deinit`/`Free`/`IsNull` spellings cite [Memory](./protocols/memory/memory.md), not Khayyam grammar |
| [observer-mutator](../modules/computer/adt/rules/observer-mutator/observer-mutator.md) | `modules/computer/adt/rules/observer-mutator/` (relocated 2026-09-29) | Liskov & Guttag ADT observer/mutator families — ADT protocol subject, not Khayyam grammar |
| [import-address](../modules/khayyam/rules/import-address/import-address.md) | `modules/dependency-management/rules/` (or the module that owns URI resolution) | URI scheme and repository-root base are dependency-management choices; Khayyam states only that `in` carries a URI |

### (b) Service capabilities — become Memar server services (not Rule text)
| Rule | Service capability | Rationale |
| --- | --- | --- |
| [abstraction-scaffolding](../modules/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md) | Delegation and abstraction scaffolding | Auto-generates missing delegation lines, method signatures, and remediation suggestions — generation, not a checkable condition |
| [method-separation](../modules/khayyam/rules/method-separation/method-separation.md) | `tidy --rule method-separation` | Source rewrite (blank lines between methods) |
| [go-clue-residue](../modules/khayyam/rules/go-clue-residue/go-clue-residue.md) | `tidy --rule go-clue-residue` | Source rewrite (Go clue block cleanup after port) |
| [commented-generic-bindings](../modules/khayyam/rules/commented-generic-bindings/commented-generic-bindings.md) | `tidy --rule commented-generic-bindings` | Source rewrite (generic Go methods → real Khayyam methods) |
| [result-parameter-names](../modules/khayyam/rules/result-parameter-names/result-parameter-names.md) | `tidy --rule result-parameter-names` | Source rewrite (`resultN`/`argN` → type-derived names) |

Additional generation not yet a separate rule but named in owner position (2026-09-29): **observer/mutator naming generation** (`Observer_X`/`Mutator_X` families) — today implemented in `abstraction_bridge.py observer-names`; should become a Memar server service, while [observer-mutator](../modules/computer/adt/rules/observer-mutator/observer-mutator.md) remains the governance condition for naming shape.

### (c) Genuinely Khayyam — keep under `modules/khayyam/rules/`
[comment-forms](../modules/khayyam/rules/comment-forms/comment-forms.md), [scope-placement](../modules/khayyam/rules/scope-placement/scope-placement.md), [unresolved-import](../modules/khayyam/rules/unresolved-import/unresolved-import.md), [name-not-declared](../modules/khayyam/rules/name-not-declared/name-not-declared.md), [kind-mismatch](../modules/khayyam/rules/kind-mismatch/kind-mismatch.md), [unbound-type-name](../modules/khayyam/rules/unbound-type-name/unbound-type-name.md), [identifier-naming](../modules/khayyam/rules/identifier-naming/identifier-naming.md), [abstraction-naming-heuristic](../modules/khayyam/rules/abstraction-naming-heuristic/abstraction-naming-heuristic.md), [qualified-names](../modules/khayyam/rules/qualified-names/qualified-names.md), [receiver-parameter-naming](../modules/khayyam/rules/receiver-parameter-naming/receiver-parameter-naming.md), [domain-capsule-naming](../modules/khayyam/rules/domain-capsule-naming/domain-capsule-naming.md), [type-as-argument](../modules/khayyam/rules/type-as-argument/type-as-argument.md), [orphan-extension](../modules/khayyam/rules/orphan-extension/orphan-extension.md), [receiver-method-names](../modules/khayyam/rules/receiver-method-names/receiver-method-names.md), [method-verb-phrases](../modules/khayyam/rules/method-verb-phrases/method-verb-phrases.md).

## Anticipated work
1. Relocate inventory entries per module owner review (priority: Khayyam compiler rules, Chapar wire rules, Error naming).
2. Update [linter.md](./protocols/computer/linter.md) authorship section to cite `rule.md` and `rules/` folder layout once relocations begin.
3. Resolve open framing question (Module versus graph-node) before promoting `rule.md` beyond Draft.
4. Execute the Khayyam rules classification above: relocate (a), extract (b) into Memar server services, keep (c) — after owner review; no moves in the planning session.

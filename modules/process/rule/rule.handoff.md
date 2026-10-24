# Rule Handoff
Open work for `rule.md`. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### Shared notation for linter-checkable Rules
Linter handoff → rule-authorship notation (`docs/modules/computer/linter.handoff.md#the-rule-authorship-notation`) remains open. Should `rule.md` grow a Practice companion once notation settles?

### Rule-engine protocol document
Should `modules/process/rule/` and `modules/process/rules-engine/` gain a protocol-level specification under `docs/modules/process/`, or remain implementation surfaces cited from `rule.md`?

### What a retiring party must establish
[Rule → Retiring a Rule](./rule.md#retiring-a-rule) states what retirement does to a Rule's claim and executable form, and nothing more. Nothing in Memar yet obliges a retiring party to establish what problem the Rule was introduced for, what it was holding true, or whether that problem still exists. The three positions a retiring party could take — the problem remains and this is still the right answer to it; the problem remains and something else answers it better now; the problem no longer exists — are stated nowhere, and the concept has no practice companion to state them in. A Rule, a mandatory step, a compatibility branch, and a legacy guard are one shape, so the answer is not specific to Rules. The question was first tracked from `process.research.002.md`, which is no longer in `docs/`.

### Vocabulary findings recorded from sources of no standing
[Rule Research 001](./rule.research.001.md) states what the SBVR and Business Rules Group vocabularies say, and read them from industry-community articles and a tertiary compilation rather than from the specification that defines them. Those sources carry no standing under [Documentation → Citations → Source standing](../../../modules-plugable/knowledge/documentation/documentation.md#citations), so the findings are this repository's own reading and are marked provisional. Whether they should be resolved against the OMG specification, or withdrawn as prior art that no document relies upon — `rule.md` derives its definition from this repository's own practice — is unanswered.

## Follow-up work: relocate document-level rules
Inventory of normative rule passages still stated at document level (not moved in this chat). Each entry: anchor, short quote, proposed `rules/` target. Count: **32** entries.

### `docs/khayyam/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| inheritance.md#compiler-rules (`docs/khayyam/inheritance.md#rules`) → No Implicit Behavior Acquisition | "Embedding a capsule … does not expose the inner capsule's methods … automatically." | `bundles/khayyam/rules/no-implicit-behavior-acquisition/` |
| inheritance.md#compiler-rules (`docs/khayyam/inheritance.md#rules`) → Explicit Delegation Required | "the developer must explicitly define a method on the host capsule and transparently delegate" | `bundles/khayyam/rules/explicit-delegation-required/` |
| inheritance.md#compiler-rules (`docs/khayyam/inheritance.md#rules`) → Abstraction Conformance Is Structural | "influencing-variable types must match exactly … influenced-variable types … covariant return" | `bundles/khayyam/rules/abstraction-conformance-structural/` |
| inheritance.md#compiler-rules (`docs/khayyam/inheritance.md#rules`) → Abstractions Have No Behavior | "An abstraction (`ab`) cannot contain method bodies, state, or default implementations." | `bundles/khayyam/rules/abstractions-have-no-behavior/` |
| inheritance.md#linter-rules (`docs/khayyam/inheritance.md#what-the-linter-may-add`) → Anti-Lazy Inheritance Check | "blocks any patterns … attempting to create implicit method promotion hooks" | `bundles/khayyam/rules/anti-lazy-inheritance/` |

### `docs/modules/process/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| error.md#enforcement-of-the-each-error-is-its-own-type-rule (`docs/modules/process/error.md#enforcement-of-the-each-error-is-its-own-type-rule`) | "`Err` prefix with the remainder in PascalCase" naming convention | `modules/process/error/rules/err-prefix-naming/` |
| control-flow.md#two-etymologically-distinct-roots-not-base-plus-negation (`docs/modules/process/control-flow.md#two-etymologically-distinct-roots-not-base-plus-negation`) | "prefer two etymologically distinct roots over a base term plus its negation" | `modules/process/control-flow/rules/conditional-pair-naming/` |
| control-flow.md#library-defined-control-flow (`docs/modules/process/control-flow.md#library-defined-control-flow`) → IF/ELSE pairing | "`ELSE` always takes an explicit reference back to the same condition value it pairs with" | `modules/process/control-flow/rules/else-explicit-condition-reference/` |

### `docs/modules/computer/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| compiler.md#runtime-mutation-of-the-artifact-is-unsafe (`docs/modules/computer/compiler.md#runtime-mutation-of-the-artifact-is-unsafe`) | "MUST be tagged `unsafe`" for runtime binary patch capability | `modules/computer/compiler/rules/runtime-mutation-unsafe/` |
| compiler.md#the-compiler-recognizes-language-primitives-not-library-names (`docs/modules/computer/compiler.md#the-compiler-recognizes-language-primitives-not-library-names`) | "does not treat library-provided operations as intrinsics" | `modules/computer/compiler/rules/no-library-intrinsics/` |
| compiler.md#entry-and-lifecycle-are-not-grammar (`docs/modules/computer/compiler.md#entry-and-lifecycle-are-not-grammar`) | "does not hardcode a syntax-level entry point or lifecycle … into the language" | `modules/computer/compiler/rules/no-grammar-entry-point/` |
| linter.md#how-a-governance-rule-is-authored (`docs/modules/computer/linter.md#how-a-governance-rule-is-authored`) | Required members: Subject, Tier, Default, Override | `modules/computer/linter/rules/governance-rule-schema/` (meta-rule for rule shape) |

### `docs/modules/memory/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| memory.md#teardown-is-explicit-and-automation-writes-source (`docs/modules/memory/memory.md#teardown-is-explicit-and-automation-writes-source`) | "every execution path … must invoke … release" | `modules/computer/capsule/rules/explicit-teardown-paths/` |
| memory.md#safety-enforcement-is-governance (`docs/modules/memory/memory.md#safety-enforcement-is-governance`) | memory-safety checks are linter/compiler governance, relaxable | `modules/computer/capsule/rules/memory-safety-governance/` |
| memory.md#uninitialized-reads-are-refused (`docs/modules/memory/memory.md#uninitialized-reads-are-refused`) | "A value that has not been definitely assigned is not readable" | `modules/computer/capsule/rules/uninitialized-read-refused/` |
| memory.md#copy-and-ownership-semantics-are-contract-members (`docs/modules/memory/memory.md#copy-and-ownership-semantics-are-contract-members`) | "contract states whether the caller retains ownership … must be *written*" | `modules/computer/capsule/rules/ownership-contract-members/` |
| memory.md#the-boundary-copy-convention-stated (`docs/modules/memory/memory.md#the-boundary-copy-convention-stated`) | "producing side prepares a copy the receiving side may retain" | `modules/computer/capsule/rules/boundary-copy-default/` |
| memory.md#allocation-claims-are-measurement-claims (`docs/modules/memory/memory.md#allocation-claims-are-measurement-claims`) | allocation claims "stated with the measurement that supports them" | `modules/computer/capsule/rules/allocation-claims-measured/` |

### `docs/modules/net/`
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (HopCount encoding) | "`0x00` is reserved exclusively as the Broadcast sentinel" | `modules/net/chapar/rules/hopcount-broadcast-sentinel/` |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (Broadcast frame shape) | "BroadCast frame must have all hop port number space with 0-byte data" | `modules/net/chapar/rules/broadcast-frame-shape/` |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (Switching adaptor) | "one of them must be as switching adaptor" | `modules/net/chapar/rules/switching-adaptor-required/` |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (Hop rewrite) | "Switch device must rewrite the received port number" | `modules/net/chapar/rules/hop-port-rewrite/` |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (Next Hop advance) | "forwarding switch advances Next Hop past its own stamped position" | `modules/net/chapar/rules/next-hop-advance/` |
| chapar.md#rules (`docs/modules/net/chapar.md#rules`) (Terminal drop) | "Unicast frame whose Next Hop points past the last hop-port entry … is dropped" | `modules/net/chapar/rules/terminal-unicast-drop/` |

### `docs/type*.md` and other `docs/` roots
| Anchor | Quote (abbrev.) | Proposed `rules/` folder |
| --- | --- | --- |
| [type.md#structure-is-fixed-by-definition](../../../docs/type.md#structure-is-fixed-by-definition) | "no concept introduction … can be minted into a running system" | `modules/computer/type/rules/structure-fixed-at-definition/` (ontology-tier; may remain concept-only) |
| [type.md#type-and-rules](../../../docs/type.md#type-and-rules) | Taxonomy: invariants, constraints, behavioral rules, business rules | Concept framing only — no relocation; informs Rule kinds |
| [modeling.md#constraints-belong-to-the-constraining-concern](../../../docs/modeling.md#constraints-belong-to-the-constraining-concern) | constraint modeled on constraining concern, not duplicated on resources | Modeling principle — optional `modules/modeling/rules/` if executable checks emerge |
| [terminology.md#architectural-rule](../../../docs/terminology.md#architectural-rule) | reasoning order: problem → concepts → principles → technologies → tools → products | `organization` repo or `modules/terminology/rules/` — not Khayyam/protocol executable |
| [documentation-explanation.md#conventions](../../../modules-plugable/knowledge/documentation/explanation/explanation.md#conventions) | PascalCase front-matter fields; hyperlink cross-references | `docs/` documentation practice — not Module `rules/` |

### Notes on inventory
- Khayyam docs not listed above already link to `bundles/khayyam/rules/` (naming, import, orphan extension, etc.).
- Memory module paths live under `modules/computer/memory/`; capsule lifecycle targets remain under `modules/computer/capsule/` until a rule document states otherwise.
- Protocol documents that are **entirely** rule sets (for example `docs/modules/net/chapar.md` wire format) may relocate rule-by-rule or gain a single `modules/net/chapar/rules/README.md` index without moving protocol narrative.

## Memar server defining document
No `docs/` document yet defines the Memar server as a concept. The name appears in Khayyam handoff → Rule model (`bundles/khayyam/khayyam.handoff.md`) (diagnostics without target invocation) and [Knowledge → Knowledge and Code](../../knowledge/knowledge.md#knowledge-and-code) (callable generative services / language-server-style tools). Anticipated work on server capabilities is routed to those handoffs until a protocol document exists.

## Follow-up work: classify `bundles/khayyam/rules/`
Plan only — read each rule, classify, move nothing. Counts over the 24 rules in the Khayyam rules index (`bundles/khayyam/rules/README.md`): **(a) 5**, **(b) 5**, **(c) 15**.

### (a) Not Khayyam-specific — belong in another module's `rules/`
| Rule | Proposed home | Rationale |
| --- | --- | --- |
| comment-policy (`bundles/khayyam/rules/comment-policy/comment-policy.md`) | `organization` repository or documentation practice | License header and documentation placement for this repository's `.kh` files — organizational policy, not Khayyam grammar |
| file-layout (`bundles/khayyam/rules/file-layout/file-layout.md`) | `organization` repository or a future module-organization rules home | File size, declaration-order, and one-abstraction-per-protocol-file convention for human-authored sources in this repository — classified not Khayyam-specific; candidate to relocate when a module-organization rules home exists (no move yet) |
| lifecycle-method-names (`bundles/khayyam/rules/lifecycle-method-names/lifecycle-method-names.md`) | `modules/computer/memory/rules/` or `modules/computer/capsule/rules/` | Conventional `Deinit`/`Free`/`IsNull` spellings cite Memory (`docs/modules/memory/memory.md`), not Khayyam grammar |
| observer-mutator (`modules/computer/adt/rules/observer-mutator/observer-mutator.md`) | `modules/computer/adt/rules/observer-mutator/` (relocated 2026-09-29) | Liskov & Guttag ADT observer/mutator families — ADT protocol subject, not Khayyam grammar |
| import-address (`bundles/khayyam/rules/import-address/import-address.md`) | `modules/dependency-management/rules/` (or the module that owns URI resolution) | URI scheme and repository-root base are dependency-management choices; Khayyam states only that `in` carries a URI |

### (b) Service capabilities — become Memar server services (not Rule text)
| Rule | Service capability | Rationale |
| --- | --- | --- |
| abstraction-scaffolding (`bundles/khayyam/rules/abstraction-scaffolding/abstraction-scaffolding.md`) | Delegation and abstraction scaffolding | Auto-generates missing delegation lines, method signatures, and remediation suggestions — generation, not a checkable condition |
| method-separation (`bundles/khayyam/rules/method-separation/method-separation.md`) | `tidy --rule method-separation` | Source rewrite (blank lines between methods) |
| go-clue-residue (`bundles/khayyam/targets/go/rules/go-clue-residue/go-clue-residue.md`) | `tidy --rule go-clue-residue` | Source rewrite (Go clue block cleanup after port) |
| commented-generic-bindings (`bundles/khayyam/targets/go/rules/commented-generic-bindings/commented-generic-bindings.md`) | `tidy --rule commented-generic-bindings` | Source rewrite (generic Go methods → real Khayyam methods) |
| result-parameter-names (`bundles/khayyam/targets/go/rules/result-parameter-names/result-parameter-names.md`) | `tidy --rule result-parameter-names` | Source rewrite (`resultN`/`argN` → type-derived names) |

Additional generation not yet a separate rule but named in owner position (2026-09-29): **observer/mutator naming generation** (`Observer_X`/`Mutator_X` families) — today implemented in `abstraction_bridge.py observer-names`; should become a Memar server service, while observer-mutator (`modules/computer/adt/rules/observer-mutator/observer-mutator.md`) remains the governance condition for naming shape.

### (c) Genuinely Khayyam — keep under `bundles/khayyam/rules/`
comment-forms (`bundles/khayyam/rules/comment-forms/comment-forms.md`), scope-placement (`bundles/khayyam/rules/scope-placement/scope-placement.md`), unresolved-import (`bundles/khayyam/rules/unresolved-import/unresolved-import.md`), name-not-declared (`bundles/khayyam/rules/name-not-declared/name-not-declared.md`), kind-mismatch (`bundles/khayyam/rules/kind-mismatch/kind-mismatch.md`), unbound-type-name (`bundles/khayyam/rules/unbound-type-name/unbound-type-name.md`), identifier-naming (`bundles/khayyam/rules/identifier-naming/identifier-naming.md`), abstraction-naming-heuristic (`bundles/khayyam/rules/abstraction-naming-heuristic/abstraction-naming-heuristic.md`), qualified-names (`bundles/khayyam/rules/qualified-names/qualified-names.md`), receiver-parameter-naming (`bundles/khayyam/rules/receiver-parameter-naming/receiver-parameter-naming.md`), domain-capsule-naming (`bundles/khayyam/rules/domain-capsule-naming/domain-capsule-naming.md`), type-as-argument (`bundles/khayyam/rules/type-as-argument/type-as-argument.md`), orphan-extension (`bundles/khayyam/rules/orphan-extension/orphan-extension.md`), receiver-method-names (`bundles/khayyam/rules/receiver-method-names/receiver-method-names.md`), method-verb-phrases (`bundles/khayyam/rules/method-verb-phrases/method-verb-phrases.md`).

### The ownership half applied to the whole catalog: fourteen Rules no module claims
A measurement applied **both** halves of [rule.md → Which Module a Rule Belongs To](./rule.md#which-module-a-rule-belongs-to) to all **27** folders under the Khayyam rules index (`bundles/khayyam/rules/README.md`). Counts: **27** folders measured, **1** passing both halves (`scope-visibility`), **14** failing the ownership half.

- State: those fourteen are this codebase's own conventions — the class the index itself already calls "The repository's" in its verdict table — and no module in this repository states their claim. [`rule.md:95`](./rule.md#which-module-a-rule-belongs-to) routes a Rule about a codebase's own sources in a language to "the owner of that codebase rather than any module inside it", and **nothing in this repository currently is that owner**. So the half that decides the home has no home to name, which is a different gap from the one the three residue Rules closed on 2026-10-04: those had a subject a module could own, and one was created for it.
- Blocks continuation: yes, for any verdict on where these fourteen go. Relocating them into modules is not the answer, and the (a) and (b) classifications above must not be read as licence to do it — the subject test says no module inside this repository owns their subject.
- Second blocker, independent of the first: the test's two halves are **recorded as disagreeing** in the catalog's own Which rules here are the language's own (`bundles/khayyam/rules/README.md#which-rules-here-are-the-languages-own`), which states that one half would fail `scope-visibility` — the one Rule whose subject is plainly the language's — and that "the sentence in `rule.md` needs one half of it rewritten". A verdict produced from either half alone is therefore not reproducible, and the disagreement must be settled in `rule.md` before any row of the 27 is acted on.
- Path: the owner's, on two questions in order. Which half of the sentence decides, and then who is the owner of this codebase as a subject's owner rather than as a module inside it.
- Not done here: no folder was moved, no Rule was re-homed, and `rule.md` was not edited. This entry records the measurement and its two blockers so the next chat starts from them.

## Anticipated work
1. Relocate inventory entries per module owner review (priority: Khayyam compiler rules, Chapar wire rules, Error naming).
2. Update `docs/modules/computer/linter.md` authorship section to cite `rule.md` and `rules/` folder layout once relocations begin.
3. Execute the Khayyam rules classification above: relocate (a), extract (b) into Memar server services, keep (c) — after owner review; no moves in the planning session.
4. Close rule.md's open items (the final notation for linter-checkable Rules, per-subject catalogs) or record why each stays open.

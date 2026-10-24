# Compiler Handoff
Open work for `compiler.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Open Questions

### The analysis-event schema
The event schema — event names, payloads, ordering guarantees, and the subscription API that definite-assignment analysis, linters, and IDEs consume — is not yet specified anywhere. It needs its own specification before the first analysis tool depends on it.

### How a single binary links multiple runtimes
How a single binary links multiple runtime libraries, each with its own boot convention, is not yet worked out — it is the concrete case where "boot is a configuration choice" most needs a specified resolution order.

### Compile-time designation
The designation mechanism itself — a naming convention, an `ab` contract, or a compiler directive — is not yet specified, nor is how a compile-time evaluation failure (a designated operation that turns out to touch runtime state) is reported.

### What the `unsafe` tag gates
What the `unsafe` tag concretely gates — a compiler refusal unless explicitly enabled, a linter rule, or both — and how a patching operation is audited, are not yet specified. Shared with [Runtime](../runtime/runtime.handoff.md).

### Language-versus-implementation boundary, with worked examples
The precise boundary between "what a language specifies" and "what a compiler of that language provides" still needs worked examples before it can be considered settled — shared with Khayyam's open question on the same boundary (`docs/khayyam/khayyam.handoff.md#the-precise-boundary-between-what-khayyam-specifies-and-what-a-khayyam-toolchain-or-module-provides-still-needs-worked-examples-before-it-can-be-considered-settled`).

### What the compiler places at the disposal of flow-management modules
- State: stated as an obligation with its questions open. [compiler.md → The compiler's obligation to flow management](compiler.md#the-compilers-obligation-to-flow-management) names the three consumers' needs and states the seven guarantees about the body a module receives; [What this obligation does not decide](compiler.md#what-this-obligation-does-not-decide) names the four mechanisms a compiler might serve a drive by — a call, a jump, a step of a state machine, a returned continuation — and what choosing each would commit the compiler to. No preference is stated and none should be read into the order.
- What a ruling must decide: which mechanism a realization serves a drive by, and therefore what a body is emitted as, whether a drive may be inlined as an ordinary optimization, and how the derived-target decisions become expressible.
- Blocked here and downstream: the flow library's branch and repetition declarations, the conditional-pair protocol's own contract, and the toolchain's step that treats library-driven control flow as available to user programs. The consumer-side question of whether the library declares the driver as a body-less method or leaves the whole mechanism to the realization is recorded in the control-flow model's handoff (`modules/process/control-flow/control-flow.handoff.md`) and is not answered by this ruling.
- Next: the owner. A ruling fixes the mechanism; the seven guarantees are stated so that each holds under whichever of the four is chosen, so a ruling that contradicts one of them is a signal that the guarantee or the mechanism is wrong.

### Where a branch decision's implementation comes from
- State: recorded as a finding, not as a proposal. [compiler.md → What no option delivers](compiler.md#what-no-option-delivers) states that all four mechanisms describe what happens once a drive is granted and none says where the decision comes from, and that in this repository the decision is a body-less method (`modules/process/control-flow/protocol/if.kh:6` (`modules/process/control-flow/protocol/if.kh`)) for which `bundles/khayyam/targets/js/link_map.json` holds no entry. The obligation and the analysis half beside it are therefore both undischarged.
- What a ruling must decide: whether source may express a condition without naming a library, whether the link phase supplies the decision the sources declare, or whether a compiler may serve a decision without recognizing a library's name — the third being in tension with [The compiler recognizes language primitives, not library names](compiler.md#the-compiler-recognizes-language-primitives-not-library-names) and therefore needing its own argument.
- Next: the owner, jointly with the control-flow model's own owner question, since the two decide the same declaration from its two ends.

### How a call against a declared specification is served here
- State: stated as a freedom in [compiler.md → How a call against a declared specification may be served](compiler.md#how-a-call-against-a-declared-specification-may-be-served), with the closed/open criterion, inlining, a generated dispatch structure, and devirtualization named as options and none preferred. What no document states is what this repository's compiler is expected to do: its one target resolves a call by the receiver's declared type, refuses a call whose receiver is typed as an abstraction, and has no dispatch over capsules it did not see (`bundles/khayyam/targets/js/target.md:60` (`bundles/khayyam/targets/js/target.md`)) — a mechanism stated by the realization, which is where this protocol's second discipline puts it, and one that exercises none of the options the freedom names.
- What a ruling must decide: whether a target in this repository is expected to serve a call against a declared specification by inlining, by a dispatch structure, or by leaving the choice to the target language — and whether a target's own model document must say so, the way it now does for this one.
- Next: the owner. A ruling that contradicts one of the freedom's three items is a signal that the item or the ruling is wrong, in the same way [What the compiler places at the disposal of flow-management modules](#what-the-compiler-places-at-the-disposal-of-flow-management-modules) makes a mechanism ruling answerable against the guarantees beside it.

### Where a declaration outside any operation's body gets its first instance
- State: stated as a freedom under [Entry and lifecycle are not grammar](compiler.md#entry-and-lifecycle-are-not-grammar) — the realization establishes it, this protocol guarantees none of the ways and forbids none. No document states what this repository's toolchain does, and the language document's own handoff (`docs/khayyam/variable.handoff.md`) still rests a premise on a sentence the 2026-10-03 audit removed (`docs/khayyam/variable.changelog.md:223`). That file was not this chat's to write.
- What a ruling must decide: whether a file-level declaration's initial state is established by generated source, by the link phase, or by the [Runtime](../runtime/runtime.md) — and which document states the answer.
- Next: the owner, jointly with the language document's own open question on file-level initialization.

### The method-ownership expectation has no home yet
- State: recorded as considered and not done in this document's [changelog entry](./compiler.changelog.md), and unresolved. The claim that abstraction composition is central to Memar-style design, so methods attached to abstractions should be plentiful, was removed from Method in Khayyam (`docs/khayyam/method.md`) on 2026-10-03 and is not this protocol's subject in any of its three statuses: it is an expectation about how a language's method surface is used, and its facet is the language's Practice companion.
- What a ruling must decide: whether that expectation is stated at all, and if so in which document — the language's Practice companion, a governance rule in `bundles/khayyam/rules/` (`bundles/khayyam/rules/README.md`), or nowhere.
- Next: the owner.

## Anticipated Work
- A conformance test suite a compiler realization can run against, turning each requirement from review-time guidance into a checkable contract.
- A dedicated specification for the compiler's emitted analysis events, before the first analysis tool depends on the contract.
- A conformance check for the branch-body guarantees, of the shape a link-map entry already records — a requirement named and the section it is read at — so that "does this compiler serve a drive by call, jump, progression, or continuation" becomes an answerable question rather than a reading of its output. It depends on the mechanism ruling above only for what the check compares against, not for whether it can be written.
- Frontend questions beyond the [Lexer](../lexer/lexer.md) — input, output, responsibility boundary, contract with a given backend — stay here until a dedicated frontend protocol is justified.
- An **Implementation Readiness Review** before any compiler code is written: for each remaining open item, settle whether the concept is defined, its boundary is clear, its semantic rule is explicit, it belongs to the language or to a compiler, it is foundational law or pluggable policy, multiple realizations can satisfy it, and what must remain invariant across realizations.
- A **first implementation prototype targeting JavaScript**: a language frontend → a semantic representation → the local Khayyam toolchain under `bundles/khayyam/` → V8, with WebAssembly as the intended second target. The prototype exists to reach running feedback quickly. Two disciplines bind it: the JS backend must never become the hidden specification of the language's semantics; standing up two backends behind one semantic representation is the earliest test that those semantics are implementation-independent. The name `Parser` is not assumed for the frontend.

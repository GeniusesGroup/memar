# Control Flow Model Handoff
Open work for [model.md](./model.md). Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See the repository's [documentation-handoff.md](../../../docs/documentation-handoff.md) for what a handoff is.

## Topic & Purpose
The model of what the control-flow library under `modules/process/control-flow/` needs to contain, so that the declarations can be written once the questions that only the owner or another document can answer are settled. The model states the concepts, their boundaries, their relations, and the names; it does not state a signature, an owner type, or a file layout, because each of those turns on a question this document carries rather than answers.

## Status
Active

## Decisions
- **The library needs three concepts, and a fourth the protocol has not designed** — Decided. Branch Scope, Flow Decision, and Conditional Pair, plus Halt, whose contract the protocol registers as a topic it does not yet hold. Reason: each survives the challenge test in [Modeling Practice → Challenging a Proposed Concept](../../../docs/modeling.md#challenging-proposed-concepts) with an independent behavioral boundary, and nothing else in the corpus enforces rules any of them would. Rejected: a concept per ecosystem form, which is the corpus's current layout and which the file-layout rule's own test ("distinct concepts") does not distinguish.
- **Repetition is a relation, not a concept** — Decided. A repetition is a Branch Scope plus the Flow Decisions that re-enter and leave it, and the relation that carries it already exists in this repository as `Container_Iteration` handing an `Iterate` abstraction. Reason: [Modeling → Domain Decomposition over Aggregate-Root Modeling](../../../docs/modeling.md#domain-decomposition-over-aggregate-root-modeling) holds aggregation to be a consequence of modeling, and the corpus already has the contract. Rejected: `while`/`for`/`loop` as three concepts, and this library as the owner of iteration.
- **Written target and derived target are one property of a Flow Decision, not two concepts** — Decided. `goto`/`jump`, `break`/`continue`, and `return` differ only in where the target comes from. Reason: a concept that adds no responsibility is a new name; the difference is what a signature records.
- **The branch-grouping primitive is a Scope and this module does not redefine it** — Decided. [Type → Scope](../../../docs/type.md#scope--type-as-semantic-boundary) already counts a local algorithmic block among the category's realizations, and [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states its inertness. Reason: two declarations of one category is the collision [Khayyam → Import Mechanism](../../../docs/khayyam/khayyam.md#import-mechanism-in) calls an architecture error. Rejected: a `Branch` or `Block` type; rejected also the `labelType` the current draft uses.
- **`return` belongs to the grammar in this realization, so the library does not declare it** — Decided. [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) makes `return` an IR marker and a compiler lowers `sc`-driven branches to internal jumps; the four commands a body may hold are listed in [the JS target document → The commands a body may hold](../../khayyam/targets/js/target.md#the-commands-a-body-may-hold) and `return` is one of them. Reason: a library method the compiler already recognizes as a primitive would be a second authority for leaving a method. Rejected: a `Return` method, which is one of the four spellings the owner has already used (`CF.Return` in the toolchain plan's step 4).
- **Error identity, iteration, and scheduling stay outside this library** — Decided. Reason: [The Error](../../../docs/protocols/process/error.md) owns the first once and language-independently, `Container_Iteration` owns the second, and [Process → Concurrency](../../../docs/process.md#concurrency) with `modules/computer/runtime/thread/protocol/scheduler-waiting.kh` own the third. Reason this matters to the model: it is what keeps the library's boundary at "where does execution land" rather than "what happens next".
- **`Conditional` in `modules/math/logic/conditional.kh` is this model's concept, filed elsewhere** — Explored-but-unresolved. Its Go block enumerates `Conditional_Then`, `Conditional_ActionAndContinue`, `Conditional_Continue`, `Conditional_Break`, `Conditional_Return`, which are outcomes of a Flow Decision written as values of one type. Reason it is unresolved: whether that enumeration is the concept, an encoding of it, or an unrelated logic value is a corpus judgment about a file this module does not own, and [Qualified Names → When qualification cannot separate two declarations](../../khayyam/rules/qualified-names/qualified-names.md#when-qualification-cannot-separate-two-declarations) sends a name claimed twice to the module that owns the concept rather than to a naming rule.
- **`Condition` is not this library's type name** — Decided. [Khayyam → Type Principles Realized](../../../docs/khayyam/khayyam.md#type-principles-realized) states there are no primitive types and that even a truth value is a named capsule, and `modules/math/boolean/protocol/boolean.kh` already declares that concept. Reason: a second capsule for it would be an architecture error under [Import Mechanism](../../../docs/khayyam/khayyam.md#import-mechanism-in). Rejected: `Condition`, `Predicate`, `Flag`; rejected also adopting `Status` from the protocol's own example, which is an example and not a claim on a name.
- **`panic`, `recover`, and `goto` are refused as concept names; `Halt`, `Jump`, and `Error` are used** — Decided. Reason: [Terminology → The Default Meaning of an Unreferenced Term](../../../docs/terminology.md#the-default-meaning-of-an-unreferenced-term) gives an unreferenced word its ordinary sense, which for all three is the Go spelling this protocol's own changelog records as prior art rather than as Memar's terms. `GOTO` survives as the name of an unstructured jump package, which the protocol's handoff already anticipates.
- **The model is conceptual; no declaration was written** — Decided. Reason: [Modeling → Modeling Produces Conceptual Abstractions, Not Implementation Structures](../../../docs/modeling.md#modeling-produces-conceptual-abstractions-not-implementation-structures), and the owner ruling that the protocol of a module is settled before anything depends on it, recorded in the protocol's changelog.

## Ambiguities Resolved
- **Whether `Scope` is this library's concept to define** — Answered by reading, not by choosing. It is a Type category already held by `docs/type.md`, and the protocol's own "the `sc` subtype and the compiler's jump/branch intrinsics" names the grammar's existing subtype rather than a new type. The model therefore attaches to the category and adds only the pairing the protocol states: entry is a property of the operation, not of the scope.
- **Whether a loop is a control-flow concept at all** — Answered. The relation that carries repetition exists already (`Iteration` hands out `Iterate`, and `Iterate` stops on error), so a loop adds an owner the repository already has. What is left for this library is the two derived-target decisions and nothing more.
- **Whether `RuntimeStack` and `PanicHandler` are control-flow concepts** — Answered. `modules/computer/runtime/protocol/stack.kh` states its purpose as panic *tracing*, and `modules/process/log/panic_handler.kh` turns a recovered value into a log event; both are diagnostics of a halt, and [The Error's boundary discipline](../../../docs/protocols/process/error.md#what-vocabulary-an-error-may-speak-across-a-layer-boundary) is what separates them from the halt itself.
- **Whether `DispatchEvent` is a Flow Decision** — Answered. Its target is a listener set rather than an execution point and it does not move the calling code, so it is an event-delivery relation. Recorded here rather than in the model because the model's relations section already excludes it in one sentence and this is the reasoning behind that sentence.

## Open Questions
### Which type owns the forms, and what category is it?
- State: four spellings are undecided in the repository. The protocol's own examples write `IF(isValid, ValidData)` owner-less; the protocol handoff names `CF.IF` from the toolchain plan's step 4, `CF.Return` from the method changelog, and `tp CF sc` as the owner's undecided hypothesis; the JavaScript target's own library puts `IF` and `ELSE` under a `Flow` capsule. No document requires one type per form or one form per file.
- What a ruling must decide: whether the owner is a Scope in Type's namespace sense, the protocol's own contract as an abstraction each organization's library realizes, or something else — and therefore the declaration form, the file layout, and whether an organization's Linter can mandate a library, which [Control Flow → Mechanism Summary](../../../docs/protocols/process/control-flow.md#mechanism-summary) says it can.
- Blocks continuation: yes. No declaration in this module can be written without it.
- Path: the owner, with the protocol's handoff entry *Which type owns the control-flow forms, and what category is it?*. The model constrains the answer rather than supplying it: the forms are methods, the owner is what they attach to, and the owner must be replaceable per organization.

### What type does a scope parameter take?
- State: [Method → Type-level arguments for `sc` and `mt`](../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) admits a `vr`, an `sc`, or an `mt` in an influencing group and does not state how the parameter's type is written. The JavaScript target's handoff records that its library declares a `Scope` capsule for this because the documents leave it unstated.
- What a ruling must decide: whether a signature writes the scope as the grammar's own `sc`, as a named abstraction, or as a capsule — which decides whether the library restates the grammar's category or names a contract over it.
- Blocks continuation: yes. Every signature in the library needs it.
- Path: the language documents, then the owner; the target's recorded reading is evidence of what the current declarations assume, not an authority.

### What type does a condition take, and does the generic form take one at all?
- State: the protocol's examples use `Status` and `Bool`; the boolean protocol is recorded as not final; the model's own finding is that the preferred form needs no condition argument, because the receiver carries it.
- What a ruling must decide: whether `IF`'s condition parameter is `Boolean`, a domain-named type, or a type-level argument — and whether the generic form is declared at all given that [the preferred form](../../../docs/protocols/process/control-flow.md#the-preferred-form-domain-specific-conditional-methods) makes it a last resort.
- Blocks continuation: yes, for the generic form's signature.
- Path: with the conditional-pair question below, since the same ruling fixes both.

### Does a form carry an influenced `err`?
- State: the current draft at `protocol/if.kh:6` writes `(err Error)`; the protocol's own example writes no influenced group at all; the protocol requires every fallible operation to expose its error path as an ordinary named output. Nothing says whether a branch decision can itself fail.
- What a ruling must decide: whether deciding to run a body is fallible — which decides whether an `Error` can appear on a branch signature, and whether [Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation)'s visibility requirement applies to the library's own forms or only to the methods it drives.
- Blocks continuation: yes, for every signature.
- Path: the protocol's handoff records it as downstream of the owner question; [Process → Failure](../../../docs/process.md#failure) is the check on it, since a failure does not by itself prescribe what happens next.

### Is `Conditional` in `modules/math/logic/conditional.kh` this module's concept?
- State: its Go block enumerates `Conditional_Unset`, `Conditional_Then`, `Conditional_ActionAndContinue`, `Conditional_Continue`, `Conditional_Break`, `Conditional_Return` — flow outcomes as values of one type. The declaration carries no method and the file imports nothing.
- What a ruling must decide: whether the enumeration is the Flow Decision concept under a wrong name in a wrong module, a derived encoding of it, or an unrelated logic value. The three answers give three different owners for the concept and three different files.
- Blocks continuation: yes for the Flow Decision declaration, because the name and the declaration site both follow from it.
- Path: the owner of `modules/math/logic/`, since the file is not this module's; the model records the collision rather than resolving it.

### Which error class justifies a Halt, and does Recovery exist?
- State: [The Error](../../../docs/protocols/process/error.md) carries `Internal`/`Temporary`/`Timeout` capability interfaces without connecting them to halting; the protocol's handoff records the owner's working position that errors temporary and outside the program's control warrant an abrupt halt while input-validation failures return errors to the caller; the corpus declares `RuntimePanicRecovery cp {}` with no methods, and `modules/computer/runtime/thread/protocol/thread.kh` carries a commented `Panic`/`Recover` pair.
- What a ruling must decide: whether a halt carries an `Error` and which class warrants one; and whether observation of a halt is a concept of this library at all or belongs to the runtime and log modules that already hold its diagnostics.
- Blocks continuation: yes for `protocol/panic.kh` and `protocol/panic-recovery.kh`; no for the branch forms.
- Path: jointly with the protocol's halting-semantics topic and [The Error](../../../docs/protocols/process/error.md); [Process → Failure](../../../docs/process.md#failure) and [Process → Cancellation](../../../docs/process.md#cancellation) are the checks, since neither rollback nor cancellation follows from a failure automatically.

### Where do `OnAbsent`/`OnPresent` and `OnFailure`/`OnSuccess` live, and under what name?
- State: both candidate pairs are already declared as method-less abstractions in two other modules — `modules/computer/adt/protocol/listeners.kh` and `modules/process/operation/protocol/on-failure.kh` beside `on-success.kh` — while the protocol's handoff records the choice between them as undecided. A file needing both cannot import both, under [Import Mechanism](../../../docs/khayyam/khayyam.md#import-mechanism-in).
- What a ruling must decide: which pair, on which abstraction, with what methods, and whether the surviving declaration moves here or the other two move into it.
- Blocks continuation: yes for the pair's declaration and for the file layout.
- Path: the owner, with the protocol's handoff entries *No final naming choice between the candidate pairs* and *Should the success/failure pair live on the Error abstraction or on a shared abstraction?*; the second is prior, since it decides which file the pair belongs in.

### Which type owns the condition's two-branch contract — a Type, a Flow Library, or neither?
- State: [Mechanism Summary → Linter Governance over Compiler Dictatorship](../../../docs/protocols/process/control-flow.md#mechanism-summary) says an organization configures its Linter to mandate its own control-flow library, which is what makes the library a replaceable Module rather than a fixed type; [Extensible Behavior Belongs to Pluggable Modules](../../../docs/modeling.md#extensible-behavior-belongs-to-pluggable-modules) is the general form.
- What a ruling must decide: whether the pair is a contract an organization's library realizes — in which case a type-level abstraction is the only owner under which replacing the library means anything — or whether the forms attach to a type fixed in this module.
- Blocks continuation: yes, because it is the question behind the owner question and is what a file layout would be built on.
- Path: the owner, together with the owner-type question above; the two are one decision wearing two hats and should be answered together.

### Is a branch's own driver a jump the library must declare, or the compiler's?
- State: [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states the compiler lowers `sc`-driven branches to internal jumps, and the grammar has no `goto`; the protocol states that a realization may package flow operations as library methods, compiler intrinsics, or another explicit mechanism. The JavaScript target's library supplies the jump itself as a body-less method on a concrete capsule, which is the language's FFI form.
- What a ruling must decide: whether this repository's library declares the jump as a body-less method whose implementation the toolchain supplies, or leaves the whole mechanism to the realization. The first is what a target needs; the second is what keeps the library free of any host detail.
- Blocks continuation: yes for `protocol/goto.kh` and `protocol/jump.kh`, and for the conditional's own implementation.
- Path: the toolchain owner, with the protocol's own statement that the branch-grouping primitive is the common denominator across realizations rather than the jump.

## Assumptions
- **The three concepts are enough for the first declarations** — Stability: Weak. What changes it: a declaration that cannot be written without a fourth concept, which is the test the first pass of declarations will apply. Mitigation: this is the question the next pass answers by writing, not by reasoning.
- **`Container_Iteration` is the established owner of repetition and will stay there** — Stability: Weak. It is a ported declaration with no methods, so its standing rests on the protocol document rather than on an implementation. What changes it: a ruling that iteration belongs to this module.
- **The protocol's preferred form is the reachable default for an organization** — Stability: Weak. It is the protocol's stated preference, and the protocol's handoff records the naming, placement, and delegation-verification mechanics for it as all undecided. What changes it: a ruling on those three, any of which could make the generic form the only writable one.
- **Nothing outside `modules/process/control-flow/` will move to make a name fit** — Stability: Unexamined. What changes it: an owner ruling that the surviving conditional pair moves here from `computer/adt` or `process/operation`, which is a propagation this module's owner may authorize but this session may not make.

## Anticipated Work
- Writing the protocol's conditional-pair topic as an abstraction contract, once the pair's owner and names are settled. Its four stated subjects — how the condition is evaluated, whether the branches are symmetric, how the receiver's state is read, and how the pair relates to the presence/absence family — are all answerable from this model except the last, which waits on the pair-placement ruling.
- Writing the halting-semantics topic jointly with [The Error](../../../docs/protocols/process/error.md), so that the temporary-and-outside-the-program's-control criterion becomes a stated rule rather than a working position.
- An iteration-shaped topic, if the ruling in *Where do `OnAbsent`/`OnPresent` and `OnFailure`/`OnSuccess` live* opens rather than closes the question of whether this module needs a loop of its own beyond the two derived-target decisions.
- A standard-library unstructured jump package, which the protocol's handoff already carries as anticipated work and which this model gives a shape: one written-target Flow Decision, replaceable like any other.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [model.md](./model.md) | Base — the model this carries the open state of | Follows this document |
| [`protocol/`](./protocol/) | Depends_on — the corpus the model describes; `if.kh` and `panic-recovery.kh` are the only files that declare anything | None in this session; `if.kh` is a draft the toolchain handoff deliberately leaves as a negative |
| [Control Flow protocol](../../../docs/protocols/process/control-flow.md) | Depends_on — states the contract this models | None; its handoff owns the owner question |
| [Control Flow protocol handoff](../../../docs/protocols/process/control-flow.handoff.md) | Depends_on — carries the questions this model cannot answer | None (read) |
| [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) | Depends_on — states the inertness the whole model rests on | Ruling needed on the scope parameter's type |
| [Khayyam handoff](../../../docs/khayyam/khayyam.handoff.md) | Depends_on — the language questions this library waits on | Ruling needed on a body's declaration order |
| [The Error](../../../docs/protocols/process/error.md) | Reference — owns what an error is; the library owns only what happens next | None (read) |
| [`modules/computer/adt/protocol/listeners.kh`](../../computer/adt/protocol/listeners.kh) | Conflicts — declares `OnAbsent`/`OnPresent` here in another module | Owner ruling needed; not this session's to make |
| [`modules/process/operation/protocol/on-failure.kh`](../operation/protocol/on-failure.kh) and `on-success.kh` | Conflicts — declares `OnFailure`/`OnSuccess` in another module | Owner ruling needed |
| [`modules/math/logic/conditional.kh`](../../math/logic/conditional.kh) | Conflicts — declares `Conditional`, whose Go block enumerates flow outcomes | Owner ruling of that module needed |
| [`modules/computer/adt/container/protocol/iteration.kh`](../../computer/adt/container/protocol/iteration.kh) and `iterate.kh` | Reference — the existing relation this model reuses for repetition | None (read) |
| [`README.md`](./README.md) | Reference — states what the folder is | Should point at this model and this handoff; not edited in this session |
| [JavaScript target](../../khayyam/targets/js/target.md) | Reference — the commands a body may hold, which fix what the library may declare | None (read) |

## Notes
- Confidence vocabulary follows the repository's handoff specification: Decided / Tentative / Explored-but-unresolved / Deferred for decisions; Strong / Weak / Unexamined for assumptions.
- The model was written before any declaration, so every question above is answerable by a ruling rather than by a measurement. The first declarations are the measurement.
- No `.kh` file under `protocol/` was edited, no file outside this folder was touched, nothing was staged, and no git command was run.
- Three defects found outside this folder are recorded in the session's report rather than fixed here: `protocol/if.kh`'s inclusion of the Go-draft `modules/process/error/error.kh` (already tracked in the toolchain handoff), the untracked root scratch `main.kh:4` naming `modules/control-flow`, which resolves to nothing, and the compiled `modules/khayyam/targets/js/build/modules/khayyam/targets/js/lib/branch.js`, a build product whose source file no longer exists.

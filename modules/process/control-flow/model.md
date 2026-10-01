---
Title: "Control Flow Model"
Status: Draft
Start Date: 2026-10-01
ID: "497454"
---

# Control Flow Model

## Abstract
This document is the model of what a control-flow library needs to be, derived from the [Control Flow protocol](../../../docs/protocols/process/control-flow.md), the Khayyam grammar's [stated position](../../../docs/khayyam/khayyam.md#scope), and the `.kh` corpus under [`protocol/`](./protocol/). It names the concepts the library needs, the responsibility each one carries, what each one deliberately does not own, the relations between them, and the names to use and to refuse. Its central finding is that the library needs three concepts and no more — **Branch Scope**, **Flow Decision**, and **Conditional Pair** — plus one the protocol has not yet designed, **Halt**; that the other thirteen names the corpus currently files under this module are ecosystem spellings of relations among these four rather than concepts beside them; and that the protocol's preferred conditional pair is already declared, empty and method-less, in two other modules of this repository, which no document records. The library's owner type, the type of a scope parameter, the type of a condition, and whether a form carries an error output are not settled here and are carried in the paired [handoff](./model.handoff.md).

## Introduction

### Motivation
Three artifacts in this repository describe control flow and they disagree. The protocol states the framework-level rules and leaves four of its own subjects undeveloped — the conditional-pair contract, loop-shaped flow, halting semantics, and the type that owns the forms. The grammar states that control flow is absent from it and that a code scope is inert until a library-provided method drives it. The corpus under [`protocol/`](./protocol/) holds sixteen files, one per mainstream spelling, of which thirteen declare nothing at all and one declares a signature whose owner, condition type, and scope type are all unbound.

A library cannot be written against that. Every declaration needs an owner, every signature needs types, and the library's file layout follows from which concepts it holds. This document settles the part that modeling can settle — which concepts are independent responsibilities, which are relations wearing the shape of concepts, and where each responsibility's boundary runs — so that the declarations that do depend on a ruling are the only ones waiting.

### Methodology
The model was derived by the procedure in [Modeling Practice](../../../docs/modeling.md#challenging-proposed-concepts): the three artifacts were read as they stand, the candidate concepts were taken from the protocol's own decomposition and from the corpus's file names, and each was then run against the challenge questions — does an equivalent concept already exist, is it a contextual view of another, is it a new responsibility or only a new name, does it have an independent lifecycle, does it enforce rules no existing concern owns, would the system lose clarity if it disappeared. Each candidate's node-or-edge standing was then decided by the audit in the same practice, and the resulting relations were searched against the existing `.kh` corpus for one that already does the same job under another name.

The separation between this document and the protocol is the one [Protocols fixes](../../../docs/protocols/README.md#where-implementations-live): the protocol states the contract, this document states what realizing it requires. Where the two overlap, this document cites the protocol rather than restating it. What is unsettled is carried in the handoff rather than here, per [Documentation — Explanation → Relevance discipline](../../../docs/documentation-explanation.md#relevance-discipline).

## Explanation

### What the library is for
[Control Flow → Library-Defined Control Flow](../../../docs/protocols/process/control-flow.md#library-defined-control-flow) states that flow constructs are explicit operations over the primitive that groups a branch body, and that the common denominator across realizations is that primitive rather than any particular library. The library's job is therefore to supply the operations; the grammar's job is to supply the primitive; and the organization's job is to choose the library, which [Structured and Unstructured Flow as Libraries](../../../docs/protocols/process/control-flow.md#structured-and-unstructured-flow-as-libraries) places under Linter governance rather than in any grammar.

That division fixes the library's boundary at both ends. It does not decide what a condition holds, because that is the receiver's own contract — [the preferred form](../../../docs/protocols/process/control-flow.md#the-preferred-form-domain-specific-conditional-methods) places the pair's methods on the result type for exactly that reason. It does not decide what an `Error` is, because [The Error](../../../docs/protocols/process/error.md) owns that once and language-independently. What it does decide is when a body runs, which body runs, and where execution lands when a body does not.

### The concepts

#### Branch Scope
A named region of statements that *would* run, held inert until something drives it.

Khayyam realizes this as the `sc` subtype, and [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states the property the whole model rests on: a code scope is inert until a library-provided method drives it, because the grammar ships no control-flow keywords or logical operators of its own. The concept is not this library's to define. [Type → Scope — Type as Semantic Boundary](../../../docs/type.md#scope--type-as-semantic-boundary) counts a namespace boundary, a module-visibility boundary, a package boundary, a transaction's isolation boundary, and a local algorithmic block as realizations of one category, and names "a local algorithmic block (as used by `if`, `loop`, `goto`)" among them. This library attaches to that category; it does not add to it.

The one thing the library must add is the pairing the protocol states and the category does not: [Control Flow → Library-Defined Control Flow](../../../docs/protocols/process/control-flow.md#library-defined-control-flow) separates them when it says a code scope names *what* would run while an explicit control-flow operation decides *when*. Entry into a Scope is therefore a property of the operation that performs it, not of the Scope itself.

**Node.** It has meaning on its own — a scope is nameable, nestable, and referable independently of any operation over it — and it survives the challenge test as an independent concept, though an existing one.

**Collides with** nothing in this module, and **is already declared** as a Type category rather than as anything this module owns.

#### Flow Decision
An explicit operation that decides whether and where execution continues.

This is the one responsibility the protocol assigns that nothing else in this repository currently owns, and it is the concept the library is actually built from. [Control Flow → Library-Defined Control Flow](../../../docs/protocols/process/control-flow.md#library-defined-control-flow) states the same operation four ways — a mid-scope return, a break, a jump, a halt — and treats them as one family, and [Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation) adds that leaving the normal path because a fallible operation failed is the same thing.

Its one distinguishing property is that it separates *what* from *when*, which is what makes it a concept rather than a synonym for a scope: a Scope is inert and says nothing about its own execution, and a Flow Decision says nothing about what its body contains.

The decision's target is where control lands. That target has exactly two shapes, and the difference is a property of the decision, not a separate concept. A **written target** is named in the operation's own arguments — a scope passed to a branch, a named point passed to a jump. A **derived target** is fixed by the decision's own kind: past the enclosing scope for a break, the next iteration for a continue, past the call for a return. [Modeling → Edge Types](../../../docs/modeling.md#edge-types-and-their-traditional-counterparts) asks whether an edge's role is open-ended; here it is not. Which shape a decision takes is what a signature records, and it is what the library's declarations differ by.

**Node.** It has an independent behavioral boundary — it can be replaced, reasoned about, or governed without any branch body changing — and it survives the challenge test.

**Collides with** `modules/math/logic/conditional.kh`, which declares a `Conditional` abstraction whose Go source block enumerates `Conditional_Then`, `Conditional_ActionAndContinue`, `Conditional_Continue`, `Conditional_Break`, and `Conditional_Return`. Those five are outcomes of a Flow Decision, written as values of one type. This model therefore treats Flow Decision as already claimed by the corpus and introduces no second declaration of it; whether that enumeration is the model concept or an encoding of it belongs to the handoff.

#### Conditional Pair
Two Flow Decisions over one condition, named by two etymologically distinct roots, each carrying an explicit reference to that same condition.

[Control Flow → Two etymologically distinct roots](../../../docs/protocols/process/control-flow.md#two-etymologically-distinct-roots-not-base-plus-negation) fixes the naming because a `Not`-prefix difference is visually subtle for a reader skimming a diff and for an agent reading quickly. [The Generic Form](../../../docs/protocols/process/control-flow.md#the-generic-form-ifelse) fixes the dependency rule: `ELSE` always takes an explicit reference back to the same condition value it pairs with, so the construct carries its dependencies in its own arguments rather than relying on position or surrounding text. Together these make the pair one well-formedness concern rather than two methods that happen to sit together — which is why [Topics to be developed here](../../../docs/protocols/process/control-flow.md#topics-to-be-developed-here) names "the conditional-pair protocol" as a single contract.

The pair has an owner, and the owner is the point at which this repository's three artifacts diverge. [The Preferred Form](../../../docs/protocols/process/control-flow.md#the-preferred-form-domain-specific-conditional-methods) places the pair's methods on the result type, so that the calling code reads as a sequence of named intentions; [Mechanism Summary](../../../docs/protocols/process/control-flow.md#mechanism-summary) then adds that a realization may express boolean and conditional logic through named capsule methods, so the general form and the domain-named form are the same pair with a different owner. `IF`/`ELSE` is the degenerate case in which the owner names no domain and the condition is supplied as an argument.

**Node.** The pair has rules no other concern owns — the two names must be visually distinct, the two branches must reference one condition explicitly, and the branches must be symmetric in structure — and those rules are the contract the protocol has yet to write.

**Collides with** two existing declarations elsewhere in this repository. `modules/computer/adt/protocol/listeners.kh` declares `OnAbsent ab` and `OnPresent ab`, carrying the commented signature `// OnAbsent(call scope) (err Error)`, which is the pair the protocol's worked example uses. `modules/process/operation/protocol/on-failure.kh` and `modules/process/operation/protocol/on-success.kh` declare `OnFailure ab` and `OnSuccess ab`, which is the pair the protocol's handoff names as the alternative. Both sets are empty of methods and neither file imports anything. Under [Khayyam → Import Mechanism](../../../docs/khayyam/khayyam.md#import-mechanism-in), a collision is an architecture error rather than a disambiguation problem, so these are one concern with three addresses and this module is where the model says it belongs; which declaration survives, and under what name, is the handoff's question.

#### Halt
Ending the current execution without passing through the ordinary path of any Flow Decision before it.

[Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation) states that abrupt execution halts are explicit operations in the realization's library or contract layer, and [Topics to be developed here](../../../docs/protocols/process/control-flow.md#topics-to-be-developed-here) registers halting semantics as a subject the protocol does not yet hold. It therefore has one settled property — it is an operation, not a grammar form — and no contract.

What already exists around it is owned elsewhere. `modules/computer/runtime/protocol/stack.kh` declares `Stack ab` with `RuntimeStack() (s String)` for the panic-tracing case, and `modules/process/log/panic_handler.kh` holds a Go-draft handler that recovers a halt and turns it into a log event. Whether a halt carries an `Error` and which class of `Error` justifies one is undecided in [The Error's handoff](../../../docs/protocols/process/error.md) and in this protocol's own.

**Node.** It has an independent lifecycle — a halt can end an execution that no Flow Decision would otherwise end — and it enforces rules nothing else owns, once those rules are written.

**Collides with** `protocol/panic-recovery.kh`, which declares `RuntimePanicRecovery cp {}` with no methods and no importer, and with the commented `Execution_Exception` block carrying a `Panic`/`Recover` pair inside `modules/computer/runtime/thread/protocol/thread.kh`.

#### Repetition
Not a concept. The corpus files [`while.kh`](./protocol/while.kh), [`for.kh`](./protocol/for.kh), and [`loop.kh`](./protocol/loop.kh) name three ecosystem forms of one composition, and [Modeling → Domain Decomposition over Aggregate-Root Modeling](../../../docs/modeling.md#domain-decomposition-over-aggregate-root-modeling) holds that aggregation is a consequence of modeling rather than a primitive. A repetition is a Scope plus the Flow Decisions that re-enter it and leave it; it earns no node of its own.

The relation that *does* carry it already exists in this repository, under another name and in another module: `Container_Iteration` in `modules/computer/adt/container/protocol/iteration.kh` hands a `Container_Iterate` abstraction and a start index, and `Iterate` in `modules/computer/adt/container/protocol/iterate.kh` states that iteration stops when the iterate reports an error. A loop body and its enclosing iteration are, in that contract, already one concept and one relation. The library's contribution is a Flow Decision whose derived target is the next iteration and whose other derived target is past the iteration; it is not a second owner of repetition.

### What each concept owns, and what it does not own

**Branch Scope** owns the statements a branch body contains, their nesting, and their name. It does not own when they run, whether they run, or what they mean — [Scope is a boundary, not a trigger](../../../docs/type.md#scope--type-as-semantic-boundary), and [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states the inertness as the reason a library-provided method exists at all.

**Flow Decision** owns when a body runs, which body runs, and where execution lands. It does not own what a condition holds; the receiver's own contract does. It does not own the grammar's lowering; [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states that a compiler lowers `sc`-driven branches to internal jumps, and [Compiler → The compiler recognizes language primitives, not library names](../../../docs/protocols/computer/compiler.md#the-compiler-recognizes-language-primitives-not-library-names) keeps the compiler from knowing any library name.

**Conditional Pair** owns the well-formedness of the two-branch form: distinct roots, one explicit condition referenced by both members, symmetric branches. It does not own the meaning of the condition — that is the receiver's — and it does not own the enumeration of branch pairs a domain exposes, which [Khayyam → Domain-Specific Containers](../../../docs/khayyam/polymorphism.md#domain-specific-containers) places on each type that has one.

**Halt** owns ending an execution outright. It does not own the halt's diagnostics, which `RuntimeStack` in `modules/computer/runtime/protocol/stack.kh` serves, nor the halt's observation, which `panic_handler.kh` in `modules/process/log/` serves, nor what an `Error` is.

Three concerns a reader will expect here are owned elsewhere, and the library deliberately does not absorb them:

- **Error identity and error routing.** [The Error](../../../docs/protocols/process/error.md) owns what an error is; [Method in Khayyam → Influencing and Influenced Variables](../../../docs/khayyam/method.md#influencing-and-influenced-variables-not-inputs-and-outputs) owns the call contract that exposes the error path as an ordinary named output. [Control Flow → Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation) is explicit that this document is concerned only with how execution continues once an error has occurred.
- **Iteration over a collection.** `Container_Iteration` and `Container_Iterate` own it, stop-on-error included.
- **Blocking, waiting, and scheduling.** `modules/computer/runtime/thread/protocol/scheduler-waiting.kh` and `modules/computer/runtime/protocol/blocking.kh` own them. A Flow Decision may cause a process to stop progressing; that it does so by descheduling is [Concurrency](../../../docs/process.md#concurrency)'s and the runtime's, not this library's.

### The relations

**A Flow Decision is taken on a Branch Scope.** One decision drives one scope per call; a scope may be driven by any number of decisions, and the same scope text may be driven forward by one decision and backward by another. The direction runs from decision to scope because [The Generic Form](../../../docs/protocols/process/control-flow.md#the-generic-form-ifelse) writes the scope as an argument of the operation, so the dependency runs with the call. This relation already exists in this repository under another name: `Iteration` in `modules/computer/adt/container/protocol/iteration.kh` hands an `Iterate` abstraction the body to run per step, which is the same relation with "iterate" for "drive" and "container" for "loop".

**A Conditional Pair is two Flow Decisions over one condition.** Exactly two members, each naming a distinct root, each taking an explicit reference to the same condition. The direction runs from the pair to its members because the pair's rules constrain them jointly and neither member constrains the other alone. The two relations a pair gives rise to — member to scope — are the relation above, one per member.

**A type may realize a Conditional Pair in place of the generic pair.** Zero or more pairs per type, one per binary interpretation the type's domain has; valid/invalid, found/absent, granted/denied. The direction runs from the type to the pair because the type supplies the condition and the branches name it, not the reverse. [The Preferred Form](../../../docs/protocols/process/control-flow.md#the-preferred-form-domain-specific-conditional-methods) makes this the expected reach and [`IF`/`ELSE`](../../../docs/protocols/process/control-flow.md#the-generic-form-ifelse) the last resort, so a type with a nameable condition should have no generic branch in its source at all.

**A Halt ends the execution every other Flow Decision runs inside.** At most one halt takes effect per execution; no decision resumes it. The direction runs from halt to execution because the execution is what ends.

**A Flow Library realizes Flow Decision, and an organization's Linter governs which library it may use.** One library per project in practice, chosen by governance rather than by grammar, per [Mechanism Summary → Linter Governance over Compiler Dictatorship](../../../docs/protocols/process/control-flow.md#mechanism-summary) and [Linter Governance over Compiler Dictatorship](../../../docs/protocols/process/control-flow.md#structured-and-unstructured-flow-as-libraries). The direction runs from the library to the decision, and the library is replaceable without any branch body changing — which is the property that makes the relation worth modeling at all.

One relation that looks adjacent is not this one. `DispatchEvent` in `modules/process/event/protocol/event-target.kh` transfers an event to a set of listeners; its target is a listener set rather than an execution point, and its direction of transfer does not change where the calling code continues. It is an event-delivery relation, not a Flow Decision.

### The names to use and the names to refuse

**Use `Scope`** for a branch body, and write it as `sc` in Khayyam source. [Type → Scope](../../../docs/type.md#scope--type-as-semantic-boundary) settles the category and [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) settles the subtype.

**Refuse `Branch`, `Block`, `CodeBlock`, `Label`, and `labelType`** for it. The first three are new names for a category [Type](../../../docs/type.md#categories-of-type) already has; the last two are what [`protocol/if.kh`](./protocol/if.kh) currently calls it, and `labelType` names no concept any document defines. [Terminology → The Default Meaning of an Unreferenced Term](../../../docs/terminology.md#the-default-meaning-of-an-unreferenced-term) is what makes refusing them a decision rather than a preference: an unreferenced word carries its ordinary sense, and "label" carries the sense of a jump target, which is a different thing from a branch body.

**Use `Boolean`** for a truth value — `modules/math/boolean/protocol/boolean.kh` — and let a domain-named condition be whatever type the receiver's own contract names.

**Refuse `Condition`, `Predicate`, and `Flag`** as this library's type names, and do not adopt `Status` from the protocol's own example either. [Khayyam → Type Principles Realized](../../../docs/khayyam/khayyam.md#type-principles-realized) states there are no primitive types and that even what other languages write as `bool` is a named capsule, so a type here names a domain concept; `modules/math/boolean/protocol/boolean.kh` already owns the truth-value concept, and a second capsule for it would be the collision [Import Mechanism](../../../docs/khayyam/khayyam.md#import-mechanism-in) calls an architecture error. The protocol writes `Status` and `Bool` as examples of what a caller might pass ([The Generic Form](../../../docs/protocols/process/control-flow.md#the-generic-form-ifelse), [The Preferred Form](../../../docs/protocols/process/control-flow.md#the-preferred-form-domain-specific-conditional-methods)); an example is not a claim on the name.

**Use `Decision` or `Flow` for the operation that changes course**, and `Conditional Pair` for the two-member form, following [Control Flow's own vocabulary](../../../docs/protocols/process/control-flow.md#library-defined-control-flow).

**Refuse `Goto` as the concept's name and keep it only as the spelling of an unstructured jump package.** [Control Flow → Library-Defined Control Flow](../../../docs/protocols/process/control-flow.md#library-defined-control-flow) already names the family "conditionals, loops, jumps, and domain-specific branch methods", and `GOTO` is prior art recorded in that document's changelog rather than a Memar term.

**Use `Halt`**, following [Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation)'s "Explicit Halt Operations" and its registered topic "Halting semantics".

**Refuse `panic` as a library concept name.** The same changelog records `panic`/`recover` among the ecosystems' answers to a question this protocol answers differently, and an unreferenced `panic` carries Go's meaning rather than Memar's. `Recover` is refused for the same reason and additionally because what observation of a halt means is [the protocol's own open topic](../../../docs/protocols/process/control-flow.md#topics-to-be-developed-here).

**Use `Error`** for a propagated failure and `Iteration` for a traversal, following [`modules/process/error/protocol/error.kh`](../error/protocol/error.kh) and `modules/computer/adt/container/protocol/iteration.kh`. **Refuse `Exception`**, which the same changelog records as rejected, and **refuse `Loop`** in favour of `Iteration`, whose owner is already established in this repository.

**Use `Conditional` for the concept this model calls Flow Decision only if it is filed under this module**; the name already exists in `modules/math/logic/conditional.kh` with a different subject, and [Qualified Names → When qualification cannot separate two declarations](../../khayyam/rules/qualified-names/qualified-names.md#when-qualification-cannot-separate-two-declarations) is the rule that governs a name claimed twice.

### What the protocol states that the language does not
The protocol states four things no language document states, and a library written without them would be missing a requirement rather than making a choice.

**A branch is a scope plus a decision, and the two are distinct concerns.** [Control Flow → Library-Defined Control Flow](../../../docs/protocols/process/control-flow.md#library-defined-control-flow) separates what from when. [Type → Scope](../../../docs/type.md#scope--type-as-semantic-boundary) describes Scope by its naming, visibility, ownership, and isolation rules and says nothing about entry; [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) records the inertness as the reason a driving method must exist, without saying what driving means.

**A construct carries its dependencies in its own arguments.** [The Generic Form](../../../docs/protocols/process/control-flow.md#the-generic-form-ifelse) requires `ELSE` to name the same condition value `IF` names. No language or toolchain document states this for a branch-shaped construct; it is a protocol rule whose only implementation today is one realization's own reading.

**An error path is a control path, and it must stay visible.** [Error Propagation](../../../docs/protocols/process/control-flow.md#error-propagation) requires every fallible operation to expose its error path as an ordinary named part of the call contract and its tooling to check that the path is handled or routed. [Khayyam → The Grammar Refuses Protocol Semantics](../../../docs/khayyam/khayyam.md#the-grammar-refuses-protocol-semantics) declines to say anything about errors at all, so nothing in the language requires the visibility the protocol requires of a library.

**Structured and unstructured flow are equal, and the choice between them belongs to a tool.** [Structured and Unstructured Flow as Libraries](../../../docs/protocols/process/control-flow.md#structured-and-unstructured-flow-as-libraries) states that a jump method is exactly as valid and exactly as unprivileged as a branch pair. The language neither privileges nor forbids either; it simply has neither in its grammar.

### What the language states that the protocol does not
The language states three things the protocol does not carry, and each is a fact a library declaration depends on.

**`return` is a command, not a method.** [Khayyam → Scope](../../../docs/khayyam/khayyam.md#scope) states that a compiler of this language lowers `sc`-driven branches to internal jumps and that `return` is an IR marker that must itself end with a line break so it cannot be written as `return 0`. The commands a body may hold are therefore fixed at four — declare, scope, invoke, return — by the JavaScript target's own reading of the grammar in [its target document → The commands a body may hold](../../khayyam/targets/js/target.md#the-commands-a-body-may-hold), and no jump appears among them. The protocol calls a mid-scope return an ordinary control-flow operation, which is true of what it does and silent on who declares it; in this realization the grammar declares it and the library does not.

**A method names its parent type and every call writes both groups.** [Khayyam → Method Invocation Rules](../../../docs/khayyam/khayyam.md#method-invocation-rules), with a call on the parent type — `W32.Sum(a, b)(total, err)` — as well as on a variable of it. The protocol's own examples write `IF(isValid, ValidData)` with no owner and no influenced group, and its handoff records that those examples stand in for wherever the owner is declared. A declaration written from those examples as printed would name no parent type.

**A scope may be received as a type-level argument.** [Method → Type-level arguments for `sc` and `mt`](../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) admits a `vr`, an `sc`, or an `mt` in a method's influencing group and leaves the spelling of the parameter's type unstated. The protocol assumes the branch-grouping primitive is available to a method that drives it and does not say how the driven scope is typed.

### What the corpus states that neither does
Three things are true of this repository's control-flow corpus and of no document in it.

**The preferred pair is already declared twice, empty, in two other modules.** `modules/computer/adt/protocol/listeners.kh` declares `OnAbsent ab` and `OnPresent ab`; `modules/process/operation/protocol/on-failure.kh` and `modules/process/operation/protocol/on-success.kh` declare `OnFailure ab` and `OnSuccess ab`. Neither set carries a method, and neither file imports anything. The protocol's handoff records the naming as undecided *between* these two pairs, so the corpus holds both sides of an open question as if it were settled, in the wrong module, with no contract.

**Sixteen files carry sixteen ecosystem spellings; three of them are one relation.** [`protocol/`](./protocol/) holds one file per form a mainstream language offers. Under this model, `case`, `default`, and `else-if` are compositions of Conditional Pair and Flow Decision; `while`, `for`, and `loop` are the one repetition composition; `goto` and `jump` are one written-target decision; `break` and `continue` are derived-target decisions. [Khayyam Rule — File Layout](../../khayyam/rules/file-layout/file-layout.md) asks for one abstraction per protocol file and says to split when abstractions are distinct concepts — which is a test this layout passes by construction and not by meaning.

**The one non-empty draft declares three unbound names.** [`protocol/if.kh`](./protocol/if.kh) writes `tp IF mt (self CF) (condition Condition, execute labelType) (err Error) {}` with an inclusion of `modules/process/error/error.kh`, a file whose entire body is inside a `TODO(go-migrate)` comment and which therefore declares no `Error`. Roughly 130 files name the real address, `modules/process/error/protocol/error.kh`; [the toolchain handoff records the count and the two files that name the wrong one](../../khayyam/execution.handoff.md). Separately, [`protocol/panic-recovery.kh`](./protocol/panic-recovery.kh) declares `RuntimePanicRecovery cp {}` — a capsule with no field, no method, and no importer — and [`protocol/continue.kh`](./protocol/continue.kh) carries only a note about which other languages spell the form.

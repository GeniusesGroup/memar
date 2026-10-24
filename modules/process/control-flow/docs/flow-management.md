---
Title: "Flow Management Model"
Status: Draft
Start Date: 2026-10-03
ID: "497514"
---

# Flow Management Model

## Abstract
This document models **flow management** — the responsibility of whoever must make execution change course — by working from the requirements outward rather than from any one layer inward. It enumerates the flow operations a program in this language can be asked to perform, stating for each what a program writes and what has to exist for it to work; it derives from that enumeration the smallest set of things a compiler must provide that between them serve every enumerated operation, and it argues that the set is minimal by naming what each of its members cannot be dropped for; it states what the abstraction is at each of the four layers and why there is no single abstraction over them all; and it separates what is language-level from what is per-target from what is protocol-level, by the test this repository has already recorded. Its central findings are that seven operations are needed and no more; that five compiler obligations serve all seven, of which three are the guarantees the [Compiler](../../../computer/compiler/compiler.md) protocol already states and two — a landing, and a decision the compiler can serve without a library's name — it does not; that four of the seven cannot be written at all under the mechanism the compiler in this repository currently uses; and that nothing in the enumeration asks a compiler for first-class re-entry, mid-body resumption, or a value returned by a body, which removes three items the protocol's own option list carries. The operations are the ones a program needs and something must decide or sequence; the operations a mainstream language offers, and the shapes a tree of ported source happens to contain, are not evidence here, and the `.kh` files under [`protocol/`](../protocol/) are the residue of an attempt that did not succeed and may not be used as a premise. `return` is no longer a command a body may hold, so leaving a method early is one of the operations here rather than a keyword, and it can be performed by a program only once a library declares the method that performs it. What is left open, and which layer each open item belongs to, is carried in the paired [handoff](./flow-management.handoff.md).

## Introduction

### Motivation
Two failures sit on either side of the question this document answers, and both are ways of asking from the wrong end.

The first asks from the compiler inward: given what a compiler already has, what flow syntax should it grow? The [Compiler](../../../computer/compiler/compiler.md) protocol answers this at the level of a rule — the compiler recognizes language primitives, never a library's names (`:35`) — and a rule against magic does not tell a reader which handful of primitives are actually *needed*. A compiler that ships a conditional, a loop, and a jump implements more than flow requires; a compiler that ships none of them but never says what a drive means has discharged nothing. The protocol's own topic on flow answers the second half by stating seven guarantees about the branch body a flow module receives (`:51`–`:60`) and by recording, in the same document, that the deciding half of a conditional is unimplemented and that no option it lists covers it (`:77`). What no document states is the link between those two facts: **which obligations the flow operations actually need, and whether the seven guarantees are all of them.** Without that link, the guarantee list is a set of true sentences of unknown coverage, and any implementation that satisfies all seven may still be unable to write half the operations a program needs.

The second failure asks from one layer's vocabulary inward, and it is the failure the owner named when they said that simple and strong means not creating one big abstraction for everything. A layer's own vocabulary is a natural place to start and a bad place to stop: a language that has a code scope suggests a conditional, a loop, and a jump because those are what a code scope is usually accompanied by, and the resulting enumeration is a list of the ecosystem's spellings rather than a list of what a program is asked to do. Working from the requirements outward instead — first what a program can be asked to do, then what each layer must be for it to be done — produces a different list, and the difference is visible: it is shorter than the ecosystem's, and two of its members need nothing at all from a compiler beyond what a third member already needs.

A third failure is specific to this repository today. `return` has left the grammar: [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:131` states that there is no keyword for leaving a method early and that until a library declares one, a program written in this language has no way to leave a method early. Any enumeration written before that statement would have counted a mid-scope return as something the language provides and would have asked the compiler for nothing on its behalf. Enumerated from the requirements, leaving a method early is one of the operations, and it is one a program can perform only once a library declares the method — which makes it the operation that most directly exposes what is still missing.

### Methodology
The enumeration was derived by the procedure in [Modeling Practice → Starting a New Requirement](../../../../docs/modeling.practice.md#starting-a-new-requirement) and [Challenging a Proposed Concept](../../../../docs/modeling.practice.md#challenging-a-proposed-concept): the criterion in [The criterion an operation must meet](#the-criterion-an-operation-must-meet) was stated first, every candidate the protocol documents name was tested against it, and each surviving candidate was then asked what a program writes and what must exist for it to work. Nothing was admitted on the grounds that a mainstream language has it, and nothing on the grounds that a `.kh` file under [`protocol/`](../protocol/) has it; the `.kh` files are the residue of an attempt to develop these ideas in another language that did not succeed, which the owner has ruled neither evidence nor a premise, and this document rests on none of them.

The compiler surface was then derived from the enumeration by a single procedure: take the union of what each surviving operation needs from a compiler, and merge only those needs that one guarantee can state without qualification. Completeness is then checked in one direction — every enumerated operation is served — and minimality in the other, which is the half a proposal cannot supply: for each member of the resulting set, the document names the operations that fail without it and states why no other member covers them.

Every claim about the language is read from the language's own documents and from the toolchain's own records of what it does, and each is cited at the point it is made. Where the network is unavailable and a claim could not be checked against a second source, the document says so; nothing here is asserted from training knowledge of any other language, and no comparison to another language's flow constructs is used as an argument anywhere in this document.

The separation between this document and [the Control Flow model](./control-flow.md) is deliberate and is argued under [Why this is a second model and not a second list](#why-this-is-a-second-model-and-not-a-second-list). This document does not restate the protocol and does not restate the Control Flow model; it cites both.

## Explanation

### What this document models, and why it is a second model here

**Flow management is the responsibility of making execution change course, whoever holds it.** The name is the repository's own: the [Compiler](../../../computer/compiler/compiler.md) protocol speaks of a module's *obligation to flow management* (`:42`) and of what a *flow-management module* is blocked on (`:77`), and the folder this document sits in is the module's. What the name denotes is a responsibility spread across four layers — the language, the protocol, the compiler, and the library — each of which holds a share of it and none of which holds all of it.

The name is deliberately not the name of an abstraction. No type, no contract, and no construct in this repository is called Flow Management, and this document states why one should not be: an abstraction is a thing with rules and an independent lifecycle, and the flow operations share neither (see [Why there is no umbrella](#why-there-is-no-umbrella)). What they share is a primitive — the branch body — and a set of guarantees about what driving that primitive means. A shared primitive is a relation between the operations, not a node above them, and [Modeling → One Reality, Multiple Abstraction Lenses](../../../../docs/modeling.md#one-reality-multiple-abstraction-lenses) treats a relation that does not add a responsibility as an edge rather than a concept.

#### Why this is a second model and not a second list
[control-flow.md](./control-flow.md) already models what the control-flow **library** needs to be: four concepts — Branch Scope, Flow Decision, Conditional Pair, Halt — what each owns, and what each does not. This document models a different subject, and the difference is not a difference of detail.

- **Different subject.** [control-flow.md](./control-flow.md) is asked *what is the library made of*. This document is asked *what can a program in this language be asked to do about its own flow, and what must each layer be for that to be possible*. The first question has an answer that is four concepts; the second has an answer that is seven operations and five compiler obligations, and neither answer contains the other.
- **Different direction of derivation.** The four concepts were derived by decomposing the protocol's operation family and testing candidates against the challenge questions, from the protocol inward. The seven operations were derived from what a program can be asked to do, and the compiler surface was derived from the operations, from the program outward. The owner's instruction is explicit that the second direction is the one to work in, and the result bears it out: the two lists do not have the same members, and the mapping between them is a relation rather than an identity.
- **Different layer.** The four concepts are the library's. This document's central object is the compiler's, and its second half is about which of its statements are the language's, which are a target's, and which are a protocol's. Merging the two would put a library's decomposition and a compiler's obligation in one document, which is the umbrella the owner refused.
- **The minimality claim belongs here and nowhere else.** Nothing in [control-flow.md](./control-flow.md) claims that a set is minimal, because nothing in it is a set of compiler obligations. A minimality argument is only meaningful against a stated surface, and the surface is this document's.

The two lists are not rivals, and the relation between them is stated once, in [How the two lists map](#how-the-two-lists-map).

### The criterion an operation must meet
An operation is counted when **both** of the following hold, and is refused when either fails.

1. **A program needs it.** Some computation a program in this language can be asked to perform cannot be performed without it. "Can be asked to" is the whole of the test: the question is not what a language offers but what a program may be *required* to express.
2. **Something must decide or sequence it.** The operation's effect is not the effect of an ordinary method call whose meaning is fully determined by its arguments and receiver. Something must choose whether it happens, or put it in a position relative to what happens next.

Two exclusions follow from the criterion rather than from taste. An operation that a language already performs for free fails the second test: doing this and then doing that is what a body already means, because its commands run in order and the method returns when they have run, so sequencing needs no operation. An operation whose decision is the caller's own judgment made on data fails the second test for the same reason: inspecting a value and acting on it is an ordinary call, and what makes a flow operation is that something *other than the value's own meaning* decides whether it happens.

The criterion is stated this way because it is checkable. Each entry below names the program-side thing that is asked for and the decision or sequencing that is not already there.

### The operations

Seven operations. Each is stated as what it is, what a program writes, and what has to exist for it to work. The spellings of the methods are illustrative — the owner type and the names are open, and are carried as open items in the paired [handoff](./flow-management.handoff.md) — while the shapes are what the protocol states and what the language admits.

#### Select
**What it is.** Running one of the bodies a condition chooses among, one run per selection.

**What a program writes.** A call that names the body to run, and the body itself declared in the same method. In the generic form, one call per branch, each branch naming the same condition value explicitly:

```khayyam
saveErr.OnAbsent(PaymentRecorded)
tp PaymentRecorded sc {
    // continue processing
}
```

The shape is the protocol's: [The Generic Form](../control-flow.md#the-generic-form-ifelse) writes `IF(isValid, ValidData)` with `tp ValidData sc { … }` and requires `ELSE` to name the same condition value it pairs with, so that the construct carries its dependencies in its own arguments; [The Preferred Form](../control-flow.md#the-preferred-form-domain-specific-conditional-methods) writes the same pair on the receiver that carries the condition, where the call site reads as a sequence of named intentions. In this language the body reaches the call as a type-level argument: [Method in Khayyam → Type-level arguments for `sc` and `mt`](../../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) at `:71` states that an `sc` in a method's influencing group is a code scope, and that a library method that drives a scope receives it there.

**What has to exist.** A body value the driving call can receive; a drive that runs it and returns; and a decision the driving operation can take that the compiler serves without knowing the driving method's name. Selecting among two bodies and selecting among five are the same operation: a compiler that serves one member serves any number of them, and no guarantee distinguishes them, so the member count is a property of a declaration rather than of what the compiler owes.

#### Repeat
**What it is.** Running a body again, while or until a condition holds.

**What a program writes.** A call on the receiver that carries the condition, naming the body to run on each pass. No protocol example of this shape exists; the shape below is this document's, derived from the generic form's:

```khayyam
rows.UntilExhausted(RowBody)
tp RowBody sc {
    // one pass
}
```

**What has to exist.** Everything Select needs, and two more things. A drive must be repeatable: driving the same body again runs it again from its first command, with nothing the compiler holds about it surviving from one driving to the next, so that a repetition is a repetition and not an accumulation. And a decision must be re-takeable, which is the same obligation Select has plus the fact that it is taken again after the body has run.

Whether the collection a repetition walks belongs here is settled elsewhere and is not re-opened: `Container_Iteration` and `Iterate` own traversal and its stopping on error, and [control-flow.md](./control-flow.md) at `:83` records that a loop body and an enclosing iteration are already one concept under that contract. What is left for the flow side is a body to run and the decision to run it again.

#### Continue
**What it is.** Stopping the current run of a repeated body and beginning its next one.

**What a program writes.** A call naming nothing but the intent — the body is the one the repetition is already running.

```khayyam
self.SkipRemainderOfRow()
```

**What has to exist.** A landing that is the start of the next run, and the repeatable drive that makes such a start meaningful. Nothing else: a continue is a repetition's own body-value and drive, applied one step earlier. This operation therefore needs no compiler obligation that Repeat does not already need, and the service table records that.

#### Leave
**What it is.** Stopping the current run of a body and continuing past the nearest enclosing one.

**What a program writes.** A call naming nothing but the intent.

```khayyam
self.StopThisPass()
```

**What has to exist.** A landing outside the current body. Where Continue's landing is the next run, Leave's landing is derived from the body's position — past the enclosing repetition or branch — and is fixed by the operation's kind rather than named in its arguments, which is what [control-flow.md](./control-flow.md) at `:52` calls a derived target.

#### Exit
**What it is.** Ending the method that contains the running body, before its last command.

**What a program writes.** A method call on some type — and, in this language today, on nothing else, because the grammar no longer offers a word for it:

```khayyam
self.FinishHere()
```

The owner type and the name are open. What is not open is that a program writes a call: [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:131` states that there is no keyword for leaving a method early, that what ends an execution before the last command of a method's body is a flow-management operation, and that until a library declares one a program written in this language has no way to leave a method early. That sentence is why this operation is counted separately from Leave: it names leaving a method as a flow operation, and it makes the absence of one a fact about the language rather than a defect in it.

**What has to exist.** A landing past the call. It is the one operation in this list whose *performance* a program cannot yet perform: the method it names does not exist, and a program's ability to leave a method early is gated on a library declaring it.

#### Transfer
**What it is.** Continuing at a point the operation names, rather than at the next command.

**What a program writes.** A call naming the point to continue at.

```khayyam
self.ResumeAt(RecoveryPoint)
```

**What has to exist.** A landing, and a way for a program to name the landing point. The landing is the compiler's; the name is the language's, and this document does not have it. The grammar ships no control-flow keyword and no label — [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:129` states that a code scope is inert until a library-provided method drives it and that the grammar ships no control-flow keywords or logical operators of its own — and [control-flow.md](./control-flow.md) at `:119` refuses both `Label` and `labelType` as names for a branch body. Whether a point in a program may be named at all, and by what construct, is a language question this enumeration raises and does not answer; it is carried in the paired [handoff](./flow-management.handoff.md).

That this operation is legitimate is the protocol's, not this document's: [Structured and Unstructured Flow as Libraries](../control-flow.md#structured-and-unstructured-flow-as-libraries) at `:134` states that a jump-shaped method is exactly as valid and exactly as unprivileged as a branch pair.

#### End
**What it is.** Ending the execution outright, without passing through the ordinary path of any decision before it.

**What a program writes.** A call on some type.

```khayyam
self.Halt(reason)
```

**What has to exist.** A landing past every frame. What else it has to exist for — what it carries, whether it carries an error and of what class, and what observes it — is not stated here: [Control Flow → Error Propagation](../control-flow.md#error-propagation) at `:144` requires abrupt halts to be explicit operations in the realization's library or contract layer and at `:152` registers the halting semantics themselves as a topic that protocol has not designed. What observation of a halt means belongs to the runtime and the log, per [control-flow.md](./control-flow.md) at `:93`.

### What no operation is
Six things a reader may expect in this list are not in it, and the reason for each is the criterion rather than a preference.

- **Sequence.** Doing this and then doing that is what a method body already means: its commands run in order and the method returns when they have run. Nothing decides or sequences it that the language does not already do, so it fails the second test.
- **A failure's route.** Choosing what happens after a fallible call fails is Select whose receiver is the error value, not an operation of its own. [The Error](../../error/error.md) at `:130` states that an `Error` is a contract addressed to the immediate caller whose sole purpose is to let that caller make a correct decision about what to do next — the decision is the caller's, made at the call site, which is exactly Select. Nothing in the repository requires a failing call to divert by itself, and the [disregarded-error Rule](../../error/rules/disregarded-error/disregarded-error.md) requires only that the failure be accounted for where the operation can see it, which the call contract's ordinary named output already provides.
- **Traversal.** Iterating a collection is owned by `Container_Iteration` and `Iterate`, including where it stops; see [control-flow.md](./control-flow.md) at `:83` and at `:98`.
- **Waiting, blocking, and descheduling.** A flow operation may cause a process to stop progressing, but that it does so by descheduling is [Concurrency](../../process.md#concurrency)'s and the runtime's; see [control-flow.md](./control-flow.md) at `:99`.
- **Observation of a halt.** A stack trace and a log event are diagnostics of an End, and both are owned elsewhere; see [control-flow.md](./control-flow.md) at `:93`.
- **Running something on the way out.** Deferred execution, teardown on the way out of a method, and setup before a body are lifecycle, and [Compiler → Entry and lifecycle are not grammar](../../../computer/compiler/compiler.md#entry-and-lifecycle-are-not-grammar) places how a program begins and ends outside the grammar and in configuration plus the selected runtime. No document in this repository asks a program for it as a flow operation, and the operation family [Library-Defined Control Flow](../control-flow.md#library-defined-control-flow) names — conditionals, loops, jumps, and domain-specific branch methods — together with the halt operations of `:144`, does not include it. Whether it belongs to flow management at all is carried as a protocol question in the paired [handoff](./flow-management.handoff.md).

### The minimal compiler surface
Take what the seven operations need from a compiler, and merge those needs that one guarantee can state without qualification. Five obligations remain.

| | Obligation | What it states |
| --- | --- | --- |
| **C1** | **The body** | Wherever the language admits a scope in an argument position, the compiler hands over a value; and within one execution, the same declared scope hands over the same value every time. |
| **C2** | **The drive** | Driving the body runs its commands to completion before the driving call returns; whatever the body wrote is visible when it returns; and driving it again runs it again from its first command, carrying nothing over. |
| **C3** | **The body's reach and its end** | The body sees every name visible where it was declared, and is seen nowhere outside itself; its meaning ends with the execution that declared it. |
| **C4** | **A landing** | There is somewhere control may go other than the next command, and the compiler knows where: past an enclosing body, at the start of a body's next run, past the call, past every frame. |
| **C5** | **A decision** | A program can say whether a body runs, in a way the compiler serves without the compiler knowing the name of any library's method. |

**Three of the five are guarantees the compiler protocol already states.** C1 is [The compiler's obligation to flow management → The branch body a flow-control module receives](../../../computer/compiler/compiler.md#the-branch-body-a-flow-control-module-receives) at `:54` (what it is) together with `:58` (whether it is the same object across calls). C2 is `:55` (what driving it does) together with `:56` (what happens when it is driven twice). C3 is `:59` (what it may see of its enclosing method) together with `:60` (what happens to it when the enclosing method returns). The enumeration adds nothing to those three, and that is the first result of deriving from the requirements rather than from the compiler: the protocol's guarantee list covers everything about the body itself.

**Two of the five are guarantees the protocol does not state.** C4 has no guarantee behind it. The protocol's item 4 at `:57` states only what a module may rely on — that a drive completes before the driving call returns, and that whatever the body produced reaches the driver through the variables the driver handed it — and names what a body hands back as open; the landing is not named in that item at all, and appears in the document only inside the mechanism it would commit a compiler to, at `:68`. C5 is the gap the protocol records in its own words: at `:77`, "**The deciding half of a conditional is unimplemented, and none of the four options covers it.** Every option above describes what happens once a drive is granted. None says where the *decision* comes from." The requirement this document adds to that finding is a statement of what a decision must be for the compiler to serve it: not a name the compiler knows, and therefore expressible over the language's own primitives. The protocol names three ways the gap could be closed and says which of them it is belongs to the owner (`:79`); this document does not choose among them.

#### The service table

| Operation | C1 body | C2 drive | C3 reach and end | C4 landing | C5 decision |
| --- | --- | --- | --- | --- | --- |
| **Select** | needs | needs | needs | — | needs |
| **Repeat** | needs | needs (incl. the re-drive clause) | needs | needs | needs |
| **Continue** | inherited from Repeat | needs (the re-drive clause) | needs | needs | — |
| **Leave** | inherited from Repeat | inherited from Repeat | needs | needs | — |
| **Exit** | inherited from Repeat | inherited from Repeat | needs | needs | — |
| **Transfer** | needs | needs | needs | needs | — |
| **End** | — | — | needs | needs | — |

"Inherited" means the operation needs it only because it composes with one that does; it is served by that composition and not by a guarantee of its own. C3 is needed by all seven because each of them either receives a body or acts inside one. C4 is needed by six and not by Select, which is the only operation whose whole content is whether a body runs.

### Why the surface cannot be smaller
A minimality claim is only a proposal until it says what fails without each member. Each member below is stated with the operations that cannot be served without it, and with why no other member covers the need. Each claim is about a compiler that keeps the other four and drops this one, so each is a claim about a proper subset.

**C5 cannot be dropped, and no subset of the other four can replace it.** Every one of C1, C2, C3, and C4 is a statement about what happens *once a body is driven* — C1 about what is handed over, C2 about what running it does, C3 about what it may see and when it stops meaning anything, C4 about where control may land afterwards. Select and Repeat are defined by *whether* a body runs, and a compiler satisfying all four is one in which every body handed over is run to completion, possibly again, and from which control may land anywhere — and in which nothing can be written that decides between running and not running. That is not a gap in the four; it is what the four are about, as the protocol itself states at `:77`. Therefore no proper subset of {C1, C2, C3, C4} serves Select or Repeat, C5 is not derivable from them, and any complete set contains it.

**C4 cannot be dropped.** Four operations — Continue, Leave, Exit, End — and the next-run landing of Repeat consist entirely of *where control lands*: each is defined by its target and would have no content without it, and Repeat cannot land its next run anywhere either. C1, C2, and C3 are all satisfied in full by a compiler that, after running any body, continues at the next command — which is a compiler that satisfies every obligation about the body and can express none of these four operations. The need is therefore not derivable from C1–C3, and the compiler protocol says so from its own side: the jump mechanism is described at `:68` as committing the compiler to "a static account of where control can land, which is what makes the derived-target decisions — past an enclosing scope, the next iteration, past the call — expressible at all."

**C2 cannot be dropped, and its re-drive clause cannot be dropped from it.** C1 alone is satisfied by a compiler that materializes a value wherever a scope appears and never runs anything, which serves no operation. The re-drive clause is a separate claim inside C2 because C1 does not imply it: a compiler may hand over a fresh value each time a body is reached, or may continue a body where its previous run stopped, and either satisfies C1 and a drive that runs the commands. Under the first, Repeat cannot be written — there is nothing to drive twice; under the second, a repetition is an accumulation, and Continue's target stops being the start of a run and becomes a position inside one, which is first-class re-entry and is not needed (see [What the enumeration does not ask the compiler for](#what-the-enumeration-does-not-ask-the-compiler-for)).

**C1 cannot be dropped.** Every operation that receives a body receives it in an argument position, because that is the only place the language admits one: [Method in Khayyam → Type-level arguments for `sc` and `mt`](../../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) at `:71` admits an `sc` in an influencing group, and [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:132` says the same from the grammar's side. With no value handed over, Select, Repeat, and Transfer have no argument, and the operation would have to locate the body's commands in the emitted artifact — which the protocol forbids by construction, naming what the body is "not a name, and not a region of an emitted artifact" (`:54`).

**C3 cannot be dropped, and this is the member most easily mistaken for a restatement of C1.** C1 says a value is handed over; C3 says that value still means what it meant where it was written. They are separable, and a compiler can satisfy C1 while failing C3: hand over the commands as a detached unit — a bare thunk, a region of emitted code with no environment — and every operation in the table is served *in form*. A branch body written beside a variable it reads would then be unable to read that variable, a repeated body would be unable to accumulate into the enclosing method's state, and Select and Repeat would run a body that computes nothing about the program that wrote it. The repository has already measured this reach and found it stated by no language document: the JavaScript target records that a scope's block closes over the enclosing method, that nothing else in the language reaches, and that "**No document of the language states this reach**" ([the JavaScript target → The commands a body may hold](../../../../bundles/khayyam/targets/js/target.md#the-commands-a-body-may-hold) at `:42`). The compiler protocol holds the rule itself at `:59`, and says in the same sentence that "those rules are this protocol's, and no language document states them."

**Therefore the surface is five obligations, no proper subset of which serves all seven operations, and every one of the seven is served by the five.** That is the completeness half and the minimality half, and they are separate claims: the service table establishes the first, the five paragraphs above establish the second.

### What the enumeration does not ask the compiler for
A minimum is a claim in both directions, and this one has a second side: what the compiler is *not* required to provide, three items the protocol's own option list carries and the enumeration does not reach for.

- **No privileged flow construct.** The compiler provides no intrinsic `if`, `while`, `goto`, `break`, `continue`, `return`, `match`, or `defer`. The compiler protocol forbids it twice over: the compiler recognizes language primitives and not library names (`:35`), and a jump-shaped method is exactly as unprivileged as a branch pair ([Structured and Unstructured Flow as Libraries](../control-flow.md#structured-and-unstructured-flow-as-libraries) at `:134`). All seven operations are ordinary methods on ordinary types, and [the JavaScript target](../../../../bundles/khayyam/targets/js/target.md) at `:125` records the same from the toolchain's side: a conditional would be a unit the program includes, not a name the compiler knows.
- **No first-class re-entry, and no mid-body resumption.** [What this obligation does not decide](../../../computer/compiler/compiler.md#what-this-obligation-does-not-decide) at `:70` names a returned continuation as one of four ways a drive may be served and says of it: "**No other option delivers that, and it is what a repetition driven from two different decisions would need.**" Nothing in this enumeration needs it. Continue's target is the *start* of a body's next run, which C2's re-drive clause already gives; Transfer's target is a point the operation names, which is an entry into a body or a jump out of one and not a resumption; Repeat's target is likewise a start. The open question the protocol records at `:72` — whether a body may be re-entered at a point other than its start, and what a body hands back to its driver — therefore blocks none of the seven. It blocks the two things this enumeration excluded: deferred execution, and a body resumed mid-way through.
- **No value returned by a body.** Guarantee 4 at `:57` leaves what a body returns open, and the enumeration leaves it open with it: what the seven operations need is that a drive completes and that the body's writes reach the driver through the variables the driver handed it, which this language already provides — every variable of a call passes strictly by reference ([Khayyam → Method](../../../../docs/khayyam/khayyam.md#method) at `:83`). A Select that needed a value back from its body would need a language this repository does not have, since the language has no literal and no construction form and every value a program handles was produced outside it ([the JavaScript target → Running a program](../../../../bundles/khayyam/targets/js/target.md#running-a-program) at `:82`).

### How the two lists map
The seven operations and [control-flow.md](./control-flow.md)'s four concepts are related, and the relation is not an identity. Branch Scope is the body every operation that receives one receives, and it is the operand of the whole table rather than an operation. Flow Decision is the responsibility the library holds for the five operations whose effect is to change where execution goes — Select, Repeat, Continue, Leave, Transfer — and it is not the same set as the seven, because Halt is not one of them and Exit is. Conditional Pair is the well-formedness of Select's two-member form. Halt is End. Repetition, which [control-flow.md](./control-flow.md) at `:81` holds to be a relation rather than a concept, is what Repeat and Continue are made of. No mapping in that sentence is one-to-one in both directions, and the three that look one-to-one — Repeat to nothing, Continue to nothing, End to Halt — are the three where this document's list has an entry the other does not.

### What the abstraction is, layer by layer
Each layer holds one abstraction, and no two of them are the same abstraction. The four statements below are the answer to what a flow-management module is *made of* at each layer, and they are what the compiler's part reduces to when it is stated without flow vocabulary.

**The language's abstraction is Scope.** [Type → Scope — Type as Semantic Boundary](../../../../docs/type.md#scope--type-as-semantic-boundary) counts a namespace boundary, a module-visibility boundary, a package boundary, a transaction's isolation boundary, and a local algorithmic block among the realizations of one category, and names "a local algorithmic block (as used by `if`, `loop`, `goto`)" among them; [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) fixes the subtype as `sc` and states the one property the whole of flow rests on: a code scope is inert until a library-provided method drives it. That is the language's entire flow abstraction, and it contains no operation, no keyword, and no notion of when. The language's protocol for flow is what it does not say — `:129` states that the grammar ships no control-flow keywords or logical operators of its own, and [The Grammar Refuses Protocol Semantics](../../../../docs/khayyam/khayyam.md#the-grammar-refuses-protocol-semantics) holds that a construct enters a grammar only when its semantics can be stated without adopting any protocol's definitions.

**The protocol's abstraction is the operation contract, not a type.** [Control Flow → Library-Defined Control Flow](../control-flow.md#library-defined-control-flow) states what such an operation is: an explicit operation over the primitive that groups a branch body, whose effect is the running of that body, and whose target is either written in its arguments or derived from its kind. That is an abstraction with rules — dependencies carried in arguments rather than in position, two branches named by etymologically distinct roots, structured and unstructured flow equally privileged, an error path visible in the call contract — and it is deliberately not a type. What the protocol owns is the contract and its equality; what it refuses is a mechanism, a spelling, and an owner. Its three registered subjects — the conditional-pair contract, iteration-shaped flow, and halting semantics (`:148`–`:152`) — are contracts still to be written, not abstractions missing from this sentence.

**The compiler's abstraction is a body, a landing, and a decision — none of which is a flow concept.** Stated without flow vocabulary, C1 through C3 are about a value the compiler materializes with a stated reach and a stated end; C4 is about where control may go; C5 is about the compiler's ability to serve a yes-or-no without a name. A compiler that satisfies all five has no concept of flow at all, which is the shape of the answer to what the compiler owes flow management: **three nouns, and not one of them is a flow noun.** What the compiler must *not* hold is the operation family, the owner type, the member count of a selection, and every name — the four things that would make it a compiler that knows a library.

**The library's abstraction is the receiver-named operation.** [The Preferred Form](../control-flow.md#the-preferred-form-domain-specific-conditional-methods) puts the conditional methods on the result type, so that the calling code reads as a sequence of named intentions, and holds that a capsule result with a natural binary or multi-way interpretation should expose its branches by those names. Under this document's enumeration that preference generalizes: each of the seven operations is a method on the type whose own state or position is what it decides, so that the receiver carries the condition and the call site names an intention. What is left for a library is therefore: the seven declarations; the owner of each; the name of each; which target each writes and which it derives; the pair's naming rule; and the governance that decides which library an organization may use, which [Mechanism Summary → Linter Governance over Compiler Dictatorship](../control-flow.md#mechanism-summary) places with that organization's own tooling.

### Why there is no umbrella
The owner asked whether the seven operations share one abstraction. They do not, and three tests say so; each is a test the repository has already recorded, applied to a candidate that is exactly the one an author would reach for.

**The challenge test: an umbrella owns no rule the seven do not already obey elsewhere.** [Modeling Practice → Challenging a Proposed Concept](../../../../docs/modeling.practice.md#challenging-a-proposed-concept) asks whether a concept enforces rules that no existing concern already owns. What the seven share is two sentences — that each is an explicit operation, and that the compiler may not privilege it by name. The first is category membership with no content: it says what the operations are, and not what any of them must do. The second is [the compiler protocol's own rule](../../../computer/compiler/compiler.md#the-compiler-recognizes-language-primitives-not-library-names) about the compiler, and it binds the compiler rather than the members. An umbrella abstraction over the seven would enforce neither, and there is no third sentence to enforce.

**The lifecycle test: no member's replacement touches any other.** [control-flow.md](./control-flow.md) at `:111` states the property that makes a flow library worth modeling at all: it is replaceable without any branch body changing. A node with an independent lifecycle is what [Modeling Practice → Node Classification Audit](../../../../docs/modeling.practice.md#node-classification-audit) calls an independent concept, and an umbrella under which every member may be removed, replaced, or forbidden by one organization's tooling without disturbing the rest has no lifecycle of its own — it is the sum, and [Modeling → Domain Decomposition over Aggregate-Root Modeling](../../../../docs/modeling.md#domain-decomposition-over-aggregate-root-modeling) holds aggregation to be a consequence of modeling rather than a primitive.

**The call-site test: the umbrella is designed to be absent from every call.** An umbrella realized as a type every flow method hangs on would have to be written at every call site — and the protocol's preferred form deliberately removes it, by putting the condition on the receiver so that `saveErr.OnAbsent(PaymentRecorded)` names the value and the intention and nothing else ([The Preferred Form](../control-flow.md#the-preferred-form-domain-specific-conditional-methods) at `:100`). A type whose design goal is to be absent from every call site it governs is not an abstraction the caller uses, and an abstraction no caller uses is not an abstraction. Realized as a contract every member satisfies, it fails the first two tests instead, because the only thing its members satisfy in common is being members.

What the seven do share is real, and it is worth stating precisely because it is what a reader will mistake for an abstraction: **they share one primitive and one guarantee set.** The primitive is the branch body, and the guarantee set is C1 through C3 — what driving that primitive means. Sharing a primitive is a relation the operations hold to Scope, not a node above them, and the relations section of [control-flow.md](./control-flow.md) already states that one in the direction that matters: a Flow Decision is taken on a Branch Scope, one decision drives one scope per call, and a scope may be driven by any number of decisions. The umbrella the owner refused would be the same fact misread as a type.

### What is language-level, what is per-target, and what is protocol-level
The test is the one this repository has already recorded, applied here as [binding.md states it](../../../computer/binding/binding.md#what-is-language-level-and-what-is-per-target). **Language-level** is what a document states about what a program may mean, and the coincidence test decides it: were a second target to state the same thing the same way, that would not make it language-level — it would make it a coincidence between two tools, and a coincidence is what [Khayyam → Minimal Legislation](../../../../docs/khayyam/khayyam.md#minimal-legislation-a-principle) exists to refuse. **Per-target** is what each realization states for itself and would state differently. **Protocol-level** is a claim whose home is a document under [`modules/`](../../../), which is protocol-level whatever any target does with it, and which the language cannot discharge at all.

| Claim | Bucket | Why, and what would move it |
| --- | --- | --- |
| A scope may appear in an argument position and is handed over as a value | **Language-level** | [Method in Khayyam → Type-level arguments for `sc` and `mt`](../../../../docs/khayyam/method.md#type-level-arguments-for-sc-and-mt) at `:71` and [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:132` state it, and neither names a target. A second target would realize it as a different thing — this one emits a `function` declared inside the method that holds it ([the JavaScript target → The artifact of one unit](../../../../bundles/khayyam/targets/js/target.md#the-artifact-of-one-unit) at `:54`, `emit.ts:423`–`:429`) — which is the coincidence test confirming the statement rather than the realization. |
| A body is inert until something drives it | **Language-level** | [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:129` states it as the language's own property of `sc`, naming no target. |
| There is no keyword for leaving a method early | **Language-level** | [Khayyam → Scope](../../../../docs/khayyam/khayyam.md#scope) at `:131` states it of the grammar. |
| A body's reach: it sees every name visible where it was declared, and is seen nowhere outside itself | **Protocol-level**, and the language is silent | The rule is the compiler protocol's, and the protocol says so — "those rules are this protocol's, and no language document states them" ([Compiler](../../../computer/compiler/compiler.md#the-branch-body-a-flow-control-module-receives) at `:59`). The JavaScript target states its own reading of it as a measurement ([target](../../../../bundles/khayyam/targets/js/target.md#the-commands-a-body-may-hold) at `:42`), and a second target is free to read it differently until a language document states it. Whether it becomes language-level is carried as a language question in the paired [handoff](./flow-management.handoff.md). |
| A body's meaning ends with the execution that declared it | **Protocol-level** | Stated at `:60`, and it is a bound rather than a service: nothing about it varies with the target, and it cannot be discharged by the language because no language document states it. |
| Driving a body runs it to completion, its writes are visible at return, and it can be driven again from its start | **Protocol-level** | Stated at `:55` and `:56` by a document under `modules/`, and each target realizes it in its own way — this one serves a drive by an ordinary call ([Compiler → The implementation in this repository is not this protocol](../../../computer/compiler/compiler.md#the-implementation-in-this-repository-is-not-this-protocol) at `:86`). |
| Where control may land, and that the compiler knows where | **Protocol-level** as an obligation; **per-target** as a mechanism; **unimplemented per-target** today | The obligation is not stated as a guarantee anywhere, which is why C4 is one of the two items this document adds. The mechanism is one of four the protocol leaves open (`:64`–`:72`), and the four are not equivalent for it: `:68` states that the jump is what makes the derived-target decisions expressible at all. This repository's realization serves a drive by a call, its representation carries three commands for a body and no jump among them, and a scope is emitted as a nested `function` (`:86`, `emit.ts:423`–`:429`) — under which a nested function's only exit is its own return, so **Leave, Exit, Transfer, and End have no expression from inside a body.** Which mechanism serves a drive is carried as a toolchain question in the paired [handoff](./flow-management.handoff.md). |
| A decision can be served without the compiler knowing a library's name | **Protocol-level** | The protocol forbids the compiler from owning the decision by name (`:35`) and records at `:77`–`:79` that the gap is open and that three things would close it. No target can discharge it by choosing differently, because the requirement is about what the compiler does not know. |
| A condition is an ordinary value produced by an ordinary call | **Language-level** | It is the influencing and influenced groups of a call — [Method in Khayyam → Influencing and Influenced Variables](../../../../docs/khayyam/method.md#influencing-and-influenced-variables-not-inputs-and-outputs) — with no compiler privilege anywhere in it. This is why the *source* of a decision is language-level while its *landing* is not. |
| How a body is realized: a closure over cells, the cell a variable is, what a body hands back, whether a body may be re-entered mid-way | **Per-target** | Each is a realization's choice and none is required by anything in the table. This repository's choices are its own: a cell per declared variable and one scope emitted as a `function` ([target](../../../../bundles/khayyam/targets/js/target.md#running-a-program) at `:52`, `:54`), an empty link map (`:75`), and a refusal of a scope used as a receiver, which the compiler protocol records as "a realization's refusal rather than a protocol rule" (`:83`). |
| That the seven operations are legitimate, equally privileged, and governable by an organization's tooling | **Protocol-level** | [Structured and Unstructured Flow as Libraries](../control-flow.md#structured-and-unstructured-flow-as-libraries) at `:134` and [Mechanism Summary](../control-flow.md#mechanism-summary) at `:130`. An organization may forbid raw jump methods in its own codebase without asking the language to make that choice once, which is why no target can settle it. |
| That a failure's path stays visible in the call contract, and that a halt is an explicit operation in the library or contract layer | **Protocol-level** | [Control Flow → Error Propagation](../control-flow.md#error-propagation) at `:141`–`:144`. Which form a target realizes it in is the realization's, and [disregarded-error Rule](../../error/rules/disregarded-error/disregarded-error.md) states the form as deliberately unprescribed. |
| The seven names, the owner type, and which declaration lives in which file | **Naming, and the protocol's open subject** | No document requires one type per form or one form per file, and the candidate spellings already in this repository's documents do not agree with each other. Carried in the paired [handoff](./flow-management.handoff.md); [control-flow.md](./control-flow.md) at `:115`–`:135` states which names are used and which are refused, and this document's seven are checked against that list rather than chosen beside it. |

### What this model does not decide
The boundaries below are the model's, and each names the layer whose decision it waits on. What each one currently is — its state, what a ruling must decide, what it blocks, and what would close it — is carried in the paired [handoff](./flow-management.handoff.md), and the whole of it is [working state rather than current design](../../../../modules-plugable/knowledge/documentation/explanation/explanation.md#relevance-discipline).

- **A language decision:** whether a program may name a point to continue at, and by what construct. Transfer needs a nameable target and the grammar ships no label.
- **A language decision:** whether the language's own documents state a body's reach and its end, or whether those stay the compiler protocol's. C3's bucket moves depending on the answer.
- **A protocol decision:** whether deferred execution and teardown on the way out are flow operations at all. They are excluded here because no document asks a program for them as one; the criterion excludes them, and a protocol ruling could put them back.
- **A protocol decision:** whether an operation's own signature may carry an error path, and what a halt carries and of what class. Both are registered subjects the Control Flow protocol has not designed.
- **A toolchain decision:** which of the four mechanisms serves a drive in this repository. Four of the seven operations are unwriteable under the one it currently uses.
- **A naming decision:** the owner type of the operations, the seven names, and which candidate conditional pair survives and where it is declared.

Two of these are the owner's and are not this document's to close: the mechanism (which the compiler protocol says belongs to the owner at `:79`), and the naming and placement of the conditional pair, which [control-flow.md](./control-flow.md)'s own handoff carries. This document states no mechanism and chooses no name; the seven names in this document name operations for the sake of talking about them, and a declaration would take the owner and the spelling from those open items.

## Where this leaves the folder
The four concepts in [control-flow.md](./control-flow.md) remain what the library is made of, and the nine questions in its handoff remain what a declaration waits on. This document does not answer any of them, and it narrows none: it says what a program is asked to do, what a compiler must therefore provide, and — for the first time in this folder — that the compiler protocol's seven guarantees are not the whole of what the seven operations need. The two items it adds, a landing and a decision, are the two the compiler protocol already records as unmet; the enumeration's contribution is that they are the *only* two, and that three capabilities the protocol's option list carries — first-class re-entry, mid-body resumption, and a value returned by a body — are needed by nothing here.

# Flow Management Model Changelog

## Changelog

### Enumerated the flow operations and derived the minimal compiler surface

- Time: 2026-10-03T13:05:00Z
- Type: Added
- Propagates to:
  - [modules/process/control-flow/control-flow.md](./control-flow.md): Pending - its paragraph at `:151` still states that the commands a body may hold are fixed at four, `return` among them, which the grammar no longer says; its owner should make that correction, and this session did not make it.
  - [docs/protocols/computer/compiler.md](../../../computer/compiler/compiler.md): Pending - the enumeration asks it to state a landing as a guarantee rather than only inside the mechanism at `:68`, and to state a decision as a guarantee at all; whether it does so is the protocol's own call and its open items belong to the owner.
  - [modules/khayyam/targets/js/target.md](../../../../bundles/khayyam/targets/js/target.md): Pending - its table of the commands a body may hold still lists `return` at `:36`.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - instructed, ruled
  - [Space Bunny](../../../../CONTRIBUTORS.md#space-bunny-alpha) via [OpenCode](../../../../CONTRIBUTORS.md#opencode) - wrote

#### What changed
- Added [flow-management.md](./flow-management.md), a new model beside [control-flow.md](./control-flow.md) rather than a section of it. It enumerates the seven flow operations a program in this language can be asked to perform - Select, Repeat, Continue, Leave, Exit, Transfer, End - under a stated two-part criterion, each with what a program writes and what has to exist for it to work.
- It derives from that enumeration five compiler obligations - a body value, a drive, the body's reach and end, a landing, and a decision the compiler can serve without a library's name - with a service table in which every operation is served, and it argues minimality per member by naming the operations that fail without it and why no other member covers the need.
- It records that three of the five are guarantees the [Compiler](../../../computer/compiler/compiler.md) protocol already states at `:54`–`:60`, and that two - a landing and a decision - it does not, which are the two that protocol's own `:77`–`:79` records as unmet.
- It records three capabilities the protocol's option list carries that nothing in the enumeration needs: first-class re-entry, mid-body resumption, and a value returned by a body. The first is the one option at `:70` the protocol says nothing else delivers; this enumeration shows nothing here needs it.
- It records that under the mechanism the compiler in this repository uses - a scope emitted as a nested `function` - four of the seven operations have no expression from inside a body, which is the compiler protocol's own claim at `:68` about the jump option reached from the needs side.
- It states each layer's abstraction - the language's Scope, the protocol's operation contract, the compiler's body-and-landing-and-decision, the library's receiver-named method - and why the seven share a primitive and a guarantee set rather than one abstraction.
- It separates every claim into language-level, per-target, and protocol-level by the coincidence test [binding.md](../../../computer/binding/binding.md#what-is-language-level-and-what-is-per-target) records.
- Added the paired [handoff](./flow-management.handoff.md), carrying six open questions each labelled with the layer whose decision it is, with what it blocks and what would close it.

#### Considered and not done
- **Extend [control-flow.md](./control-flow.md) with the enumeration instead of writing a new model.** The four concepts there are the library's, derived from the protocol inward; the seven operations are a program's, derived from the requirements outward, and the minimality claim is a claim about a compiler surface rather than about a library. Merging them would also have put the library's decomposition and the compiler's obligation in one document.
- **Take the sources under `protocol/` as evidence for or against any shape.** The owner has ruled the `.kh` code under `modules/**` the residue of an attempt that did not succeed and neither evidence nor a premise. Every claim is cited to a document, and one sentence in the model says so.
- **Count multi-way selection as an operation.** No compiler guarantee distinguishes a two-member selection from a five-member one, so it would have added an operation and no obligation.
- **Count a failure's route as an operation distinct from Select.** [The Error](../../error/error.md) at `:130` puts the decision in the immediate caller, and the [disregarded-error Rule](../../error/rules/disregarded-error/disregarded-error.md) requires only that the failure be accounted for where the operation can see it. Nothing requires a failing call to divert by itself.
- **Count deferred execution as an operation.** The criterion excludes it, no document asks a program for it as a flow operation, and [Compiler](../../../computer/compiler/compiler.md#entry-and-lifecycle-are-not-grammar) places a program's beginning and end outside the grammar. It is carried as a protocol question instead of dropped.
- **Choose a mechanism for serving a drive.** The compiler protocol says at `:79` that which of the three ways to close the decision gap it is belongs to the owner, and names no preference among the four options at `:64`–`:72`. The model states what the landing must mean for every one of them and selects none.
- **Write an open-questions section into the model's body.** [Documentation → Explanation → Relevance discipline](../../../../modules-plugable/knowledge/documentation/explanation/explanation.md#relevance-discipline) holds that open questions are working state and live in the handoff, so the body carries what the model does not decide and which layer owns each decision, and the handoff carries the state, the blocks, and the closers.
- **Correct the two documents outside this folder that still list `return` among the commands a body may hold.** Both were recorded under `Propagates to` and in the handoff instead, and `modules/khayyam/` was under another agent's edits during the session.

#### Deliberation
- The owner asked how much the compiler must give the flow-management modules and answered the question by redirecting the work: work from the requirements outward rather than from the compiler inward, and treat "simple and strong" as meaning that there is no one big abstraction for everything (Omid Hekayati - instructed, ruled).
- The work therefore began from the criterion rather than from the sources, and the enumeration's members were tested against the criterion one at a time; a member that passed was then asked what a program writes and what must exist for it, and the second question produced the compiler obligations (Space Bunny - wrote).
- The minimality half was treated as the load-bearing part from the start, on the owner's statement that a minimality claim without it is a proposal. Each obligation was tested by dropping it while keeping the other four, and the third obligation - the body's reach - was found to be separable from the first, since a compiler may hand over a detached body and satisfy the first alone; that separation became its own paragraph in the model (Space Bunny - wrote).
- The no-umbrella question was settled by applying three recorded tests rather than by preference: the challenge test, the lifecycle test recorded in [control-flow.md](./control-flow.md) at `:111`, and the observation that the protocol's preferred form removes its own owner from every call site (Space Bunny - wrote).
- The owner ruled that `return` has left the grammar, and the model's Exit operation was written against that state: it is counted, and the document records that a program cannot perform it until a library declares the method (Omid Hekayati - ruled; Space Bunny - applied).

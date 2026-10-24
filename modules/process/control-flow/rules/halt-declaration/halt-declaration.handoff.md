# Control Flow Rule — Halt Declaration Handoff
Open state for [halt-declaration.md](./halt-declaration.md). See the repository's [documentation-handoff.md](../../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Status
Active — drafted 2026-10-03 on the owner's ruling that the concern which existed as a refusal inside another Rule be given a module and Rules of its own, written imperatively. The module turned out to exist: `modules/process/control-flow/` already holds the model that names **Halt** as an independent concept, the two declarations that would realize it, and the contract they realize. What it lacked was a `rules/` folder.

## Placement
The Rule was drafted into `modules/process/control-flow/rules/halt-declaration/` rather than into a new module, on three pieces of evidence read this session:
- `modules/process/control-flow/control-flow.md:69-78` names **Halt** as the fourth concept of the control-flow library, independent of Branch Scope, Flow Decision, and Conditional Pair, and `:129` settles the name.
- `modules/process/control-flow/protocol/panic.kh` and `protocol/panic-recovery.kh` are the only declarations in the repository of a halt and of its observation, and they are already filed here.
- `docs/modules/README.md:16` names `modules/process/control-flow/` as the implementation module for the Control Flow protocol, and `modules/process/rule/rule.md:61` lets any Module carry `rules/` beside `protocol/`.

An independent `panic` module was considered and not taken: it would duplicate a module the repository has, and `panic` is a refused name ([Control Flow model `:131`](../../docs/control-flow.md#the-names-to-use-and-the-names-to-refuse)).

## Withdrawn Framing
The concern previously existed as the second half of the "What it refuses" bullet of what was then a Khayyam Rule — a signal reaching past the point where a failure could have been handled, "of which a halt is the ordinary case". What was withdrawn is that sentence's carrying of halting, not the claim: the refusal itself is unchanged and now belongs to [disregarded-error.md](../../../error/rules/disregarded-error/disregarded-error.md), whose own text has always said halting is not its subject.

- **What it would have foreclosed.** A Rule about a failure that names halting in order to refuse it makes the halting question answerable only as the answer to someone else's Rule. An organization that halts deliberately — a runtime that aborts on an unrecoverable invariant, a library that reports a contract violation — would find the question closed in a document about error propagation, and a second realization of the protocol would inherit a ruling made about neither.
- **What replaced it, and what it deliberately does not decide.** A Rule whose subject is the declaration of a halt, stating that the operation is written where the caller reads it, that what leads to it is stated with it, and that governance over it is the organization's. It does not design the contract, decide what a halt carries, decide whether a halt may exist, or decide anything about observation.

## Open Questions
- **Where a halt's declaration goes when the caller cannot see the signature.** The Rule requires the operation to be written where the caller reads it, and a library boundary is where a caller often cannot. Whether the contract of the owning type carries it, whether a library states it in prose beside the declaration, and whether a caller across a network boundary receives anything at all are three answers, and no document chooses between them.
- **What a halt carries, and whether an `Error` justifies one.** Undecided in [The Error's handoff](../../../error/error.handoff.md) and in the protocol's own. The Rule is written so that this answer changes nothing in it: it requires visibility, not a payload.
- **What becomes of `protocol/panic.kh` and `protocol/panic-recovery.kh`.** The model records the collision at `:78` — a `RuntimePanicRecovery cp {}` with no field, no method, and no importer, beside a commented `Panic`/`Recover` pair inside `modules/computer/runtime/thread/protocol/thread.kh`. Whether one Halt contract replaces both, and under what name, is not this Rule's to settle and is not settled here.
- **Whether any live `.kh` declaration in this repository states a halt in a signature.** Not measured, and no longer a question this Rule's standing makes worth asking: the code under `modules/**` is residue of an attempt to develop these ideas in another language that did not succeed, and the owner has ruled that it is neither evidence nor a premise. The Rule reaches declarations nobody has yet written, which is the ordinary state of a Rule whose subject is new; a scan for a halt operation in a live `.kh` declaration would answer it, and no scan was run this session.
- **Whether the fate of `return` inside a halt belongs here.** A `return` leaves the method that writes it, and a halt ends the execution that contains it; whether a halt runs a scope's teardown before it ends is the protocol's registered topic at `:152` and is open there.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [halt-declaration.md](./halt-declaration.md) | Base — the Rule | Keep in sync with the owner's answers on this folder's open questions |
| [disregarded-error.md](../../../error/rules/disregarded-error/disregarded-error.md) | Sibling — the Rule that owns a failure's carriage, and that names this one as the owner of halting | Keep in sync; neither may take the other's subject |
| [Control Flow → Error Propagation](../../control-flow.md#error-propagation) | Depends_on — `:144` for the halt operation being explicit in the library or contract layer, `:141` and `:143` for the visibility it mirrors, `:152` for the contract not yet designed | None (read) |
| [Control Flow → Structured and Unstructured Flow as Libraries](../../control-flow.md#structured-and-unstructured-flow-as-libraries) | Depends_on — `:134`, that an organization governs its own flow constructs with its own tooling | None (read) |
| [Control Flow Model → Halt](../../docs/control-flow.md#halt) | Depends_on — the concept, its independence, and the collision at `:78` | None (read) |
| [Control Flow Model → The names to use and the names to refuse](../../docs/control-flow.md#the-names-to-use-and-the-names-to-refuse) | Depends_on — `:129` for `Halt`, `:131` for the refused `panic` and `Recover` | None (read) |
| [modules/process/control-flow/README.md](../../README.md) | Member — the module's own README, which names the protocol contract its declarations realize | Cross-reference, do not duplicate |
| [modules/process/control-flow/rules/README.md](../README.md) | Catalog index | Created this session |
| [`modules/computer/runtime/thread/protocol/thread.kh`](../../../../computer/runtime/thread/protocol/thread.kh) | Record — the repository's own statement of the distinction, at `:29`; not evidence for the Rule | None (read) |
| This folder's `README.md` | Convention debt | Not created — a folder of peers has no main document, so its README is a real file; a rule folder that did have one would take a symlink, which is a git operation this session may not perform |

## Notes
- Every `.kh` line and every protocol line the Rule names was read at the line it names. The `.kh` lines are named as record of the repository's state and are the ground of no claim in the Rule, per the owner's standing that the code under `modules/**` is residue and neither evidence nor a premise.
- Files this session wrote: `modules/process/control-flow/rules/README.md`, this folder, the relocated [`disregarded-error.md`](../../../error/rules/disregarded-error/disregarded-error.md) and its handoff, the Khayyam catalog index, [`bundles/khayyam/rules/scope-visibility/`](../../../../../bundles/khayyam/rules/scope-visibility/), the placement criterion in [`modules/process/rule/rule.md`](../../../rule/rule.md), and the four files under `bundles/khayyam/targets/js/` whose links into the relocated Rule were repaired. No git command of any kind was run and no test suite was executed.

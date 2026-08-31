---
Title: "Khayyam Runtime Specification (Reference Architecture)"
Status: Proposed
Start Date: 2026-06-26
ID: 495120
---

# Khayyam Runtime Specification (Reference Architecture)
*Note: Khayyam is a syntax and a set of architectural rules. It does not dictate a specific runtime. However, this document outlines the Memar runtime architecture (the Memar Framework) designed to maximize Khayyam's potential, particularly for high-performance and Unikernel/Exokernel environments.*

This document is addressed to the developers of a Khayyam runtime — specifically the Memar Framework's — not to the Khayyam language. Nothing here adds to, restricts, or amends Khayyam's syntax or semantics; every requirement below is a recommendation about how Khayyam's own thinking — explicit, predictable behavior over hidden runtime magic, and governance over syntactic dictatorship — should find concrete manifestation in the execution layer the framework provides.

## Abstract
Khayyam does not dictate a runtime; this document is a reference architecture — the Memar Framework — one concrete answer to what a runtime built to maximize Khayyam's potential looks like, particularly for high-performance and Unikernel/Exokernel environments. It states two runtime-side commitments: the concurrency model is delegated entirely to user-space runtime libraries (scheduling, synchronization primitives as swappable capsules, core-pinning for lock-free design) rather than hardcoded into a language core; and the default deployment model is Immutable Infrastructure, with runtime code mutation existing only as an `unsafe`, opt-in escape hatch. Both commitments are requirements on an *implementation*, never on the language: a Khayyam program remains valid — and a different runtime remains permitted — regardless of what the Memar Framework chooses here.

## Introduction

### Motivation
Traditional languages hardcode concurrency primitives (like `channels` or `mutexes`) and black-box schedulers into the language core. That is a language-level decision, and Khayyam declines to make it; but declining alone leaves the runtime side unanchored — a runtime built carelessly could reintroduce through hidden machinery exactly the opacity Khayyam's syntax removes: implicit scheduling decisions, synchronization that appears from nowhere, execution behavior a reader cannot predict from source.

The runtime is the last layer where such magic could quietly return, because it is the layer furthest from the source a reader reads. This document exists to hold that line on the implementation side: it records, for the runtime's own developers, which behaviors MUST remain swappable library decisions, which performance mechanisms the framework commits to providing, and why runtime code mutation stays outside the default path. A runtime implementer who has read it should never need to re-derive, from the language specification alone, how Khayyam's philosophy constrains an execution layer that the language itself deliberately does not specify.

## Explanation

### Concurrency and Execution Model
Unlike traditional languages that hardcode concurrency primitives (like `channels` or `mutexes`) and black-box schedulers into the language core, the Khayyam ecosystem delegates these entirely to the runtime library.

* **User-Space Scheduling:** Thread management, yielding, and context switching are handled by user-space schedulers provided by the framework. This eliminates the overhead of kernel-level context switches.
* **Library-Driven Primitives:** Synchronization tools (Channels, Mutexes, WaitGroups) are capsules (libraries) rather than syntax keywords. This allows developers to swap, rewrite, or bypass them entirely based on domain needs.
* **Core Affinity & Lock-Free Design:** The runtime framework MUST provide mechanisms to pin specific tasks (e.g., handling TCP packets for a specific IP/Port pair) to dedicated CPU cores. This empowers developers to achieve true lock-free concurrency, entirely avoiding the performance penalties of `mutexes` for isolated state mutations.

#### Discussion

##### Drawbacks
Library-driven synchronization means there is no single, universally-optimized primitive: a swapped-in custom primitive carries none of the battle-testing a language builtin would have accumulated, and composing user-space schedulers with blocking syscalls (file I/O, network) remains a genuine engineering problem each deployment must solve. Kernel-free context switching also shifts correctness responsibility — preemption points, fairness, starvation — from an OS onto framework code that application authors can replace.

##### Rationale and alternatives
- **Build channels/mutexes/async-await into a Khayyam core (rejected):** hardcodes one concurrency paradigm into the grammar — the same coupling Khayyam declines for control flow, applied to scheduling. It would also make primitive behavior invisible: a keyword-synchronized operation reads as atomic without revealing its cost or its failure modes.
- **Delegate to the OS kernel's scheduler (rejected as the default):** kernel context switches are the overhead this model exists to avoid, and kernel scheduling policies are neither swappable nor inspectable from source — a black-box dependency in the exact layer Khayyam requires to be explicit.
- **User-space framework ownership (chosen):** scheduling and synchronization become ordinary capsules — visible in imports, swappable per domain, and governable by linter policy like any other library decision.

##### Prior art
Erlang/BEAM and Go's runtime are the closest precedents for user-space scheduling with language-level integration; Go is the cautionary half of the comparison — its channels and scheduler are exceptional engineering, but permanently privileged, which is precisely the coupling Khayyam refuses. Seastar (the ScyllaDB framework) is the closest precedent for the core-affinity/lock-free model: shared-nothing, pin-per-core task ownership at framework level, below the language. Unikernel systems (MirageOS, IncludeOS) demonstrate the deployment end of the same philosophy — the runtime is the application's actual operating environment, not a guest above someone else's scheduler.

##### Unresolved questions
The interaction model between user-space scheduling and unavoidable kernel boundaries — how a pinned task blocks on file I/O without stalling its core's run queue — is not yet specified, and is the most likely place this model leaks complexity to application developers.

### Change Logic in Runtime (Unsafe)
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)

> **Relation to Immutable Infrastructure:** The Memar framework's Immutable Infrastructure principle (“no runtime addition of capability without recompilation; every capability increase requires a rebuild” — see [khayyam-polymorphism.md#dynamic-dispatch-reducibility-under-immutable-infrastructure](./khayyam-polymorphism.md#dynamic-dispatch-reducibility-under-immutable-infrastructure)) describes the *default, safe* deployment model. The `unsafe` runtime patching described here is an *explicit, opt-in escape hatch* — not the default path — comparable to WASM module replacement. It does not contradict the principle; it is the controlled violation that the principle warns must be tagged, audited, and never used for normal capability evolution.

#### Discussion

##### Rationale and alternatives
- **Make runtime module replacement a first-class, always-available capability (rejected)**: would contradict Immutable Infrastructure as the default deployment model — no runtime addition of capability without recompilation — and normalize the uncontrolled capability evolution that principle exists to prevent.
- **Omit the capability entirely (rejected)**: microservice-style module turnover has genuine uses; removing it entirely would push adopters toward out-of-band binary manipulation with no audit story at all.
- **Keep it opt-in and tagged `unsafe` (chosen)**: the capability exists, is visibly dangerous at the call site, and sits outside the normal path — the same shape as the [compiler-side resolution](./khayyam-compiler.md#change-logic-in-runtime-unsafe) of this topic.

##### Prior art
WebAssembly's module add/remove at runtime is the design the text itself names. Erlang/OTP's hot code loading shows runtime replacement can be industrialized — but only behind significant surrounding machinery (supervision trees, versioned state-transition code), evidence that the feature is legitimate yet never free; the machinery is the runtime's concern, not the language's.

##### Unresolved questions
What the `unsafe` tag concretely gates at the runtime layer — an API surface requiring explicit enablement, a linter/compiler cooperation, or both — and how a module replacement is audited, are not yet specified.

## Results
No observed results are recorded yet. This section will be updated when the Memar Framework's execution model is exercised in real deployments and yields evidence that can be distinguished from its intended rationale.

## Discussion

### Drawbacks
This document specifies a reference architecture for a runtime that does not yet exist in implemented form: its MUST-level commitments (core pinning, user-space scheduling) are currently enforced only by review against this document, not by shipped, measured behavior. It is also deliberately one-runtime opinionated — a reader might mistake the Memar Framework's choices for Khayyam's requirements, when Khayyam itself remains runtime-agnostic; the opening note exists to prevent exactly that reading, and the boundary between the two is still being worked out (see Unresolved questions).

### Rationale and alternatives
- **Declare no runtime document at all (rejected)**: Khayyam genuinely does not dictate a runtime — but leaving the execution layer entirely unspecified hands the last, least-visible layer of the stack to whoever implements it first, with no record of how the framework is expected to honor the philosophy. The magic-prevention argument that justifies keeping the compiler out of the language applies equally here, one layer down.
- **Elevate this document to "the Khayyam runtime" (rejected)**: would convert a reference architecture into a de-facto language requirement, contradicting the runtime-agnostic stance the document itself opens with. Its Status and framing remain that of one framework's design, consumable and replaceable.
- **Fold runtime concerns into [Khayyam](./khayyam.md) (rejected)**: Khayyam's own Methodology keeps that document a short overview linking outward; execution-layer detail there would couple language evolution to framework implementation choices.

### Prior art
The runtime-as-separate-specification pattern is common in language ecosystems — Go's memory model and scheduler docs, the JVM specification, Erlang/OTP's design principles — each documenting execution semantics the language grammar deliberately does not carry. This document follows that shape, with the Memar Framework in the role those projects' runtimes occupy, and Unikernel/Exokernel literature as the deployment-side tradition it targets.

### Unresolved questions
1. The precise boundary between "what Khayyam specifies" and "what a Khayyam implementation provides" — shared with [Khayyam's own Unresolved questions](./khayyam.md#discussion) — applies here with special force: which parts of this reference architecture, if any, should eventually be promoted into requirements any Khayyam runtime must meet (a conformance floor), versus remaining Memar-Framework-specific choices.

### Future possibilities
- A minimal conformance floor for any Khayyam runtime (what the language actually assumes from below, if anything), separating portable guarantees from Memar-Framework specifics.
- The scheduler/synchronization capsule contracts, specifying what a swappable primitive must satisfy to interoperate with the framework's scheduling — resolving the syscall-boundary question under [Concurrency and Execution Model](#concurrency-and-execution-model).

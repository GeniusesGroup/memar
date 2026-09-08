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

Library-driven synchronization means there is no single, universally-optimized primitive: a swapped-in custom primitive carries none of the battle-testing a language builtin would have accumulated, and composing user-space schedulers with blocking syscalls (file I/O, network) remains a genuine engineering problem each deployment must solve. Kernel-free context switching also shifts correctness responsibility — preemption points, fairness, starvation — from an OS onto framework code that application authors can replace.

### Change Logic in Runtime (Unsafe)
You can write code to change(add or remove) modules binary code in runtime. It is like `WASM` idea. It can be very dangerous feature and MUST tag as `unsafe`. It is useful to add or remove modules in microservice way but as describe by [this paper from google expert software developers](https://dl.acm.org/doi/pdf/10.1145/3593856.3595909)

> **Relation to Immutable Infrastructure:** The Memar framework's Immutable Infrastructure principle (“no runtime addition of capability without recompilation; every capability increase requires a rebuild” — see [khayyam-polymorphism.md#dynamic-dispatch-reducibility-under-immutable-infrastructure](./khayyam-polymorphism.md#dynamic-dispatch-reducibility-under-immutable-infrastructure)) describes the *default, safe* deployment model. The `unsafe` runtime patching described here is an *explicit, opt-in escape hatch* — not the default path — comparable to WASM module replacement. It does not contradict the principle; it is the controlled violation that the principle warns must be tagged, audited, and never used for normal capability evolution.

## Results
No observed results are recorded yet. This section will be updated when the Memar Framework's execution model is exercised in real deployments and yields evidence that can be distinguished from its intended rationale.

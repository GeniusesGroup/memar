---
Title: "Runtime"
Status: Draft
Start Date: 2026-06-26
ID: 495120
---

# Runtime

## Abstract
A **runtime** is the environment in which a system's already-established structure is exercised. It is execution time, not definition time — the site of instances, not of new structure ([Type → Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition)). The concept is not a language virtual machine: an operating system is a runtime for processes, a unikernel is a runtime for a single image, a WebAssembly host is a runtime for modules, a JavaScript engine is a runtime for scripts, and a language library that schedules work inside a process is one kind of runtime among these. This document is Memar's protocol for that environment: what a runtime is, what it must not establish, that boot and lifecycle are runtime-plus-compiler configuration rather than grammar, that concurrency mechanics are libraries the runtime hosts rather than language keywords (the substrate itself is owned by [Concurrency](./concurrency.md)), and that mutating a running artifact is an `unsafe` hatch, not the default path.

## Introduction

### Motivation
"Runtime" is routinely narrowed to "the language's VM" — Go's runtime, the JVM, a JavaScript engine — until every other execution environment has to be named something else. The narrowing hides the common contract: whatever is running a system's definition must not silently become a second place that definition is written. A language runtime that introduces hidden scheduling, a container host that rewrites the image's capabilities, and an OS that offers per-variable services the process did not name are the same failure at different scales.

The opposite failure is leaving the execution side unanchored because a language declined to hardcode `main`, channels, or a garbage collector. Declining is not a runtime protocol. Without one, each execution layer reintroduces through hidden machinery the opacity the language's grammar removed.

### Methodology
The type-level rule that structure is established at definition time and enters execution only through the artifact is owned by [Type](../type.md); this document states the execution-side consequence, not a second copy of that rule. User-space threading, channel-as-signal, and worker pooling are owned by [Concurrency](./concurrency.md) and are not restated here. Operating-system grants and the responsibility boundary are owned by [OS](./os.md). What remains is the environment-contract: what counts as a runtime, what it hosts, how a program becomes running, and where the `unsafe` hatch sits relative to the type-level default. Positions were first drafted as a Memar-framework reference architecture beside one language; they are stated here without that language as owner.

## Explanation

### What a runtime is
A runtime is the environment that takes a system's delivered artifact — a binary, a module, a process image, a script, a unikernel — and exercises the structure that artifact already carries. Selection among established alternatives (dispatch, branching, configuration values whose vocabulary is a defined type) is execution; minting a new capability, a new type, or a new constraint into the running instance is not. The runtime may be a language library, an OS, a hypervisor-adjacent image, a browser tab's engine, or a host that loads WebAssembly: the kind of host does not change the contract.

A language is not a runtime. A compiler is not a runtime. The [Compiler](./compiler.md) produces a target; the runtime is where that target runs. Several runtimes may run artifacts produced from one language; one runtime may run artifacts from several languages.

### A runtime does not establish structure
The default path is [Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition): a running system executes its definition and never establishes structure. Configuration that selects among compiled alternatives is execution. Inputs are data. Consuming another system's services through interfaces this system's definition already names is not structure acquisition. Any mechanism whose operation *establishes* this system's structure at execution time is a violation of the default path.

### Boot and lifecycle are configuration, not grammar
How an artifact becomes running — process entry, unikernel boot, WASM `_start`, a serverless handler, a host that calls an exported function — is a property of the chosen runtime and of [Compiler](./compiler.md) configuration, not of a language's grammar. A language that hardcodes `main` has collapsed this topic into syntax and must then grow new syntax when the environment changes. This protocol forbids that collapse as a requirement on runtimes and compilers, not as a requirement that every language delete `main` tomorrow: a realization for C may still *use* `main` as the C runtime's convention, which is exactly configuration-plus-runtime, not C's claim to own all boot.

### Concurrency is hosted, not defined, here
Scheduling, synchronization primitives, and the user-space substrate are [Concurrency](./concurrency.md)'s contract. A runtime *hosts* that substrate — it is one of the environments in which Workers run — and must not re-introduce kernel-thread-per-activity or channels-as-stores as if they were this document's invention. What this document adds is only the placement: those mechanics are libraries the runtime loads, not keywords a language core owns, and a runtime that hides scheduling decisions from the artifact's source is failing the explicitness the concurrency protocol already requires. Core-pinning and lock-free affinity are not this protocol's requirement; if they belong anywhere as a MUST, that is a [Concurrency](./concurrency.md) extension, not a runtime-definitional one.

### Mutating a running artifact is `unsafe`
A runtime may offer a way to add or remove modules' binary code while the system is running — the WASM module-replacement shape. The capability MUST be tagged `unsafe`. It is an explicit, opt-in escape hatch from the default in [Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition), comparable to replacing a WASM module, and it does not contradict the principle: it is the controlled violation that must be tagged, audited, and never used for normal capability evolution. [Immutable infrastructure](./immutable_infrastructure.md) owns the deployment-side working-out of the same principle.

---
Title: "Concurrency Realization"
Status: Draft
Start Date: 2026-09-06
ID: 496869
---

# Concurrency Realization

## Abstract
This document states how Memar realizes concurrency at the framework level. The *concept* — concurrency as a property of how a process's activities progress relative to each other, the escalating decision chain before any synchronization, the Worker/core distinction — is defined in [Process → Concurrency](../process.md#concurrency) and is not repeated here. This document covers the *realization* contract: the execution substrate a Memar system provides (user-space threads, not kernel-thread-per-activity), the synchronization and signaling primitives it exposes, and the rules their use must follow. The single most load-bearing rule: **signaling and data transport are different mechanisms, and a channel must not be used as both.**

## Introduction

### Motivation
The ecosystem's most-loved concurrency features are pleasant to *start* with and silent about *correct* use. Three specific patterns recur:

1. **Buffered channels carrying data.** A channel is used as a bounded data structure — buffers sized into the millions — and the failure arrives as apparent memory exhaustion, because the buffer's cost was invisible at the call site. A channel's internal buffer is a fixed-capacity ring with expensive per-element machinery; it is built for coordination, not for storing data.
2. **Thread-per-request at scale.** Per-request execution units spawned without a pool produce starvation under load (tens of thousands of in-flight units, tail latency collapse) — the well-understood reason high-performance servers use worker pools, rediscovered by each generation of applications the hard way.
3. **Kernel-space threading as the default substrate.** Systems that map every logical activity onto an OS thread inherit the kernel scheduler's costs (context switches, stack sizes, syscalls) for concurrency that is entirely logical; user-space threading — multiplexing many logical activities onto few kernel threads — is the entire point of the modern runtime designs, and treating it as optional re-pays the cost it exists to remove.

### Methodology
Positions were formed alongside [Memory](./memory.md) and [Networking](./networking.md)'s position on the traditional network stack, checked against a mainstream language's channel implementation source (read through its pre-generics era, where the ring-buffer machinery was directly visible) and against production-scale server experience. The concept-level treatment in [process.md](../process.md) is treated as given here; this document adds only what a framework must realize and constrain.

## Explanation

### The substrate: user-space threads
A Memar system's execution substrate multiplexes many logical activities (the framework's Workers, in process.md's terms) onto a small set of kernel threads. This is a stated requirement, not an implementation detail, because it determines what the framework's other guarantees cost: blocking operations, per-activity stacks, and scheduling are framework-managed rather than kernel-managed, which is what makes millions of lightweight activities feasible and makes the Worker model of [process.md](../process.md#concurrency) realizable without kernel-side configuration.

The requirement binds the framework's own libraries: an operation that would block a kernel thread (a socket read, a file operation, a lock wait) is either realized through the substrate's suspension mechanism or explicitly documented as substrate-hostile. A library that silently blocks its carrier thread degrades the whole system while appearing locally correct.

### Channels are signals, not stores
The channel primitive Memar exposes follows the coordination contract: a channel carries *signals* — occurrences that wake or hand off another activity. Its rules:

- A channel's buffer, where one exists, is sized for coordination tolerances (typically small; the common correct size is one), never for data retention.
- Data to be conveyed travels in the system's storage or explicit message structures; the channel notifies of its availability.
- A channel used to hold data — sized to the expected backlog — is a modeling error this framework treats as a defect, because the data's real requirements (persistence, observability, backpressure policy) are exactly the ones the channel cannot answer.

This rule is deliberately stricter than the ecosystem's, where buffered channels-as-queues are idiomatic; the rationale is the evidence above (invisible memory cost, no backpressure semantics, no observability) plus the storage-layer principle that data with retention requirements belongs to the components that own those requirements.

### Execution units are pooled, not spawned
Handling an incoming request does not spawn an execution unit per request. Units are drawn from the system's worker pool — sized by the system's own configuration ([Process → Requests, Cancellation, and Timeout](../process.md#requests-cancellation-and-timeout)'s budget rule applies: pool sizing is configuration owned by the executing system, not a per-request decision). The per-request-spawn pattern's failure mode (starvation, tail latency, unbounded memory under load) is why every mature server runtime converged on pools; the framework makes the converged answer the default rather than leaving each application to rediscover it.

A mainstream language's channel implementation (read through its pre-generics era) exposes the fixed-capacity ring buffer with per-element machinery directly in its source — the structural evidence that the primitive was built for coordination, not data retention. Worker pools are the converged answer of every high-performance server runtime — the premise the pooling rule above generalizes.

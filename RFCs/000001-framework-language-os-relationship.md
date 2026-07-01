---
RFC Number: 000001
Title: "The Relationship Between Framework, Language, and Operating System"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: []
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
The conventional hierarchy in software development places the framework as a guest living inside a language and operating system — the language defines what is expressible, the OS defines what is executable, and the framework merely organizes how developers use both. Memar inverts this: the **framework** is the primary architectural authority. The language and the operating system are components whose design assumptions are themselves defined by the framework, not the other way around.

## Motivation
When a framework is subordinate to a language and an OS, it inherits every assumption those layers baked in — often assumptions made decades ago for very different hardware, scale, and application models. A framework built inside Go must accept Go's concurrency model, Go's memory model, and Go's standard library conventions. A framework built on Linux must accept POSIX's process/thread model, its I/O abstractions, and its general-purpose kernel interface. These inherited assumptions are invisible until they become constraints, at which point they are very expensive to remove.

The deeper problem is that these layers were never designed with each other in mind at the architectural level. A language is typically designed to be OS-agnostic and framework-agnostic. An OS is typically designed to be language-agnostic. A framework, arriving last, is left to patch the gaps between whatever assumptions the first two happened to make independently. The result is a stack of layers that each hide complexity from the layer above — and where each layer's hidden complexity eventually leaks upward as surprising constraints, performance cliffs, or security surfaces.

Memar's position is that this ordering is historical accident, not architectural necessity. A framework that defines its own assumptions first — and then specifies what language and OS behavior it needs to support those assumptions — can maintain coherence across all three layers rather than inheriting incoherence from two independent prior decisions.

## Guide-level explanation
In Memar's model, a developer working on a business feature does not think about "which OS API to call" or "which language runtime to trust." They think about the domain model and the framework's contracts. The OS and the language are implementation details of those contracts — present, but not surfaced. This is the same thinking behind Unikernel architectures, where the application and the OS are compiled together into a single artifact with no general-purpose kernel in between: the application does not "call the OS," it is co-designed with the minimal substrate it actually needs.

Concretely, this means:
- The Khayyam language is not "Memar's language" in the sense that Memar is a framework for Khayyam. Khayyam is a language whose design assumptions are specified by Memar, so that code written in Khayyam already expresses the architectural constraints Memar cares about — explicit state, explicit error paths, no hidden control flow, no invisible allocations.
- An OS running Memar applications is not a general-purpose OS that Memar happens to run on. It is a substrate whose interface is defined by what Memar actually needs — no more. In a fully realized deployment, this means a Unikernel or Exokernel model, not a POSIX kernel offering thousands of syscalls that the application will never use.
- The Memar framework itself is not a library the developer downloads and links against a pre-existing language and OS. It is the primary artifact. The language and OS choices are consequences of the framework's requirements.

## Reference-level explanation
This RFC has no syntax or grammar implications — it is an architectural stance that shapes the design decisions made in every subsequent RFC. Specifically:
- It is the reason why control flow keywords, memory management, concurrency primitives, and standard library shapes are not baked into the Khayyam language itself but instead live in the Memar framework (RFC 000003, RFC 000008, RFC 000011).
- It is the reason why the framework's recommended toolchain (compiler, linter, scaffolding) is designed as a coherent unit rather than as independent tools that happen to be compatible.
- It is the reason why architectural constraints (e.g. "no hidden state," "every error path must be visible") are expressed as framework-level contracts rather than as optional conventions.

## Drawbacks
Inverting the conventional hierarchy means Memar cannot be adopted incrementally by adding it to an existing Go or Java or Rust codebase. The architectural assumptions are too different for a gradual migration to be coherent. This is an explicit trade-off: correctness and long-term sustainability of the design over short-term adoption convenience.

## Rationale and alternatives
The conventional model (framework lives inside language and OS) was rejected because it guarantees that the framework will eventually be constrained by assumptions it did not make and cannot change. The cost of that constraint compounds over time — each new capability the framework needs must be negotiated against what the language and OS already decided, rather than being specified from first principles. Memar's inversion accepts a higher initial cost (no incremental adoption, no reuse of existing language/OS tooling without design review) in exchange for eliminating that compounding constraint cost.

## Prior art
- **Unikernel projects** (MirageOS, IncludeOS, Nanos): the closest architectural parallel, specifically in their treatment of the OS as a consequence of the application's requirements rather than a given substrate.
- **Singularity (Microsoft Research)**: an OS research project that co-designed the language (Sing#) and the OS from shared first principles, rather than fitting a language onto an existing OS.
- **Erlang/BEAM**: a language+runtime that is, in practice, its own OS-like substrate — the BEAM VM defines process scheduling, memory isolation, and fault tolerance in ways that make the underlying OS largely irrelevant to application code.
- **General-purpose OS + framework combinations** (Spring Boot on JVM on Linux, Rails on Ruby on Linux): the conventional prior art being explicitly rejected, not because they are bad engineering for their context, but because their inherited-assumption problem is well-documented and the cost of navigating it is visible in every large codebase that has lived long enough.

## Unresolved questions
None at this time. This RFC is intentionally a statement of architectural stance, not a specification of a concrete mechanism — the concrete mechanisms flow from it in subsequent RFCs.

## Future possibilities
A formal specification of the minimal OS interface Memar applications actually require (the boundary between "what the framework needs from a substrate" and "what a substrate provides") would be the natural follow-up to this RFC at the OS-design layer.

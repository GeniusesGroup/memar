# Khayyam Migration Guide & Ecosystem Bootstrapping
Migrating libraries from traditional programming languages to Khayyam is not a painful rewrite, but rather a structured transition toward extreme clarity. Khayyam replaces implicit compiler magic and primitive types with explicit, self-documenting abstractions.

This document outlines the mechanical complexity of porting code to Khayyam, the strategy for ecosystem bootstrapping, and the architectural benefits of this migration.

## Language Porting Complexity Matrix
With the aid of the Khayyam Transpiler, the mechanical difficulty of porting (rated from 1 to 20) is significantly lower than manual rewriting.

| Source Language        | Paradigm Match             | Memory Translation        | Difficulty (1-20) |
| :--------------------- | :------------------------- | :------------------------ | :---------------- |
| **Assembly (via FFI)** | Native                     | Explicit                  | **2**             |
| **C**                  | Low (Procedural)           | Malloc to ADT Allocators  | **6**             |
| **Zig**                | High (Explicit allocation) | Manual to ADT Allocators  | **6**             |
| **Go**                 | Medium (Interfaces)        | GC to Explicit Allocators | **8**             |
| **TypeScript**         | Medium (Structural)        | GC to Explicit Allocators | **8**             |
| **Rust**               | Medium (Traits)            | Borrow Checker to Linter  | **10**            |
| **C++**                | Low (Templates)            | RAII to `Deinit` & ADTs   | **10**            |
| **Python / JS**        | Low (Dynamic)              | GC to Explicit Allocators | **14**            |

## The Architectural Gains of Migration
Porting to Khayyam is not just a syntax translation; it is an upgrade to your codebase's maintainability.

### 1. Self-Documenting Code by Default (No Magic Numbers)
In traditional languages, developers often write raw formulas like `if a == b + 1` and rely on comments to explain what `1` means. Khayyam forces developers to eliminate magic numbers. By declaring an explicit variable for `1` with a descriptive name before using it in a method call, the code becomes inherently self-documenting, eliminating the need for redundant comments.

### 2. The Simplicity of "De-Primitive-ing"
Replacing primitives is a mechanical, zero-cost task. A traditional `int32` is simply mapped to Khayyam's `W32` capsule. The developer only needs a single `tp ... in ...` declaration at the top of the file to import the correct behavior, unifying the type system without adding complexity.

### 3. Explicit Memory Sovereignty
Khayyam removes hidden Garbage Collection overhead. Migrated libraries must assign lifecycles explicitly via Memory ADTs (e.g., Arenas, Pools). This makes resource utilization 100% predictable.

---

## Ecosystem Bootstrapping Strategy
To rapidly build the Khayyam and Memar framework ecosystem, the community employs a dual-track strategy:

* **The Transpiler Approach:** An automated Transpiler will be developed to mechanically convert legacy codebases (like C or Go networking and crypto libraries) into valid Khayyam ASTs. This allows rapid onboarding of battle-tested algorithms.
* **Native AI-Assisted Development:** Simultaneously, core standard libraries will be developed purely in Khayyam from scratch. By leveraging AI models and deep developer collaboration, these native libraries will perfectly embody the Khayyam architecture, setting the gold standard for the ecosystem.
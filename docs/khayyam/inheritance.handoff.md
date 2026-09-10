# Inheritance in Khayyam Handoff

Open work for `inheritance.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Design Pattern Catalog
What is the complete catalog of OO design patterns that rely on behavior transfer, and what are the Khayyam equivalents for each? A dedicated document may be needed to guide developers migrating from OO languages.

### Performance Benchmarking of Explicit Delegation
What is the actual runtime performance impact of explicit delegation compared to behavior-transfer-based dispatch? Early evidence from Zig and similar systems suggests the overhead is negligible, but formal benchmarking is needed.

### Code Generation Standards
What are the standards for AI or tooling-generated delegation code? Should generated code be marked with specific annotations? Should there be a standard directory or naming convention for generated files?

### Abstraction Inclusion Depth
How deep can abstraction inclusion chains go (abstraction A includes B includes C)? Is there a practical limit, and does it introduce any of the visibility problems that behavior transfer creates? The current position is that inclusion depth is not inherently problematic because no behavior is transferred.

## Anticipated Work

- **AI-Assisted Delegation Scaffolding:** The linter and IDE tooling could automatically generate explicit delegation methods when a developer composes capsules, reducing the boilerplate of explicit delegation while preserving source-level visibility.
- **Delegation Pattern Library:** A standard library of common delegation patterns (forwarding, adapting, decorating, intercepting) that developers can use as templates for explicit delegation.
- **Ownership Visualization:** IDE tooling that visualizes the explicit delegation graph for a capsule, showing which methods are native and which delegate to embedded capsules. This would provide the "overview" benefit of hierarchies without the hidden behavior.
- **Formal Proof of Completeness:** A formal argument that explicit delegation can express every relationship that behavior transfer can express, with examples demonstrating the translation. This would address the concern that some patterns are "impossible" without behavior transfer.

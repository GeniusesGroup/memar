---
RFC Number: 000017
Title: "Rejection of Default Implementations (No Trait Default Methods)"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002", "000007"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam rejects "Default Implementations" or default trait methods (as in Rust or Java interfaces). An abstraction (`ab`) is a pure contract with no executable logic of its own. Shared behavior across multiple capsules must use Explicit Delegation through internal capsules, not implicit code inherited from a trait.

## Motivation
Allowing executable logic inside an abstraction violates its contractual purity and introduces implicit, dynamic routing behavior that clouds compile-time optimization and hardware transparency — an abstraction should describe *what* is required, never silently supply *how*.

## Guide-level explanation
If several capsules need to share common behavior (e.g. a default "presence check" implementation reused by multiple types implementing the same abstraction), each capsule explicitly delegates to a shared internal capsule that actually implements the behavior — a one-line delegation call is written in each implementing capsule's method body, rather than the behavior being silently inherited from the abstraction itself.

## Reference-level explanation
- Abstractions (`ab`) contain no method bodies — only contracts.
- Shared logic lives in an ordinary capsule, referenced explicitly via delegation from each implementer.
- Boilerplate elimination for this delegation pattern is strictly offloaded to organizational Linter and Scaffolding tooling (which can verify the delegation call exists and even auto-generate it), ensuring the final source remains 100% explicit, linear, and free of compiler magic.

## Drawbacks
Every capsule implementing a shared-behavior abstraction must carry its own explicit delegation line, rather than inheriting the behavior automatically — this is deliberate, visible boilerplate, repeated across every implementer, in place of inheritance.

## Rationale and alternatives
Default trait methods (Rust, Java's `default` interface methods) were rejected because they let an abstraction silently provide behavior, which both violates the "abstraction as pure contract" principle and reintroduces a form of implicit code execution at a point where the language elsewhere strives for total explicitness (RFC 0002, RFC 0005).

## Prior art
Rust traits and Java 8+ interface default methods are the direct prior art being explicitly rejected here. Go's interfaces (which, like Khayyam's abstractions, carry no default implementations at all) are closer in spirit to this design.

## Unresolved questions
The exact mechanism for "Explicit Delegation Verification" by the Linter/Scaffolding tooling — how it recognizes a valid delegation call versus a hand-written duplicate implementation — is not yet specified in detail.

## Future possibilities
None recorded yet.

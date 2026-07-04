---
RFC Number: 0000
Title: "Containers, Generics Elimination, and Rich Domain Models"
Status: Proposed
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000002"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam has no generic syntax (`List<T>`, `[T]`) and no method overloading. Type-safe, polymorphic behavior is achieved instead via interface-based abstraction and domain-specific intermediate capsules (e.g. `ConnectionList` instead of `List<Connection>`), generated/scaffolded as needed rather than expressed generically.

## Motivation
Generic collections create an illusion of correctness: domain logic that must live inside the container (e.g. "no duplicate Service IDs in this list") gets pushed outside the encapsulated type into disconnected layers (controllers, random services) because the generic abstraction has no room for it — directly breaking encapsulation and producing "Anemic Domain Models." Generic syntax (`<T>`) also introduces parsing/readability overhead that conflicts with Khayyam's minimal-syntax philosophy.

## Guide-level explanation
Instead of a generic `List<Connection>`, a developer (or a code generator/AI assistant) defines an intermediate domain-specific capsule, `ConnectionList`, whose public methods strictly accept and return only `Connection` capsules, and whose internal validation rules (e.g. duplicate prevention) live directly inside its own methods (`ConnectionList.Add()`), exactly where that logic belongs. Where a method needs to accept any implementer of a shared behavior, it refers to the abstraction directly (e.g. `Index(el Element)` rather than `Index[T](el T)`).

## Reference-level explanation
- **No Method Overloading:** a method name must represent one clear, unambiguous intent.
- **Interface-based Polymorphism:** abstractions (`ab`) are referenced directly rather than parameterized generically.
- **Compiler-Driven Implementation:** whether a given abstraction usage is resolved via compile-time monomorphization/inlining or run-time dynamic dispatch is decided automatically by the compiler based on context, not chosen syntactically by the developer.
- **Domain-Specific Containers:** raw ADTs are not exposed directly to application logic; intermediate domain capsules (`ConnectionList`, `ServiceRegistry`) wrap them.
- **Linter-Enforced Type Safety:** because Khayyam has no type inference (variables must be explicitly typed) and relies on strict linters, passing an incorrect capsule type to a container method's `Add()` triggers an immediate linting error.
- The base ADTs (e.g. a raw hash map) act as plain "hosts" — they do not need generic syntax to know their "guest" element's identity; the guest capsule manages its own identity/memory rules.
- **Method overriding** (run-time polymorphism) is treated as inherently in tension with a language that does not provide a rich, generalized runtime — it is not separately supported beyond what interface-based dispatch already provides.

## Drawbacks
The cost of writing an intermediate domain-specific capsule for every container usage is real, ongoing engineering effort, even for cases that would otherwise be a single line of generic syntax (`List<Connection> connections;`) in another language. This is reframed in this RFC as "a fundamental investment in Clean Architecture," but it is still a genuine, non-trivial cost paid on every container use, not just complex ones.

## Rationale and alternatives
Adding generic syntax (the mainstream default) was rejected because it structurally permits domain logic to live outside the type it concerns, which conflicts with Khayyam's encapsulation principle (RFC 0002) more directly than almost any other common language feature.

## Prior art
Statically typed mainstream languages (Java, C#, Rust, Go since 1.18) all provide generics as a core mechanism for type-safe containers. Khayyam's approach is closer in spirit to a strict "wrapper type per use case" discipline sometimes manually adopted in DDD-heavy codebases as a best practice, here made the only available path.

## Unresolved questions
Whether scaffolded concrete container capsules (e.g. a generated `connection_list.kh`) are intended to be committed to version control or generated fresh on every build is not yet settled; this affects IDE/autocomplete behavior before a build has run. This is a tooling-level question, not a language-design question.

## Future possibilities
None recorded yet.

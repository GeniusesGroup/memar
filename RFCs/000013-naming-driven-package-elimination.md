---
RFC Number: 000013
Title: "Naming-Driven Package Elimination"
Status: Draft
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
Khayyam has no package-level encapsulation or global namespace concept. Producers (library authors) never define a package name; consumers include a file directly and assign it a local capsule name themselves via the `in` keyword (e.g. `tp JsonEncoder in "memar/codec/data_exchange/json/encode.kh"`).

## Motivation
Relying on packages tends to produce lazy naming (e.g. naming a method `Parent()` simply because it lives inside an `ast` package, relying on the package prefix to disambiguate) and eventually causes naming collisions across a codebase or ecosystem, since package names are a shared, contested global namespace.

## Guide-level explanation
Developers must write clear, fully self-explanatory names for capsules and methods — `Parent() T` is ambiguous and discouraged; `ParentCommand() Command` or `ParentElement() Element` is preferred, since this makes code readable without needing any package prefix for context. When a developer wants to use code from another file, they import that file directly and choose the local name themselves: `tp JsonEncoder in "memar/codec/data_exchange/json/encode.kh"`. Because the consumer — not the producer — controls the local scope and name, there is no central package registry to collide with.

## Reference-level explanation
- **Explicit Naming:** required for every capsule/method, since no package prefix will ever disambiguate it.
- **Consumer-Driven Inclusion:** the `in` keyword binds a file's contents to a locally chosen name; producers do not declare or reserve any name on the consumer's behalf.

## Drawbacks
Without any package-level grouping, every imported file's contents must be named individually and explicitly by every consumer, which removes the convenience of a package prefix automatically scoping a whole family of related names together. This places the entire disambiguation burden on naming discipline rather than the namespace system.

## Rationale and alternatives
Conventional package/namespace systems were rejected because they encourage context-dependent, prefix-reliant naming (the `Parent()` example) and introduce a shared global namespace as a potential collision surface — both in tension with Khayyam's broader explicitness principles (RFC 0002, RFC 0007).

## Prior art
Go and Java both rely heavily on packages for both organization and disambiguation. Khayyam's consumer-driven inclusion model is closer in spirit to ES module imports with explicit local aliasing (`import { encode as jsonEncode } from "..."`), but goes further by never having a producer-defined export name to alias *from* in the first place.

## Unresolved questions
The rationale source material also describes a hypothetical, exploratory `im` keyword (`tp {name} im {addr}`) for importing an entire file under one local name (e.g. `jsonEncode.Encoder`), distinct from `in`. This was clarified during design discussion as an illustrative/exploratory mention only, not a committed second keyword alongside `in` — it should not be read as confirming two parallel import mechanisms exist. Whether a second import form is actually needed (versus `in` alone covering both "import a specific named entity" and "import a whole file under a local name") remains genuinely undecided and should be resolved before this RFC can move to Final status.

## Future possibilities
None recorded yet.

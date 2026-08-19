---
Title: "Modularity in Khayyam"
Status: Draft
Start Date: 2026-07-29
ID: 495930
---

# Modularity in Khayyam

## Abstract
This document specifies how Khayyam represents and resolves modular relationships without making a storage, distribution, or package-management mechanism part of the language grammar. The architectural definition of a Module — a System under a modular boundary, identified by coherent responsibility and explicit relationships — belongs to [Modularity](./modularity.md). Khayyam applies that definition at the language and ecosystem layers: `in` includes named entities from a file; explicit names carry their meaning without package prefixes; and dependency location, version selection, integrity, and caching remain framework or tooling responsibilities. A companion manifest is the proposed location for the latter concerns, but its format and resolution algorithm are not yet specified.

## Introduction

### Motivation
Programming languages often couple three independently changing concerns: the language mechanism that refers to code, the logical Module that owns a responsibility, and the ecosystem mechanism that finds, versions, distributes, and verifies source. A repository move, package-manager change, or distribution change can then force source-level or language-level change even though the responsible Module has not changed.

Khayyam separates those concerns. The language needs a small, explicit way to include a named entity from another file. It does not need to define repository identity, network transport, registry policy, dependency-version selection, or authentication. These are real needs, but they belong to the framework and tooling layer, where they can evolve independently of the grammar.

### Ecosystem Coupling
The issue is not that package-oriented ecosystems fail to solve practical problems. It is that they commonly make one representation carry several meanings at once. The comparison below identifies the coupling Khayyam avoids; it does not treat any ecosystem as generally inferior.

| Language / ecosystem | Concerns coupled to the programming model | Long-term consequence |
| --- | --- | --- |
| C / C++ | Physical file layout through `#include` | Logical inclusion depends directly on filesystem organization. |
| Java | Package hierarchy and directory structure | Namespace, storage layout, and module identity become tightly coupled. |
| C# / .NET | Namespaces, assemblies, and project structure | Several partially overlapping concepts determine a modular boundary through tooling conventions. |
| Go | Repository location, module identity, and dependency resolution | Import paths encode distribution details, so changes in hosting or dependency policy affect source code. |
| Rust | Cargo package model | The package manager strongly shapes the language's modular structure, making alternative module ecosystems harder to introduce. |
| JavaScript / Node.js | npm package resolution | Distribution conventions strongly influence module identity in the programming model. |

Programming-language grammar, package-management policy, repository hosting, and distribution mechanisms evolve at different rates. A design that combines them turns ordinary ecosystem evolution into pressure for language evolution. Khayyam's separation is intended to preserve a stable inclusion grammar while leaving its surrounding ecosystem replaceable.

### Relationship to Modularity
[Modularity](./modularity.md) is the authoritative conceptual document for Module identity, responsibility, boundaries, relationships, optional Modules, and the distinction between modularity and its physical representations. This document does not redefine any of those concepts. It records only the consequence for Khayyam: file paths, directories, repositories, packages, manifests, and deployment artifacts may represent or help resolve a Module, but none is the language-level definition of one.

### Methodology
The decisions in this document are derived by first modeling the concepts required for modular software construction independently of a programming language, operating system, file system, package manager, repository layout, or development tool. Existing languages and ecosystems are then examined as implementations rather than authorities: the analysis asks which concepts they represent accurately, which concerns they couple unnecessarily, and which implementation constraints shaped their architecture.

This methodology is shared with the broader conceptual work in [Modularity](./modularity.md), but it remains material here because it governs how Khayyam-specific language constructs are evaluated. The language syntax is a consequence of the model — in this case, the separation of source inclusion from distribution and resolution — rather than the starting point that determines the model.

## Explanation

### Inclusion Is Not Module Definition
Khayyam uses `in` as a routing operator for including named Types and Variables from another file:

```khayyam
tp TcpConn in "net/tcp"
vr MaxTimeout in "net/config"
```

This syntax makes a source-level dependency explicit. It does not assert that a file is a Module, that a directory is a package, or that a path identifies a versioned distribution artifact. Those are separate representations and resolution concerns. Keeping `in` limited to inclusion prevents the grammar from acquiring rules about hosting, registries, versions, transport protocols, or organizational layout.

### Naming Without Package Context
Khayyam has no package-level namespace or package-level encapsulation. A name must therefore state its own domain meaning rather than relying on a package prefix to supply the missing context. `Parent()` is ambiguous when seen alone; `ParentCommand()` or `ParentElement()` communicates the intended concept directly.

This is not a claim that names never collide or that a file path is irrelevant to reading code. It is a rule about where meaning must be carried: a package prefix must not be the only explanation of an otherwise vague name. The `in` declaration identifies the source of an included entity, while the entity's own name remains responsible for expressing what it is.

#### Discussion

##### Drawbacks
Without package-level grouping, code cannot rely on a package prefix to make a family of vague names readable. This increases the naming discipline required of every Type and Method and can make migration from package-oriented codebases feel more verbose.

##### Rationale and alternatives
Conventional package and namespace systems were rejected as the language's primary source of semantic context because they encourage prefix-reliant naming and couple a logical grouping mechanism to source organization. Khayyam instead requires meaningful entity names and uses `in` only to make the source dependency explicit.

The practical concern is not merely aesthetic. A package can make `Parent()` appear adequate only because a reader is expected to supply the package context mentally. That context can be absent in review, search results, generated documentation, or an AI-assisted analysis. `ParentCommand()` and `ParentElement()` preserve the distinction in the entity name itself.

##### Prior art
Go and Java rely on packages for organization and disambiguation. ES-module imports demonstrate one useful part of the alternative: an explicit import identifies where a dependency comes from without making a global package hierarchy the sole carrier of meaning. Khayyam applies the stronger requirement that the included entity's own name must remain meaningful without depending on such a prefix.

##### Unresolved questions
Earlier design material mentioned a hypothetical `im` keyword (`tp {name} im {address}`) for including an entire file under one local name, such as `jsonEncode.Encoder`. It was exploratory, not a commitment to a second import mechanism. Whether `in` alone can cover both inclusion of a named entity and any future whole-file inclusion need remains unresolved.

### Dependency Resolution and Companion Manifest
An `in` address is a source-level path, not a network locator or a version declaration. Consequently, version selection, source discovery, integrity verification, caching, and conflict resolution do not belong in the `in` grammar.

The need for a resolution layer remains real even when Khayyam does not offer it as language syntax. For example, two parts of a project can require different versions of the same imported source, and a build can require integrity verification through pinning or hashes. The question is therefore where this work belongs, not whether it exists. The answer proposed here is the framework and tooling layer.

The preferred direction is a companion manifest at the framework/tooling layer. It may resolve import roots such as `memar/` to concrete source locations and versions or hashes, while leaving the source syntax unchanged:

```khayyam
tp TcpConn in "memar/net/tcp"
```

### Manifest as the Module Contract
The manifest is not merely a dependency file. It is the formal external contract through which a Module can be identified, referenced, validated, and consumed without inspecting its internal directory layout. It describes the Module's published surface and the conditions under which external tooling resolves it. Dependency resolution is one responsibility derived from this contract, not the whole of it.

This does not make the manifest the ontological definition of Module: [Modularity](./modularity.md) defines a Module through its coherent responsibility, boundaries, and relationships. The manifest is the framework-level representation of those aspects that consumers and tools need to discover and use. A change in manifest syntax, storage, or resolver must not change the Module's conceptual identity.

The following model is a directional content model, not yet a settled manifest schema:

```text
Manifest
│
├── Identity
├── Entry Points
├── Public Contracts
├── Dependencies
├── Version Constraints
├── Integrity
├── Resolution Rules
├── Capabilities
├── Compatibility
└── Metadata
```

Different build systems, package managers, deployment environments, and organizational infrastructures may interpret this contract differently without requiring any change to Khayyam grammar. This separation allows the language and its ecosystem to evolve independently while retaining a stable, inspectable module-facing contract.

Two locations for version information were considered:

1. **Embed it in the `in` address.** Rejected: it imports a distribution and versioning concern into language syntax and makes source code depend on external resolution conventions.
2. **Resolve it through a companion manifest.** Preferred: it keeps the grammar stable while allowing framework tooling to evolve its source-location, versioning, and integrity policies independently.

#### Discussion

##### Drawbacks
Until a manifest format and resolver exist, the design identifies the correct responsibility boundary without answering operational cases such as conflicting version requirements, offline cache policy, or integrity failure handling.

The manifest can also become an accidental second language if it absorbs concepts that ought to stay in Khayyam's grammar, or if it is treated as the Module's definition instead of as its external representation. Its eventual schema must preserve the boundary stated here.

##### Rationale and alternatives
Encoding source location or version information directly in an `in` address was rejected because it makes an ecosystem convention a permanent part of the language grammar. A companion manifest keeps that policy external, allowing different build systems, package managers, deployment environments, and organizations to interpret or replace it without changing Khayyam syntax.

Treating a manifest as only a dependency lock file was also rejected. Consumers need more than a resolved source location: they need a stable way to discover a Module's identity, entry points, published contracts, capabilities, compatibility conditions, and integrity information. Conversely, treating a manifest as the Module itself was rejected because the conceptual Module exists independently of whichever representation a particular toolchain uses.

##### Prior art
Go's `go.mod`, Node's `package.json` and lock files, and Rust's `Cargo.toml` and `Cargo.lock` all place significant dependency-resolution data beside source code rather than inside their languages' import grammar. Khayyam follows the companion-manifest direction while avoiding source-level import strings that encode a distribution location or version.

##### Unresolved questions
The manifest format; the exact resolution algorithm; resolution of the `memar/` prefix; multi-version conflict policy; supply-chain integrity mechanisms such as pinning or hashing; and the authoritative meaning of each proposed manifest field remain out of scope and undecided.

##### Future possibilities
A dedicated document can specify the manifest format, resolution algorithm, integrity model, and compatibility policy once the directional decision to keep them outside the `in` grammar is confirmed.

## Results
No observed results are recorded yet. This section will be updated when use of the language and tooling boundary yields evidence that can be distinguished from its intended rationale.

## Discussion

### Drawbacks
The separation creates an intentional two-layer reading task: a developer must understand both Khayyam's simple inclusion grammar and the relevant framework's resolution policy. It also postpones concrete tooling ergonomics until the manifest and resolver are specified. This cost is accepted because combining the two layers would make changes in distribution policy changes to the language itself.

### Rationale and alternatives
Khayyam does not define modularity through files, directories, repositories, packages, or manifests; [Modularity](./modularity.md) establishes why none of these representations can define Module. Nor does it embed dependency-management policy in `in`. The language's responsibility is explicit inclusion of source-level entities; ecosystem tooling's responsibility is selecting and validating the corresponding source.

### Prior art
The comparison with package-centric ecosystems is not evidence that their designs are incorrect. They solve practical engineering problems. It illustrates a different boundary choice: Khayyam refuses to make the current solution for source distribution part of the programming-language model.

### Unresolved questions
1. Is a whole-file inclusion form beyond `in` genuinely needed?
2. What manifest schema and resolver model can support versioning and integrity without creating a second, hidden language-level module system?
3. Which resolution policies are foundational framework law, and which are pluggable organizational rules?

### Future possibilities
Once a manifest and resolver are designed, their document should define the framework/tooling contract and link back here for the language boundary, rather than extending `in` with distribution policy.

---
Title: "Modularity in Khayyam"
Status: Draft
Start Date: "2026-07-29"
ID: "495930"
Applied to: []
Citations:
    - Title: "Khayyam - Programming Language"
      URI: "./Khayyam.md"
      Relation: "Reference"
      Reason: "The canonical specification defines the `in` subtype."
    - Title: "Encapsulation in Khayyam"
      URI: "./khayyam-encapsulation.md"
      Relation: "Depends_on"
      Reason: ""
Contributors:
  - Name: "Omid Hekayati"
    URI: "mailto:omid@geniuses.group"
    Tasks:
      - Works: ["Original design decisions for <modular programming>"]
        URI: ""
  - Name: "ChatGPT"
    URI: "https://openai.com"
    Model: "GPT-5.5"
    Tasks:
      - Works: ["Argumentation", "Argued for and against alternatives; incorporated revisions."]
        URI: ""
---

# Modularity in Khayyam

## Abstract
[Modular programming](https://en.wikipedia.org/wiki/Modular_programming) is a programming paradigm that emphasizes organizing the functions of a codebase into independent modules, each providing an aspect of a computer program in its entirety without providing other aspects.

## Introduction

### Motivation
One of the recurring problems in modern modular programming is the gradual migration of ecosystem concerns into programming language semantics. A programming language should define how software components are expressed, referenced, and composed. It should not define where those components are stored, how they are distributed, which transport protocol retrieves them, how versions are resolved, or how packages are authenticated. These concerns belong to the surrounding ecosystem. Once they become part of the language itself, they become extremely difficult to evolve independently. The history of modern programming languages demonstrates that many modularity problems originate from coupling independent concerns that should have remained separate. The following table summarizes some common examples.

| Language / Ecosystem | Language Coupled To | Long-Term Consequence |
|----------------------|--------------------|-----------------------|
| C / C++ | Physical file layout (`#include`) | Logical modules become dependent on filesystem organization. |
| Java | Package hierarchy and directory structure | Namespace, storage layout, and module identity become tightly coupled. Refactoring physical organization becomes harder than necessary. |
| C# / .NET | Namespaces, assemblies, and project structure | Multiple concepts partially overlap, making modular boundaries depend on tooling conventions. |
| Go | Repository location, module identity, and dependency resolution | Import paths encode distribution details. Changes in hosting, repository organization, or dependency management affect source code. The language specification must evolve alongside ecosystem concerns. |
| Rust | Cargo package model | Cargo provides an excellent ecosystem, but the package manager effectively defines the language's modular structure. Alternative module ecosystems become significantly harder to introduce. |
| JavaScript / Node.js | npm package resolution | Package manager conventions become part of the programming model. Module identity is strongly influenced by distribution mechanisms rather than architectural contracts. |

None of these approaches are inherently "wrong." Most of them solve practical engineering problems successfully. The architectural concern is different. Each of these designs couples concepts that naturally evolve at different rates.
- Programming languages evolve slowly.
- Package managers evolve more rapidly.
- Repository hosting changes frequently.
- Distribution mechanisms continue to change as software ecosystems mature.

When these concerns become part of the language semantics, every ecosystem evolution places pressure on the language itself. Features originally introduced to solve distribution or dependency problems gradually become permanent language constructs, even though they are not fundamentally language concepts. Khayyam intentionally follows a different architectural direction. A module is defined by its contract rather than by its storage location. Its identity is independent of repositories, directories, package managers, hosting providers, or transport protocols. The responsibility of the language ends once it defines how modules are identified and composed. Questions such as:

- where a module is stored,
- how it is discovered,
- how it is downloaded,
- how versions are selected,
- how integrity is verified,
- how dependencies are cached,

are responsibilities of the surrounding software ecosystem rather than the language itself. For this reason, Khayyam introduces an explicit module manifest. The manifest is not simply a dependency file. It is the formal contract describing the module's identity, published capabilities, entry points, dependencies, compatibility requirements, and other metadata required by external tools. Different build systems, package managers, deployment environments, or organizational infrastructures may interpret this manifest differently without requiring any change to the language itself. This separation allows both the language and the surrounding ecosystem to evolve independently while preserving long-term architectural stability.

### Methodology
The decisions presented in this document were derived through a concept-first modeling methodology rather than by extending existing language designs. The process begins by identifying the fundamental concepts required for modular software construction independently of any programming language, operating system, file system, package manager, repository layout, or development tool. Once these concepts are modeled, existing programming languages and ecosystems are analyzed as real-world implementations rather than as authoritative references. Their designs are evaluated to understand which concepts they represent accurately, which concerns they couple unnecessarily, and which implementation constraints have influenced their architecture. The purpose of this analysis is not to reproduce existing solutions, but to distinguish fundamental concepts from implementation-specific decisions. Only after this separation are language constructs proposed. As a result, the language syntax is expected to emerge naturally from the conceptual model instead of becoming the starting point of the design.

## Explanation

### Modularity Is About Contracts, Not Storage
The essence of modular programming is not dividing source code into directories. It is defining explicit boundaries and contracts between independently evolving parts of a software system. Directories, repositories, packages, and archives are merely storage conventions. They should not become part of the language semantics.

### What Is a Module?
A module is not a directory. A directory is merely one possible storage mechanism. Likewise, a module is not a repository, a package, a namespace, or a versioned archive. Those are implementation concerns. A module is a logical unit that publishes a well-defined contract describing:
- what it provides,
- how it can be referenced,
- what dependencies it requires,
- and under which conditions those dependencies are resolved.

The physical layout of files is therefore independent from the logical identity of the module. Different storage systems may organize the same module differently without changing the module itself.

### Why a Manifest Instead of Direct Language Semantics?
Khayyam intentionally places module metadata in a manifest rather than embedding it into language syntax. This design follows a simple architectural principle:
> Software architecture should depend on explicit contracts, not on incidental storage conventions.

A manifest provides a stable contract describing a module without requiring the programming language to understand repository layouts, package registries, network protocols, or distribution strategies. As software ecosystems evolve, these external mechanisms may change repeatedly while the language itself remains unchanged. Separating these concerns reduces unnecessary coupling and allows independent evolution of both the language and its surrounding tooling ecosystem.

### Manifest as the Module Contract
The manifest is not merely a dependency file. It is the formal description of a module. A module should be understandable without inspecting its internal directory layout. The manifest provides the information required to identify, reference, validate, and consume the module. Dependency resolution is only one responsibility derived from this contract.

```
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

### Modules Are Not Directories
Directories exist because today's file systems require them. Nothing in the definition of a module depends on directories. A future storage mechanism may organize modules inside databases, object stores, content-addressable storage, or distributed repositories. The logical identity of a module must remain independent from its physical storage.

### Language Should Describe Modules, Not Distributions
A programming language should define how software components are composed. It should not define where they are downloaded from, how they are versioned, how they are authenticated, or how they are distributed. Those concerns belong to the surrounding ecosystem rather than the language itself.

### Naming-Driven Package Elimination
Khayyam has no package-level encapsulation or global namespace concept. Producers (library authors) never define a package name; consumers include a file directly and assign it a local capsule name themselves via the `in` keyword (e.g. `tp JsonEncoder in "memar/codec/data_exchange/json/encode.kh"`).

Developers must write clear, fully self-explanatory names for capsules and methods — `Parent() T` is ambiguous and discouraged; `ParentCommand() Command` or `ParentElement() Element` is preferred, since this makes code readable without needing any package prefix for context. When a developer wants to use code from another file, they import that file directly and choose the local name themselves: `tp JsonEncoder in "memar/codec/data_exchange/json/encode.kh"`. Because the consumer — not the producer — controls the local scope and name, there is no central package registry to collide with.

- **Explicit Naming:** required for every capsule/method, since no package prefix will ever disambiguate it.
- **Consumer-Driven Inclusion:** the `in` keyword binds a file's contents to a locally chosen name; producers do not declare or reserve any name on the consumer's behalf.

#### Motivation
Relying on packages tends to produce lazy naming (e.g. naming a method `Parent()` simply because it lives inside an `ast` package, relying on the package prefix to disambiguate) and eventually causes naming collisions across a codebase or ecosystem, since package names are a shared, contested global namespace.

#### Discussion

##### Drawbacks
Without any package-level grouping, every imported file's contents must be named individually and explicitly by every consumer, which removes the convenience of a package prefix automatically scoping a whole family of related names together. This places the entire disambiguation burden on naming discipline rather than the namespace system.

##### Rationale and alternatives
Conventional package/namespace systems were rejected because they encourage context-dependent, prefix-reliant naming (the `Parent()` example) and introduce a shared global namespace as a potential collision surface — both in tension with Khayyam's broader explicitness principles (RFC 0002, RFC 0007).

##### Prior art
Go and Java both rely heavily on packages for both organization and disambiguation. Khayyam's consumer-driven inclusion model is closer in spirit to ES module imports with explicit local aliasing (`import { encode as jsonEncode } from "..."`), but goes further by never having a producer-defined export name to alias *from* in the first place.

##### Unresolved questions
The rationale source material also describes a hypothetical, exploratory `im` keyword (`tp {name} im {addr}`) for importing an entire file under one local name (e.g. `jsonEncode.Encoder`), distinct from `in`. This was clarified during design discussion as an illustrative/exploratory mention only, not a committed second keyword alongside `in` — it should not be read as confirming two parallel import mechanisms exist. Whether a second import form is actually needed (versus `in` alone covering both "import a specific named entity" and "import a whole file under a local name") remains genuinely undecided and should be resolved before this RFC can move to Final status.

##### Future possibilities
None recorded yet.

### Dependency Resolution via File URI and Companion Manifest
Khayyam's `in`-based import resolves to a file-system-style path (e.g. `memar/net/tcp`), not a network/version-aware URI. Because plain File URI resolution (RFC 8089) has no concept of versioning, dependency/version resolution must be solved one layer up — by a framework-level tooling convention, most likely a companion manifest file placed alongside a module — rather than inside the language grammar itself.

A developer writes `in "memar/net/tcp"` exactly as today; nothing about the import syntax itself changes. Separately, somewhere outside the language grammar — most plausibly a manifest file living alongside a module, in the spirit of how a `go.mod` or `package.json` sits beside source code rather than inside it — a framework-level tool determines which actual source (and which version of it) the `memar/` prefix resolves to for a given build. This keeps the language's stated promise (`in` is a simple, file-system-style path, not a network protocol) fully intact, while still giving an answer to "which bytes get linked" at the tooling layer.

Two concrete mechanisms were considered for where version information should live:
1. **Encoding a version inside the import path itself** (e.g. a query-string-like extension to the `in` address, similar in spirit to an HTTP URI's query component). This was evaluated and is **not** the recommended direction, because it would import a foreign concept (version syntax) directly into the language grammar — the same objection already raised against Go's URL-shaped import paths.
2. **A companion manifest file alongside a module**, external to the language grammar entirely, responsible for resolving `memar/`-prefixed (and other) import roots to actual source locations and specific versions/hashes. This is the preferred direction, since it keeps the `in` keyword's grammar untouched and treats versioning purely as a build/tooling-layer concern, consistent with RFC 0001's framework-over-language philosophy.

Plain File URI resolution (RFC 8089) was confirmed to have no built-in versioning concept whatsoever — it addresses only a path on a filesystem, with no notion of "version" of that path's contents — which rules it out as a sufficient mechanism on its own and motivates the need for this RFC.

#### Motivation
Earlier source material stated tersely: "We don't offer any version control for your codes, so we must not offer any dependency management too." In practice this leaves open real, unanswered questions: when two parts of a project need two different versions of the same imported file, or when the supply-chain integrity of an imported file needs to be verified (hashing/pinning), something has to resolve that — the question is only *where* that resolution mechanism should live, not whether the need exists at all.

#### Discussion

##### Drawbacks
Deferring all dependency resolution to an external, not-yet-specified manifest format means, until that manifest format is actually designed, there is no concrete answer to "what happens when two parts of a project need different versions of the same file" — this RFC identifies the right *layer* for the answer to live in, but does not yet provide the answer itself.

##### Rationale and alternatives
Encoding version information directly into the `in` address string (option 1 above) was considered and rejected for reintroducing a network/versioning-shaped concept into the language grammar — precisely the same objection already raised against Go's `import "github.com/user/repo/v2"`-style paths, where a concern external to the language (source location and versioning) is baked into syntax.

##### Prior art
Go's `go.mod`, Node's `package.json`/`package-lock.json`, and Rust's `Cargo.toml`/`Cargo.lock` are all examples of companion-manifest-driven dependency resolution living beside, not inside, the source language's import syntax — the direction this RFC leans toward, while explicitly avoiding Go's choice to also bake a source-location/versioning convention into the import string itself.

##### Unresolved questions
The actual manifest format, its exact resolution algorithm (including how it would resolve the `memar/` prefix specifically to "the canonical Memar framework source"), and how supply-chain integrity (hashing/pinning) is verified are all still completely open and out of scope for this RFC.

##### Future possibilities
A dedicated follow-up RFC specifying the manifest file's exact format and resolution algorithm is the natural next step once this directional decision (manifest-based, not import-syntax-based) is confirmed.

## Results

## Discussion

### Drawbacks

### Rationale and alternatives

### Prior art

### Unresolved questions

### Future possibilities

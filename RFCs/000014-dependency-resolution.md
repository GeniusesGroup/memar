---
RFC Number: 000014
Title: "Dependency Resolution via File URI and Companion Manifest"
Status: Draft
Start Date: 2026-06-30
Applied to: []
Supersedes: null
Superseded by: null
Related:
  Depends_on: ["000013"]
  Extends: []
  Conflicts with: []
Author(s): []
---

## Summary
Khayyam's `in`-based import resolves to a file-system-style path (e.g. `memar/net/tcp`), not a network/version-aware URI. Because plain File URI resolution (RFC 8089) has no concept of versioning, dependency/version resolution must be solved one layer up — by a framework-level tooling convention, most likely a companion manifest file placed alongside a module — rather than inside the language grammar itself.

## Motivation
Earlier source material stated tersely: "We don't offer any version control for your codes, so we must not offer any dependency management too." In practice this leaves open real, unanswered questions: when two parts of a project need two different versions of the same imported file, or when the supply-chain integrity of an imported file needs to be verified (hashing/pinning), something has to resolve that — the question is only *where* that resolution mechanism should live, not whether the need exists at all.

## Guide-level explanation
A developer writes `in "memar/net/tcp"` exactly as today; nothing about the import syntax itself changes. Separately, somewhere outside the language grammar — most plausibly a manifest file living alongside a module, in the spirit of how a `go.mod` or `package.json` sits beside source code rather than inside it — a framework-level tool determines which actual source (and which version of it) the `memar/` prefix resolves to for a given build. This keeps the language's stated promise (`in` is a simple, file-system-style path, not a network protocol) fully intact, while still giving an answer to "which bytes get linked" at the tooling layer.

## Reference-level explanation
Two concrete mechanisms were considered for where version information should live:
1. **Encoding a version inside the import path itself** (e.g. a query-string-like extension to the `in` address, similar in spirit to an HTTP URI's query component). This was evaluated and is **not** the recommended direction, because it would import a foreign concept (version syntax) directly into the language grammar — the same objection already raised against Go's URL-shaped import paths.
2. **A companion manifest file alongside a module**, external to the language grammar entirely, responsible for resolving `memar/`-prefixed (and other) import roots to actual source locations and specific versions/hashes. This is the preferred direction, since it keeps the `in` keyword's grammar untouched and treats versioning purely as a build/tooling-layer concern, consistent with RFC 0001's framework-over-language philosophy.

Plain File URI resolution (RFC 8089) was confirmed to have no built-in versioning concept whatsoever — it addresses only a path on a filesystem, with no notion of "version" of that path's contents — which rules it out as a sufficient mechanism on its own and motivates the need for this RFC.

## Drawbacks
Deferring all dependency resolution to an external, not-yet-specified manifest format means, until that manifest format is actually designed, there is no concrete answer to "what happens when two parts of a project need different versions of the same file" — this RFC identifies the right *layer* for the answer to live in, but does not yet provide the answer itself.

## Rationale and alternatives
Encoding version information directly into the `in` address string (option 1 above) was considered and rejected for reintroducing a network/versioning-shaped concept into the language grammar — precisely the same objection already raised against Go's `import "github.com/user/repo/v2"`-style paths, where a concern external to the language (source location and versioning) is baked into syntax.

## Prior art
Go's `go.mod`, Node's `package.json`/`package-lock.json`, and Rust's `Cargo.toml`/`Cargo.lock` are all examples of companion-manifest-driven dependency resolution living beside, not inside, the source language's import syntax — the direction this RFC leans toward, while explicitly avoiding Go's choice to also bake a source-location/versioning convention into the import string itself.

## Unresolved questions
The actual manifest format, its exact resolution algorithm (including how it would resolve the `memar/` prefix specifically to "the canonical Memar framework source"), and how supply-chain integrity (hashing/pinning) is verified are all still completely open and out of scope for this RFC.

## Future possibilities
A dedicated follow-up RFC specifying the manifest file's exact format and resolution algorithm is the natural next step once this directional decision (manifest-based, not import-syntax-based) is confirmed.

# App relation - object (build artifacts)

## Model

- Candidate (unconfirmed): object-to-app build-artifact labels `OSImage`, `BinaryExecutable` (direction unconfirmed), e.g. `(object)-[:os_image]->(app)` / `(object)-[:binary_executable]->(app)`.

## Policies (rules)

- The artifact is expected to carry image/application metadata — source TODO: "some info about the image and the application e.g. framework, builder, ...".

## Placement

- **Structural artifact edges stay core `software` pending the metadata verdict; framework/builder metadata is a pluggable bill-of-materials candidate (decide later).** A relationship needing processing semantics keeps edge + processing in one module — if bill-of-materials query/storage appears, that complete capability installs and removes as a whole, attaching to software; label-only vocab is a parameter and stays here.

## Open questions

- Is the framework/builder metadata a software bill-of-materials concept?
- Build-artifact or deployment relation (shared with [sub-compile](../sub-compile/sub-compile.md))?
- Which node kind plays "object" — OS image, binary executable, or both under one edge?


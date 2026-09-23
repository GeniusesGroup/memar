# Modularity in Khayyam Handoff

Open work for `modularity.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Naming Without Package Context
1. Is a whole-file inclusion form beyond `in` genuinely needed? Earlier design material mentioned a hypothetical `im` keyword (`tp {name} im {address}`) for including an entire file under one local name, such as `jsonEncode.Encoder`; it was exploratory, not a commitment to a second import mechanism. Whether `in` alone can cover both inclusion of a named entity and any future whole-file inclusion need remains unresolved.

### Dependency Resolution and Companion Manifest
1. What manifest schema and resolver model can support versioning and integrity without creating a second, hidden language-level module system?
2. The manifest format; the exact resolution algorithm; resolution of the `memar/` prefix; multi-version conflict policy; supply-chain integrity mechanisms such as pinning or hashing; and the authoritative meaning of each proposed manifest field remain out of scope and undecided.
3. Which resolution policies are foundational framework law, and which are pluggable organizational rules?
4. Direction recorded 2026-09-22 (owner ruling): the manifest is the place a module declares *which files belong to it* and *how other modules interact with it* — file membership plus the published surface, not only dependency resolution. The shaping constraint against Go's `go.mod` (and similar) is recorded as an anti-goal: `go.mod` puts source *location* (module path encoding host, e.g. GitHub organization) into a file every checkout carries, so moving a codebase GitHub → enterprise self-host forces editing every module's source tree. Khayyam's manifest must keep hosting/location policy separable from the declaration of identity and membership, so a move does not touch the source files themselves. Format, schema fields, and the location/identity split mechanism remain undecided (feeds items 1–3 above).

### Which method set does a file's importer see?
- State: open (review 2026-09-22). `in` includes named entities from a file; what the *importer* of a type can see and attach — only methods declared in the including file, or methods attached to that type across the module's files (the same-directory extension rule for file-splitting) — is not stated for the cross-file case. Visibility of methods across the module boundary interacts with the local/distant monkey-patching boundary already stated in the base document.

### What is the exact `in` path shape?
- State: mostly settled in examples, not as a rule: paths end in `.kh` (e.g. `"memar/process/services/errors/service-not-found.kh"`). Whether the extension is mandatory in the grammar, optional with a tooling default, or forbidden (tooling always appends it) is not stated as a rule. (Review 2026-09-22.)

### Cyclic Module Dependencies
Khayyam has not settled whether and how its grammar or tooling restrict cycles among module inclusions. Go forbids cyclic package imports outright, and the ban behaves like a compilation-speed measure rather than a modeling truth: developers satisfy it by dropping type information across package boundaries (for example, passing an account identifier as a plain string where a real identifier Type exists), losing exactly the nominal distinction the type model is for. The conceptual layer has already ruled that mutual conceptual dependence between Modules is not, by itself, a defect and that language cycle restrictions must not be forced onto the model ([Modularity → Conceptual Relationships Are Not Runtime Coupling](../modularity.md#conceptual-relationships-are-not-runtime-coupling)); the language layer still owes the positive decision — no restriction, a restriction with an escape hatch, or an out-of-band tooling rule — and its rationale.

## Anticipated Work

- A dedicated document can specify the manifest format, resolution algorithm, integrity model, and compatibility policy once the directional decision to keep them outside the `in` grammar is confirmed. (From the Manifest-as-Module-Contract topic's retired Future possibilities.)
- Once a manifest and resolver are designed, their document should define the framework/tooling contract and link back to `modularity.md` for the language boundary, rather than extending `in` with distribution policy. (From the document-level retired Future possibilities.)

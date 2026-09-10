# Modularity in Khayyam Handoff

Open work for `modularity.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Open Questions

### Naming Without Package Context
1. Is a whole-file inclusion form beyond `in` genuinely needed? Earlier design material mentioned a hypothetical `im` keyword (`tp {name} im {address}`) for including an entire file under one local name, such as `jsonEncode.Encoder`; it was exploratory, not a commitment to a second import mechanism. Whether `in` alone can cover both inclusion of a named entity and any future whole-file inclusion need remains unresolved.

### Dependency Resolution and Companion Manifest
1. What manifest schema and resolver model can support versioning and integrity without creating a second, hidden language-level module system?
2. The manifest format; the exact resolution algorithm; resolution of the `memar/` prefix; multi-version conflict policy; supply-chain integrity mechanisms such as pinning or hashing; and the authoritative meaning of each proposed manifest field remain out of scope and undecided.
3. Which resolution policies are foundational framework law, and which are pluggable organizational rules?

## Anticipated Work

- A dedicated document can specify the manifest format, resolution algorithm, integrity model, and compatibility policy once the directional decision to keep them outside the `in` grammar is confirmed. (From the Manifest-as-Module-Contract topic's retired Future possibilities.)
- Once a manifest and resolver are designed, their document should define the framework/tooling contract and link back to `modularity.md` for the language boundary, rather than extending `in` with distribution policy. (From the document-level retired Future possibilities.)

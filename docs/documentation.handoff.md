# Documentation Handoff

## Topic & Purpose
Open questions and anticipated work for the documentation meta-layer (`documentation.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

Open work for `documentation.md`. Entries are mutable current state - revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Open Questions

### Mixed-facet documents
- State: whether a single document should ever carry both facets' structures simultaneously (for example, an Explanation-facet body with a Practice-facet appendix) is not settled. The current position - one facet per document, choose the dominant purpose - is simpler and avoids ambiguity, but may prove too rigid if a real need for mixed content arises.
- Next: decide when a real mixed-content document appears.

### Facet registry
- State: whether a facet should carry metadata of its own (canonical name, one-line definition, reference to its governing specification) in a centralized machine-readable registry, or whether the current loose convention (each facet documented in its own specification file, cross-referenced from here) is sufficient. At the current scale of five facets the registry overhead is not justified; the prose here is authoritative and can be extracted mechanically if tooling ever needs it.
- Next: revisit when tooling consumes facet metadata or the facet count grows.

### Citations: Reference versus Depends_on boundary
- State: the boundary between `Reference` and `Depends_on` is not precisely defined - the current wording conflates whether the cited work is needed to *understand* the document's text with whether it is needed to *implement* it correctly. A proposed starting criterion for the understandability axis (unintelligible without the cited work → `Depends_on`; a mere pointer → `Reference`) is a reasonable basis, but whether an implementability axis needs separate tracking is unresolved.
- Next: dedicated terminology session.

### Entry-title uniqueness in changelog files
- State: changelog entry titles are short and author-chosen, with no uniqueness requirement - two entries could land on the same title, which would be ambiguous if ever linked by anchor. Entries are currently expected to be found by reading or full-text search, not by anchor.
- Next: decide if anchor-linking entries ever becomes a real need.

### Are digits permitted in a slug?
- State: this specification's former `File` wording banned numbers and domain prefixes in filenames, which contradicted practice the naming convention now describes: `networking-osi_1-Asb.md` carries a digit inside a conceptual term, and a Research companion's ordinal (`<base>.research.<NNN>.md`) is a digit by design. The contradiction was removed by pointing `File` at [documentation.md → File Naming](./documentation.md#file-naming), which specifies what each separator means but says nothing about which characters a term may contain. Whether digits are legitimate inside a slug generally, or only inside the two constructs that already use them, is unsettled.
- Next: settle when a third digit-bearing name is actually proposed.

## Anticipated Work

### Facet growth
- If a sixth facet is ever added, the [Facets currently defined](./documentation.md#facets-currently-defined) section grows by one entry per facet, and each new facet's governing specification follows the same pattern: an Explanation-facet document that specifies the new facet's structure, cross-referenced from here. No change to the facet concept itself or to the existing facet specifications is required - the system is additive by design. (The Research facet was added this way on 2026-09-08, with one adoption-path inversion: its specification was drafted from a stated requirement set before any informal accumulation, rather than consolidated from a practiced convention.)

### Further reader relationships
- State: whether further reader relationships will emerge within this project's scope that don't fit any of the five current facets - if they do, the system extends by adding a new facet following the same pattern. (The Handoff facet was added this way, resolving the earlier version of this question: the discussion-resumption relationship had emerged in real records before it was named. The Research facet was added the same day with the inverted adoption path noted under Facet growth.)
- Next: watch for a real document type that fits none of the five.

### Re-deriving the method once the organization exists
- State: [File Naming](./documentation.md#file-naming) and the dot-keyed companion mechanism are shaped by the medium this project currently uses - a repository of files addressed by path. That is a fact about the medium, not a commitment of the method: content's identity in Memar is its addressability ([Content → Addressability](./content.md#addressability)), and what a record *is* is never contained in what its file is *called*. The generalization is unwinnable from the file side: a film's information exceeds its name by so much that naming conventions derived from path habits are the wrong primitive to extend. Once Memar's own organization exists - where records are addressed rather than pathed - the naming convention, the companion pairing, and whatever the repository-directory conventions in this set's READMEs assume all need re-deriving against that medium.
- Next: revisit when the organization exists. Deliberately not generalized now, and the naming convention should not be stretched to cover content that is not a document (a film, an audio recording, a model artifact) on the assumption that today's separators will survive the change of medium. (Omid Hekayati - raised 2026-09-14.)

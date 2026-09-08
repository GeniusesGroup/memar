# Documentation — Changelog Handoff

Open work for `documentation-changelog.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Topic & Purpose
Open questions and anticipated work for the Changelog facet's governing specification (`documentation-changelog.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

## Open Questions

### The dot-boundary criterion for companion naming
- State: the companion rule keys on the dot (`modeling.practice.md` is a companion of `modeling.md`), with hyphenated standalone documents as counter-examples. If a future document legitimately falls between the two patterns — a hyphenated name that IS a companion, or a dotted name that is not — the rule needs a principled criterion (for example, derivability of the relationship from the name alone) rather than case-by-case judgment.
- Blocks continuation: No
- Next: evaluate when a real case appears.

### Changelog entry-title uniqueness
- State: entry titles are short and author-chosen, with no uniqueness requirement — two entries could land on the same title, which would be ambiguous if ever linked by anchor. Entries are expected to be found by reading top-to-bottom or full-text search.
- Blocks continuation: No
- Next: decide if anchor-linking entries ever becomes a real need.

### Session-consolidation boundary
- State: the Session consolidation rule says a new entry is added only when the kind of work changes. Whether "kind of work" should be tied to the `Type` field's vocabulary, to a structural boundary in the base artifact, or left as author judgment is not yet tested against a real multi-kind session.
- Blocks continuation: No
- Next: observe the first session that produces both a `refactor` and a substantive `Added` change on one artifact.

## Anticipated Work

### content.changelog.md remediation
The only file the 2026-09-07 campaign could not remediate from its own text: the "Initial revision" entry carries untagged narrative paragraphs across four contributors whose decision chronology is unattributable without guessing. Needs owner-assisted repair (the owner holds the memory the text lacks) or explicit acceptance of the entry as-is.

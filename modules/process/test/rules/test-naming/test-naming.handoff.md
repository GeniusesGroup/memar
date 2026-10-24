# Test Rule — Test Naming Handoff
Open state for [test-naming.md](./test-naming.md). See the repository's [documentation-handoff.md](../../../../../modules-plugable/knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Status
Active — rule added 2026-09-30 alongside [Test Placement](../test-placement/test-placement.md), which it depends on.

## Open Questions
- **Whether the subject should be machine-readable in the name.** The Rule makes the name a reader's shortcut and requires the statement inside the Test, which leaves the protocol's "every Test names its Process" obligation uncheckable against the tree. A name encoding the subject would make it checkable at the cost of the name no longer being the file's own base name. Undecided, and it is the same question [Test Placement's handoff](../test-placement/test-placement.handoff.md) raises from the other side.
- **What a Test of a foundational document is.** The Rule now covers every Test in the Memar ecosystem, a document's included, but no document has a Test yet, because why a document owes one — what Process it names and what a Check over it decides — is not settled. Until it is, the Rule has nothing there to name.
- **Whether Test-support artifacts belong in the same folder.** The Rule names them and distinguishes them from Tests, but says nothing about whether they sit beside the Tests or in a sibling folder inside `tests/`. Nothing here needs the answer yet.

## Related Artifacts
- [test.md](../../test.md) — the subject this Rule checks.
- [test-placement](../test-placement/test-placement.md) — the sibling Rule this one depends on; the pair is adopted or relaxed together.
- [documentation.md → File Naming](../../../../../modules-plugable/knowledge/documentation/documentation.md#file-naming) — the repository's rule for a name that states another angle on the same subject, which this Rule deliberately does not use.

# Khayyam Rule — Method Separation Handoff
Open state for [method-separation.md](./method-separation.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — applied 2026-09-28 to the ported corpus under `modules/` (excluding `modules/khayyam/`): 265 blank lines in 80 files. A second run changes nothing.

## Decisions
- **One blank line between methods in commented files** — Decided (2026-09-28, owner). The owner's example is `modules/time/timer/protocol/timer.kh`.
- **A method is taken with the comments above it** — Decided (2026-09-28). The blank line goes above the comment, so a comment stays attached to the method it documents.
- **The license block and the `TODO(go-migrate)` marker do not make a file commented** — Tentative (2026-09-28, applied by the tool; awaiting the owner's review). Every ported file carries both, so counting them would apply the rule to every file and the condition would mean nothing.

## Open Questions
- **Whether a source-layout rule belongs in this catalog.** The [membership criterion](../README.md#membership-criterion) asks that a rule's subject be Khayyam itself; blank lines are not in the grammar. The rule is kept here beside the other rewrite rules of the port until the owner says whether layout rules belong in the catalog or in a project's own rule set.
- **Whether an abstraction and its first method are separated.** The rule separates methods from methods only; an `ab` directly followed by its first method stays adjacent.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [method-separation.md](./method-separation.md) | Base — the rule | Keep in sync with the tool |
| [comment-policy.md](../comment-policy/comment-policy.md) | Depends_on — where documentation lives | None (read) |
| [targets/go/abstraction_bridge.py](../../targets/go/abstraction_bridge.py) | Implements — `tidy --rule method-separation` | Keep in sync |
| [targets/go/test_abstraction_bridge.py](../../targets/go/test_abstraction_bridge.py) | Implements — the `Tidy` tests | Keep in sync |

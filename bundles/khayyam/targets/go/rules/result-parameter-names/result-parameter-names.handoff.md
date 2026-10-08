# Go Port Rule — Result Parameter Names Handoff
Open state for [result-parameter-names.md](./result-parameter-names.md). See the repository's [documentation-handoff.md](../../../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — applied 2026-09-28 to the ported sources under `modules/` (excluding `bundles/khayyam/`): 336 parameters renamed in 152 files. A second run changes nothing. No `resultN` or `argN` name remains in the ported sources as of 2026-10-04; the subject the Rule governs is now only what the port's writer still produces, and it produces one per unnamed Go parameter it transfers.

## Decisions
- **First letter, then two letters, then a number** — Decided (2026-09-28, owner).
- **Author-chosen names stay** — Decided (2026-09-28, owner). Only `resultN` and `argN` are synthetic.
- **The type's word is the last segment of a qualified name** — Tentative (2026-09-28, applied by the tool; awaiting the owner's review). `Timer_Status` gives `s` rather than `t`, so the name follows what the value is rather than the module it comes from. The alternative, the first letter of the whole name, would make most names in a module the same letter.
- **Keywords are skipped** — Tentative (2026-09-28). A type starting with `Tp…` or `In…` would otherwise produce a keyword as a name at the two-letter step.

## Open Questions
- **Whether the rule should run in the port itself.** The bridge still writes `resultN` for an unnamed Go parameter; this rule renames afterwards. Writing the derived name at transfer time would make the rule unnecessary for new transfers.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [result-parameter-names.md](./result-parameter-names.md) | Base — the rule | Keep in sync with the tool |
| [Khayyam — Method in Khayyam](../../../../../../docs/khayyam/method.md#method-structure) | Depends_on — parameters are named in the two variable groups | None (read) |
| [targets/go/abstraction_bridge.py](../../abstraction_bridge.py) | Implements — `tidy --rule result-parameter-names` | Keep in sync |
| [targets/go/test_abstraction_bridge.py](../../test_abstraction_bridge.py) | Implements — the `Tidy` tests | Keep in sync |
| [Khayyam Go Target](../../target.md) | Describes — the target whose toolchain holds this Rule | Keep in sync |

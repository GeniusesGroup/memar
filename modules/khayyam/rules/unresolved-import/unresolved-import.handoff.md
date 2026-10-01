# Khayyam Rule — Unresolved Import Handoff
Open state for [unresolved-import.md](./unresolved-import.md). See the repository's [documentation-handoff.md](../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — decided 2026-09-25 as one of the three outcomes rerouted out of the language documents; recorded as a rule 2026-09-26; its malformed-target entry corrected against the code 2026-09-27.

## Decisions
- **A file that is absent and a file that is malformed are two refusals** — State (2026-09-27, checked against the code). [core/src/frontend.ts](../../core/src/frontend.ts) refuses `unresolved-import` only when the file system returns nothing; a target that is there and does not parse is refused with the reason the target itself reports, at its own line. The rule's text above and the [import address rule](../import-address/import-address.md)'s — that the toolchain refuses only a URI with no file behind it — are both the position the code holds.

## Open Questions
- **Whether a malformed target is this rule at all.** [core/src/frontend.ts](../../core/src/frontend.ts) keeps the two facts apart: when the file system returns nothing the refusal is `unresolved-import` (line 43), and when the file is there and does not parse the refusal is the *target's own* reason at the target's own line (lines 45-49) — the matrix asserts that as its own row (*an import of a file that is there and does not parse — the target's own fault*). An earlier entry here claimed the two were indistinguishable to a caller; that was true of the code before the split and is no longer. What remains is the rule-engine question: a caller that wants "the URI resolved" as a single fact has to ask twice, and whether the engine's input should carry both, or the target's fault should be the target's own file's report, is undecided.
- **Whether the URI is resolved once or re-resolved.** The file system is injected per request, so a missing URI is re-read on every analysis. Whether the rule engine's incremental model caches a resolution, and how a change to the target invalidates it, waits on the analysis-event schema the [toolchain handoff](../../execution.handoff.md) carries as open.
- **Whether a missing URI is a `compiler-gate` or a `governance` rule.** Recorded as compiler-gate because it refuses. The accepted model distinguishes the classes by who may disable them, and the Rule protocol members that would settle it are provisional.
- **Mutual inclusion.** Whether the toolchain must reject a cycle of `in` inclusions between files is open in the [language handoff](../../../../docs/khayyam/khayyam.handoff.md#whether-the-compilerlinker-must-reject-mutual-in-inclusion-cycles-between-files-independent-of-module-level-cycles). This rule is one of the conditions such a cycle would have to survive, so the two questions are adjacent even though the cycle question is not this folder's.

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [unresolved-import.md](./unresolved-import.md) | Base — the rule | Keep in sync with the resolver |
| [import-address.md](../import-address/import-address.md) | Depends_on — the rule that says what the value is | Keep in sync |
| [core/src/frontend.ts](../../core/src/frontend.ts) | Implements — the `unresolved-import` refusal | None (unchanged) |
| [core/test/refusal.test.ts](../../core/test/refusal.test.ts) | Reference — the row that asserts this rule | Keep in sync |
| [execution.handoff.md](../../execution.handoff.md) | Reference — the rerouting decision and the rule model | Keep in sync |

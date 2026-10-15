# Revision Changelog

## Changelog

### Document created: Revision protocol

- Time: 2026-10-05T10:44:38Z
- Type: Added
- Propagates to:
  - ../../../modules/khayyam/services/rename/rename-management.handoff.md: Done — the protocol draft this entry creates is the Next the 2026-10-05 protocol-owner decision called for; review of the draft itself stays open in this file's own handoff.
- Contributors:
  - [Meta AI](../../../CONTRIBUTORS.md#meta-ai) (muse-spark-1.3 via [OpenCode](../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- New Explanation-facet document `revision.md`: the Revision contract (enumerate sources, reviewable plan, explicit write, refuse-on-newly-broken, report) lifted in portable form from the declaration-rename engine classification; the twin split (Content owns text identity, analyzer owns binding truth); non-duplication boundaries against Lexer, Compiler, and Linter; the Binding narrowing consequence (language-independent; Khayyam one consumer); and the explicit non-definitions (structural rules, per-target shapes, unexamined languages).

#### Considered and not done
- Naming the document after its first consumer (`rename-engine`) or its mechanism (`explicit-rewrite`) (rejected): the contract is the enacted revision, and the name must survive consumers this repository has not built.
- Carrying the dry-by-default posture as a separate clause (rejected): it is already entailed by "writes only under an explicit request" and a second clause would state the same commitment twice.
- Defining exit codes or plan renderings (rejected): per-target decisions, explicitly disowned in the body.

---

### Settled entries moved out of the handoff

- Time: 2026-10-14T12:48:22Z
- Type: Removed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Claude](../../../CONTRIBUTORS.md#claude) (claude-opus-5-5 via Claude Code) - judged, recorded

#### What changed
- Removed the Anticipated Work entry "A walkthrough of this contract against a second consumer" from `revision.handoff.md`: the walkthrough was done 2026-10-05 against `go-clue-residue` (`tidy --rule`). The contract held without per-target smuggling: enumerate, explicit write, and report fit; reviewable plan and refuse-on-newly-broken misfit only as consumer implementation gaps (no pre-write plan artifact; per-file writes with no all-or-nothing gate), fixable without a contract change. Those two gaps are carried as chartered work in `bundles/khayyam/targets/go/rules/go-clue-residue/go-clue-residue.handoff.md` (Anticipated Work, "Pre-write plan artifact for `tidy --rule`" and "All-or-nothing refuse gate"), so nothing of the walkthrough is owed by this document.

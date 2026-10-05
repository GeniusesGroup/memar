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

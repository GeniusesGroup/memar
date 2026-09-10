# Immutable Infrastructure Changelog

## Changelog

### Initial recording of the principle
- Time: unknown (historical import — concept dated 2026-07-06; first committed 2026-07-09)
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — claimed

#### What changed
- The placeholder document established the immutability statement (configuration change = artifact change requiring rebuild/recompile), its proposed foundational status with the expected Khayyam compiler/PGO benefit, the closely related no-runtime-code-addition governance rule treated as a single "what code enters the repository" concern addressed through source review alone, and explicit deferral of all deeper analysis — motivation depth, guide/reference treatment, drawbacks, rationale, prior art — to a dedicated future session, with only candidate prior-art directions noted (Omid Hekayati — the concept; Claude — recorded).

#### Deliberation
- The immutable-infrastructure concept and its companion governance rule were raised in discussion (Omid Hekayati — claimed).
- The concept was recorded as raised in conversation, with content intentionally left minimal, to preserve it for a dedicated future deep-dive (Claude — claimed).

---

### Type-level identity relationship absorbed from the dissolved Static Concepts document
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Cited:
  - [Type](../type.md) — Depends_on: the added section analyzes this document's governance rule against that document's stateless-Types identity principle; both sides of the relationship are needed for the argument.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Added "Relationship to Type-Level Identity", absorbing the compatibility-and-logical-independence analysis originally authored inside *Static Concepts Must Be Types* (495421, dissolved the same day): convergence without interdependence; the sentinel-value counterexample (immutable infrastructure satisfiable with data-based identity); the runtime-registry counterexample (identity-in-type achievable while violating recompilation governance); and the compile-time-*typed*-identity gain.
- The section carries forward the original's provisional-content caveat — which now applies to this document itself, since it is the placeholder that caveat warned about — and remains due for revision against the dedicated session already listed under Future possibilities.
- Recorded for a future pass: this document otherwise retains legacy `Applied to`/`Citations`/`Contributor(s)`/`Supersedes` front matter and the retired template pending its own facet migration.

#### Deliberation
- Why substantive architectural analysis was sitting in another document's changelog ledger was questioned, and relocation into the explanatory home was directed (Omid Hekayati — directed).

---

### Absorption of the "Emergency Halt & Connection Continuity" context note
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, applied

#### What changed
- The standalone context note `immutable-infrastructure and Connections.md` (an untracked working note marked "Deferred — for a dedicated future chat") was merged as the new "Open Design Threads" section.
- The section carries (1) the emergency halt ("God-halt") service — a pre-compiled run/halt path-selection mechanism that is explicitly *not* an exception to the governance rule, with its three recorded design needs (Code-vs-Rule graph placement, single-point-of-failure/security surface, distributed halt-propagation scope and consistency); and (2) connection continuity across a sub-minute redeploy — whether `ApplicationInstanceID` survives an II-driven update or long-lived Connections are necessarily dropped, the Erlang hot-swap comparison (call/session continuity vs. swap speed), and the graceful-draining/handoff decision.
- The Motivation section's narrower emergency-shutoff question now cross-references the God-halt thread.
- No mechanism was designed anywhere — the source note existed solely to preserve open questions and their reasoning, and that intent is stated verbatim in the section intro; the source file is deleted with nothing left behind.

#### Deliberation
- Merging the standalone context note into this document was directed so the micro-file could be deleted (Omid Hekayati — directed).

---

### Migration to the Explanation-facet template
- Time: 2026-08-25T00:00:00Z
- Type: refactor
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

#### What changed
- Restructured per `documentation-explanation.md`.
- Summary split into the Abstract plus "The Principle" as the first Explanation topic.
- Motivation moved under Introduction with a Methodology composed from this document's record-minimal history.
- Open Design Threads and Relationship to Type-Level Identity retained as Explanation topics.
- Legacy empty deferred placeholders (Guide-level explanation, Reference-level explanation, Drawbacks, Rationale and alternatives) removed, their owed status now recorded under Results.
- Prior art, Unresolved questions, and Future possibilities became Discussion subsections.
- Future possibilities now names the connection-continuity decision explicitly.
- Empty legacy front-matter fields (`Applied to`, `Supersedes`/`Superseded by`, `Citations` — all empty) dropped and `Contributor(s)` moved into this file's entries.
- No substantive content changed.

#### Deliberation
- Continuing the documentation-correction pass onto this document itself was requested (Omid Hekayati — requested).

---

### Second migration wave: `## Discussion` retired per the finalized method
- Time: 2026-09-08T00:00:00Z
- Type: refactor
- Propagates to:
  - immutable_infrastructure.handoff.md: Created - open questions and anticipated work moved there.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [OpenCode](../../CONTRIBUTORS.md#opencode) (qwen3.8-flash) - moved

#### What changed
- The body's top-level sections are now Abstract, Introduction, Explanation, Results only; the `## Discussion` section was removed.
- The two unresolved questions — the full scope and definition of "immutable infrastructure" within Memar, and the extent to which immutable infrastructure eliminates the Khayyam compiler's need for Profile-Guided Optimization, with its reference to the memar-go dispatch-resolution question — moved to the paired handoff's Open Questions.
- The Future-possibilities item — a dedicated session defining the relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning, including the connection-continuity decision under Open Design Threads — moved to the paired handoff's Anticipated Work.
- The deferred prior-art candidate directions relocated to this entry's Related work below.
- Body cross-references into the removed section were repointed: the Type-level-identity caveat now points to the paired handoff, and the Results deferred-analyses list now points to this changelog.
- Final audit pass: the Results section no longer names retired body section titles in its deferred-analysis list (phrased now as drawback accounting, rejected-alternative reasoning, and prior-art research); the prior-art candidate directions themselves live in this entry's Related work.

#### Related work
- Prior-art research was deferred at retirement; likely candidates to research include immutable infrastructure practices in ops/deployment tooling (e.g. container image rebuilds instead of in-place config mutation), and their relationship, if any, to compile-time vs. runtime specialization in compilers. (Migrated from the retired Prior art section)

---

### Relocation to `protocols/` per the folder's membership criterion
- Time: 2026-09-09T00:00:00Z
- Type: refactor
- Cited:
  - [Protocols folder README](./README.md) — Depends_on: the membership criterion this relocation was judged against.
- Propagates to:
  - type.practice.md: Rejected — the practice's runtime-registration governance derives from the base layer's own principles (Structure Is Fixed by Definition, Stateless Types via its step 3); a base document holds no reference up to a protocol document.
  - khayyam-polymorphism.md: Rejected — the dispatch-reducibility argument derives from Structure Is Fixed by Definition and Explicit Behavior Ownership (type.md); the same base-to-protocol reference boundary.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — proposed, corrected
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — argued, moved

#### What changed
- The document and its paired changelog and handoff moved from `docs/` root to [`docs/protocols/`](./README.md); relative links repaired for the new depth (`type.md`, `CONTRIBUTORS.md`, `documentation-handoff.md`).
- A membership statement was added to "The Principle" recording why the document lives there.
- No substantive content of the principle changed; the document remains a Draft placeholder pending its dedicated session.

#### Deliberation
- The relocation was proposed from a review of the documentation set's layering: root holds the lowest-level concept documents from which mental models are built, and this document is not one of them (Omid Hekayati — proposed).
- The proposal was tested against the counter-reading that the document is a framework-level principle like "no hidden control flow" and belongs beside the root's concept documents; rejected because the repository's own distinction is general-concept-definition vs. Memar-owned rule set, not principle vs. protocol — the Error contract is equally cross-cutting and lives in protocols/, and this document's body carries the rule while its concept definition is explicitly deferred to the paired handoff's open questions, which is protocol-shaped, not concept-shaped (Super Z — argued).
- The first application attempt repointed the base documents' references to this document's new location; withdrawn and recorded as Rejected above — references may not run from a base document up to the protocol layer projected onto it; base documents derive their constraints from their own layer's principles, and the citation direction runs from this document down (it already cites type.md for the identity relationship) (Omid Hekayati — corrected; Super Z — applied).

---

### Rescoped to the deployment domain; type-level principle established in Type
- Time: 2026-09-09T00:00:00Z
- Type: Changed
- Cited:
  - [Software Configuration Management](https://en.wikipedia.org/wiki/Software_configuration_management) — Reference: prior-art survey for the lifecycle working-out recorded in the handoff (configuration identification, baselines, change control, status accounting, audit).
- Propagates to:
  - type.md: Done — the type-level principle this document realizes ("Structure Is Fixed by Definition") is now stated there; this document cites it downward.
  - immutable_infrastructure.handoff.md: Done — lifecycle-positioning open question added; title updated.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- The document's scope is now explicitly the deployment domain. Infrastructure names the base a deployed system runs on — the platform layer whose capacity a system's operations ride on — and the immutability rule governs that base and the configuration reaching it; the document no longer presents itself as a general Memar foundation spanning every structural question.
- The title drops "as a Memar Foundation": the general structural principle is now owned by the base layer ([Type → Structure Is Fixed by Definition](../type.md#structure-is-fixed-by-definition)), which this document cites downward and realizes for deployment; the identity-relationship section notes the adoption and marks the runtime-registry counterexample for revision against it in the dedicated session.
- The paired handoff's open questions updated: lifecycle positioning (candidate home: a dedicated software-life-cycle document, treating software as the objective manifestation of a system of aggregated processes), with the ambiguous "ecosystem" terminology flagged for decision.

#### Related work
- Configuration-management practice (IEEE Std 828, ISO 10007 lineage) treats change through identified configuration items, baselines, change control, and audit — the institutional counterpart of the definition-execution boundary; candidate reference for the lifecycle document the handoff anticipates. Ops/deployment tooling (container image rebuilds, unikernel images) remains the other recorded prior-art direction.

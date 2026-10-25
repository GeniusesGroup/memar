# Immutable Infrastructure Changelog

## Changelog

### Initial recording of the principle
- Time: unknown (historical import — concept dated 2026-07-06; first committed 2026-07-09)
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Claude](../../../../CONTRIBUTORS.md#claude) (claude-sonnet-5, extended thinking) — claimed

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
  - [Type](../../../../docs/type.md) — Depends_on: the added section analyzes this document's governance rule against that document's stateless-Types identity principle; both sides of the relationship are needed for the argument.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- Added "Relationship to Type-Level Identity", absorbing the compatibility-and-logical-independence analysis originally authored inside *Static Concepts Must Be Types* (495421, dissolved the same day): convergence without interdependence; the sentinel-value counterexample (immutable infrastructure satisfiable with data-based identity); the runtime-registry counterexample (identity-in-type achievable while violating recompilation governance); and the compile-time-*typed*-identity gain.
- The section carries forward the original's provisional-content caveat — which now applies to this document itself, since it is the placeholder that caveat warned about — and remains due for revision against the dedicated chat already listed under Future possibilities.
- Recorded for a future pass: this document otherwise retains legacy `Applied to`/`Citations`/`Contributor(s)`/`Supersedes` front matter and the retired template pending its own facet migration.

#### Deliberation
- Why substantive architectural analysis was sitting in another document's changelog ledger was questioned, and relocation into the explanatory home was directed (Omid Hekayati — directed).

---

### Absorption of the "Emergency Halt & Connection Continuity" context note
- Time: 2026-08-25T00:00:00Z
- Type: Added
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted, applied

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — rewrote

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - requested
  - [Qwen](../../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) - moved

#### What changed
- The body's top-level sections are now Abstract, Introduction, Explanation, Results only; the `## Discussion` section was removed.
- The two unresolved questions — the full scope and definition of "immutable infrastructure" within Memar, and the extent to which immutable infrastructure eliminates the Khayyam compiler's need for Profile-Guided Optimization, with its reference to the memar-go dispatch-resolution question — moved to the paired handoff's Open Questions.
- The Future-possibilities item — a dedicated chat defining the relationship to deployment, the Khayyam compiler, and Chapar/sRPC device provisioning, including the connection-continuity decision under Open Design Threads — moved to the paired handoff's Anticipated Work.
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
  - [Protocols folder README](../../../README.md) — Depends_on: the membership criterion this relocation was judged against.
- Propagates to:
  - type.practice.md: Rejected — the practice's runtime-registration governance derives from the base layer's own principles (Structure Is Fixed by Definition, Stateless Types via its step 3); a base document holds no reference up to a protocol document.
  - khayyam-polymorphism.md: Rejected — the dispatch-reducibility argument derives from Structure Is Fixed by Definition and Explicit Behavior Ownership (type.md); the same base-to-protocol reference boundary.
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — proposed, corrected
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — argued, moved

#### What changed
- The document and its paired changelog and handoff moved from `docs/` root to [`docs/protocols/`](../../../README.md); relative links repaired for the new depth (`type.md`, `CONTRIBUTORS.md`, `documentation-handoff.md`).
- A membership statement was added to "The Principle" recording why the document lives there.
- No substantive content of the principle changed; the document remains a Draft placeholder pending its dedicated chat.

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
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — directed
  - [Super Z](../../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — drafted

#### What changed
- The document's scope is now explicitly the deployment domain. Infrastructure names the base a deployed system runs on — the platform layer whose capacity a system's operations ride on — and the immutability rule governs that base and the configuration reaching it; the document no longer presents itself as a general Memar foundation spanning every structural question.
- The title drops "as a Memar Foundation": the general structural principle is now owned by the base layer ([Type → Structure Is Fixed by Definition](../../../../docs/type.md#structure-is-fixed-by-definition)), which this document cites downward and realizes for deployment; the identity-relationship section notes the adoption and marks the runtime-registry counterexample for revision against it in the dedicated chat.
- The paired handoff's open questions updated: lifecycle positioning (candidate home: a dedicated software-life-cycle document, treating software as the objective manifestation of a system of aggregated processes), with the ambiguous "ecosystem" terminology flagged for decision.

#### Related work
- Configuration-management practice (IEEE Std 828, ISO 10007 lineage) treats change through identified configuration items, baselines, change control, and audit — the institutional counterpart of the definition-execution boundary; candidate reference for the lifecycle document the handoff anticipates. Ops/deployment tooling (container image rebuilds, unikernel images) remains the other recorded prior-art direction.

---

### PGO question narrowed to the case inventory
- Time: 2026-10-05T09:47:47Z
- Type: Changed
- Propagates to:
  - immutable_infrastructure.handoff.md: Done — the entry now carries `State:` and `Next:` and names only the inventory it still owes.
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- The paired handoff's Open Questions entry "Does immutable infrastructure eliminate the need for Profile-Guided Optimization in the Khayyam compiler?" narrowed to its residue, and given the `State:`/`Next:` shape the [Handoff facet's Open Questions](../../../../modules-plugable/knowledge/documentation/handoff/handoff.md#open-questions) section asks for, which it previously lacked.
- Recorded as settled: [The Principle](./immutable_infrastructure.md#the-principle) already states that Khayyam's compiler and runtime are expected "to benefit directly — for example, by reducing or eliminating the need for runtime profile-guided optimization wherever configuration-driven behavior can instead be resolved at compile time". The whole-elimination reading is therefore refused and the subset reading is taken, and the criterion is named: a behavior loses its runtime-data dependence, and with it the reason for PGO, when the configuration it depends on is fixed by the redeploy rule; per-request and per-connection behavior is not, because a redeploy does not fix it.
- Residue recorded: the passage is illustrative and enumerates no cases, so which currently PGO-addressed cases fall in which class is the whole of what the decision still owes.
- The base document's body is unchanged; the lifecycle-positioning entry is untouched.

---

### The runtime-code rule and the pre-compiled emergency shutoff stated as a check
- Time: 2026-10-05T17:18:32Z
- Type: Changed
- Contributors:
  - [Space Bunny Alpha](../../../../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny via [OpenCode](../../../../CONTRIBUTORS.md#opencode)) — argued, drafted, applied

#### What changed
- `immutable_infrastructure.md` → [The Principle](./immutable_infrastructure.md#the-principle): the governance rule as it now stands is that every capability a running Memar application can reach is present in the artifact it was built from — a runtime signal selects among capabilities so compiled and introduces none, and a capability increase goes through recompilation.
- The check that now decides it is per capability: name the capability and the artifact that carries it, and a capability with no such artifact is what the principle refuses; source review is where it is caught, one control point rather than a second one in a runtime-loading mechanism.
- A narrow, explicitly pre-compiled emergency shutoff is stated as compatible with the principle rather than an open exception question, because its halt path and its run path are both in the built artifact and the signal choosing between them is not code — the standing [Emergency halt](./immutable_infrastructure.md#emergency-halt-god-halt-service) already gave that proposal; what the service still needs stays recorded under [Open Design Threads](./immutable_infrastructure.md#open-design-threads), untouched.
- The Abstract and [Relationship to Type-Level Identity](./immutable_infrastructure.md#relationship-to-type-level-identity) carry the same wording as the principle they name, rather than the "no logic or code may be added at runtime" phrasing, whose "added" no input defined — selecting among pre-compiled capabilities and adding one both sat inside it.
- The runtime-registry counterexample is unaffected and stays valid: a registry that registers a Type the artifact does not carry is exactly a capability with no artifact.

---

### A change carried to a site with no network
- Time: 2026-10-24T16:04:00Z
- Type: Added
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — argued, drafted, applied

#### What changed
- `immutable_infrastructure.md` gained [A change carried to a site with no network](./immutable_infrastructure.md#a-change-carried-to-a-site-with-no-network), Tentative: the release carried in is one signed whole with a manifest of digests and the version it replaces; the site verifies it against a key installed at commissioning before anything runs; site configuration is inside the release; a release carries the conversions of stored shapes and the system reads only the new; going back is the release before plus the backup taken before a conversion; data edited at runtime, such as rules and approval matrices, selects among the artifact's capabilities and the console accepts no code.
- The handoff gained the question whether a site's secrets are configuration inside the release or key material kept outside it, with option 1 (outside, generated on site) assumed meanwhile.

#### Deliberation
- A Memar-built system on an isolated industrial site has no network and needs automatic migrations, backup and restore and an update path; the governance rule of [The Principle](./immutable_infrastructure.md#the-principle) already decides that such a change is a new artifact, so the section applies it rather than adding a rule (Claude — argued).
- The owner's ruling that rules, workflows and approval matrices are data meets the rule that every capability is in the artifact only if the data cannot name an operation the artifact lacks (Claude — argued).

---

### The site-without-network section: who signs, the update order, and what a restore loses
- Time: 2026-10-24T16:50:00Z
- Type: Changed
- Tasks:
  - main:.agents/tasks/20261024-T162240Z-16944/: Complete - applies the independent critique of task 20261024-T161344Z-16944 to the Python-first delivery path
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) — applied the critique's findings

#### What changed
- [A change carried to a site with no network](./immutable_infrastructure.md#a-change-carried-to-a-site-with-no-network): a release is signed by a party the site trusts, and a site may trust several keys installed at commissioning; the two cases, only the builder's key or also the site owner's, are stated with what each allows, and the choice is left to the owner.
- The same section: an update stops every service that writes before it takes its backup; a new bullet states that a restore loses every record written after the update, that going back is lossless only until the new release's first write, and that after it going back needs the Requests written since carried back by a reverse conversion, or a release that fixes forward.
- The same section points to the open questions on site secrets and on converting the signed payloads of past Requests ([Request Handoff](../../request/request.handoff.md#decisions)).
- The [handoff](./immutable_infrastructure.handoff.md) gained three open questions (who may sign a release a site installs; who holds a signing key and what is done on its loss or compromise; how a site's key is rotated or revoked with no network), a Tentative decision naming the options a site's release is designed on meanwhile, and, on the secrets question, the statement that its recommended option is an exception to The Principle.

#### Deliberation
- The critique (task 20261024-T161344Z-16944, findings (c)2, (d)1, (d)2 and (d)3) found the delivery design both signing every release with the builder's key and letting the site's owner rebuild releases, the backup taken before the services stop, the loss on restore unstated, and keys named without custody, rotation or revocation (Claude — checked against the section and the design).
- Who signs and how keys are governed are choices of the owner's, not consequences of The Principle, so they are questions and not rules (Claude — argued).

---

### A site's key is rotated and revoked by a release, recorded Tentative
- Time: 2026-10-24T17:00:00Z
- Type: Changed
- Propagates to:
  - [immutable_infrastructure.md](./immutable_infrastructure.md): Pending - when the decision is no longer Tentative, the bullet "The site verifies before it loads" states that a key change is a release, and stops calling rotation and revocation open
- Tasks:
  - dev-knowledge:.agents/tasks/20261024-T164111Z-16944/: Closed - records the answer the questions-answer agent of task 20261024-T074257Z-16944 gave from the owning document
- Contributors:
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5) - recorded

#### What changed
- The [handoff](./immutable_infrastructure.handoff.md) gained the Tentative decision "A key change is itself a release": a release signed by a currently trusted key adds a new verification key, a later release removes the old one, and a revocation is the same kind of release removing the compromised key; the signer of a revoking release follows the open custody question.
- The open entry "How is a site's trusted verification key rotated or revoked without a network?" was removed, its answer being that decision; the decision on what a site's release is designed on now points to it for rotation and revocation.

#### Considered and not done
- A separate signed key file installed outside the release: a second artifact kind, which The Principle does not name.
- Never rotating, revoking only by recommissioning: a key would live as long as the site.

---

### The owner's working answers to the three release entries recorded as Tentative decisions
- Time: 2026-10-25T14:30:00Z
- Type: Changed
- Propagates to:
  - [immutable_infrastructure.md](./immutable_infrastructure.md): Pending - "Configuration is part of the release" still says whether secrets are configuration is open, and the single exception the secrets answer names is not yet stated; to be carried by task 20261025-T140521Z-16944. Only its two links were repointed to the handoffs' Decisions.
- Tasks:
  - dev-knowledge:.agents/tasks/20261025-T140621Z-16944/: Closed - records the owner's acceptance of 2026-10-25
  - dev-knowledge:.agents/tasks/20261024-T074257Z-16944/: Reference - the design task whose report asked the entries
- Contributors:
  - [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) - decided
  - [Claude](../../../../CONTRIBUTORS.md#claude) (Opus-5.5 via Claude Code) - recorded

#### What changed
- On 2026-10-25 the owner accepted the recommended option of each of three open entries of [the handoff](./immutable_infrastructure.handoff.md) as a working answer, all to be studied in depth in task 20261025-T140521Z-16944. Each entry left Open Questions and is now a Tentative decision carrying its reasons, the options not taken, and that task:
  - "Are a site's secrets configuration that must be in the release, or key material kept outside it?": key material generated on the site and kept outside the release, stated as an exception to The Principle that stays visibly a working answer.
  - "Who may sign a release that a site installs: only its builder, or also the site's owner?": only the builder; the site's owner verifies its own builds and does not install them; tied to the licence task 20261024-T074259Z-16944.
  - "Who holds a release-signing key, and what is done when it is lost or compromised?": an offline hardware token with a recovery key. The decision states the owner's position that the key model must be made exact and independent of any adopting organization, and that bearer-token practice such as JWT is a security disaster, a premise the deeper task tests.
- The decision on what a site's release is designed on names these working answers; the decision "A key change is itself a release" now says the recovery key of the custody decision signs a revocation, instead of linking the removed entry.
- [The changelog's](./immutable_infrastructure.changelog.md) one link to the removed Request entry was repointed to the Request handoff's Decisions.

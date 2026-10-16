# Documentation — Changelog Handoff
Open work for `documentation-changelog.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./documentation-handoff.md) for what a handoff is.

## Topic & Purpose
Open questions and anticipated work for the Changelog facet's governing specification (`documentation-changelog.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

## Open Questions

### Changelog entry-title uniqueness
- State: entry titles are short and author-chosen, with no uniqueness requirement — two entries could land on the same title, which would be ambiguous if ever linked by anchor. Entries are expected to be found by reading top-to-bottom or full-text search.
- Blocks continuation: No
- Next: decide if anchor-linking entries ever becomes a real need.

### Session-consolidation boundary
- State: the Session consolidation rule says a new entry is added only when the kind of work changes. Whether "kind of work" should be tied to the `Type` field's vocabulary, to a structural boundary in the base artifact, or left as author judgment is not yet tested against a real multi-kind session.
- Blocks continuation: No
- Next: observe the first session that produces both a `refactor` and a substantive `Added` change on one artifact.

### An entry whose whole subject is the registry has no home
- State: a placement audit of every changelog in the repository found one entry that records no change to any paired artifact: *Stealth models recorded in CONTRIBUTORS.md; attribution shape and character encoding repaired* (`documentation-changelog.changelog.md`). Its first bullet changes the `## Stealth Models` section of `CONTRIBUTORS.md`, which is paired to no artifact and therefore has no changelog; its remaining bullets belong to about two dozen different ledgers. The rule that sends an entry to the changed artifact's ledger has no destination to send this one to, and the rule admitting entries that record no change does not reach it either, since this entry records plenty. Its three sibling registry entries stay correctly placed because each also carries a bullet changing this specification's own section or Template.
- Blocks continuation: No
- Next: rule whether `CONTRIBUTORS.md` gets a ledger of its own, or whether a session whose only lasting change is to the registry leaves no entry anywhere and is recorded solely in its per-artifact residue.

### A change with no single subject has no tie-breaker
- State: four entries were found whose subject is genuinely more than one artifact, and the routing rule does not say which of them owns such an entry. *Restate the relation of two sources recorded before the standing rule* (`knowledge.changelog.md`) states that no entry above it is edited and changes a rule under `documentation.md` → Citations, citation relations in `content.changelog.md`, and two research records. *Anchors re-derived after the 2026-10-03 removals shifted lines* (`docs/khayyam/khayyam.changelog.md`) records no change to `khayyam.md` at all and names four artifacts whose anchors were re-derived. *Field abstractions rule added; shape moved from qualified names* (`observer-mutator.changelog.md`) records both its own family's addition and a removal that belongs to `qualified-names`. *Repository and realization placement settled — Khayyam modules live here* (`compiler.changelog.md`) is repository-wide, naming about thirty artifacts, and stays only because its first bullet closes a question that file had raised. Session consolidation answers the first half of this — one session, one entry, on the artifact the session was about — but says nothing about a session with no such artifact.
- Blocks continuation: No
- Next: rule what a session whose change has no single subject records, and whether the Session consolidation rule is the tie-breaker or only a rule about how many entries one session writes.

### Repairing a defect inside an existing entry is ungoverned
- State: two entries carry a Python f-string fragment where a rendered character belongs — `" + chr(0x2192) + "` in `documentation-changelog.changelog.md:336` and `" + chr(0x2014) + "` at two link texts in `process.changelog.md` — so their link text reads as an expression rather than as the arrow or dash. The routing rule does not reach them, because the entry is in the right file, and the trivial rule does not reach them, because the entry is not trivial. `content check` reports zero problems on both, so nothing catches them. The entry *character encoding repaired* (2026-09-30) claims that the repository now holds no sequence of that shape outside build output; the arrow instance is that claim's surviving counterexample. Two further instances of the same class were judged BELONGS by the audit and deleted as trivial rather than repaired: *Knowledge Management link retargeted after the rename* and *The event-taxonomy cluster's link repaired after the question it names was answered*.
- Blocks continuation: No
- Next: rule whether a defect inside a frozen entry may be corrected in place at all, and if so whether the correction takes an entry of its own.

### A move can land beside the entry that already records the same change
- State: *Added Edge computing as a Networking-level architectural principle* was moved from `docs/modules/net/giti.changelog.md` to `networking.changelog.md` as unambiguously misplaced. The destination already held *Renamed GP's registry row, added GP-App, and recorded the Edge computing principle* at the same timestamp, covering the same topic, so the destination now carries two entries for one change. The audit left both, because collapsing them would have edited an entry the audit was told not to touch.
- Blocks continuation: No
- Next: rule whether a move that lands beside its twin is merged into the existing entry's `What changed` and dropped, or left as two entries.

### Is the Contributors placeholder `{ModelName}` renamed `{AIModelName}`, and which spelling of a model is recorded?
- State: the Contributors entry field is written `{ModelName} via {ToolName}` ([Contributors (entry field)](./documentation-changelog.md#contributors-entry-field) and the paragraphs on `CONTRIBUTORS.md` above it), and `CONTRIBUTORS.md`'s Template lists `{ModelName}` under a brand's Models. The owner finds `ModelName` misleading (2026-10-14): in Memar a model is first the modeling artifact. A session plan is to name the model that runs it in a key `AIModelName`, written exactly as `CONTRIBUTORS.md` and the Contributors bullets name a model, so the two should use one word. Two spellings are in use for one model: `CONTRIBUTORS.md` lists `Opus-5`, `Sonnet-5`, `Fable-5`, while this specification says the officially documented identifier is recorded and gives `claude-sonnet-5` as its example. [Field Naming Convention](./documentation-explanation.md#field-naming-convention) lists `Model` among its example field names.
- Options: (1) rename the placeholder `{AIModelName}` here and in the `CONTRIBUTORS.md` Template, record a model as `CONTRIBUTORS.md` lists it (`Opus-5.5`), correct the `claude-sonnet-5` example to that form, and drop `Model` from the Field Naming examples, recommended: one name and one spelling everywhere a model is written; cost: the old entries keep the spelling they were written with, since entries are frozen. (2) rename the placeholder only; cost: two spellings stay. (3) keep `{ModelName}`; cost: the plan key and the changelog field differ for one fact.
- Anchor: `docs/documentation-changelog.md`, the `CONTRIBUTORS.md` paragraphs and Contributors (entry field); `CONTRIBUTORS.md`, Template; `docs/documentation-explanation.md`, Field Naming Convention.
- Ruling: owner (2026-10-15): yes, one spelling, the one `CONTRIBUTORS.md` lists (`Opus-5.5`), and every place where Memar's saying and its concrete form disagree is made one. Since then the plan's key became a type, `AIModel` with `ModelName`, `Effort` and `ReasoningLevel` (the two numbers on the scale `Priority` uses), so the rename is re-asked against the type: (1) the bullet writes `({AIModel} via [{ToolName}](…))`, the AIModel on one line as `ModelName` followed, where the agent knows them, by `Effort N` and `ReasoningLevel N` (`Opus-5.5, Effort 4, ReasoningLevel 9 via …`); the `CONTRIBUTORS.md` Template's list item stays `{ModelName}`, now the part's own name; the free words for a setting ("extended thinking") go, being an app's vocabulary, recommended: one type, written the same in a plan (what the task needs) and in an entry (what ran). (2) `{AIModelName}` as first asked, numbers left out of entries; cost: a changelog cannot say at what effort a model ran, which this specification's `Effort` sentence asks for. (3) `{ModelName}` kept with the numbers beside it as free text; cost: two forms of one type. A smaller disagreement rides with it: the bullet names the tool `{ToolName}`, the `CONTRIBUTORS.md` Template heads its section `{Tool}`.
- Anchor: as above; `docs/labels-design.md` of session `20261015-T103826Z-16432`, One type in plans, changelogs and CONTRIBUTORS.md.
- Blocks: the edit of this specification's `CONTRIBUTORS.md` paragraphs and Contributors (entry field), of the `CONTRIBUTORS.md` Template, and of the Field Naming examples. Assumption meanwhile: option 1 (Tentative); the spelling is ruled.
- Asked: 2026-10-15, Claude (session `20261014T120306Z-20292-0`), for Omid Hekayati; re-asked against the type by session `20261015-T103826Z-16432`.

### Should every `Propagates to` entry be answerable to which operation, over which inputs, produced which result?
- State: [Propagates to](./documentation-changelog.md#propagates-to) names each artifact a change should affect with a status of Pending, Done or Rejected. A Done entry claims that the artifact was touched; it does not say which operation did it, over which inputs, with which result, so a reader or a check cannot tell a propagation that was carried out from one that was only asserted. Requiring each entry to be answerable (or to state why it cannot be) would make a propagation a checkable step. No document states the question.
- Options: (1) require a Done entry to cite the change (the revision or the session) that carried it out, so that a check can compare the cited change with the artifact named (recommended; cost is a longer entry and a check); (2) require the answer only for propagations that rewrite generated or derived material; (3) keep the field a claim and rely on review.
- Anchor: docs/documentation-changelog.md, Propagates to and the ledger; docs/documentation-changelog.practice.md. The answer lands in the field's definition.
- Blocks: nothing is blocked. Assumption meanwhile: the field stays a claim reviewed by a reader (Tentative).
- Asked: 2026-10-13, Claude (queued as session `20261013-T072630Z-28940`, written by session `20261015-T103826Z-18580`), for Omid Hekayati.

## Anticipated Work

### Dead `Propagates to` paths left by the two folder moves
- State: the moves of `docs/protocols/` to `docs/modules/` and `modules/khayyam/` to `bundles/khayyam/` left propagation ledgers naming the old paths. The `docs/modules/computer/` changelogs alone carry 27: nine under the former `docs/protocols/`, seven under the former `modules/`, and the rest bare basenames the moves renamed. `docs/khayyam/khayyam.changelog.md` and `docs/modules/computer/token.changelog.md` carry more, some under `Cited` rather than `Propagates to`. Some in-prose labels are stale as well — `protocols/net/sRPC.md` — while their link targets were correctly retargeted. None of this is misplacement, and the placement audits deliberately left it alone; it is a repair pass over ledgers, not an audit of entries.
- Next: a pass that resolves each dead path to its current home, or records that the artifact it named no longer exists.

### Two entries missing their separator
- State: `docs/modeling.changelog.md` has two entries, one before *Modeling review and vocabulary cleanup* and one before *A shared relation is defined once*, that lack the `---` separator every other entry carries.
- Next: add the separator; judge whether a formatting repair takes an entry.

### content.changelog.md remediation
The only file the 2026-09-07 campaign could not remediate from its own text: the "Initial revision" entry carries untagged narrative paragraphs across four contributors whose decision chronology is unattributable without guessing. Needs owner-assisted repair (the owner holds the memory the text lacks) or explicit acceptance of the entry as-is.

### Pending queue: blocking ruling, enforcement, and traceability surface
- State: the Pending queue was triaged (18 discharged Done, 5 re-pointed, 37 kept open with named blockers; recorded in [Spec Kit comparison](./comparisons/spec-kit.001.md), section 12), and `check` reports what remains (52 undischarged propagations at last run). Still undecided: which Pending classes block versus report only, and any enforcement behind the report. `backlinks` and `obligations` enumerate incoming links and undischarged obligations, but "which documents depend on this one" is still not an enumerable traceability surface.
- Next: a ruling for which Pending classes block versus report-only; a decision whether traceability stays enumeration by those verbs plus full-text search (stated with why) or becomes a surface of its own.

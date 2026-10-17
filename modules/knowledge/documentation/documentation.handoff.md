# Documentation Handoff

## Topic & Purpose
Open questions and anticipated work for the documentation meta-layer (`documentation.md`), relocated there when the documentation method removed unresolved-question lists from base documents' bodies.

## Status
Active

Open work for `documentation.md`. Entries are mutable current state - revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](./handoff/handoff.md) for what a handoff is.

## Open Questions

### Facet registry
- State: whether a facet should carry metadata of its own (canonical name, one-line definition, reference to its governing specification) in a centralized machine-readable registry, or whether the current loose convention (each facet documented in its own specification file, found by listing the folder) is sufficient. At the scale this project works at the registry overhead is not justified; each facet's own specification is the authoritative statement of its name and reader relationship, and a registry would be a second place the next facet has to be recorded, which is what [Extensibility](./documentation.md#extensibility) rules out.
- Next: revisit when tooling consumes facet metadata.

### Citations: Reference versus Depends_on boundary
- State: the boundary between `Reference` and `Depends_on` is not precisely defined - the current wording conflates whether the cited work is needed to *understand* the document's text with whether it is needed to *implement* it correctly. A proposed starting criterion for the understandability axis (unintelligible without the cited work → `Depends_on`; a mere pointer → `Reference`) is a reasonable basis, but whether an implementability axis needs separate tracking is unresolved.
- Next: dedicated terminology session.

### Entry-title uniqueness in changelog files
- State: changelog entry titles are short and author-chosen, with no uniqueness requirement - two entries could land on the same title, which would be ambiguous if ever linked by anchor. Entries are currently expected to be found by reading or full-text search, not by anchor.
- Next: decide if anchor-linking entries ever becomes a real need.

### Are digits permitted in a slug?
- State: this specification's former `File` wording banned numbers and domain prefixes in filenames, which contradicted practice the naming convention now describes: `networking-osi_1-Asb.md` carries a digit inside a conceptual term, and a Research companion's ordinal (`<base>.research.<NNN>.md`) is a digit by design. The contradiction was removed by pointing `File` at [documentation.md → File Naming](./documentation.md#file-naming), which specifies what each separator means but says nothing about which characters a term may contain. Whether digits are legitimate inside a slug generally, or only inside the two constructs that already use them, is unsettled.
- Next: settle when a third digit-bearing name is actually proposed.

### Dependency-direction convention
- State: the rule that fundamental concepts must not depend on derived mechanisms — Polymorphism may cite Modeling and Type, never the reverse; base documents may not cite the protocol layer projected onto them; Terminology stands independent of other documents — is applied case by case but has never been stated as a named documentation convention. The polymorphism session proposed it for a conventions file; that file was later retired into this document's meta layer, and the convention itself never followed it home.
- Next: decide whether to register it as a convention in [documentation.md → Citations](./documentation.md#citations) (or a sibling section) or to leave it as applied-only practice re-derived at each review.

### Merged Status vocabulary: report-only values
- State: the owner ruled that a session report's Outcome and Status are one concept in one vocabulary, the type `Status` ([documentation.md → Status](./documentation.md#status)), and accepts that some values are for reports only. The type now has none: a run that ended unmet reads `Active`, one that stopped at an approval reads `Blocked`, and `success` and `clean no-op` both read `Complete`, the report's Result part saying which. The cost is that `clean no-op` (the check passed because nothing needed doing, no artifact changed) is no longer machine-visible, and neither is `exhausted` against `no progress`.
- Options: (1) keep the vocabulary as it is, the Result part carrying the difference (recommended: nothing reads the difference today, and the scripts keep the old words as a reading table, so a value is cheap to add later); (2) add `No-op` for the session report alone, leaving it a `Complete` variant that a plan never takes; (3) add `Exhausted` for the report alone, left Active in the plan, which breaks the rule that a plan and its report agree by equal Statuses.
- Anchor: [documentation.md → Status](./documentation.md#status); `modules/process/session/services/report.py`, `LEGACY_OUTCOME_STATUS`.
- Blocks: nothing. Assumed meanwhile: option 1; also provisional by the owner's ruling: the words `Active`/`Complete` for `open`/`done`, PascalCase keys, lazy migration.
- Asked: 2026-10-13, session `20261013-T142914Z-28176`, for the owner.

### Where does a base concept's Khayyam declaration live
- State: a base document states a concept and its reasons in text and does not retype real code ([A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once)). The owner's answer of 2026-10-15 says a concept can very probably be declared as a Khayyam abstraction in at least one file even before any implementation exists. Open: where that file lives for a concept whose subject is at the base (Type, Error, Status), since the base holds documents only and refers to modules as concepts ([Citation Direction](./documentation.md#citation-direction)).
- Options: (1) a module named for the concept holds the declaration, and the base document names the concept (recommended: uses the two layers as they stand); (2) the base gains a code folder (a third kind of base content no rule names).
- Anchor: [documentation.md → A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once); [documentation.md → Citation Direction](./documentation.md#citation-direction).
- Blocks: nothing. Assumed meanwhile: option 1 (Tentative).
- Asked: 2026-10-13, session `20261013-T160504Z-14980`, for the owner; restated 2026-10-15, session `20261015-T122252Z-5984`.

### Can a check find a retyped fact in code
- State: the rule is kept only by whoever writes. `memar content check` reports an upward link; nothing reports a document that lists the values, fields or transitions of a type (the Status values left explanation, handoff and research with session `20261016-T194830Z-21416`), or a help text that retypes them.
- Options: (1) a test beside each type that compares a named document's listing to the type, where a listing is allowed to remain (recommended once types exist: a copy that must stay is then checked); (2) a content check that flags a table whose cells equal a type's values (needs the types readable by the check); (3) rely on review.
- Anchor: [documentation.md → A Fact in Code Is Written Once](./documentation.md#a-fact-in-code-is-written-once); `modules/knowledge/content/services/check.py`.
- Blocks: nothing. Assumed meanwhile: option 3 (Tentative).
- Asked: 2026-10-13, session `20261013-T160504Z-14980`, for the owner.

### Is the prose label the whole mark for owed or planned material that has no code, default or entry point?
- State: the Content Rule ([Owed or planned capability is marked in all three places](./documentation.md#content-rule-no-fabricated-or-redundant-provenance)) requires the prose claim, the quiescent default in code, and the pointer at the entry point to agree, and says the mark is an `Owed: <id>` line in the document; owed capability no Test can execute is marked by the same line and judged by a reader. For material with no code, no default and no entry point a reader arrives by (a row in a table of owed activities, a planned phase), the rule does not say whether the `Owed:` line is then the whole mark or whether something at the place a reader enters from must also say that it is owed. Without an answer, a reader who arrives by a link past the label sees the claim with no mark.
- Options: (1) the `Owed:` line is the whole mark where no other surface exists, and the rule says so (recommended; cost is one clause); (2) the document or table a reader arrives from must also carry the mark, and a check looks for it; (3) such material is not written until it exists.
- Anchor: docs/documentation.md, Content Rule, the clause on owed or planned capability; docs/documentation-comparison.md requirement 4; the owed rows of modules/process/software/software.md. The answer lands in the Content Rule.
- Blocks: nothing is blocked. Assumption meanwhile: the `Owed:` line is the whole mark for such material (Tentative).
- Asked: 2026-10-13, Claude (queued as session `20261013-T072631Z-19820`, written by session `20261015-T103826Z-18580`), for Omid Hekayati.

### Does the principle of referencing belong in the definition of concepts
- State: [Citation Direction](./documentation.md#citation-direction) states how a document refers to another and in which direction, and that a link is never removed to comply. The owner's answer of 2026-10-16 is that this principle belongs in the definition of concepts, since how one concept refers to another is part of what a concept is; the owner leans to [Terminology](../../../docs/terminology.md). Not settled; until it is, the section stays in Documentation. The earlier form of the question (Terminology or a layering matter of Modularity) is in session `20261015-T122303Z-23544`'s plan, P4 decision 3.
- Options: (1) Terminology owns the principle, and Citation Direction keeps only how a document carries it (the owner's lean); (2) Modularity owns it as a matter of layering; (3) it stays in Documentation.
- Anchor: [documentation.md → Citation Direction](./documentation.md#citation-direction); [Terminology](../../../docs/terminology.md).
- Blocks: nothing. Assumed meanwhile: option 3, the section stays where it is (Tentative).
- Asked: 2026-10-16, owner's third-round answer, recorded by session `20261016-T075834Z-5360`, for Omid Hekayati.

### File Naming's own examples join one term with a hyphen
- State: [File Naming](./documentation.md#file-naming) says a hyphen marks the boundary between category and topic and an underscore joins the words of one term, and that a name whose parts all wear the same separator states no boundary at all. Its own examples `modules/process/control-flow/control-flow.md` and `modules/computer/identifier/media-type.md`, and the Khayyam rule folders `bundles/khayyam/rules/composition-not-duplication`, `orphan-extension`, `abstraction-naming-heuristic`, join the words of one term with hyphens. Either the examples and the folders are renamed, or the rule has an exception it does not state.
- Options: (a) rename those folders and files to underscores (`control_flow`), a wide rename across links; (b) amend the rule so a folder name of one model may hyphenate its words, with the file inside it keeping the same name; (c) leave the rule and mark the examples as the exception to be fixed. The owner's standing ruling is that contradictions in the documents are corrected (2026-10-16).
- Anchor: [documentation.md → File Naming](./documentation.md#file-naming)
- Blocks: nothing. Assumed meanwhile: the rule as written.
- Asked: 2026-10-16, found by session 20261016-T123037Z-21048, for Omid Hekayati; to be decided with the front matter conventions session 20261016-T095101Z-22960, which finds the same kind of contradiction.

## Anticipated Work

### Facet growth
- A new facet is added by writing its governing specification into a subfolder of [the documentation module](./documentation.md) named for it, and by nothing else: no entry, no section and no count in `documentation.md`, and no edit to any existing facet specification. The specification is an Explanation-facet document that follows the same pattern as the others — it states its own reader relationship, what makes it distinct from the facets already in use, the structure its documents follow, and the Status values it draws on. The Research facet was added this way on 2026-09-08, with one adoption-path inversion: its specification was drafted from a stated requirement set before any informal accumulation, rather than consolidated from a practiced convention. On 2026-10-16 the definitions themselves moved out of `documentation.md` and into each facet's own specification, so nothing a later facet needs is added to that document.

### Practice/agent-configuration split
- State: recovered 2026-09-17 from an audit of retired chats-context files (`project instruction and skills - chats.md`, `ساختار-پلاگین-برای-Agent.md`). A documentation-architecture session reached a three-way separation — **Documentation** = the project's truth (what), **Practices** = how that truth is worked with (how, valid for any consumer: human, AI, IDE, automation), **Agent Configuration** = how the two are introduced to a particular agent/platform. The session's acceptance test: if a practice would still be worth keeping when no AI agent exists, it is documentation; if it exists only to satisfy one agent's limitations, it belongs in agent configuration, never in `docs/`. The repository has been *operating* on this separation ever since (Practice-facet documents live in `docs/`, tool-dependent discovery lives in `.agents/skills/`, and the retired `.agents/skills/main/` skill's rules were absorbed into [Cognition](../../../docs/cognition.md)), and the same separation is stated operationally in the memar skill's own "Separation of knowledge" — but no Memar document owns the separation as a stated principle with its acceptance test.
- Next: when the documentation documents are next revised, state the split in the Practice facet's governing specification ([documentation-practice.md](./practice/practice.md)) or [documentation.md](./documentation.md), with the no-agent-existence test as the boundary criterion; the complementary Content-vs-Practice framing (a practice is content taking a role, not an intrinsic artifact type — from the same sessions) belongs with it.

### Re-deriving the method once the organization exists
- State: [File Naming](./documentation.md#file-naming) and the dot-keyed companion mechanism are shaped by the medium this project currently uses - a repository of files addressed by path. That is a fact about the medium, not a commitment of the method: content's identity in Memar is its addressability ([Content → Addressability](../content/content.md#addressability)), and what a record *is* is never contained in what its file is *called*. The generalization is unwinnable from the file side: a film's information exceeds its name by so much that naming conventions derived from path habits are the wrong primitive to extend. Once Memar's own organization exists - where records are addressed rather than pathed - the naming convention, the companion pairing, and whatever the repository-directory conventions in this set's READMEs assume all need re-deriving against that medium.
- Next: revisit when the organization exists. Deliberately not generalized now, and the naming convention should not be stretched to cover content that is not a document (a film, an audio recording, a model artifact) on the assumption that today's separators will survive the change of medium. (Omid Hekayati - raised 2026-09-14.)

### The place of Documentation under Content is not final
- State: by the owner's ruling of 2026-10-15, Documentation leaves the base documents and becomes a module inside a Content category (`modules/knowledge/documentation/`), with one module beneath it for each kind of documentation it governs (Explanation, Practice, Changelog, Handoff, Research, Comparison). The place was chosen because Documentation has code to hold — the checks and declarations its documents name — and because concepts such as Status surfaced that need a home; it is not a settled decomposition, and it may move. It sits under Content because a document is content taking a role for a reader; Knowledge, which documentation serves by making knowledge available beyond one agent ([Agency → Documentation as an Agency Mechanism](../../../docs/agency.md#documentation-as-an-agency-mechanism)), remains a plausible home, and so does the process that records. The layer it moves into holds no folder as final (`modules/README.md`). Nor is the file medium a premise of the place: files are how Memar and the organization repository cover the existing ecosystem today, and the filesystem is to be set aside after its critique. What the module states about a record — the subject it is attached to, its kind, its companions — holds without files; paths, dot-keyed companion names and folder READMEs are one realization of it ([Re-deriving the method once the organization exists](#re-deriving-the-method-once-the-organization-exists)).
- Next: revisit the place when Documentation's module contract is written, when the Content category gains members other than Documentation, or when the critique of the filesystem lands. A later move is one rename per file, committed as a pure move so the history records it as a rename. The proposal and its reasoning are in session `20261015-T122252Z-20076`. (Omid Hekayati - ruled 2026-10-15; written by Claude.)

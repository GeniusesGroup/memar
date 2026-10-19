# Bundles Changelog

## Changelog

### Nested `modules/` defined; society corpus lands as bundle modules
- Time: 2026-09-21T12:40:00Z
- Type: Added, clarified
- Cited:
  - Owner session (organization, 2026-09-21) - Relation: Evidence: `modules/` means the base rules of its enclosing folder at every nesting level; a statute still needs computer code and is therefore a module; Memar `docs/society` is not the transfer shape; a bundle may introduce modules; spread the corpus by concept, not under one society umbrella; `bundles/economy` is a candidate to retire into government; transplant the Memar society commits then purge them from Memar including GitHub
- Propagates to:
  - `bundles/knowledge-management/knowledge-management.md`: Done — the three-layer table no longer reads as if a bundle cannot own modules
  - `bundles/government/government.md`: Done — government is composition plus bundle modules, not umbrella-only
  - `libraries/`: Done — removed; instance packs are bundle modules
  - `modules/rights/law/law.changelog.md`: Pending — its propagate still pointed at `libraries/` and at dual-maintaining Memar society
  - Memar `docs/society/` and `docs/README.md` society subsection: Done — invert-path rewrite of `main` and force-push `origin/main` `50e15b1` → `46196ec`; local backup at `memar-backup-before-society-purge.git`
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — claimed, decided
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — recorded

#### What changed
`bundles.md` now states that `modules/` is a role (base rules of the container), that a bundle may introduce `bundles/<name>/modules/` without becoming a kernel type, that this folder's membership list is not a closed taxonomy, and that former Memar society requirement pages land as named bundle modules per the table in the base document. The twelve Memar theme directories are recorded as a notebook grouping with no leftover rule; the skipped `docs/society/README.md` corpus operating rules (requirement-as-question, rejected-stays-visible, network-vs-consumer dependency direction, stable approach section-ids) remain constraints on the imported pages until rewritten. Memar `docs/README.md` in `d5888fd` added only the three-line `society/` register; after the invert-path rewrite its blob is identical to parent `15a9413` (`e28f1f0`). `e064798` touched only `docs/society/` files.

#### Deliberation
Owner: the earlier reading that only root `modules/` can hold modules was wrong. The same word at `bundles/X/modules/` means X's base rules. A page that is a law still needs computer code, so it is a module wherever it lives; it does not become "documentation" by sitting under a bundle.

Owner: do not copy Memar's `docs/society/<theme>/` tree as the destination shape. Transfer by the correct module home.

Owner: a bundle introducing modules is allowed and should be written here so the question does not recur. Knowledge-management remaining composition-only does not forbid government (or energy, land, …) from owning modules.

Owner: spread the corpus across existing and new bundles by concept. The society umbrella was a false grouping. The `bundles/` cut itself is not final: `economy/` likely dies because kernel `modules/economics/` already holds the types, and civic economic policy belongs as government modules that *use* those types.

Owner: transplant the Memar society commits into this repository, then delete those commits from Memar's history including GitHub, so the mistaken placement is not in that history at all.

Owner (close of transfer): the twelve theme folders have no leftover rule to rebuild here. The skipped society README was corpus operating rules, not a folder map. Audit of `d5888fd` / `e064798`: the only non-society file was `docs/README.md`, and that diff was only the three-line folder register.

#### Considered and not done
- Fourth root `libraries/` for instance packs — rejected: a statute with computer code is a module of the bundle that runs it, not a non-module catalog.
- Dumping the whole corpus on `bundles/society/modules/` — rejected: that re-welds the false umbrella.
- Landing economic-policy pages in `bundles/economy/` — rejected: that bundle is the leftover cut, not the destination.

### law-validity left government for plugable
- Time: 2026-09-21T14:25:00Z
- Type: moved
- Cited:
  - [Law Validity Changelog](../modules-plugable/rights/law-validity/law-validity.changelog.md) - Relation: Evidence: the git mv and the owner reason
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — moved

#### What changed
`git mv bundles/government/modules/law-validity modules-plugable/rights/law-validity`. The import landing table in the base document is left as the record of *where the Memar page first landed*; later placement lives here. A full pass of other imported modules (which are general organisational capabilities vs settlement statutes) is still open.

#### Deliberation
Owner: some concepts went to bundles too early. Time/validity of a law is needed by many organisations, not only Geniuses.Group. Plugable restores that importance without making duration a kernel type.

### Wholesale plugable pass closed
- Time: 2026-09-21T14:29:00Z
- Type: clarified
- Cited:
  - [Law Validity](../modules-plugable/rights/law-validity/law-validity.md) - Relation: Evidence: the only high-confidence wholesale move from this pass
- Propagates to:
  - `modules/rights/law/law.changelog.md`: Done — its Partial on remaining candidates is closed here
  - `modules/rights/law/law.handoff.md`: Done — duration remains the only plugable move from this import
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — requested the pass, exemplar was duration
  - [Grok](../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — classified, recorded

#### What changed
Fifty-eight imported bundle modules classified. The only high-confidence wholesale `git mv` is duration, already at `modules-plugable/rights/law-validity`. No imported page is a missing kernel type. Settlement fabric stays in-bundle. Membership and judiciary remain split questions in the handoff, not folder moves. The fifty-eight-row list is not kept as a document.

#### Deliberation
Owner asked for a full review of what landed in bundles too early, with `git mv` so history is not dropped. Duration was the exemplar. The pass found no second module that is a general organisational capability *as a whole folder*. Moving membership or judiciary wholesale would relocate Geniuses.Group citizenship gates and this package's court ladder as if they were reusable types; those types already live in kernel identity/group/`case`.

#### Considered and not done
- `git mv` of `membership-and-identity` or `judiciary-and-dispute` — rejected this pass: medium-confidence *split*, needs owner confirmation, not a folder move.
- Persisting the fifty-eight-row inventory as a table in `bundles.md` — rejected: a derivative cache of the filesystem.

### Bundle-promotion trigger left open
- Time: 2026-10-08T09:05:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) — decided

#### What changed
`bundles.handoff.md` gained the open question of when a bundle composition acquires enough unique semantics that a piece must graduate into a real module. A bundle owns no kernel schema; a piece graduates only once it already owns identity, lifecycle, authorization, and processing that no existing module owns. The retired session slip `____Chats/2026-09-21-society-transfer.md` is no longer cited and its pointer was removed from `bundles.handoff.md`; the slip recorded that its content lives in `bundles.md` and this changelog.

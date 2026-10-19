# Organization Handoff

## Topic & Purpose
Go → Khayyam conversion of `modules/identity/organization/` (2026-10-02). What the domain's three `.kh` files say in Khayyam, what could not be settled, and what would have to change in other domains to finish it.

## Status
Protocol converted. The two `edges/` label files were deliberately given no Khayyam — see "Edge label vocabularies" below.

## Converted

- `protocol/dt-uuid.kh` — `UserUUID` included from `modules/identity/user/protocol/dt-uuid.kh`; `Field_OrganizationUUID` with `OrganizationID`; `Field_OrganizationOwnerID` with `OrganizationOwnerID`. No `cp` (rule 1), no method bodies (rule 2).

## Decisions

- **The organization's UUID is the user's UUID — included, not re-declared.** The Go said so itself (`type UUID user_p.UUID`); the [thing](../thing/README.md) domain says UUID "can be same with any other UUID domains ... It MUST be unique ID in all domains"; the [graph](../../storage/graph/README.md) data model types its vertices by that one UUID. Declaring an `OrganizationUUID` here would have been two abstractions claiming one concept, which is the architecture error the language names. The `org/` import prefix is rule 4 and is kept.
- **`Field_OrganizationID` → `Field_OrganizationUUID`.** Follows the one converted sibling ([user `dt-uuid.kh`](../user/protocol/dt-uuid.kh): `Field_UserUUID` + `UserID`) and the thing domain's `Field_ThingUUID`. Method names `OrganizationID` and `OrganizationOwnerID` are unchanged from the Go, so every implementing capsule keeps the same method set.
- **`Field_OwnerID` → `Field_OrganizationOwnerID`.** The Go field name and its method name disagreed (`Field_OwnerID` / `OrganizationOwnerID()`), and the plain name `Field_OwnerID` is also declared by [person `dt-uuid.kh`](../person/protocol/dt-uuid.kh) for a person owner. Qualifying it is the collision answer; the person side is not this domain's to change.

## Open — needs a decision outside this domain

1. **Who owns the base UUID abstraction.** `thing/protocol/dt-uuid.kh` is the documented home ("the base identifier for any other domains") but declares no Khayyam at all; the user pilot declared the concept locally as `UserUUID`; this domain now includes that. Until one owner exists, roughly a hundred `dt-uuid.kh` files each declare a `UUID`, and the qualified-names rule calls that one concept declared many times. My inclusion is a stopgap pointing at the wrong owner — `UserUUID` reads as the *user's* identifier in this domain's signatures.
2. **`UserUUID` is empty** (`tp UserUUID ab` with no requirements), so satisfaction is vacuous. Rule 6. Carried over unchanged from the pilot; needs a decision before implementers arrive — render, compare, and localization are the likely requirements.
3. **`Field_OrganizationID` → `Field_OrganizationUUID` breaks every consumer.** These name `org_p.Field_OrganizationID` and must be repointed: `modules-plugable/uri/username/widget/protocol/{data_model,business-services}.kh`, `modules-plugable/uri/number-itu/protocol/{data_model,business-services,storage}.kh`, `modules-plugable/gui/page-services/protocol/bs-get_detail.kh`, `modules-plugable/gui/page-products/protocol/gui-page.kh`, `modules-plugable/knowledge/analytics/edu-score/protocol/data_model.kh`, `modules-plugable/economics/discount/analytics/price-payable/protocol/data_model.kh`. Method names are unaffected, so only the composed abstraction name moves.
4. **Person's `Field_OwnerID` should step up to `Field_PersonOwnerID`** for the same collision reason.
5. **No `OrganizationModel` exists.** Thing and user each have `protocol/model.kh`; this domain has none, and no document describes what behavior an organization model requires. Declaring one now would be rule 6's empty abstraction.
6. **One product across organizations (2026-10-10, open).** When an invoice reaches every organization it involves, the product is registered in both, with the same identifier or a different one — the owner has not decided ([invoice exchange](../../economics/invoice/invoice.handoff.md#open-questions)). A fact moves from the organization that owns it to another organization's identity through a [follow](../thing/edges/follow/follow.md#open-questions) under the owner's AAA; how an owner authenticates an identity of another organization is open there. Both bear on item 1 and on whether one UUID is unique across organizations.

## Edge label vocabularies — no Khayyam written

`edges/organization.kh` and `edges/organization-relation-organization.kh` are `package label` constant enums. I wrote no Khayyam into them and left their Go blocks whole. Reasons:

- **A label is data, not code, in this repository.** The graph data model types an edge's label `Graph[thing_p.UUID, thing_p.UUID, label_p.UUID]`, [label](../../knowledge/label/README.md) says the module keeps only the attachment `(thing)-[:label]` and that registries of what a word means live elsewhere, and a label's human text lives in the [text](../../knowledge/text/README.md) domain. Declaring an edge label as a Khayyam type would put vocabulary back into code, which is what the Go `const` already did wrong.
- **Nothing to require of them.** There is no `Label` or `Edge` abstraction in this repository to attach a method to, so the honest conversion is the empty `ab` rule 6 forbids.
- **The vocabularies are unratified.** Recorded here rather than in the document:
  - `edges/organization.kh` — `Online`; a `TODO:::` note lists `School`, `Government`, `NGO` as further subtypes.
  - `edges/organization-relation-organization.kh` — `Branch`, `Agent`, `Franchise`: the kinds of relation between one organization and another.
- **`edges/organization.kh` is filed under the wrong kind-folder.** It is a classification on one organization — `(organization)-[:organization]->(---)` — and belongs under `edges-loop/`. `organization-relation-organization.kh` is correct where it is: both ends are organizations, so it is an ordinary edge, and the kind classification rides on it. A folder move belongs with the unapplied Phase 0 review, not with this conversion.
- **Neither edge has a document.** Phase 0's one-folder-per-edge convention (`edges/<name>/<name>.md`) is unmet for both; `edges/citizen/citizen.md` shows the shape. Same reasoning: a document-set change across domains is the main session's call.

## Tooling notes for whoever runs the frontend next

- **Every parameter needs a name.** The parser's `parseParamList` (`core/src/parse.ts:204`) reads name-then-type for every parameter, so `(UserUUID)` refuses with `declaration-form` while `(u UserUUID)` accepts. This is the sole cause of the pre-existing refusal on `modules/identity/user/protocol/dt-uuid.kh:15` — the pilot's `tp UserID mt (self Field_UserUUID) () (UserUUID)` accepts once the parameter is named `(u UserUUID)`. Not this domain's file to fix; worth one token in the user domain.
- **`unresolved-import` on this file is the missing manifest, not the import.** `modules/identity/organization/protocol/dt-uuid.kh` refuses on disk and accepts once the `org/` URI is made resolvable (verified with the target supplied as an override). Same cause as the standing `modules/identity/user/protocol/model.kh` refusal — rule 7's gate: no module manifest yet, so nothing answers for `org/`.
- **Go clue blocks left whole** in all three files, per the brief. The repository's own `go-clue-residue` rule would shrink them (a ported file carries only what the Khayyam has not yet carried) and commit `12b04aad` stripped them from the three pilots outright; `abstraction_bridge.py tidy --rule go-clue-residue` over this domain is the consistent follow-up.

## Open questions this conversion could not settle

- Is an organization's identity value really one UUID with every other domain's, or should a UUID's *domain* be part of it? Everything here assumes one concept, from the Go's own `type UUID user_p.UUID` and the thing domain's "MUST be unique ID in all domains". Nothing in the documents says an organization is not identified in its own namespace.
- `Online` as an organization label: is that "an organization with an online presence" (a property, near the label vocabulary `knowledge/label` keeps), or a kind of organization (a subtype, belonging with the `School`/`Government`/`NGO` note)? The Go files them together under one `package label` and do not say.
- `Branch` / `Agent` / `Franchise`: direction is unrecorded. Which end is the parent, and does `Agent` mean the second organization acts for the first, or represents it? Nothing in this domain or [its edges-loop document](edges-loop/organization/organization.md) answers it.

## Research 001 questions and next steps (2026-10-18)

### Status
Proposals only, from [organization.research.001.md](organization.research.001.md) (eleven scenarios, a thin kernel, five rival models and an identification axis, a mapping of every file including the Go residue in management/organization, eleven missing pieces sketched, twenty-five test scenarios, twelve contradictions). Nothing is ratified; every item is **Tentative**, **Explored** or **Deferred**, none Decided. The settled facts above (naming rationale, no identifier of its own, kind as a label, organization and group as settled) are not re-argued; the research reads "group of groups" as a claim about membership.

### Open Questions raised by the research
Each carries a recommended default and what it blocks; the full text is in the research's [Open Questions](organization.research.001.md#8-open-questions-for-the-owner). The first three change what the domain is.

1. **Does "organization" name only the participant (the declarer a role it plays), or also the authority scope or tenant?** Default: only the participant; no tenant concept; hosting is a separate capability. Blocks: the meaning of `Field_OrganizationUUID` and `Field_OrganizationOwnerID`, the siblings' "one node per organization", item 6 above.
2. **Must an organization have members, an owner, a body or a legal recognition?** Default: none; recognition is an optional relation; the opening definition is amended. Blocks: sole proprietor, DAO and endowment cases; the register service's founder rule.
3. **How is an organization identified from another organization's graph?** Default: each graph mints its own identity; links are `same_as` assertions; registry numbers are references with an issuer and a period. Blocks: item 6 and open question 1 above, invoice exchange, follow's identity proof.
4. **Who may form an organization, and may it form with no registry?** Default: any recognisable user, a guardian, a registry process or its participants, each leaving the requester. Blocks: the register service (stated three ways).
5. **Is recognition a separate, plural, dated fact of a society, and is a block its suspension?** Default: yes to both; block is society-relative. Blocks: `Representative`, `Transferred`, `Blocked`; the society pluggable.
6. **What are the stages of life, and is the dissolving stage kernel?** Default: formed, active, dissolving, ceased; dissolving a pluggable (Explored). Blocks: the `status/` folder, the finish-date idea.
7. **Is acting-for one capability in delegate for user, group and organization?** Default: yes. Blocks: formation, delegate open question 4.
8. **Do Branch, Agent and Franchise split to their owners (group hierarchy, ownership, contract with a group, acting-for)?** Default: yes. Blocks: the direction question above, `organization-relation-organization.kh`.
9. **Is `Online` a property and the kind vocabulary data?** Default: yes to both. Blocks: the two Open questions on `Online` above.
10. **Which changes keep an identity and which end it?** Default: rename, officers and society keep it; merger and split supersede many to many.
11. **What passes to a successor?** Default: a successor rule recorded as data.
12. **Do membership and citizenship live in group's record or in `citizen`?** Default: group's record; `citizen` a kind. Blocks: `citizen`, `national_of` direction.
13. **How is the "Government" name collision resolved?** Default: the existing pluggable stays an identifier; the hosting layer is named by its capability.
14. **What must an `OrganizationModel` require?** Default: the classification accessor (and the stage if kernel). Blocks: open item 5 above.
15. **Does `organization` stay a thin domain or become only a loop on user?** Default: stays thin.
16. **Who owns the plural `Field_OrganizationsUUID`, and when?** Default: this domain, next protocol wave (inventory was told so on 2026-10-08).
17. **Does an organization have credentials of its own?** Default: no; it acts through representatives.

### Next Steps
1. Owner answers questions 1 to 3 first; they change what the domain is.
2. On the defaults, still Tentative: write the domain's Model and Policies (classification, declarer scope), amend the opening definition, complete the loop's who and triggers; no `OrganizationModel` before question 14.
3. Settle recognition with the society pluggable and ask delegate to take representation once; resolve the Government naming.
4. Split the relation enum to its owners; make the kind vocabulary data.
5. Harvest and retire the management/organization Go residue after the destinations exist; add `Field_OrganizationsUUID`.
6. Reconcile contradictions C1 to C12 in the documents that own each side.

### Related Artifacts added
- [organization.research.001.md](organization.research.001.md) — the research (Update).
- [organization.changelog.md](organization.changelog.md) — the record of this addition (Update).

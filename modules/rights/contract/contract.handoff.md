# Contract Handoff

## Topic & Purpose
The boundary with law, and whether companions law already has — executive guarantee, computer code, and possibly goal and explanation — are the same relations a contract uses.

## Status
Active — the boundary of sources is stated on both types. The shared-edge question is not.

## Decisions
- A contract is a source of rights distinct from a right, and marriage is a contract. *(Decided — owner, earlier)*
- A contract that takes the place of an earlier contract uses [supersedes](../../identity/thing/edges/supersedes/supersedes.md) on thing. *(Decided)*
- When a contract yields to a law is a statute in [laws](../../../modules-plugable/rights/laws/laws.md), [contract within law](../../../modules-plugable/rights/laws/contract-within-law/contract-within-law.md), not a field of either type. *(Decided — owner)*
- The bare edge name code is not used. Human code is the human-language sentence. Computer code is the machine-checkable form. This domain's former code edge is computer code and points at a rule. *(Decided — owner)*

## Open Questions
1. **One computer-code edge or two.** The name is settled. This domain's machine-checkable form is [computer code](edges/computer_code/computer_code.md), `(contract)-[:computer_code]->(rule)`. Law's computer code points at text and is realized by rules. Are those one shared edge?
2. **Terms and human code.** [Terms](edges/terms/terms.md) points at text and also at a Solidity object. Human code is the human-language sentence. Is terms that sentence, a mix to split, or another relation? Goal and explanation on a law are separate from its human code. Contract has not said whether it needs those too.
3. **Executive guarantee.** Law has one. This domain has financial and settlement edges and no guarantee edge. Is settlement that path, or is the guarantee a shared edge still missing?
4. **Whose signature.** A contract is signed by its parties. A law is signed by the people the vote binds. If a companion is shared, the digest still has to say who signed this record.
5. **Supersedes across the boundary.** The type does not decide. An organization that wants a law to take the place of a contract adopts [law supersedes contract](../../../modules-plugable/rights/laws/law-supersedes-contract/law-supersedes-contract.md). [Contract within law](../../../modules-plugable/rights/laws/contract-within-law/contract-within-law.md) leaves the contract node in place and only refuses a contract that explicitly contradicts a law in force.
6. **Drafts that are contracts.** [Family](../../../modules-plugable/rights/family/family.md) and [marriage](../../../modules-plugable/rights/marriage/marriage.md) are contract drafts. If the companions are required of every contract the way they are required of every law, those drafts are incomplete until they carry them. That requirement is not decided.

## Related Artifacts
- [`contract.md`](contract.md) — type (Update only if a decision above graduates)
- [`../law/law.handoff.md`](../law/law.handoff.md) — the same questions from the law side (Related)
- [`../law/law.md`](../law/law.md) — law as the other source (Related)
- [`edges/computer_code/computer_code.md`](edges/computer_code/computer_code.md) — contract computer code (Related)
- [`../law/edges/human_code/human_code.md`](../law/edges/human_code/human_code.md) — law human code (Related)
- [`../law/edges/computer_code/computer_code.md`](../law/edges/computer_code/computer_code.md) — law computer-code edge (Related)
- [`../law/edges/executive_guarantee/executive_guarantee.md`](../law/edges/executive_guarantee/executive_guarantee.md) — law guarantee edge (Related)

## Go → Khayyam conversion (protocol layer)

### Status
All three `.kh` files in this domain accept under the Khayyam frontend. Two declarations are blocked on `computer/module` and two findings below are recorded rather than encoded.

### Converted
- `protocol/dt-uuid.kh` — `Field_ContractID` + `ContractID () (t ThingUUID)`
- `edges/form/protocol/data_model.kh` — `ContractExpertOpinion`, composing `Field_ContractID`, `Field_ExpertID`, `Field_Opinion`, `Field_Progress`
- `edges/terms/protocol/dt-data.kh` — `ContractTermsData`, its three fields, `Array_ContractTermsData`, and `Field_ContractTerms` + `ContractTerms`

### Decisions
- **The contract's identity is `ThingUUID`.** The Go declared `type UUID group_p.UUID` with the comment "UUID is group to support many functionality like chats, expert opinion, ...". `group_p.UUID` was itself `user_p.UUID`, so the alias reached nothing but a different domain's name for one identifier; it now imports the owner, `identity/thing/protocol/dt-uuid.kh`. The comment is a stale note about which alias to reach through and is obsolete. **If "a contract is a group's record" was ever meant rather than being a convenience, that is a model question for [contract.md](./contract.md), not a UUID alias** — and [management/group](../../../management/group/protocol/dt-uuid.kh) is not converted.
- **The expert opinion's fields became field abstractions.** The Go wrote `ExpertID()`, `Opinion()` and `Progress()` as bare methods on the interface. They are now `Field_ExpertID` / `Field_Opinion` / `Field_Progress`, so the generator the governing rules require can produce the bodies. [form.md](edges/form/form.md) confirms `ContractExpertOpinion` is one of the form labels, so this is a form's record and not a contract sub-type.
- **`Progress` returns `Myriad`** from `memar/modules/math/per/myriad.kh`. That file declares `Myriad` as an **empty** abstraction — the rule-6 smell — and its `Calculate` behaviour is still only in its Go block. So `Progress` names a value with no behaviour behind it yet. Not this domain's file to fix.
- **Terms data is a record of three field abstractions.** The Go's `Data` was a struct of unexported fields (`label`, `id`, `moduleID`); it is `ContractTermsData` now, and `Data() []Data` became `ContractTerms () (d Array_ContractTermsData)` because a Go `[]T` is not `Array_Dynamic T`. `moduleID` returns `ThingUUID`; when `computer/module` converts it should become that domain's `Field_ModuleID` instead.

### Findings
1. **Legal meaning encoded as structure — not converted, deliberately.** [terms.md](edges/terms/terms.md): "If the `contract` have `template` label, terms will be in blank format; if the `contract` don't have `template` label, terms will just data to fill base terms." That is a rule about when terms are blank and when they are filled, and today the only way to reach it is to compose `Field_ContractTermsLabel` and read the label. [form.md](edges/form/form.md)'s "MUST NOT any change in LifeCycle_StableRelease, new template MUST born if any changes required" is the same kind of rule. Neither was written as a method; a legal rule is content, and the contract-shape declarations here say nothing about either.
2. **`edges/status` is filed as an edge and is not one.** [status.md](edges/status/status.md) says so itself: the six labels are a value list, and the ratified home is loop-edge folders under `contract/status/<name>/` read through `knowledge/status`. It carries no `.kh` and none was written. This is the migration map's high-confidence kind-error class (statuses filed under `edges/`).
3. **"Service: fulfill the obligation"** — the Go comment in `protocol/dt-uuid.kh` — is already in [settlement_by.md](edges/settlement_by/settlement_by.md) under Services. Extracted; no comment was left above the code.

### Open Questions added by the conversion
1. **Is a contract a group's record?** The `group_p.UUID` alias suggested it once; nothing in [contract.md](./contract.md) says so. Decide before `management/group` converts, or the alias question will reappear.
2. **Whose terms are these** — `Field_ContractTerms` has no owner declared; whether terms hang off the contract node or off the form is not written anywhere.
3. **Whether the two file names match what they hold.** `edges/form/protocol/data_model.kh` holds an expert-opinion form specifically, not the form relation generally; `edges/terms/protocol/dt-data.kh` holds the terms value record, not the edge. Neither name is wrong under this repository's "the path is the owner" convention, but a reader arriving at `data_model.kh` expecting the form relation will not find it.

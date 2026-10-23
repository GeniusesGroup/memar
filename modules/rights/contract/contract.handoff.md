# Contract Handoff

## Topic & Purpose
The boundary with law, and whether companions law already has — executive guarantee, computer code, and possibly goal and explanation — are the same relations a contract uses.

## Status
Active — the boundary of sources is stated on both types. The shared-edge question is not.

## Decisions
- A contract is a source of rights distinct from a right, and marriage is a contract. *(Decided — owner, earlier)*
- A contract that takes the place of an earlier contract uses [supersedes](../../identity/thing/edges/supersedes/supersedes.md) on thing. *(Decided)*
- When a contract yields to a law is a statute in [laws](../../../modules-plugable/rights/law/laws/laws.md), [contract within law](../../../modules-plugable/rights/law/laws/contract-within-law/contract-within-law.md), not a field of either type. *(Decided — owner)*
- The bare edge name code is not used. Human code is the human-language sentence. Computer code is the machine-checkable form. This domain's former code edge is computer code and points at a rule. *(Decided — owner)*

## Open Questions
1. **One computer-code edge or two.** The name is settled. This domain's machine-checkable form is [computer code](edges/computer_code/computer_code.md), `(contract)-[:computer_code]->(rule)`. Law's computer code points at text and is realized by rules. Are those one shared edge?
2. **Terms and human code.** [Terms](edges/terms/terms.md) points at text and also at a Solidity object. Human code is the human-language sentence. Is terms that sentence, a mix to split, or another relation? Goal and explanation on a law are separate from its human code. Contract has not said whether it needs those too.
3. **Executive guarantee.** Law has one. This domain has financial and settlement edges and no guarantee edge. Is settlement that path, or is the guarantee a shared edge still missing?
4. **Whose signature.** A contract is signed by its parties. A law is signed by the people the vote binds. If a companion is shared, the digest still has to say who signed this record.
5. **Supersedes across the boundary.** The type does not decide. An organization that wants a law to take the place of a contract adopts [law supersedes contract](../../../modules-plugable/rights/law/laws/law-supersedes-contract/law-supersedes-contract.md). [Contract within law](../../../modules-plugable/rights/law/laws/contract-within-law/contract-within-law.md) leaves the contract node in place and only refuses a contract that explicitly contradicts a law in force.
6. **Drafts that are contracts.** [Family](../../../modules-plugable/rights/family/family.md) and [marriage](../../../modules-plugable/rights/marriage/marriage.md) are contract drafts. If the companions are required of every contract the way they are required of every law, those drafts are incomplete until they carry them. That requirement is not decided.

## Open Questions added by Contract Research 001
Full wording, recommended defaults and what each blocks are in [contract.research.001.md](contract.research.001.md#open-questions); the research is unratified. Ordered by what they change.

7. **Is agreement a state derived from assents on one digest, the assent the shared atom, contract the node?** Default: yes; no Agreement node (answers the question in [contract.md](contract.md#open-questions)). Blocks: offer-and-acceptance (X6), group admission, task acceptance, invoice answer, law vote.
8. **Are a contract's terms frozen at the first assent, a change being a new contract that supersedes or amends?** Default: yes. Blocks: the kernel, `amends`, the invoice relation.
9. **Is the party record a membership of the contract, with witness, expert and arbitrator as a separate non-party relation?** Default: yes. Blocks: the five side folders, the three participant folders, the conversion question "is a contract a group's record" (default: no).
10. **When text and executable form differ, which binds?** Default: an assent binds to the digest of every form; a divergence refuses opening for assent. Blocks: questions 1 and 2 above, `computer_code`.
11. **Do the contract status words reduce to proposed, in force and ended with cause, partly signed and legal action being readings?** Default: yes. Blocks: [status.md](edges/status/status.md), the single source of "legal action" (the case edge).
12. **Is a partial change an `amends` relation and a party change a novation by the others' assent?** Default: yes. Blocks: addenda, late joiners.
13. **Is silence an acceptance only where an organization's rule says so?** Default: yes. Blocks: click-wrap terms, invoice answer.
14. **Does extension of a contract to non-parties by law belong to a statute and a `concerns` relation, not to `law supersedes contract`?** Default: yes. Blocks: collective agreements, beneficiaries.
15. **Does the rights category wait on `obligation` and `license` until a case breaks "right plus correlative duty"?** Default: wait; name the capability for `financial` and `settlement_by`. Blocks: boundaries questions 2 and 3.
16. **Is `origin_is` one relation defined once on thing?** Default: yes. Blocks: origin fields in title, delegation, obligation.
17. **Do title and record stewardship differ, and is ownership a node?** Default: yes to both; see [ownership handoff](../ownership/ownership.handoff.md). Blocks: the `owner` edge, TH.8, RU.9.
18. **Is authority three homes (acting-for in delegate, stewardship as a rule, permission in authorization), and is a delegation a record?** Default: yes to both; see [delegate handoff](../delegate/delegate.handoff.md). Blocks: the synthesis's X3.

## Proposed Next Steps
1. Owner answers questions 7, 17 and 18 first; they change what the three domains are.
2. Rewrite the opening paragraphs of [contract.md](contract.md), [ownership.md](../ownership/ownership.md) and [delegate.md](../delegate/delegate.md) once 7, 17 and 18 are answered (not done here).
3. Queue a session for the shared assent capability with the sibling domains that hold copies (group, task, invoice, law).
4. Reclassify the edge folders as in finding 5 of the research, after the answers; move nothing before.
5. Take the `origin_is` question to the thing domain.
6. Write no `ContractModel`, `OwnershipModel` or `DelegateModel` until the kernels are ratified (Khayyam rule 6).

## Related Artifacts

- [`contract.research.001.md`](contract.research.001.md) — agreement, title and authority research; questions 7 to 18 above (Related)
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
- **The contract's identity is `ThingUUID`.** The Go declared `type UUID group_p.UUID` with the comment "UUID is group to support many functionality like chats, expert opinion, ...". `group_p.UUID` was itself `user_p.UUID`, so the alias reached nothing but a different domain's name for one identifier; it now imports the owner, `identity/thing/protocol/dt-uuid.kh`. The comment is a stale note about which alias to reach through and is obsolete. **If "a contract is a group's record" was ever meant rather than being a convenience, that is a model question for [contract.md](./contract.md), not a UUID alias** — and [management/group](../../management/group/protocol/dt-uuid.kh) is not converted.
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

## Health-directive labels (idea, not ratified)
- State: carried 2026-10-19 from organization's `modules/knowledge/knowledge.md` → Idea backlog, when organization merged into memar (task 20261019-T103359Z-18676 recorded it in [knowledge.changelog.md](../../knowledge/knowledge.changelog.md)). Two bare label comments, "Life support" and "Donate", sat in the knowledge category's root protocol package with no semantics. Review discipline per [vocabulary discipline](../../management/vocabulary-discipline.handoff.md).
- Questions: what capability owns an advance health directive: a signed instrument of Contract, a label set on the person record, or something else? Until who may set it and what it triggers is written, both labels fail the no-bare-edges test and stay backlog, not schema. And why did the category root carry them at all: a misplaced protocol?

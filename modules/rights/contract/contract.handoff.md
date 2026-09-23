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

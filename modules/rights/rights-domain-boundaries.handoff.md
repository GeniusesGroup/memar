# Rights Domain Boundaries Handoff

## Topic & Purpose
Drawing the internal boundary of the `rights` category: which domains it contains, which concepts reduce to edges/rules, and how rights connect to neighboring categories (accounting, estate). Produced from a session that was deliberately a *test of the assistant's mastery of Memar's method* — Omid stated no position of his own in it.

## Status
Blocked — awaiting Omid's own model of the rights category, which was never stated in the source session. Everything below is the assistant's proposal under test, not a decision.

## Decisions
None. The entire content is a **proposal awaiting review** (confidence: Explored-but-unresolved throughout). Its structural commitments live in [`README.md`](README.md) ("Boundary notes" — the three items Omid *did* confirm in the estate chat: accounting outside rights, estates as subjects not members, rights-first ordering) and in the per-module open questions:
- [`ownership/README.md`](ownership/README.md) — bare edge vs node vs rights-creating relation
- [`contract/README.md`](contract/README.md) — Contract ≠ Right; marriage-as-contract (Omid-confirmed)
- [`law/README.md`](law/README.md) — law as independent normative source, not right's attribute; Rule-vs-Law boundary
- [`delegate/README.md`](delegate/README.md) — Authority ≠ Permission
- [`case/Readme.MD`](case/Readme.MD) — the Event → Liability → Obligation chain question

## Proposed domain map (Explored-but-unresolved — the proposal under test)
- **Ownership** (near-certain per proposer): who holds what right over what; may be a legal relation with subject/object/scope/fraction/start-end/origin rather than a bare `owns` edge.
- **Contract**: agreed relation between parties creating rights and obligations; one *origin* of rights among several.
- **Law** (with caution): rules determining which rights/obligations are possible, valid, forbidden, enforceable.
- **Obligation** (against common terminology): not the inverse of Right; `Right ──correlative_to──> Obligation` as a candidate fundamental edge; origins: contract, law, court decision.
- **Permission** (?): independent domain, kind of Right, or rule — must be settled by the attribute-or-edge test (parking spot, easement, software license).
- **Authority** (?): "may validly act on behalf of" — distinct from Permission; may belong to the delegate/agency machinery.
- **Liability** (?): `Event ──gives_rise_to──> Liability ──creates──> Obligation`; may be a case-domain matter rather than a rights domain.
- Deliberately excluded: License (candidate special Permission), Transfer (an operation changing rights), Share (an accounting unit), Registration (a mechanism creating/proving/publishing a right's state).
- Accounting deliberately outside the category: it records/measures rights, does not create them.

## Open Questions
1. **Blocking**: Omid's own model of the Rights category — the entire map awaits his reaction; the proposal expects large parts to be rejected (his estate-session positions already partially contradict its framing).
2. Does Obligation deserve a domain, or does a Right-with-correlation-edge model suffice until a case breaks it?
3. Where does Permission's attribute-or-edge test get run (which cases first)?
4. Do Transfer/Registration enter the map as operations/mechanisms once modeled?
5. Reconcile this map with the existing `modules/rights/` subfolders (case, contract, delegate, law, ownership) — names and structure.

## Assumptions
- **Hohfeld's jural framework** is the likely backbone for the Right/Permission/Authority/Liability split — stability: Unexamined (not yet evaluated against it).
- **The existing module subfolders are a reasonable starting inventory** — stability: Weak; the map may restructure them.

## Key Definitions Established
- Omid-confirmed (from the estate chat, recorded in [`README.md`](README.md)): rights exist first; ownership/legal relations arise from rights. Marriage is a contract like any other.

## Proposed Next Steps
1. Omid states his own rights model (the test's missing half).
2. Diff the assistant's map against it: which domains survive, which reduce to edges/concepts/rules.
3. Run the attribute-or-edge test on Permission with concrete cases.
4. Reconcile surviving structure with the existing subfolders.

## Related Artifacts
- [`README.md`](README.md) — boundary notes (Update after the diff)
- [`ownership/README.md`](ownership/README.md), [`contract/README.md`](contract/README.md), [`law/README.md`](law/README.md), [`delegate/README.md`](delegate/README.md), [`case/Readme.MD`](case/Readme.MD) — per-module questions (Review)
- [`normative-bootstrap.handoff.md`](normative-bootstrap.handoff.md) — Law/Consent/Authority at founding time (Related)
- [`../identity/estate/estate.handoff.md`](../identity/estate/estate.handoff.md) — the estate side of rights-first ordering (Related)

## Notes
- Prior art recorded with the proposal: LADM (RRR structure), Hohfeld jural relations, ownership-vs-license practice.
- The source chat (2026-09-05) is retired; its full content is here and in the per-module files above.

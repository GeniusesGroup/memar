# Structural Material System Changelog

## Changelog

### Record created by requirements migration
- Time: 2026-09-13T14:26:00Z
- Type: created
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed (all source ideas and materials)
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — migrated

#### What changed
The document was created by migrating the requirement's approaches out of the per-idea record store, texts preserved verbatim. Approaches migrated in document order (the id ledger was retired 2026-09-15; sections speak for themselves):

Cross-document links created at migration (from the records' syn/links fields):
- buildings/placement-and-routing-of-service-flows.md; buildings/structural-material.md; form-and-land/buildable-share-and-density-allocation.md; form-and-land/sound-environment.md

### English conceptual upgrade and reviewer critique
- Time: 2026-09-14T00:00:00Z
- Type: rewrote, clarified, reviewed
- Propagates to:
  - buildings/daylight-to-interiors.md; form-and-land/sound-environment.md; water-and-matter/treatment-and-return-of-used-waters.md: Pending — these documents still link the sections' old Persian anchors; incoming links are to be re-pointed to the new English headings when those documents' own passes run (the same pending-sync state the earlier upgrades left; see the 2026-09-13 audit's cleanup gate).

- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — rewrote, critiqued

#### What changed
The document was rewritten as a conceptual English upgrade: body language set to English; the template Abstract and Motivation replaced by claims derived from this document's own Explanation; "The problem the answers share" sharpened onto its three axes (what carries load, what the surface treatment is, where the carbon is booked); a "How the approaches collide and compose" section added. Every claim, number, unit and attribution of the Persian source survives; the numeric-token self-check confirms zero removals (multiset of digit tokens preserved; additions only restate source figures). Legacy-reference sweep: the body carried no bare legacy-id tokens and no unresolvable ids; outgoing links to [Thermoactive deep load-bearing foundations (Energy Piles & Diaphragm Heat Exchangers)](../energy/thermal-sources-and-storage.md#thermoactive-deep-load-bearing-foundations-energy-piles--diaphragm-heat-exchangers) were re-pointed to the target's current heading after that record's own upgrade.

The following analytical fields are reviewer-authored (Omid Hekayati has not yet confirmed them); per the owner's ruling of 2026-09-14 no inline flags appear in the body:

- "Hybrid structure: impervious reinforced concrete below grade, mass engineered timber above (Hybrid Concrete-Mass Timber)": fit, anchor, hook
- "Permanent mass-timber formwork left in place as thermal insulation and finished facade (Permanent Mass Timber Shuttering & Carbon Lock)": fit, anchor, hook

The collision section itself is reviewer-authored analysis grounded in the two records' own texts (the shuttering prerequisite against the hybrid's CLT deck; the two carbon ledgers), and its owner decision is opened as handoff Q1–Q3; a reviewer doubt on the "CO2 lock equivalent to total cement consumed" metric is recorded in the handoff (Q2), not settled in the body. A paired handoff, `structural-material.handoff.md`, was created.

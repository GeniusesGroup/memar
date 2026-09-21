# Authority for the Indoor Climate Signal Changelog

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
- buildings/daylight-to-interiors.md; buildings/placement-and-routing-of-service-flows.md; food/meals-and-shared-cooking.md; information-systems/observability-of-flows.md; living-and-culture/continuous-health-watch.md

### English conceptual upgrade and reviewer critique
- Time: 2026-09-14T00:00:00Z
- Type: rewrote, clarified, reviewed
- Propagates to:
  - buildings/dwelling-provision-and-adaptability.md: Done — repointed in the 2026-09-15 conformance pass.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — rewrote, critiqued

#### What changed
The document was rewritten as a conceptual English upgrade: body language set to English; Abstract and Motivation re-derived from this document's own Explanation (the shared neutral-requirement boilerplate replaced by the page's own claim — the setpoint as a claim about a body, and the two records as one control loop with an asymmetric dependency); the shared question sharpened to its three open edges (authority, actuation, data); a cross-approach collision-and-composition section added (the forced adjudication order of controller and bus; the sub-0.5-degree tolerance versus the 20-percent saving reconciling in exactly one reading; the plural-body authority question as one question two answers; physiological-data custody against the dependency-direction doctrine); both approach blocks preserved field by field with every claim, number, unit and attribution intact — zero removals. Terminology normalized per policy: society, never "city" as the unit; existing-fabric rendering for «شهر موجود»-type references. Headings carry strippable legacy-id suffixes (([Bio-adaptive control of the indoor…](climate-signal-authority.md#bio-adaptive-control-of-the-indoor-climate-on-operative-temperature-and-body-physiology-bio-adaptive-control)), ([Environmental-metabolic data bus for optimizing…](climate-signal-authority.md#environmental-metabolic-data-bus-for-optimizing-hvac-operative-temperature-environmental-metabolic-data-bus-for-hvac))) per the migration map, kept until every cross-reference is rewritten; no bare legacy-id tokens appear in the body (none were present in the Persian source). [Environmental-metabolic data bus for optimizing…](climate-signal-authority.md#environmental-metabolic-data-bus-for-optimizing-hvac-operative-temperature-environmental-metabolic-data-bus-for-hvac)'s first prerequisite retains its original link target despite reading as a migration misfire — flagged in the handoff for owner confirmation rather than silently corrected. A reciprocal Related-documents entry for `meals-and-shared-cooking.md` was added to reflect [Environmental-metabolic data bus for optimizing…](climate-signal-authority.md#environmental-metabolic-data-bus-for-optimizing-hvac-operative-temperature-environmental-metabolic-data-bus-for-hvac)'s prerequisite link (reciprocity per the audit's rules; noted in the meals document's own upgrade entry).

The following analytical fields are reviewer-authored (Omid Hekayati has not yet confirmed them); inline flags were moved out of the body per the owner's ruling of 2026-09-14:

- "Bio-adaptive control of the indoor climate on operative temperature and body physiology (Bio-Adaptive Control)": hook
- "Environmental-metabolic data bus for optimizing HVAC operative temperature (Environmental-Metabolic Data Bus for HVAC)": fit, anchor, hook

The paired handoff (`climate-signal-authority.handoff.md`) was created in the same pass and carries the reviewer's critiques, including the mislinked-prerequisite finding. Numeric-token self-check: every numeric token of the Persian source survives in the English body (loss-free).

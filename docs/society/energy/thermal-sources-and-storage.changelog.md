# Thermal Sources and Storage Changelog

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
- energy/directed-energy-transfer.md; energy/energy-carriers-and-grid-posture.md; energy/large-generation-site.md; energy/solar-tower-purpose.md; energy/thermal-sources-and-storage.md; form-and-land/ground-surface-treatment.md; form-and-land/which-plane-carries-which-flow.md

### Battery definition fixed and elevated-water storage approach added
- Time: 2026-09-14T00:00:00Z
- Type: added, clarified
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — recorded

#### What changed
Terminology section added: "battery" = any system taking energy in the off-peak window and returning it at peak (chemical cells are one instance; gravity, thermal mass and compressed air are the platform's native ones). New approach "Elevated water reservoir — night-pumped gravity battery co-serving green-space irrigation" inserted; owner-dictated verbatim.

### English conceptual upgrade and reviewer critique
- Time: 2026-09-14T00:00:00Z
- Type: rewrote, clarified, reviewed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — rewrote, critiqued
- Propagates to:
  - buildings/structural-material.md, buildings/placement-and-routing-of-service-flows.md, energy/directed-energy-transfer.md (three lines and its handoff's Q6), water-and-matter/water-supply-and-security.md: Done — inbound links repointed in the 2026-09-15 conformance pass.
  - energy-carriers-and-grid-posture.md: Done - this document's outbound [Energy stabilization by carrier separation…](energy-carriers-and-grid-posture.md#energy-stabilization-by-carrier-separation-and-time-shifting-of-consumption-energy-time-shifting)/[Banning retail gas distribution in…](energy-carriers-and-grid-posture.md#banning-retail-gas-distribution-in-the-society-and-preventing-exergy-destruction-exergy-destruction) links and the inbound-side [Seasonal heat and cool storage…](thermal-sources-and-storage.md#seasonal-heat-and-cool-storage-in-aquifers-and-plain-sand-layers-ates--utes) references were re-pointed to the new English anchors in the same session (both documents upgraded together).

#### What changed
**Source:** dictated by Omid (ZCode session 2026-09-13) — recorded precautionarily so it survives the gap between sessions

Reviewer-authored analytical fields (not yet confirmed by the owner):
- "Seasonal heat and cool storage in aquifers and plain sand layers (ATES / UTES)": narrative hook.
- "Thermoactive deep load-bearing foundations (Energy Piles & Diaphragm Heat Exchangers)": fit, anchor, hook.
- "Mechanical energy storage on gravity blocks in subterranean shafts (Deep-Shaft GES)": fit, anchor, hook.
- "Reversible solid-oxide fuel cells and seasonal hydrogen storage (Deep Subsurface rSOC)": fit, anchor, hook.
- "Ice-crystal and skimo living zones in the depths as a winter exergy heat sink (Subterranean Cryo-Zone and Ice Sink)": fit, anchor, hook.
- "Elevated water reservoir — night-pumped gravity battery co-serving green-space irrigation": tags, scale (derived from the record's own text), fit, anchor, hook.

The handoff (`thermal-sources-and-storage.handoff.md`) was created in this pass. It opens six questions the upgrade surfaced rather than answered: the shared-ground thermal budget ([Seasonal heat and cool storage…](thermal-sources-and-storage.md#seasonal-heat-and-cool-storage-in-aquifers-and-plain-sand-layers-ates--utes) vs [Thermoactive deep load-bearing foundations](thermal-sources-and-storage.md#thermoactive-deep-load-bearing-foundations-energy-piles--diaphragm-heat-exchangers)), the minus-10 tenancy ([Mechanical energy storage on gravity…](thermal-sources-and-storage.md#mechanical-energy-storage-on-gravity-blocks-in-subterranean-shafts-deep-shaft-ges)/[Reversible solid-oxide fuel cells and…](thermal-sources-and-storage.md#reversible-solid-oxide-fuel-cells-and-seasonal-hydrogen-storage-deep-subsurface-rsoc)/[Ice-crystal and skimo living zones…](thermal-sources-and-storage.md#ice-crystal-and-skimo-living-zones-in-the-depths-as-a-winter-exergy-heat-sink-subterranean-cryo-zone-and-ice-sink)), the battery-counting boundary ([Elevated water reservoir — night-pumped…](thermal-sources-and-storage.md#elevated-water-reservoir--night-pumped-gravity-battery-co-serving-green-space-irrigation)'s schedule abstraction vs the device records), [Reversible solid-oxide fuel cells and…](thermal-sources-and-storage.md#reversible-solid-oxide-fuel-cells-and-seasonal-hydrogen-storage-deep-subsurface-rsoc)'s 65-degree water against the 40-to-60 bus band, the irrigation-versus-arbitrage priority on dead-calm nights, and a reviewer critique of [Thermoactive deep load-bearing foundations](thermal-sources-and-storage.md#thermoactive-deep-load-bearing-foundations-energy-piles--diaphragm-heat-exchangers)'s "100% drilling cost" metric as a cost transfer rather than a cost cut.

### Source recovery from transfer audit
- Time: 2026-09-14T00:00:00Z
- Type: recovered
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed (source author)
  - [Qwen](../../../CONTRIBUTORS.md#qwen) (qwen3.8-flash via ZCode) — recovered

#### What changed
The transfer audit found one lost owner approach: the compressed-air member of the non-chemical battery family, named in the Terminology section ("compressed air") but never recorded as an answer — the energy-competition proposal lists «تولید هوا یا گاز فشرده» among the non-chemical batteries charged in off-peak windows «نه صرفا محدود به شب ها» and spent at peak «عملا حذف مفهوم پیک مصرف». Added as "Compressed-air energy storage: the fifth non-chemical battery — air compressed in off-peak windows and returned at peak, the concept of peak itself abolished (Compressed-Air Battery)" — id (new; next free owner id, claimed lowest after [Abolition of the hotel concept:…](../governance/resident-matching-and-mobility.md#abolition-of-the-hotel-concept-one-continuum-of-stay-lengths-from-a-day-to-years-with-reserved-short-guest-capacity-one-continuum-of-stays)) — the Terminology line now links it, and the Abstract's and Motivation's answer counts were extended to seven; the existing collision paragraphs (the shared negative floor, the ladder by substrate) were left as written; no text removed or softened. In the new record the Mechanism, Metrics, Prerequisites, Conventional-model flaw and Tags carry the owner's claims (translated, key clauses quoted in the original); Fit & substrate, Cognitive anchor and Narrative hook are reviewer-authored and unconfirmed. The thermal-accounting of compression heat is left open by the source itself and marked so in the Mechanism — the record is written as a network client of [Fifth-generation district heating/cooling loop for…](directed-energy-transfer.md#fifth-generation-district-heatingcooling-loop-5gdhc--thermal-bus-for-binding-chillers-to-heat-sinks)/[Seasonal heat and cool storage…](thermal-sources-and-storage.md#seasonal-heat-and-cool-storage-in-aquifers-and-plain-sand-layers-ates--utes), not as a decided design.

#### Considered and not done
- Absorption chillers as the thermal-lift device for recovered surplus heat (چیلرهای جذبی — the same clause in the energy proposal, Yalda-Life-Complex-Proposal.docx and شهر_سبز.docx) were weighed for this page as a sixth non-chemical mechanism and left out: on the corpus the lift is bought with electrically driven heat pumps bound to the thermal bus, not with a second machine class. The full disposition is recorded in energy/directed-energy-transfer.md's changelog, the page whose [Fifth-generation district heating/cooling loop for…](directed-energy-transfer.md#fifth-generation-district-heatingcooling-loop-5gdhc--thermal-bus-for-binding-chillers-to-heat-sinks) the chiller route competes with.

# Water Supply and Security — Handoff

Companion of `water-supply-and-security.md`.

## Open Questions
1. **Who holds the strategic reserve — the aquifer or a surface volume?** The page's sharpest collision: none of the three records ([Solar Industrial Desalination](water-supply-and-security.md#central-solar-desalination-and-water-sweetening-plant-solar-industrial-desalination), [Desiccant AWG](water-supply-and-security.md#atmospheric-water-harvesting-by-low-grade-waste-heat-recovery-desiccant-awg-via-5gdhc), [Telemetry-Monitored ASR](water-supply-and-security.md#gravity-fed-aquifer-recharge-and-subsidence-control-by-injection-wells-and-piezometry-telemetry-monitored-asr)) carries the potable-reserve duty its question demands, and the bank-vs-buffer choice is already split across records (the ASR wells store below ground; the desalination plant injects product into the lake above it). Rule: underground bank (irreversibility argument — compacted storage cannot be rebuilt; telemetry is the audit) or a metered surface volume (auditability argument — the reserve that failed the conventional plain once is the one that exists only as head pressure). The missing number both sides need: the reserve volume and the days-without-rain horizon it must cover. *(Why: the requirement's second half has no holder, so no combined verdict is enforceable. Blocking: yes for the reserve doctrine and for the lake's potable share in `water-bodies-as-common-infrastructure.md`; no for the source questions.)*
2. **Does the desalination plant owe the settlement drinking water, or only high-purity product?** The plant record's own offtake list — hydroponic farms, the datacenter, the artificial lake — contains no household tap, yet the page's question is about drinking water. Is that an omission to amend in the mechanism text, or the intended architecture (drinking water produced downstream at the point of use)? *(Why: an adoption of this record "as written" silently decides the whole settlement's potable path runs through the lake or the dual-pipe network, which nothing here states. Blocking: yes for any verdict on the desalination record.)*
3. **Surface-versus-subsurface accounting boundary.** The lake's stored freshwater and the alluvial groundwater the injection wells fill are the same hydrological system in the same plain; the plant counts credit when it injects, the wells count credit when they recharge. Who owns the boundary rule (which ledger meters which cubic meter), and is the answer a clause here or an observability-architecture entry? *(Why: without it the settlement's balance can show one cubic meter twice — the false-statistics failure the plant's own flaw text accuses the pipeline model of. Blocking: yes for the combined adoption of desalination plus ASR.)*
4. **The harvester's "zero additional electricity" is borrowed from the energy ledger.** The AWG record's process power is zero only because the thermal bus delivers its 45-to-60°C regeneration heat; the cascade priority of that bus (which consumer gets the heat first, including this record's own share) is an abstract network rule owned by `energy/directed-energy-transfer.md`, not here. Should this page open a declared-need line (temperature band and hours of demand) toward that network record? *(Why: dependency direction requires the consumer to declare; today the band is in the AWG record but not addressed to the bus as a need. Blocking: no for the requirement; yes for any adoption of the AWG record.)*

## Decisions
- (none; no verdict recorded.)

## Extensions / anticipated work
- Once Q1's volume and horizon exist, a reserve arithmetic table (days of drinking demand vs. lake share, aquifer head and plant output) can be added to the Explanation without new claims.
- The ASR record's InSAR/piezometer telemetry pair is a candidate shared instrument for the water-bodies ledger's flood metrics; if both ledgers adopt it, consider a single observability hook rather than duplicated instrumentation.
- Cross-check the 2 mm/year subsidence threshold against the plain-wide numbers recorded in the supply-side geotechnical prerequisites when the Shiraz stratigraphy data is pulled.

## Assumptions
- Shiraz's night humidity of 50-to-70 percent and noon under-20-percent swing (AWG mechanism) hold at settlement scale — as asserted in the record; no independent measurement in the ledger (stability: Weak).
- The plain's brackish wells are renewable on the settlement's timescale when fed only by RO reject water and ASR return flows (stability: Unexamined).
- The lake's liner and aeration keep eutrophication out at hundreds-of-thousands-of-cubic-meter scale — a premise imported from `water-bodies-as-common-infrastructure.md` (stability: Weak).

## Proposed Next Steps
1. Owner: answer Q1 (reserve doctrine); its two named answers and the missing volume/horizon are written in the page's collision section.
2. Owner: settle Q2 (drinking duty) before any verdict on the desalination record.
3. Delegatable: draft the declared-need line for the thermal bus (Q4) against the network record's cascade rule.
4. Deferred to `water-bodies-as-common-infrastructure.md`'s own handoff: the lake-share question that Q1's second answer presupposes.

# Bundles
A **bundle** is a named composition toward a higher-level requirement: which capabilities an OS image, a product, or a kind of organization brings together. The word lives here. The base rules of that composition — when they are not already kernel or pluggable types — live in a `modules/` folder *inside the bundle*.

## Abstract
`modules/` is not a single privileged directory at the repository root. It is a role: **the base rules of the container it sits in**. At the repository root, `modules/` is the kernel of Organization — types every organization needs. Inside `bundles/<name>/`, `modules/` is the base rules of *that* bundle. A bundle may introduce modules; it is not required to. Knowledge-management composes kernel types and introduces none. Government will introduce modules (organs, membership, civic statutes). A statute, a construction method, a grid posture — once it has computer code — is a module of the bundle that owns that rule, not a page in a framework wiki and not a new kernel type. The law *type* stays at [`modules/rights/law`](../modules/rights/law/law.md). An instance such as buildable-share is a module under the bundle that enforces it. This folder's own membership list is not closed: several names here are leftovers of an earlier cut and are expected to move or retire.

## Introduction

### Motivation
Three failures this definition prevents. (1) Reading root `modules/` as the only place a module can exist, so a society's base rules have nowhere to live except kernel or a markdown corpus in another repository. (2) Reading a bundle as a label that must not own schema, so every statute is forced into kernel or left as documentation. (3) Keeping one umbrella (`society`, `economy`) after the same cut has already made a tighter home — kernel `modules/economics/` for economic *types*, government modules for economic *policy*.

### Methodology
Kernel vs pluggable remains the core-by-necessity test at repository root. Bundle vs kernel is a different test: does this rule apply only when that composition is in the image? If yes, it is a bundle module. The memar `docs/society` tree is not a template for folder shape here; it was a requirements notebook. Landing shape is `bundles/<bundle>/modules/<module>/` with the ordinary domain document, changelog, handoff, and later code.

## Explanation

### The word `modules`
A `modules` folder means **base rules of this container**. The container supplies the scope:

- `modules/` at repo root — base rules of Organization as such (person, law-as-type, task, account, …). Removing one would force fabricating another foundational type.
- `modules-plugable/` at repo root — optional capabilities of Organization; still modules, scoped as installable.
- `bundles/<bundle>/modules/` — base rules of that bundle. Present in the image only when the bundle is. They may be law-nodes with computer code, task graphs, content, or other types already defined in the kernel; they are still *modules of the bundle* because they are that composition's standing rules.

The same word is not a collision. It is the same role at two scales, the way `protocol/` inside a module is that module's protocol, not the protocols Memar specifies under `docs/modules/`.

### What a bundle may own
A bundle always names a composition. It may also introduce modules. Those are not exclusive:

- **Composition only** — the bundle points at kernel and pluggable modules and adds no `modules/` of its own. Leadership and knowledge-management are this shape today.
- **Composition plus bundle modules** — the image loads kernel types *and* this bundle's base rules. Government is this shape: it uses `modules/rights/law`, and it will carry statutes (membership, organs, land-tenure policy) as its own modules.

A bundle module is still a module in the ordinary sense: it needs a domain document, and once it is a law it needs computer code. It is not a kernel type. Buildable-share does not belong in `modules/rights/law/`; that folder defines what a law *is*. Buildable-share belongs in the bundle that runs that statute.

### This folder's membership is not a taxonomy
Names under `bundles/` were cut at different times. They are not a closed classification of the world. Two known defects:

- **`economy/`** — economic *types* (account, product, transaction) already live in kernel `modules/economics/`. A bundle named economy now mostly duplicates that cut. Society pages about tenure, payment rails, monetary standard, and intermediation are *policy*, not those types; they land as modules of **government**, which uses the kernel economics types. `bundles/economy/` is a candidate for retirement, not a destination.
- **`society/`** — a livable settlement is a composition of many bundles (government, justice, energy, land, …), not one notebook. This directory may hold a composition index for a settlement image. It must not hold the modules of land, energy, food, or law.

New bundle names (energy, water, food, buildings, land, travel, security) are opened when a cluster of base rules has no honest existing home. They can merge or rename later; that is cheaper than stuffing them under a false umbrella.

### Landing shape for former Memar society pages
Each requirement becomes a module folder, not a remaining `docs/society/<theme>/` tree. Companions (`.changelog.md`, `.handoff.md`) stay with that module. Rival approaches inside a page stay until a later session graduates them into code or drops them; the import does not freeze Memar's requirement-page format as the module's forever shape.

Paths below are relative to Memar `docs/society/` on the left and to `bundles/` here on the right. Companions (`.changelog.md`, `.handoff.md`) travel with the module. Memar `docs/society/README.md` is not imported. The law *type* stays at kernel [`modules/rights/law`](../modules/rights/law/law.md); `law-form-and-validity` lands as `law-validity` because what remains after that type is duration and sunset.

| Former Memar path | Bundle module |
|---|---|
| `governance/government-organs` | `government/modules/government-organs` |
| `governance/decision-and-deliberation-process` | `government/modules/decision-and-deliberation-process` |
| `governance/membership-and-identity` | `government/modules/membership-and-identity` |
| `governance/resident-matching-and-mobility` | `government/modules/resident-matching-and-mobility` |
| `governance/extra-basin-relations` | `government/modules/extra-basin-relations` |
| `governance/law-form-and-validity` | `government/modules/law-validity` |
| `governance/judiciary-and-dispute` | `justice/modules/judiciary-and-dispute` |
| `economy/bubble-drain-and-renewal` | `government/modules/bubble-drain-and-renewal` |
| `economy/custody-of-making-tools` | `government/modules/custody-of-making-tools` |
| `economy/land-housing-tenure` | `government/modules/land-housing-tenure` |
| `economy/monetary-standard-and-resource-wealth` | `government/modules/monetary-standard-and-resource-wealth` |
| `economy/payment-rails-and-service-charging` | `government/modules/payment-rails-and-service-charging` |
| `economy/permitted-intermediation` | `government/modules/permitted-intermediation` |
| `economy/reward-cooperation-thrift` | `government/modules/reward-cooperation-thrift` |
| `information-systems/data-storage-and-processing` | `information_system/modules/data-storage-and-processing` |
| `information-systems/observability-of-flows` | `information_system/modules/observability-of-flows` |
| `information-systems/platform-custody-and-records` | `information_system/modules/platform-custody-and-records` |
| `living-and-culture/continuous-health-watch` | `Health/modules/continuous-health-watch` |
| `living-and-culture/education-path` | `Ensan/modules/education-path` |
| `living-and-culture/recreation-and-culture-venues` | `Ensan/modules/recreation-and-culture-venues` |
| `living-and-culture/narrating-the-system` | `government/modules/narrating-the-system` |
| `form-and-land/space-for-differing-minds` | `Ensan/modules/space-for-differing-minds` |
| `form-and-land/airflow-through-fabric` | `land/modules/airflow-through-fabric` |
| `form-and-land/buildable-share-and-density-allocation` | `land/modules/buildable-share-and-density-allocation` |
| `form-and-land/ground-surface-treatment` | `land/modules/ground-surface-treatment` |
| `form-and-land/service-placement-scale` | `land/modules/service-placement-scale` |
| `form-and-land/settlement-grain-and-scaling` | `land/modules/settlement-grain-and-scaling` |
| `form-and-land/sound-environment` | `land/modules/sound-environment` |
| `form-and-land/stewardship-of-ground-cover` | `land/modules/stewardship-of-ground-cover` |
| `form-and-land/which-plane-carries-which-flow` | `land/modules/which-plane-carries-which-flow` |
| `form-and-land/wildlife-safe-surfaces` | `land/modules/wildlife-safe-surfaces` |
| `buildings/daylight-to-interiors` | `buildings/modules/daylight-to-interiors` |
| `buildings/deep-dryness` | `buildings/modules/deep-dryness` |
| `buildings/dwelling-provision-and-adaptability` | `buildings/modules/dwelling-provision-and-adaptability` |
| `buildings/multifunctional-surfaces` | `buildings/modules/multifunctional-surfaces` |
| `buildings/placement-and-routing-of-service-flows` | `buildings/modules/placement-and-routing-of-service-flows` |
| `buildings/structural-material` | `buildings/modules/structural-material` |
| `energy/ambient-power-harvest` | `energy/modules/ambient-power-harvest` |
| `energy/climate-signal-authority` | `energy/modules/climate-signal-authority` |
| `energy/deep-machinery-manning` | `energy/modules/deep-machinery-manning` |
| `energy/directed-energy-transfer` | `energy/modules/directed-energy-transfer` |
| `energy/energy-carriers-and-grid-posture` | `energy/modules/energy-carriers-and-grid-posture` |
| `energy/in-fabric-thermal-buffer` | `energy/modules/in-fabric-thermal-buffer` |
| `energy/large-generation-site` | `energy/modules/large-generation-site` |
| `energy/passive-cooling-paths` | `energy/modules/passive-cooling-paths` |
| `energy/solar-tower-purpose` | `energy/modules/solar-tower-purpose` |
| `energy/thermal-sources-and-storage` | `energy/modules/thermal-sources-and-storage` |
| `water-and-matter/fate-of-residues-and-nutrients` | `water/modules/fate-of-residues-and-nutrients` |
| `water-and-matter/the-dead-among-the-living` | `water/modules/the-dead-among-the-living` |
| `water-and-matter/treatment-and-return-of-used-waters` | `water/modules/treatment-and-return-of-used-waters` |
| `water-and-matter/water-bodies-as-common-infrastructure` | `water/modules/water-bodies-as-common-infrastructure` |
| `water-and-matter/water-supply-and-security` | `water/modules/water-supply-and-security` |
| `food/food-production-and-assurance` | `food/modules/food-production-and-assurance` |
| `food/meals-and-shared-cooking` | `food/modules/meals-and-shared-cooking` |
| `movement/last-mile-of-goods` | `logistics/modules/last-mile-of-goods` |
| `movement/human-travel-network` | `travel/modules/human-travel-network` |
| `movement/transport-boundary-interface` | `travel/modules/transport-boundary-interface` |
| `security-and-resilience/securing-sensitive-spaces` | `Dideban/modules/securing-sensitive-spaces` |
| `security-and-resilience/autonomy-in-crisis` | `security/modules/autonomy-in-crisis` |

The kernel law type is not copied. `libraries/` was a fourth root invented to hold instance packs; that job is bundle modules, so `libraries/` does not remain. Imported pages keep the requirement-notebook shape they had in Memar until a later session rewrites each as a module document and computer code; this import does not freeze that notebook format as the module's forever shape.

The twelve Memar theme directories (`governance`, `economy`, `form-and-land`, …) were a notebook grouping of questions, not a second taxonomy. They carried no extra rule beyond "these pages sit together." Spreading by concept already dropped the false umbrellas; the table above is the whole record of that grouping. What was *not* folder structure — and was skipped with `docs/society/README.md` — are the corpus operating rules that still apply to those pages until rewritten: a requirement is a question that favors no answer; a rejected approach stays visible; network pages (energy, water, data, movement) state abstract rules and name no consumer, while consumer pages declare their needs toward the network; approach headings keep their section-id suffix. Those rules are working constraints for anyone editing an imported page, not a reason to rebuild the theme tree.

### Related
- [`modules/rights/law/law.md`](../modules/rights/law/law.md) — what a law is
- [`modules/economics/economics.md`](../modules/economics/economics.md) — economic types, not civic economic policy
- [`knowledge-management/knowledge-management.md`](knowledge-management/knowledge-management.md) — a composition-only bundle; its table must not be read as "bundles never own modules"

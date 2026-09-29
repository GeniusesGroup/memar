# Rule Changelog

## 2026-09-29 — Initial concept document

### What changed
- Created `docs/rule.md` (Draft) as the language-neutral Rule and rule-engine concept document at `docs/` root beside `modularity.md`.
- Created `docs/rule.research.001.md` (Complete) recording terminology research (rule vs policy vs constraint vs convention; SBVR, BRG, production rules).
- Created `docs/rule.handoff.md` with open questions and an inventory of 32 document-level rule passages proposed for relocation to Module `rules/` folders.
- Linked from [modularity.md → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) and [modules/khayyam/rules/README.md](../modules/khayyam/rules/README.md).

### Why
- Owner position: Rule is a Memar-wide concept; any Module may carry `rules/` beside `protocol/`; rules are owner-introduced, not language/protocol properties; rule-making is general practice.

### Cited
- [Rule Research 001](./rule.research.001.md) — `Evidence`
- [Modularity → Rules as a Provisional Term](./modularity.md#rules-as-a-provisional-term) — `Extends`
- [Linter](./protocols/computer/linter.md) — `Reference`
- [Modeling → Separating Structure (Code) from Policy (Rule)](./modeling.md#separating-structure-code-from-policy-rule) — `Reference`

### Applied to
- modularity.md: Done — pointer to `rule.md` added; section no longer marked provisional in title.
- modules/khayyam/rules/README.md: Done — link to general Rule concept at top.

### Considered and not done
- **Relocating inventory entries in the same session**: scoped out; recorded in handoff only.
- **Promoting `rule.md` to Proposed immediately**: left Draft until framing open question is reviewed.

## 2026-09-29 — Rules, code, and services boundary

### What changed
- Added [rule.md → Rules, Code, and Services](./rule.md#rules-code-and-services): a Rule states a condition; generation/scaffolding/rewriting is a service capability, not Rule text; enforcement by a service keeps behavior in code.
- Extended [rule.handoff.md](./rule.handoff.md) with Memar server doc gap note, Khayyam rules classification inventory (25 rules: 4 / 5 / 16), and anticipated relocation work.
- Recorded "generate a service from its name and path" in [SDK handoff](./protocols/modules/sdk.handoff.md) and [Khayyam execution handoff](../modules/khayyam/execution.handoff.md).

### Why
- Owner position (2026-09-29): Rule must not replace code and services; generative work belongs in the Memar server; many `modules/khayyam/rules/` entries are mis-placed.

### Cited
- [Khayyam execution handoff → Rule model](../modules/khayyam/execution.handoff.md) — `Reference` (Memar server mention; no defining doc)
- [Knowledge → Knowledge and Code](./knowledge.md#knowledge-and-code) — `Reference` (callable generative services)

### Considered and not done
- **Linking to a Memar server protocol document**: none exists under `docs/`; noted in handoff instead of inventing one.

## 2026-09-29 — Observer/mutator rule relocated to ADT module

### What changed
- Moved observer/mutator governance from `modules/khayyam/rules/observer-mutator-abstractions/` to `modules/computer/adt/rules/observer-mutator/`.
- Updated [rule.handoff.md](./rule.handoff.md) Khayyam rules classification: observer-mutator under (a) ADT; Khayyam index count 24; (a) 5 / (b) 5 / (c) 15.
- Added `modules/computer/adt/rules/README.md` index.

### Why
- Owner decision (2026-09-29): Liskov & Guttag observer/mutator families are ADT protocol subject matter, not Khayyam grammar.

### Cited
- [observer-mutator.md](../modules/computer/adt/rules/observer-mutator/observer-mutator.md) — `Extends`
- [ADT handoff](./protocols/computer/adt.handoff.md) — `Reference`

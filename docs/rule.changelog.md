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

---

### The module a Rule belongs to
- Time: 2026-10-03T12:01:30Z
- Type: Added
- Cited:
  - [Linter → A rule's home is its subject's document](./protocols/computer/linter.md#a-rules-home-is-its-subjects-document) — `Evidence`: the principle this criterion extends from the claim to the `rules/` folder
  - [Khayyam → Minimal Legislation](./khayyam/khayyam.md#minimal-legislation-a-principle) — `Evidence`: `:177` and `:181` for the language test
  - [Modeling → Constraints Belong to the Constraining Concern](./modeling.md#constraints-belong-to-the-constraining-concern) — `Evidence`: a condition is owned by the concern that originates it
  - [Control Flow Model → Halt](../modules/process/control-flow/control-flow.md#halt) — `Reference`: `:129` for the name `Halt` and `:131` for the refused `panic`
  - [protocols → Where implementations live](./protocols/README.md#where-implementations-live) — `Reference`: `:16` names the module the relocated Rule's protocol claims
  - [Test → Placement](../modules/process/test/rules/test-placement/test-placement.md) — `Reference`: a Rule already filed in the module that owns its subject

#### What changed
- Added [rule.md → Which Module a Rule Belongs To](./rule.md#which-module-a-rule-belongs-to): a Rule belongs to the module that owns its subject; it belongs to a language exactly when no program satisfies every Rule of that language's catalog and still violates it; enforcement does not decide the home; and the two cases the subject test does not decide are named as undecided.
- Relocated [Disregarded Error](../modules/process/error/rules/disregarded-error/disregarded-error.md) from `modules/khayyam/rules/` to `modules/process/control-flow/rules/` and then, on the owner's ruling that the concern it governs is failure, to `modules/process/error/rules/`, on that criterion. Its normative claim is [The Error](./protocols/process/error.md) at `:88` and `:130` together with [Control Flow → Error Propagation](./protocols/process/control-flow.md#error-propagation) at `:141` and `:143`, and the same document's `:139` is what the first relocation read as claiming the subject away from The Error.
- Created `modules/process/control-flow/rules/` with a catalog index and two Rules: the relocated Disregarded Error and [Halt Declaration](../modules/process/control-flow/rules/halt-declaration/halt-declaration.md), which gives the halting concern a Rule of its own rather than a refusal inside a Rule about a failure.
- Added [Scope Visibility](../modules/khayyam/rules/scope-visibility/scope-visibility.md) to the Khayyam catalog; its subject is name resolution in the language.
- Updated the [Khayyam rules index](../modules/khayyam/rules/README.md) — the Disregarded Error row removed, the Scope Visibility row added, and a pointer to the module catalogs added — and repaired every link into the relocated Rule.

#### Deliberation
The owner's challenge of 2026-10-03 asked whether all rules relating to Khayyam belong in the language's rules folder, whether the Khayyam language itself claims to solve them, and whether a concern such as `panic` should be a module with its own rules written imperatively rather than a prohibition carried elsewhere. Measured over the catalog as it stood, it held 26 Rules of which 13 had a subject this repository chose rather than the language — a subject the catalog's own membership criterion excludes — while the concern about halting existed only as a sentence inside another Rule's refusal. The answer given is a criterion rather than a move in either direction, and it is placed here because this document is what owns where Rules live: `modules/README.md` puts specifications and general claims in `docs/` and not in the implementation layer.

#### Considered and not done
- **Moving the catalog's 13 repository-convention Rules out of it**: named as the measurement that motivates the criterion, not performed. Each is a separate relocation with its own subject to argue, and the question was where a Rule goes rather than which Rules leave.
- **Placing the relocated Rule in `modules/process/error/rules/`**: that folder exists and is empty and the owner named it as a candidate; not taken, because what an Error *is* is that module's subject and how execution continues once one has occurred is not — `docs/protocols/process/control-flow.md:139` draws that line itself.
- **Creating an independent `panic` module**: not taken; `modules/process/control-flow/` already holds the concept, its two declarations, and its contract, and `panic` is a refused name at `control-flow.md:131`.
- **Writing the Scope Visibility claim into `docs/khayyam/`**: not written. `docs/khayyam/khayyam.research.001.md:444` records the statement of a `sc` block's reach as owed beside `khayyam.md:129`, and that folder is not this session's to write; the Rule cites the debt rather than closing it.
- **Settling the two cases the criterion leaves undecided**: recorded in the body as undecided rather than answered, because those two are questions about subjects and no placement rule can decide them.

---

### Correct the standing of a vocabulary source in a completed research
- Time: 2026-10-04T13:27:43Z
- Propagates to:
  - rule.md: Reference - its definition derives from this repository's own practice and rests on no external source, so no change was needed
  - rule.handoff.md: Done - an open question added recording that the vocabulary findings are a reading and are provisional against the specification
- Contributors:
  - [Omid Hekayati](../CONTRIBUTORS.md#omid-hekayati) - requested, decided
  - [Space Bunny Alpha](../CONTRIBUTORS.md#space-bunny-alpha) (space-bunny-free via [OpenCode](../CONTRIBUTORS.md#opencode)) - claimed, argued, applied

#### What changed
- `rule.research.001.md` no longer cites the industry-community articles and the tertiary compilation it read as `Evidence`, and no longer records their URLs. Each affected finding is now attributed to internet research with the `Reference` relation.
- `### Methodology` now states what those sources may carry: an industry-community article belongs to the vendor class of source and a tertiary compilation is a pointer toward primary sources, so neither supports a claim, and every claim drawn from them is the research's own reading rather than a finding those sources establish.
- `### Methodology` names the limitation the record did not: the specification defining that vocabulary was not consulted, so a finding stating what the vocabulary says is provisional against it.
- `### Conclusion` states that the standing of those sources bears on how far the vocabulary findings may be relied upon and not on the Rule definition, which `rule.md` derives from this repository's own practice.
- No finding's content was altered. What changed is the standing claimed for the material each was read from.

#### Considered and not done
- A superseding research was not opened (Omid Hekayati — declined). The facet's own lifecycle makes supersession the correction mechanism for a frozen record, and that rule was set on the owner's approval; he directed that the record be corrected in place regardless of its status, and the tension between the two instructions is recorded here rather than resolved by this entry.
- Re-attributing the vocabulary definitions to the specification was rejected as fabrication (Space Bunny Alpha — argued). The inquiry did not read that specification, and attributing a reading to a document nobody opened is exactly what [Documentation → Content Rule](./documentation.md#content-rule-no-fabricated-or-redundant-provenance) forbids. The gap is recorded as a limitation and as an open question instead.
- Withdrawing the vocabulary findings as prior art no document relies upon was not done (Omid Hekayati — pending). It is a defensible outcome and is now a question in `rule.handoff.md`.

#### Deliberation
The new `Source standing` rule in `documentation.md` was found to invalidate citations this record had carried since it was written, and the record's `Complete` status would normally have left the defect in place (Space Bunny Alpha — argued). The owner directed that the record be fixed and that its status not be treated as a reason to leave it (Omid Hekayati — decided). The two instructions conflict on their face, and the entry records the conflict so a later reader sees that the in-place correction was a decision and not an oversight (Space Bunny Alpha — argued).

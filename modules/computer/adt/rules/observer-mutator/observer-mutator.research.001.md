# ADT Rule — Observer and Mutator Research 001 — Field vs Method meta-abstractions

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [F1 — Corpus inventory](#f1--corpus-inventory)
  - [F2 — Paired Field/Method pattern](#f2--paired-fieldmethod-pattern)
  - [F3 — Literature and Memar docs](#f3--literature-and-memar-docs)
  - [F4 — Composition collision](#f4--composition-collision)
  - [F5 — Recommendation](#f5--recommendation)
- [Open Questions](#open-questions)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)
- [Notes](#notes)

## Status
Complete

## Question and Goals
### Questions
1. What do `Field_*` and `Method_*` abstractions in `modules/` actually do today — read, write, or both? — **Answered**
2. Should `Field_X` cover both query and mutate sides of one piece of state, or is a paired abstraction needed — and what should it be named? — **Answered** (recommendation; owner ruling pending)

### Goals
1. Inventory every `tp Field_*` and `tp Method_*` declaration under `modules/` with role classification. — **Met**
2. Ground the answer in Memar encapsulation/method docs, command–query separation, and relevant literature. — **Met**
3. Record the composition-collision constraint already noted for field accessors and test it against mutate naming. — **Met**
4. Produce a durable research record per [Documentation — Research](../../../../../docs/documentation-research.md) and link it from the [observer and mutator handoff](./observer-mutator.handoff.md). — **Met**

### Scope
The `modules/` Khayyam protocol corpus (excluding `modules/khayyam/rules/` example lines) as of 2026-09-29, plus `docs/khayyam/encapsulation.md`, `docs/khayyam/method.md`, and [Method Verb Phrases Research 001](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md). Does not rename the corpus, does not change governing rules beyond what the ADT rule states.

## Participants
- [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; review outcome: **Not yet reviewed**.
- [Cursor](../../../../CONTRIBUTORS.md#cursor) — **Researcher**; review outcome: **Not yet reviewed**.

## Methodology
1. Read [Documentation — Research](../../../../docs/documentation-research.md) for Research facet structure.
2. Read [observer-mutator.md](./observer-mutator.md), [observer-mutator.handoff.md](./observer-mutator.handoff.md), [method-verb-phrases.md](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.md), [method-verb-phrases.research.001.md](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md), [Encapsulation in Khayyam](../../../../../docs/khayyam/encapsulation.md), [Method in Khayyam](../../../../../docs/khayyam/method.md), and `modules/computer/capsule/protocol/field.kh`.
3. Grep of `modules/**/*.kh` for `tp Field_*`, `tp Method_*`, `mt (self Field_*`, and `mt (self Method_*`; spot-read of every file defining a `Method_*` abstraction and of owners composing both a field and a method abstraction for the same state.
4. Classified each method as **query** (influenced variables carry data out; no state-changing signature shape), **mutate** (influencing variables only or command verb; observable state change intended), or **mixed bundle** (abstraction grouping several commands/queries). Signature shape follows [Method in Khayyam → Influencing and Influenced Variables](../../../../docs/khayyam/method.md#influencing-and-influenced-variables-not-inputs-and-outputs); side-effect intent follows comments and CQS (Meyer, *OOSC* Ch. 23).
5. Compared findings to CQS (Meyer 1997), Java/C# property versus command conventions (Alsuhaibani et al., ICSE 2021; Høst & Østvold, ECOOP 2009), and the composition-collision argument in [Method Verb Phrases Research 001 → F4](../method-verb-phrases/method-verb-phrases.research.001.md#f4--field-accessor-naming-options).

Limits: classification is manual from protocol signatures and comments, not runtime analysis; Go `type … interface` stubs in TODO blocks were noted but not counted as Khayyam declarations.

## Findings
### F1 — Corpus inventory
Automated scan of `modules/**/*.kh` (excluding `modules/khayyam/rules/`):

| Declaration kind | `Field_*` | `Method_*` |
| --- | ---: | ---: |
| `tp …` lines (all kinds) | 252 | 25 |
| Unique `ab` definitions | 107 | 10 |
| `in` imports | 129 | 5 |
| `mt` types whose **name** starts with the prefix | 16 | 10 |
| Methods with `self Field_*` | ~100 | — |
| Methods with `self Method_*` | — | 20 |

**Role split**

| Abstraction | With methods declared | Query (read) | Mutate (write/command) | Both on same `ab` |
| --- | ---: | ---: | ---: | ---: |
| `Field_*` | 93 of 107 | ~100 methods; **all** accessors are query-shaped | **0** | **0** |
| `Method_*` | 10 of 10 | 4 methods on 2 abs (`Method_URI_Directory`, `Method_File_GUI`) | 16 methods on 8 abs | 2 abs (`Method_File`, `Method_Directory_Helpers`) group query **and** command methods |

Fourteen `Field_*` abstractions have no `mt` method yet (contract-only composition members). The meta-model in `modules/computer/capsule/protocol/field.kh` defines `Field_Field` / `Field_Capsule_Fields` — query-only accessors over capsule metadata, with no mutate counterpart.

**No `Field_*` abstraction in the corpus declares a mutating method on itself.** Every mutate path found uses a separate `Method_*` abstraction (or an entity-level command bundle — see F2).

### F2 — Paired Field/Method pattern
Six **field-scoped pairs** expose query on `Field_X` and command on `Method_X` (or `Method_<Concept>` aligned with the field concept):

| Query (`Field_*`) | Command (`Method_*`) | Owner example |
| --- | --- | --- |
| `Field_MemoryAddress` → `Field_MemoryAddress_MemoryAddress` | `Method_SetMemoryAddress` → `SetMemoryAddress` | `Memory_Pointer` |
| `Field_Name` → `FileName`, `FileNameWithoutExtension` | `Method_Rename` → `Rename` | composed into `Method_File` |
| `Field_SocketStatus` → `SocketStatus` | `Method_SocketStatus` → `SetStatus` | `Net_Socket` |
| `Field_HTTP_Status` → `StatusCode`, `ReasonPhrase` | `Method_Status` → `SetStatus` | `PseudoHeader_Response`, `HTTP_Response` |
| `Field_HTTP_Body` → `HTTPBody` | `Method_Body` → `SetBody` | `HTTP_Request`, `HTTP_Response` |
| `Field_Buffer_Indexes` → `ReadIndex`, `WriteIndex` | `Method_Indexes` → `SetReadIndex`, `SetWriteIndex` | `Computer_Buffer` |

A second use of `Method_*` is **entity command bundles** not tied to a single field value:

| Abstraction | Role | Methods |
| --- | --- | --- |
| `Method_File` | File lifecycle commands | `Save`, `Delete`, `Erase`; composes `Method_Rename` |
| `Method_Directory_Helpers` | Directory helper commands/queries | `FileByPath`, `FindFile` (query); `Copy`, `Move`, `DeleteByPath`, `Remove`, `RemoveByPath` (command) |

These bundles reuse the `Method_` prefix but name the **owning entity's command surface**, not a single field's mutator. They still obey CQS at the method level; they are not counter-examples to splitting query field contracts from command contracts.

### F3 — Literature and Memar docs
**Command–query separation (CQS).** Meyer (*Object-Oriented Software Construction*, 2nd ed., Prentice Hall, 1997, Ch. 23) requires that queries return data without changing observable state and commands change state without returning domain data. Khayyam's influenced-variable groups already encode call roles ([Method in Khayyam](../../../../docs/khayyam/method.md#influencing-and-influenced-variables-not-inputs-and-outputs)); [Method Verb Phrases Research 001 → F1](../method-verb-phrases/method-verb-phrases.research.001.md#f1--literature-on-method-naming) cites the same baseline for naming.

**Properties vs split accessors.** Mainstream OO often collapses read and write into one surface (`getX` / `setX` on the same type, or C# **properties** — see Albahari & Albahari, *C# in a Nutshell*, O'Reilly, property accessors). Surveys show professional disagreement on accessor form but agreement that callables should read as verbs (Alsuhaibani et al., ICSE 2021). Memar already rejects anonymous positional grouping ([Encapsulation in Khayyam → Tuples Rejection](../../../../docs/khayyam/encapsulation.md#tuples-rejection)) and treats the public method set as the contract ([Encapsulation → Sovereign Encapsulation](../../../../docs/khayyam/encapsulation.md#sovereign-encapsulation)). Splitting **query contract** (`Field_X`) from **command contract** (`Method_X`) matches CQS more sharply than a unified property type and matches the corpus's zero mutate-on-`Field_*` practice.

**Encapsulation doc.** [Encapsulation → Capsule Structure and Privacy](../../../../docs/khayyam/encapsulation.md#capsule-structure-and-privacy) states that even read access requires methods and that mechanical get/set for every field is discouraged unless explicitly requested. [Encapsulation → Naming Conventions](../../../../docs/khayyam/encapsulation.md#naming-conventions) defers `Get…` / `Set…` policy to the method verb phrases handoff — consistent with keeping mutate verbs domain-specific (`Rename`, `SetStatus`) on `Method_*` rather than generic `Set` on `Field_*`.

**Meta-model.** `Field_Field` in `modules/computer/capsule/protocol/field.kh` models introspection over capsule fields (query only). It does not introduce a `Method_Field` — field metadata mutation is out of band for that abstraction.

### F4 — Composition collision
[Method Verb Phrases Research 001 → F4](../method-verb-phrases/method-verb-phrases.research.001.md#f4--field-accessor-naming-options) records that generic **`Read` on every `Field_X` collides** when one owner composes several field abstractions. The same argument applies to **generic mutate verbs on `Field_*`**:

- If each composed `Field_X` exposed `Set` (or shared a domain verb), call sites and owner vtables could not distinguish which state is mutated without extra qualification — violating Deißenböck & Pizka's concise, bijective naming (IWPC 2005).
- The buffer pair avoids this: `Field_Buffer_Indexes` uses distinct query names (`ReadIndex`, `WriteIndex`); `Method_Indexes` uses distinct command names (`SetReadIndex`, `SetWriteIndex`). A single `Field_Buffer_Indexes` carrying both queries **and** sets would force either duplicated verbs or overloaded meaning.

Composing **`Field_HTTP_Status` and `Method_Status` in the same owner does not collide**: query methods live on the field abstraction; `SetStatus` lives on the method abstraction. The owner exposes two composed members, not two methods with the same name.

**Constraint to govern:** when one owner composes multiple field abstractions, **method names reachable through each field abstraction must be unique per owner** (already stated for query verbs in Research 001 F4). When a mutate counterpart exists, it should live on a **`Method_*` member** whose command methods are named for the operation (`SetStatus`, not bare `Status`), keeping query and command namespaces separate.

### F5 — Recommendation
**Keep the paired model; do not extend `Field_X` to cover mutate.**

| Layer | Prefix | Contract | Method verbs |
| --- | --- | --- | --- |
| Query (read) | `Field_<Concept>` | State observation; no intended mutation | Domain query verbs or (when ruled) `Get<Concept>` — see method verb phrases handoff |
| Command (mutate) | `Method_<Concept>` | State change for the same concept when mutation is part of the protocol | Domain command verbs per [method verb phrases rule](../method-verb-phrases/method-verb-phrases.md); not bare nouns |

**Naming rules for the pair**

1. **`Method_<Concept>`** when it mutates the same concept as **`Field_<Concept>`** — examples already in corpus: `Field_HTTP_Status` / `Method_Status`, `Field_HTTP_Body` / `Method_Body`, `Field_Buffer_Indexes` / `Method_Indexes`. Prefer the same concept token after the prefix (`Status`, `Body`, `Indexes`); use a more specific token when needed (`Method_SetMemoryAddress` pairs `Field_MemoryAddress`; `Method_Rename` pairs the name field accessed via `Field_Name`).
2. **Compose both** in the owning abstraction when the protocol allows mutation (`Memory_Pointer`, `Computer_Buffer`, `HTTP_Response`, `Net_Socket`). Compose **only `Field_*`** when the protocol is read-only (most of the 107 field abstractions today).
3. **`Method_<Entity>` bundles** (`Method_File`, `Method_Directory_Helpers`) remain valid for **entity-level** command surfaces that are not a single field value; they should not be folded into arbitrary `Field_*` types.
4. **Reject** putting mutate methods on `Field_*` — zero corpus precedent, CQS blur, and collision risk if multiple fields share command verb shapes.
5. **Reject** new prefixes (`Command_*`, `Mutator_*`, `Setter_*`) unless a future corpus need appears — `Method_*` is already established, readable next to `Field_*`, and aligned with Khayyam's view that behavior is always `mt` ([Method in Khayyam → No Dedicated fn/func Keyword](../../../../docs/khayyam/method.md#no-dedicated-fnfunc-keyword)).

**Alternatives considered**

| Option | Verdict | Reason |
| --- | --- | --- |
| Single `Field_X` with query + mutate methods | **Reject** | 0/107 corpus; blurs CQS; composed owners risk verb collisions |
| Mutate on `Field_X`, query-only `Method_*` | **Reject** | Inverts established corpus pattern; `Field_` prefix marks held state, not commands |
| Generic `Set` on every `Field_X` | **Reject** | Same collision class as generic `Read` (Research 001 F4) |
| C#-style unified property abstraction | **Reject for Memar protocols** | Hides command/query role at abstraction boundary; conflicts with influenced-variable role grammar |
| Keep `Method_*` as mutate/command counterpart | **Recommend** | 6 field pairs + entity bundles; matches Meyer CQS and encapsulation doc |

## Open Questions
Graduated to [observer-mutator.handoff.md](./observer-mutator.handoff.md) for owner ruling:

1. **Adopt the paired `Field_*` / `Method_*` model as governance?** — this research recommends yes; the rule document does not yet state it.
2. **Exact naming when concepts diverge** — e.g. `Method_SetMemoryAddress` vs `Method_MemoryAddress`; document a tie-breaker?
3. **Entity command bundles** — should `Method_File` / `Method_Directory_Helpers` be documented as a second sub-pattern under the same prefix?
4. **Field accessor query verbs** — decided for Observer/Mutator families in [observer-mutator.md](./observer-mutator.md); Get/Set question outside those families remains open in [method verb phrases handoff](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.handoff.md).

## Conclusion
The corpus contains **107** `Field_*` and **10** `Method_*` abstraction definitions (**252** and **25** total `tp` lines respectively). **All ~100 methods on `Field_*` are query-shaped; none mutate.** Mutating behavior appears only on **`Method_*`** abstractions — six times as a explicit pair for the same mutable state, plus two entity command bundles. Literature (Meyer 1997 CQS; Alsuhaibani et al. 2021; Høst & Østvold 2009) and Memar encapsulation support **keeping `Field_X` as the query contract and `Method_X` as the command counterpart**, not merging them. Composition collision arguments that reject generic `Read` on every field apply equally to generic mutate verbs on `Field_*`. **Recommended governance:** paired `Field_<Concept>` + `Method_<Concept>` when mutation is allowed; domain command verbs on `Method_*`; owner ruling still required before the rule document is updated.

Owner review (2026-09-29): decided — `Observer_`/`Mutator_` adopted; see [handoff Decisions](./observer-mutator.handoff.md#decisions).

## Related Artifacts
| Artifact | Relation |
| --- | --- |
| [observer-mutator.md](./observer-mutator.md) | Base rule — absorbed owner decision |
| [observer-mutator.handoff.md](./observer-mutator.handoff.md) | Owner ruling recorded |
| [method-verb-phrases.research.001.md](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md) | Query accessor options and `Read` rejection |
| [Encapsulation in Khayyam](../../../../../docs/khayyam/encapsulation.md) | Sovereign encapsulation; get/set not mandated |
| [Method in Khayyam](../../../../../docs/khayyam/method.md) | Influencing/influenced variable roles |
| [modules/computer/capsule/protocol/field.kh](../../../capsule/protocol/field.kh) | Meta-model for `Field_*` |
| [Documentation — Research](../../../../../docs/documentation-research.md) | Governs this artifact |

## Notes
- Inventory command: Python scan over `modules/**/*.kh` excluding `modules/khayyam/`; accessor count ~100 from ripgrep per-file match totals.
- `Method_File_Save` / `Delete` / `Erase` are commands with `(err Error)` influenced variables — classified as mutate by intent despite empty influenced data group in the signature pattern.

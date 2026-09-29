# Khayyam Rule — Method Verb Phrases Research 001 — Method and field accessor naming

## Table of contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Methodology](#methodology)
- [Findings](#findings)
  - [F1 — Literature on method naming](#f1--literature-on-method-naming)
  - [F2 — Techniques that reduce naming ambiguity](#f2--techniques-that-reduce-naming-ambiguity)
  - [F3 — Implicit rules in this repository](#f3--implicit-rules-in-this-repository)
  - [F4 — Field accessor naming options](#f4--field-accessor-naming-options)
- [Open Questions](#open-questions)
- [Conclusion](#conclusion)
- [Related Artifacts](#related-artifacts)
- [Notes](#notes)

## Status
Active

## Question and Goals
### Questions
1. What does the software-engineering literature recommend for method naming — verb phrases, query versus command, and accessors? — **Answered**
2. Which naming or structure conventions are already applied in this repository but not written as standalone rules under `modules/khayyam/rules/`? — **Answered**
3. How should a query method on a `Field_X` abstraction be named? — **Open**
4. Are `Get…` / `Set…` prefixes appropriate governance for this repository? — **Open**

### Goals
1. Ground the [method verb phrases rule](./method-verb-phrases.md) and the [observer and mutator rule](../../../computer/adt/rules/observer-mutator/observer-mutator.md) in citable evidence rather than anecdote. — **Met**
2. Inventory implicit conventions so they can be automated or promoted to rules. — **Met**
3. Record accessor naming options, including options the owner rejected, for ruling in the paired handoff. — **Met**
4. Produce a durable research record per [Documentation — Research](../../../../docs/documentation-research.md). — **Met**

### Scope
Peer-reviewed and widely cited work on identifier and method naming (2000–2021), command–query separation, and the Memar `modules/` corpus and existing Khayyam rules as of 2026-09-29. It does not change the corpus, does not edit `docs/khayyam/*`, and does not decide `Get`/`Set` policy — that remains open in the [handoff](./method-verb-phrases.handoff.md).

## Participants
- [Omid Hekayati](../../../../CONTRIBUTORS.md#omid-hekayati) — **Questioner**, **Goal-setter**; review outcome: **Not yet reviewed**.
- [Cursor](../../../../CONTRIBUTORS.md#cursor) — **Researcher**; review outcome: **Not yet reviewed**.

## Methodology
1. Read [Documentation — Research](../../../../docs/documentation-research.md) for the Research facet structure and naming (`<base>.research.<NNN>.md`).
2. Web search and bibliographic verification for the sources the owner named (Deißenböck & Pizka, Høst & Østvold, Arnaoudova et al., Hill et al. / SWUM, Newman et al., Alsuhaibani et al., Caprile & Tonella, Lawrie et al., Butler et al., Meyer CQS).
3. Grep and spot-read of `modules/` for `Field_` declarations, accessor method shapes, and conventions referenced in existing rules (`qualified-names`, `receiver-method-names`, `result-parameter-names`) and in `docs/khayyam/encapsulation.md#naming-conventions` (read only; not edited).
4. Distilled findings into claim-shaped statements; cited sources at findings with the **Evidence** relation per [documentation.md → Citations](../../../../docs/documentation.md#citations).
5. Owner rulings received after the first draft (2026-09-29): `Get`/`Set` neither required nor forbidden; generic `Read` on every `Field_X` rejected; `Elapsed` on `Time` returns `Duration`, not `Time`.

Limits: no new empirical study on the Memar corpus; Alsuhaibani et al. survey percentages are taken from the published paper, not re-measured here.

## Findings
### F1 — Literature on method naming
The table below is the literature base for this rule. Venues are verified from publisher records; Butler et al. publish two distinct 2015 papers (ICPC survey vs ICSME NOMINAL tool study).

| Source | Year | Venue | Relevant finding |
| --- | --- | --- | --- |
| Deißenböck & Pizka | 2005 | IWPC | Identifiers should map **bijectively** to concepts; names must be **concise and consistent**; homonyms and synonyms harm comprehension (**Evidence**: doi:10.1109/WPC.2005.14). |
| Høst & Østvold | 2009 | ECOOP | Method names are **natural-language phrases**; corpus phrase books pair patterns (`get-[noun]`, `set-[noun]`, `find-[noun]-by-[noun]`) with semantics; **name–implementation mismatch** is detectable (**Evidence**: LNCS 5653, pp. 294–317). |
| Høst & Østvold | 2009 | ECOOP (workshop) | *The Java Programmer's Phrase Book*: method phrases have grammatical structure; the **first fragment is usually a verb** in Programmer English (**Evidence**: LNCS, pp. 322–341). |
| Arnaoudova et al. | 2013 | CSMR | **Linguistic antipatterns**: methods that say more than they do, do more than they say, or do the opposite — often tied to misleading or noun-only names (**Evidence**: doi:10.1109/csmr.2013.28). |
| Hill, Pollock & Vijay-Shanker | 2009 | ICSE | **SWUM**: extract verb, noun, and prepositional phrases from identifiers using static analysis; supports maintenance tools (**Evidence**: doi:10.1109/ICSE.2009.5070524). |
| Butler, Wermelinger, Yu & Sharp | 2011 | ECOOP | Identifier **tokenisation** and naming-feature study across 60 Java projects; method names are a distinct construct from class and reference names (**Evidence**: LNCS, pp. 130–154). |
| Butler, Wermelinger & Yu | 2011 | ICSM | Java **class** names follow noun-phrase patterns; naming conventions vary by project (**Evidence**: doi:10.1109/ICSM.2011.6080776). |
| Newman et al. | 2020 | J. Systems & Software | **Grammar patterns** (POS sequences): **function/method names predominantly use verb-phrase patterns** (verb + noun phrase); noun-only patterns are rarer for callables (**Evidence**: doi:10.1016/j.jss.2020.110740). |
| Alsuhaibani et al. | 2021 | ICSE | **Ten method-naming standards**; survey of 1100+ professionals: broad agreement that methods should contain a **verb or verb phrase** (~84% agreement on Standard 3); main disagreement is **accessors/predicates** (`getX` vs bare `x`) (**Evidence**: doi:10.1109/ICSE43902.2021.00061). |
| Caprile & Tonella | 2000 | ICSM | Identifier quality has **lexicon** and **syntax** (term arrangement); restructuring improves meaningfulness (**Evidence**: doi:10.1109/icsm.2000.883022). |
| Lawrie, Morrell, Feild & Binkley | 2006 | ICPC | **Full-word** identifiers improve comprehension over single letters and opaque abbreviations (**Evidence**: doi:10.1109/ICPC.2006.51). |
| Lawrie, Feild & Binkley | 2009 | Empirical Software Engineering | Very long chained names hurt recall; favour **limited, consistent vocabulary** (**Evidence**: doi:10.1007/s10664-008-9101-7). |
| Butler, Wermelinger & Yu | 2015 | ICPC | Survey of **reference-name** forms (fields, parameters, locals) in 60 Java projects; phrasal structure varies widely (**Evidence**: doi:10.1109/ICPC.2015.30). |
| Butler, Wermelinger & Yu | 2015 | ICSME | **NOMINAL** library for declarative naming checks; developers largely follow conventions but **phrase-level adherence** is uneven (**Evidence**: doi:10.1109/ICSM.2015.7332450). |
| Meyer | 1997 | *Object-Oriented Software Construction* (Prentice Hall) | **Command–query separation (CQS)**: queries return information without abstract side effects; commands change observable state; names should reflect role (Ch. 23). |

#### References (full citations)
- Deißenböck, F., & Pizka, M. (2005). *Concise and Consistent Naming.* Proceedings of the 13th International Workshop on Program Comprehension (IWPC). IEEE. doi:10.1109/WPC.2005.14
- Høst, E. W., & Østvold, B. M. (2009). *Debugging Method Names.* ECOOP 2009, LNCS 5653, pp. 294–317. Springer. doi:10.1007/978-3-642-02032-6_14
- Høst, E. W., & Østvold, B. M. (2009). *The Java Programmer's Phrase Book.* ECOOP 2009 workshop, LNCS, pp. 322–341.
- Arnaoudova, V., Di Penta, M., Antoniol, G., & Guéhéneuc, Y.-G. (2013). *A New Family of Software Anti-Patterns: Linguistic Anti-Patterns.* 17th European Conference on Software Maintenance and Reengineering (CSMR). IEEE. doi:10.1109/csmr.2013.28
- Hill, E., Pollock, L., & Vijay-Shanker, K. (2009). *Automatically Capturing Source Code Context of NL-Queries for Software Maintenance and Reuse.* 31st International Conference on Software Engineering (ICSE). IEEE. doi:10.1109/ICSE.2009.5070524
- Butler, S., Wermelinger, M., Yu, Y., & Sharp, H. (2011). *Improving the Tokenisation of Identifier Names.* ECOOP 2011, LNCS, pp. 130–154. Springer.
- Butler, S., Wermelinger, M., & Yu, Y. (2011). *Mining Java Class Naming Conventions.* 27th IEEE International Conference on Software Maintenance (ICSM). pp. 93–102. doi:10.1109/ICSM.2011.6080776
- Newman, C. D., AlSuhaibani, R. S., Decker, M. J., Peruma, A., Kaushik, D., Mkaouer, M. W., & Hill, E. (2020). *On the Generation, Structure, and Semantics of Grammar Patterns in Source Code Identifiers.* Journal of Systems and Software, 170, 110740. doi:10.1016/j.jss.2020.110740
- Alsuhaibani, R. S., Newman, C. D., Decker, M. J., Collard, M. L., & Maletic, J. I. (2021). *On the Naming of Methods: A Survey of Professional Developers.* 43rd International Conference on Software Engineering (ICSE). IEEE. doi:10.1109/ICSE43902.2021.00061
- Caprile, B., & Tonella, P. (2000). *Restructuring Program Identifier Names.* 16th International Conference on Software Maintenance (ICSM). IEEE. pp. 97–107. doi:10.1109/icsm.2000.883022
- Lawrie, D., Morrell, C., Feild, H., & Binkley, D. (2006). *What's in a Name? A Study of Identifiers.* 14th International Conference on Program Comprehension (ICPC). IEEE. doi:10.1109/ICPC.2006.51
- Lawrie, D., Feild, H., & Binkley, D. (2009). *Identifier Length and Limited Programmer Memory.* Empirical Software Engineering, 14, pp. 263–292. doi:10.1007/s10664-008-9101-7
- Butler, S., Wermelinger, M., & Yu, Y. (2015). *A Survey of the Forms of Java Reference Names.* 23rd International Conference on Program Comprehension (ICPC). pp. 196–206. doi:10.1109/ICPC.2015.30
- Butler, S., Wermelinger, M., & Yu, Y. (2015). *Investigating Naming Convention Adherence in Java References.* 31st International Conference on Software Maintenance and Evolution (ICSME). pp. 41–50. doi:10.1109/ICSM.2015.7332450
- Meyer, B. (1997). *Object-Oriented Software Construction* (2nd ed.). Prentice Hall.

### F2 — Techniques that reduce naming ambiguity
1. **Verb-phrase methods (action + entity)** — Newman et al. (2020); Alsuhaibani et al. Standard 3 (ICSE 2021); Høst & Østvold (ECOOP 2009): callable identifiers should lead with a **verb** naming the operation. Noun-only names are atypical for functions and risk misreading as types or fields (Arnaoudova et al., CSMR 2013).
2. **Query vs command naming (CQS)** — Meyer (*OOSC*): separate read operations (no abstract side effect) from mutating operations; the method name should signal which role the method plays. Khayyam's influenced-variable groups already encode call roles ([Method in Khayyam](../../../../docs/khayyam/method.md)); naming should align.
3. **Domain query verbs for accessors** — A verb that states the operation in domain language (`Elapsed`) is clearer than repeating the field or return type as a bare noun. Alsuhaibani et al. (ICSE 2021): professionals disagree on accessor form, but agree methods should not be opaque.
4. **Name–behaviour alignment checks** — Høst & Østvold (ECOOP 2009); Arnaoudova et al. (CSMR 2013): static analysis can flag noun-named methods that mutate state or verb-named methods that only read — supports governance linting.
5. **Consistent vocabulary** — Deißenböck & Pizka (IWPC 2005); Lawrie et al. (ICPC 2006; ESE 2009): one concept → one term; avoid synonymous verbs in one scope (`find` vs `search`).
6. **Grammar patterns for automation** — Newman et al. (JSS 2020); Hill et al. (ICSE 2009): POS taggers for code (SWUM, POSSE, successors) enable lint rules for `V+NP` vs bare `N` on methods.
7. **Receiver supplies context** — Alsuhaibani Standard 9 (ICSE 2021): avoid repeating owner or class in the method name when the receiver disambiguates — aligns with the [receiver method names rule](../receiver-method-names/receiver-method-names.md).

### F3 — Implicit rules in this repository
Rules that already have folders under `modules/khayyam/rules/` are excluded. **Twelve** implicit or partially documented conventions were found:

| # | Implicit rule | Where visible | Automatable? |
| --- | --- | --- | --- |
| 1 | **`Field_X` field abstraction** — state exposed through accessor methods; declared as `ab` | `modules/net/uri/protocol/scheme.kh`; `modules/time/protocol/time.kh`; `modules/computer/capsule/protocol/field.kh`; 200+ `Field_` in `modules/` | Partially (prefix + kind `ab`) |
| 2 | **Field accessor named for return value**, not doubled field name | [receiver-method-names.md](../receiver-method-names/receiver-method-names.md); `scheme.kh`; `targets/go/abstraction_bridge.py` | Partially (return type) |
| 3 | **`Field_` then qualifier** — `Field_URI_Path`, not `URI_Field_Path` | [qualified-names.md](../qualified-names/qualified-names.md) §Field abstractions; `abstraction_bridge.py` | Yes (spelling) |
| 4 | **Method names as verb phrases** (governance; corpus still has bare nouns) | [method-verb-phrases.md](./method-verb-phrases.md); `encapsulation.md#naming-conventions` (non-binding) | Partial (POS / heuristics) |
| 5 | **PascalCase** for public methods, abstractions, capsules | `encapsulation.md#naming-conventions`; corpus-wide | Yes (casing) |
| 6 | **`protocol/` subtree** for contract declarations | `modules/*/protocol/*.kh` layout | Yes (path) |
| 7 | **Abstraction composition** — `tp X ab { Member1 Member2 }` | `modules/time/protocol/time.kh`; `modules/computer/datatype/protocol/data-type.kh` | Partially |
| 8 | **`self` as receiver parameter name** | `docs/khayyam/method.md#method-structure` | Yes |
| 9 | **Module qualifier only on collision** | [qualified-names.md](../qualified-names/qualified-names.md) | Yes (corpus uniqueness) |
| 10 | **Bare method name when reached via receiver** | [receiver-method-names.md](../receiver-method-names/receiver-method-names.md) | Partially |
| 11 | **Result parameter: first letter of type** | [result-parameter-names.md](../result-parameter-names/result-parameter-names.md) | Yes (tidy) |
| 12 | **Collision = architecture error** (no import alias) | `docs/khayyam/khayyam.md`; [qualified-names.md](../qualified-names/qualified-names.md) | Yes (duplicate plain names) |

Items 1–3 are now also stated in [observer-mutator.md](../../../computer/adt/rules/observer-mutator/observer-mutator.md); item 4 in [method-verb-phrases.md](./method-verb-phrases.md).

### F4 — Field accessor naming options
The receiver (`Field_Scheme`, `Field_Time`) already names **what** is held; the method must name **what it does** (verb phrase). Bare nouns (`Scheme`, `Time`) fail that test (owner ruling; Arnaoudova et al., CSMR 2013; Newman et al., JSS 2020).

| Option | Example | Status | Notes |
| --- | --- | --- | --- |
| **Domain query verb** | `tp Elapsed mt (self Time) () (d Duration)` | **Under examination** — owner 2026-09-29: effective in many places | Verb states the operation in domain language. `Elapsed` returns **`Duration`**, not `Time`. A domain verb must not carry another meaning in the same domain (`Resolve` on a URI field already means reference resolution, RFC 3986 §5), and two field abstractions composed into one owner must not end up with the same verb. |
| **`Get<Concept>`** | `GetScheme` on `Field_Scheme` | **Under examination** | Corpus-common (`get-[noun]`, Høst & Østvold 2009); Alsuhaibani survey split on `getX` vs shorter forms. |
| **`Is` / `Has` predicates** | `IsEmpty`, `HasPort` | **Under examination** (Open Question 4) | Alsuhaibani ICSE 2021 comments; Høst phrase-book predicates. |
| **Bare noun** | `Scheme`, `Time` | **Rejected** | Does not state action; linguistic antipattern risk. |
| **Generic `Read`** | `Read` on every `Field_X` | **Rejected** (owner 2026-09-29) | When one abstraction composes several field abstractions, each would expose `Read` and call sites lose which field is queried; `Read` is a **homonym** of stream I/O read (Deißenböck & Pizka 2005, bijective naming). |
| **`Get…` / `Set…` prefixes (policy)** | `GetTimeout`, `SetTimeout` | **Open** | Neither required nor forbidden by [method-verb-phrases.md](./method-verb-phrases.md). Wording in [Encapsulation → Naming Conventions](../../../../docs/khayyam/encapsulation.md#naming-conventions) is non-binding; owner states he never decided a ban — see [handoff](./method-verb-phrases.handoff.md). |

## Open Questions
Questions 3–4 graduate here while this research is Active; on completion they remain in [method-verb-phrases.handoff.md](./method-verb-phrases.handoff.md) until ruled.

1. **Default pattern for field accessors without an obvious domain verb** — `Get<Concept>`, a coined query verb, or qualify the verb when bare form collides?
2. **`Get…` / `Set…` in this repository** — adopt, discourage, or leave to author choice?
3. **Migration** — rename bare-noun accessors in `modules/` in one pass or grandfather until touched?
4. **Boolean fields** — mandate `Is`/`Has` only, or allow domain predicates (`Empty`, `Open`)?

## Conclusion
Literature supports **verb-phrase method names** and **query/command distinction** as the baseline for [method-verb-phrases.md](./method-verb-phrases.md). **Twelve** implicit conventions were inventoried; `Field_X` shape is now a sibling rule. **Generic `Read` on field accessors is rejected**; **domain query verbs** (`Elapsed`) are effective in many places but are one option among several. **Accessor default** and **`Get`/`Set` policy** remain open. This research stays **Active** until the owner reviews it and the open accessor question is ruled.

## Related Artifacts
| Artifact | Relation |
| --- | --- |
| [method-verb-phrases.md](./method-verb-phrases.md) | Base rule grounded by this research |
| [method-verb-phrases.handoff.md](./method-verb-phrases.handoff.md) | Open accessor and Get/Set questions |
| [observer-mutator.md](../../../computer/adt/rules/observer-mutator/observer-mutator.md) | ADT rule; accessor naming for Observer/Mutator families | Keep in sync |
| [observer-mutator.handoff.md](../../../computer/adt/rules/observer-mutator/observer-mutator.handoff.md) | Observer accessor naming decided in ADT rule | Keep in sync |
| [receiver-method-names.md](../receiver-method-names/receiver-method-names.md) | Bare method spelling when unambiguous |
| [qualified-names.md](../qualified-names/qualified-names.md) | `Field_*` qualification and collisions |
| [Documentation — Research](../../../../docs/documentation-research.md) | Governs this artifact |

## Notes
- Prior draft lived at `chats-context/memar-go-migration/decisions/method-naming-research.md` (2026-09-29); superseded by this file.
- Butler et al. (2015): the ICPC paper surveys reference-name **forms**; the ICSME paper presents **NOMINAL** adherence checking — previously conflated under one venue in the draft table.

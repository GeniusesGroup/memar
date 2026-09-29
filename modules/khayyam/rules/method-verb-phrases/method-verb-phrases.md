---
Title: "Khayyam Rule — Method Verb Phrases"
Status: Draft
Start Date: 2026-09-29
ID: 510442
---

# Khayyam Rule — Method Verb Phrases
Khayyam's rules live one rule per folder under [`modules/khayyam/rules/`](../README.md), and this is the rule for the shape a method name takes when the name must state what the method does without reading the comment or body. It is a governance rule of this repository, companion to the [receiver method names rule](../receiver-method-names/receiver-method-names.md) (which governs whether a method keeps a bare name) and the [observer and mutator rule](../../../computer/adt/rules/observer-mutator/observer-mutator.md) (which governs `Observer_X` / `Mutator_X` accessor and mutator naming; the Get/Set question here applies outside those families).

## The rule
A method name is a verb phrase: it names an action — a verb or verbal head — applied to the concepts named in the rest of the phrase. A bare noun or noun phrase alone is not a method name; the reader should know what the method does from the name alone.

Query methods — those whose influenced variables receive data and whose implementation does not change observable state of the receiver or influencing variables (Meyer, command–query separation) — use a query verb. A domain-specific verb (`Elapsed`) is effective in many places, provided it carries no other meaning in the same domain and does not collide with a sibling field's verb inside one composing owner. Boolean predicates use `Is` or `Has` when that fits the domain. Mutating methods use a domain command verb (`ApplyTimeout`, `AssignPort`).

The receiver supplies context for what is acted on; the method name does not repeat the owner's or field abstraction's name unless the bare verb is ambiguous in the corpus ([receiver method names rule](../receiver-method-names/receiver-method-names.md)).

`Get…` and `Set…` prefixes are neither required nor forbidden by this rule. Whether they belong in this repository is an open question — see the [handoff](./method-verb-phrases.handoff.md).

A generic `Read` on a `Field_X` accessor is not recommended: when one abstraction composes several field abstractions, each would offer `Read` and the call site loses which field is queried; `Read` is also a homonym of stream I/O read (Deißenböck & Pizka 2005). How a field abstraction's query method is named is open in the handoff.

### Examples — good
```khayyam
tp Elapsed mt (self Time) () (d Duration)
tp ApplyTimeout mt (self AppConfig) (timeout Duration) (err Error)
tp IsEmpty mt (self Container) () (empty Boolean)
```

### Examples — bad
```khayyam
tp Scheme mt (self Field_Scheme) () (s URI_Scheme)      // noun only — action unclear
tp Time mt (self Field_Time) () (t Time)                // noun only
```

## Research
Literature review, implicit-rules inventory, and accessor options (including rejected `Read`): [Method Verb Phrases Research 001](./method-verb-phrases.research.001.md).

## Why it exists
Callable identifiers in professional practice and in corpus studies predominantly follow verb-phrase grammar (Newman et al., J. Systems & Software 2020; Alsuhaibani et al., ICSE 2021). Noun-only method names risk linguistic antipatterns — a name that says more than the method does, or less (Arnaoudova et al., CSMR 2013). Method phrases in Programmer English are natural-language behaviour descriptions whose first token is typically verbal (Høst & Østvold, ECOOP 2009). Separating query from command at the name supports command–query separation (Meyer, *Object-Oriented Software Construction*). Names should map concisely and consistently to concepts (Deißenböck & Pizka, IWPC 2005).

## Keep it or drop it
An organization may require `Get`/`Set`, allow bare nouns when the receiver is a field abstraction, or qualify every method with its owner. This rule is Geniuses.Group's convention for this repository, not a language guarantee.

## What this rule does not claim
- It does not claim the grammar rejects non-verb method names.
- It does not forbid or require `Get`/`Set` prefixes — that question is open in the [handoff](./method-verb-phrases.handoff.md).
- It does not prescribe `Read` as the default field accessor.
- It does not override the [receiver method names rule](../receiver-method-names/receiver-method-names.md) or the [qualified names rule](../qualified-names/qualified-names.md).

## Open questions
This rule's own open state lives in its [handoff](./method-verb-phrases.handoff.md).

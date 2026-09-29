---
Title: "ADT Rule — Observer and Mutator"
Status: Draft
Start Date: 2026-09-29
ID: 510443
---

# ADT Rule — Observer and Mutator
Rules for the ADT module live one rule per folder under [`modules/computer/adt/rules/`](../README.md). This rule governs abstract state a capsule exposes through methods without naming storage — the observer and mutator families from Liskov & Guttag's ADT operation classification. It is a governance rule of this repository, companion to the [qualified names rule](../../../../khayyam/rules/qualified-names/qualified-names.md) (collision and qualification over `Observer_*` spellings) and the [method verb phrases rule](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.md) (verb-phrase shape for methods outside these families).

## The rule
An **observer** abstraction is declared as an abstraction (`ab`) whose name is `Observer_` followed by the concept name. Any qualifier the concept needs comes after `Observer_`, never before: `Observer_Scheme`, `Observer_URI_Path`, `Observer_Time_Access`.

The observer abstraction declares one or more methods with `self` typed as that observer abstraction. Those methods return information about abstract state without changing it. An observer's method is **`Get` followed by the full concept in natural English order** — the same word order a reader would use in prose, not the underscore order of the abstraction name. `Observer_Time_Access` → `GetAccessTime`; `Observer_Scheme` → `GetScheme`; `Observer_URI_Path` → `GetURIPath`. A plain `GetTime` is acceptable only where the general concept is really meant; the correct default is a method name that fully represents the concept, and modules that expose time should state which reading they intend. Bare-method spelling when unambiguous is governed by the [receiver method names rule](../../../../khayyam/rules/receiver-method-names/receiver-method-names.md).

A **mutator** abstraction is declared as an abstraction (`ab`) whose name is `Mutator_` followed by the concept name, with the same qualifier-after-prefix spelling as observers. Its methods change abstract state. A mutator's method uses a **domain verb** when one fits the operation (`Rename`, `Clear`, `Append`); when no domain verb fits, use **`Set` followed by the full concept** in the same natural English order as observers (`SetMemoryAddress` on `Mutator_SetMemoryAddress`). When mutation on one piece of state is paired with an observer for the same state, both are composed into the owning abstraction (`Observer_MemoryAddress` and `Mutator_SetMemoryAddress` on `Memory_Pointer`).

An entity's command surface that groups several mutating methods and no queries is a single `Mutator_<Entity>` bundle (`Mutator_File`). When a bundle mixes queries and mutations, split it into `Observer_<Entity>` and `Mutator_<Entity>` (command–query separation).

A capsule or abstraction that holds the state composes observer and mutator abstractions in its `ab { … }` block and implements their methods. The abstraction is the contract; the capsule chooses representation.

A module prefix on `Observer_*` or `Mutator_*` is kept only when the bare concept after the prefix is ambiguous in the corpus — the same collision criterion as the [qualified names rule](../../../../khayyam/rules/qualified-names/qualified-names.md). The owner's ruling on `modules/net/uri/protocol/scheme.kh` (2026-09-29) is the example: `Observer_Scheme` when one module claims a scheme; `Observer_URI_Path` when five modules claim a path; `Observer_Time_Access` when the accessor returns a `Time`.

### Side files
A type's observer and mutator abstractions **strongly default** to companion files beside the type's protocol file: `time.observers.kh` and `time.mutators.kh` next to `time.kh` under the same `protocol/` folder (for example `modules/time/protocol/`). This keeps query and command contracts readable without crowding the main protocol file. It is a strong default, not mandatory — a module may keep all three in one file when the surface is small.

### Examples — good
```khayyam
tp Observer_Scheme ab {
    GetScheme mt (self Observer_Scheme) () (s URI_Scheme)
}

tp Observer_Time_Access ab {
    GetAccessTime mt (self Observer_Time_Access) () (t Time)
}

tp URI ab {
    Observer_Scheme
    Observer_URI_Path
}

tp Mutator_File ab {
    Rename mt (self Mutator_File) (n String) (err Error)
}
```

### Examples — bad
```khayyam
tp URI_Observer_Scheme ab          // qualifier before Observer_
tp Observer_Scheme mt (self Observer_Scheme) () (s URI_Scheme)  // bare noun accessor — use GetScheme
tp Observer_Time_Access mt (self Observer_Time_Access) () (t Time)  // GetTime when AccessTime is meant
tp Mutator_SetMemoryAddress mt (self Mutator_SetMemoryAddress) (a Memory_Address) ()  // bare Set — use SetMemoryAddress
```

## Research
Observer accessor naming options and literature grounding: [Method Verb Phrases Research 001](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md) (F3–F4). Observer vs `Mutator_*` counterpart: [Observer and Mutator Research 001](./observer-mutator.research.001.md).

## Why it exists
Separating the query contract (`Observer_X`) from the command contract (`Mutator_X`) supports command–query separation (Meyer, *OOSC* Ch. 23; Liskov & Guttag, *Abstraction and Specification in Program Development*, MIT Press, 1986 — creators, producers, observers, mutators). The names also agree with [Agency → From Observer to Agent](../../../../../docs/agency.md#from-observer-to-agent), where an observer sees a System without acting on it. Fields are not public; only methods on these abstractions cross the boundary ([Encapsulation in Khayyam](../../../../../docs/khayyam/encapsulation.md)). `modules/computer/capsule/protocol/field.kh` is the meta-model for capsule-held state.

## Keep it or drop it
An organization may expose state through owner methods only, use another prefix, or use public fields in another language. This rule is Geniuses.Group's convention for Memar protocol modules that model ADT-held state.

## What this rule does not claim
- It does not claim Khayyam has a `field` keyword or enforced privacy.
- It does not claim every piece of state needs an `Observer_X` abstraction.
- Whether `Get…` / `Set…` prefixes are discouraged **outside** observer and mutator families remains open in the [method verb phrases handoff](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.handoff.md).
- `Observer_` here is not the GoF Observer pattern (event subscriber); the event module must not reuse the name.

## Open questions
This rule's own open state lives in its [handoff](./observer-mutator.handoff.md).

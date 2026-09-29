# ADT Rules (`modules/computer/adt/rules/`)

Rules for abstract data types in this module — conditions the ADT protocol corpus is held to. The general Memar concept of Rule is defined in [`docs/rule.md`](../../../../docs/rule.md).

| Rule | Subject | What it is |
| --- | --- | --- |
| [Observer and Mutator](./observer-mutator/observer-mutator.md) | `Observer_X` / `Mutator_X` state contracts | Query state via `Observer_`; change it via `Mutator_`; accessor and mutator method naming; side-file layout |

Khayyam toolchain rules (qualified names, method verb phrases, receiver method names) remain under [`modules/khayyam/rules/`](../../../khayyam/rules/README.md) and are cited from ADT rules where they apply.

# ADT Rules (`modules/computer/adt/rules/`)
Rules for abstract data types in this module — conditions the ADT protocol sources are held to. The general Memar concept of Rule is defined in [`modules/process/rule/rule.md`](../../../process/rule/rule.md).

| Rule | Subject | What it is |
| --- | --- | --- |
| [Observer and Mutator](./observer-mutator/observer-mutator.md) | `Observer_X` / `Mutator_X` state contracts | Query state via `Observer_`; change it via `Mutator_`; accessor and mutator method naming; side-file layout |
| [A Collection Composes the Container](./collection-composes-container/collection-composes-container.md) | A collection of a domain element | The collection composes `Container_GetElement` and `Container_Count`; it does not declare `Count` again or take a capsule such as `W32` |

Khayyam toolchain rules (qualified names, method verb phrases, receiver method names) remain under [`bundles/khayyam/rules/`](../../../../bundles/khayyam/rules/README.md) and are cited from ADT rules where they apply.

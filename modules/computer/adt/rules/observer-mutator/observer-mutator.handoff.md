# ADT Rule — Observer and Mutator Handoff
Open state for [observer-mutator.md](./observer-mutator.md). See the repository's [documentation-handoff.md](../../../../../docs/documentation-handoff.md) for what a handoff is.

## Status
Active — rule relocated from `modules/khayyam/rules/observer-mutator-abstractions/` to `modules/computer/adt/rules/observer-mutator/` 2026-09-29 (owner). Observer/mutator family names, method naming, and side-file default decided same day.

## Decisions
- **An observer abstraction is `Observer_<concept>`, qualified after `Observer_` only when the corpus makes the concept ambiguous** — Decided (2026-09-29, owner). `URI_Field_Scheme` was poor; `Field_URI_Scheme` better; `Observer_Scheme` best when `URI` only repeats where the file lives. Applied by `abstraction_bridge.py observer-names`.
- **Declared as `ab`; methods use `self Observer_X` or `self Mutator_X`; composed into owners** — Decided (2026-09-29, owner). Extracted from [qualified names](../../../../khayyam/rules/qualified-names/qualified-names.md) into this rule.
- **Observer and mutator family prefixes** — Decided (2026-09-29, owner). **`Observer_X`** for abstractions that return information about abstract state without changing it; **`Mutator_X`** for abstractions that change it. Both come from Liskov & Guttag's ADT operation classification (creators, producers, observers, mutators). Rejected: `Field_`/`Method_` (ambiguous roles), `Command_` (may only report), `Selector_`/`Modifier_`, `Accessor_`, `Query_`. Entity command bundles use `Mutator_<Entity>` when all methods mutate; mixed bundles split into `Observer_<Entity>` and `Mutator_<Entity>` (`Method_Directory_Helpers`, `Method_File_GUI` in the pre-rename corpus). Corpus renamed 2026-09-29.
- **Observer accessor naming** — Decided (2026-09-29, owner). An observer's method is `Get` followed by the full concept in natural English order (`Observer_Time_Access` → `GetAccessTime`; `Observer_Scheme` → `GetScheme`). Plain `GetTime` only when the general concept is really meant. Stated in [observer-mutator.md](./observer-mutator.md); closes the Observer/Mutator slice of the open question in [method verb phrases handoff](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.handoff.md).
- **Mutator method naming** — Decided (2026-09-29, owner). Domain verb when one fits (`Rename`); otherwise `Set` followed by the full concept (`SetMemoryAddress`).
- **Side files for observer and mutator families** — Decided (2026-09-29, owner). Strong default: companion files beside the type's protocol file (`time.observers.kh`, `time.mutators.kh` next to `time.kh`); not mandatory.

## Open Questions
- **Which module owns a concept declared twice** — `Record_Observer_RecordUUID` / `Storage_Observer_RecordUUID` and related pairs; see [qualified names handoff](../../../../khayyam/rules/qualified-names/qualified-names.handoff.md).

## Related Artifacts
| Artifact | Relation | Action |
| --- | --- | --- |
| [observer-mutator.md](./observer-mutator.md) | Base — the rule | Keep in sync |
| [qualified-names.md](../../../../khayyam/rules/qualified-names/qualified-names.md) | Sibling — collision logic; observer shape lives here | Keep in sync |
| [method-verb-phrases.md](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.md) | Sibling — verb phrases outside Observer/Mutator families | Keep in sync |
| [receiver-method-names.md](../../../../khayyam/rules/receiver-method-names/receiver-method-names.md) | Sibling — bare accessor when unambiguous | Keep in sync |
| [modules/net/uri/protocol/scheme.kh](../../../../net/uri/protocol/scheme.kh) | Example — owner's observer-shape ruling | None (read) |
| [targets/go/abstraction_bridge.py](../../../../khayyam/targets/go/abstraction_bridge.py) | Implements — `observer-names` mode | Keep in sync |
| [method-verb-phrases.research.001.md](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md) | Evidence — accessor naming research | None (read) |
| [observer-mutator.research.001.md](./observer-mutator.research.001.md) | Evidence — Field/Method pair research; led to Observer/Mutator decision | None (read) |

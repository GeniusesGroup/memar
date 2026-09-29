# ADT Rule — Observer and Mutator Changelog

## Changelog

### Rule relocated to ADT module; method naming and side files decided
- Time: 2026-09-29T21:00:00Z
- Type: Changed
- Cited:
  - [Rule → Where Rules Live: rules/ Beside protocol/](../../../../../docs/rule.md#where-rules-live-rules-beside-protocol) - Premise: ADT subject owns observer/mutator governance, not Khayyam grammar.
  - [observer-mutator.handoff.md](./observer-mutator.handoff.md) - Premise: owner decisions on Get/Set naming and side-file default.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Moved rule from `modules/khayyam/rules/observer-mutator-abstractions/` to `modules/computer/adt/rules/observer-mutator/`; renamed documents to `observer-mutator.*`.
- Added observer accessor naming (`Get` + full concept in natural English order) and mutator naming (domain verb, else `Set` + full concept) to [observer-mutator.md](./observer-mutator.md).
- Added side-file default (`*.observers.kh`, `*.mutators.kh` beside the protocol file) to the rule.
- Added [rules README](../README.md) index for `modules/computer/adt/rules/`.
- Updated cross-references in Khayyam rules, `docs/rule.handoff.md`, and `docs/protocols/computer/adt.handoff.md`.

### Observer and Mutator family rename; corpus migrated
- Time: 2026-09-29T18:00:00Z
- Type: Changed
- Cited:
  - [Abstraction and Specification in Program Development](https://mitpress.mit.edu/9780262121125/abstraction-and-specification-in-program-development/) (Liskov & Guttag, MIT Press, 1986) - Premise: ADT operation classification (observers, mutators).
  - [Agency → From Observer to Agent](../../../../../docs/agency.md#from-observer-to-agent) - Premise: observer sees without acting.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Renamed rule folder `field-abstractions/` → `observer-mutator-abstractions/` and rule documents accordingly.
- Corpus: `Field_*` → `Observer_*`, `Method_*` → `Mutator_*`; mixed bundles `Method_Directory_Helpers` and `Method_File_GUI` split per command–query separation.
- `abstraction_bridge.py` mode `field-names` → `observer-names`.
- Owner decision moved from handoff open questions to Decisions.

### Field abstractions rule added; shape moved from qualified names
- Time: 2026-09-29T12:00:00Z
- Type: Added
- Cited:
  - [Concise and Consistent Naming](https://doi.org/10.1109/WPC.2005.14) (Deißenböck & Pizka, IWPC 2005) - Premise: consistent `Field_` role marking.
  - [On the Generation, Structure, and Semantics of Grammar Patterns in Source Code Identifiers](https://doi.org/10.1016/j.jss.2020.110740) (Newman et al., J. Systems & Software 2020) - Premise: attribute vs function grammar patterns.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- Added [field-abstractions.md](./field-abstractions.md), [field-abstractions.handoff.md](./field-abstractions.handoff.md), and this changelog from [Method Verb Phrases Research 001](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.research.001.md).
- §Field abstractions removed from [qualified-names.md](../../../../khayyam/rules/qualified-names/qualified-names.md) with a link here.
- Index entry added in [Khayyam rules README](../../../../khayyam/rules/README.md).

### Good example no longer picks an accessor name
- Time: 2026-09-29T12:30:00Z
- Type: Changed
- Cited:
  - [Method Verb Phrases Handoff](../../../../khayyam/rules/method-verb-phrases/method-verb-phrases.handoff.md) - Premise: how a query on a field abstraction is named is open.
  - [RFC 3986 §5 Reference Resolution](https://www.rfc-editor.org/rfc/rfc3986#section-5) - Premise: `Resolve` on a URI already means reference resolution.
- Contributors:
  - Auto (model not recorded) via [Cursor](../../../../../CONTRIBUTORS.md#cursor) - applied

#### What changed
- The good example showed `Resolve` on `Field_Scheme` and `Elapsed` on `Field_Time`. The first carries another URI meaning; the second is not an accessor of the held `Time`. The example now shows only the shape and composition, with the accessor omitted until the open question is ruled.

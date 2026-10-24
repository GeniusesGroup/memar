# URI Handoff

## Topic & Purpose
State of converting `modules/identity/uri/` from Go to Khayyam under the seven governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md): what each of the five protocol files now declares, which of those were judgment calls, and what is still undecided or blocked on a domain this one does not own.

## Status
Active — the five `.kh` files are converted and return `accept` from the Khayyam frontend once the imports they name are supplied; three of the declarations they depend on do not exist in the tree yet.

## Decisions

- **Decided: this domain declares no UUID of its own.** `protocol/dt-uuid.kh` includes `ThingUUID` from the thing domain rather than declaring a `URIUUID`. Reason: a URI record is a thing (`URIModel` composes `ThingModel`), so its identity is the thing's identity, and a second value abstraction over the same record identifier would be two abstractions claiming one concept — the architecture error rule 3 names. This is the route `modules/identity/time/protocol/dt-uuid.kh` already took.
- **Decided: `Field_URI` is split into `Field_URIID` and `Field_QuiddityURI`.** The Go source declared `Field_URI` twice inside this one domain — once returning the record's UUID in `protocol/dt-uuid.kh`, once returning the URI bytes in `widgets/quiddity-uri/protocol/dt-uri.kh`. Two plain names with two meanings inside one domain is a collision to be qualified, never aliased.
- **Decided: the widget's URI value is `QuiddityURI` and composes memar's `String`.** Bare `URI` is already claimed by `memar/modules-plugable/net/uri/protocol/uri.kh`, so a qualified name was owed anyway; composing `String` gives the value the two behaviors the domain actually needs — equality for the storage lookup by value, rendering for the readonly label — instead of the empty abstraction rule 6 forbids. memar declares its own URI parts (`URI_Host`, `URI_Path`) the same way.
- **Decided: `DataModel` becomes `QuiddityURIDataModel` and `StorageServices` becomes `QuiddityURIStorage`.** Rule 3 full domain-qualified names; `StorageServices` also drops the utility-flavoured "Services" that the domain-capsule-naming rule discourages.
- **Tentative: `QuiddityURI ab { String }` may over-require.** It hands every URI value split, join, clone and character-encoding behavior the domain never asks for. A narrower composition (equality and rendering only) may be the better contract; nothing in the domain document rules the wider one out, and no implementer exists to say which it needs.
- **Explored-but-unresolved: two accessor spellings now sit side by side** — bare `URIID` for an identity, `GetURI` for a value. The bare form follows this repository's converted `Field_*` files; `Get…` follows memar's value accessors and the method-verb-phrases rule. One of the two has to go, and the choice belongs to the repository rather than to one domain.

## Ambiguities Resolved

- Whether the URI domain's UUID is the same concept as the user domain's `UserUUID`: they are the same concept under two spellings, not two concepts, and neither is a competing abstraction of the other. Evidence: every one of the 90 `dt-uuid.kh` files in the tree declares `type UUID <other>_p.UUID`, every chain ends at the storage record UUID, and `thing/protocol/dt-uuid.kh` states the identifier "MUST be unique ID in all domains".
- Whether a URI record may carry an identity of its own: not on the evidence available. The domain document describes only the value — a locale name in the computer world, produced by URI protocols elsewhere — and nothing here mints an identifier.

## Open Questions

- **Highest-leverage conversion left in the repository:** `modules/identity/thing/protocol/dt-uuid.kh` is unconverted. It has to declare `ThingUUID` and `Field_ThingUUID` before this domain's files resolve, before `modules/identity/time/` resolves, and before the many other `dt-uuid.kh` files that already import those names can be written at all.
- **Blocks this domain's `model.kh`:** `modules/knowledge/text/protocol/model.kh` is unconverted, so the `TextModel` entry in `URIModel` cannot resolve. The Go source listed `text_p.Model` as a requirement of the URI model, and that requirement is preserved in source but unresolved in the tree.
- May a URI record's identity ever diverge from its thing identity? If it may, `protocol/dt-uuid.kh` needs a `URIUUID` value abstraction after all, and every `URIID` implementation changes with it.
- Should `widgets/quiddity-uri` carry documents of its own? The sibling widget of the same shape, `modules-plugable/uri/username/ui/`, has none at all, so there is no precedent either way; this domain's widget is currently described from [`uri.md`](uri.md).

## Assumptions

- **`ThingUUID` and `Field_ThingUUID` are the names the thing domain will declare** — stability: Weak. They are read off `modules/identity/time/protocol/dt-uuid.kh`, which already imports them, so this domain is following a sibling conversion rather than a decided convention. Different names there mean four of these five files change.
- **`TextModel` is the name the text domain will declare for its `Model`** — stability: Weak. It follows rule 3 and the `ThingModel` / `UserModel` precedent rather than any statement by the text domain.
- **The `org/` and `memar/` import roots resolve through a manifest that does not exist yet** — stability: Strong. Rule 7 of the migration map already names the missing stack as the hard gate, and every converted file in the repository refuses `unresolved-import` on disk for that reason alone.

## Proposed Next Steps

1. Convert `modules/identity/thing/protocol/dt-uuid.kh` (declaring `ThingUUID`, `Field_ThingUUID`) and `modules/knowledge/text/protocol/model.kh` (declaring `TextModel`). Each is a short addition that unblocks files this domain has already written.
2. Decide the `Field_*` accessor spelling for the whole repository — bare noun or `Get…` — and sweep the converted files together rather than leaving the two forms adjacent.
3. Record in the migration map that a domain whose model extends `ThingModel` includes `ThingUUID` instead of declaring its own, so that the `user`, `organization`, `time` and `uri` forks converge on one answer instead of three.

## Related Artifacts

- [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) — the seven governing rules; where the UUID and accessor decisions above should graduate.
- `modules/identity/thing/protocol/dt-uuid.kh` — must declare `ThingUUID` and `Field_ThingUUID`.
- `modules/knowledge/text/protocol/model.kh` — must declare `TextModel`.
- `modules/identity/time/protocol/dt-uuid.kh`, `modules/identity/organization/protocol/dt-uuid.kh` — the two conversions that answered the UUID question differently from this one; the `organization` file re-imports the pilot's `UserUUID`.
- `modules-plugable/uri/uri.md` — the URI protocol family that produces the values this domain stores.
- `modules-plugable/uri/username/ui/protocol/` — the sibling widget of the same shape; its `Field_Username` shows what avoiding this domain's two `Field_URI`s looks like.

## Notes

- The frontend was run with `overrides` standing in for the unresolvable `org/` and `memar/` roots and for the two unconverted neighbouring protocol files. All five files return `accept` that way. Run against the tree as it stands, all five return `refuse` / `unresolved-import` — the same condition every already-converted file outside this domain that carries an import is in, and not a property of these five.
- `abstraction_bridge.py go-to-khayyam` produced no output for these five paths, so nothing here is tool-suggested; every declaration was written by hand against the rules.
- `memar-documentation.py --newline crlf` writes the literal text `crlf` where a carriage return and line feed belong: `write_utf8` expects `"\r\n"` and is handed the choice string. Omitting the flag lets the file's own convention be detected, which is what these files were written with.
- The two `README.md` files already in this domain have no final newline. The new `README.md` here has one; the older two were left as they are.

# Time Handoff

## Topic & Purpose

Converting the Khayyam protocol layer of `modules/identity/time`: the identity surface the domain owns (`protocol/dt-uuid.kh`) and the `ttl` edge's protocol (`edges/ttl/protocol/ttl.kh`), under the governing rules in [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md).

## Status

Protocol layer converted (2026-10-02). `edges/ttl/protocol/ttl.kh` accepts against the Khayyam frontend as written. `protocol/dt-uuid.kh` accepts only once `modules/identity/thing/protocol/dt-uuid.kh` declares the identity abstraction it includes — that file is still a Go block, and it belongs to another domain.

The substance this domain was expected to carry is not here: see Open Questions, `dt-signal_data`.

## Decisions

- **A time's identity is the thing domain's identity — the same concept, not a new one.** The Go source wrote `type UUID thing_p.UUID`, a Go named-type re-declaration of one concept, and the thing domain's own comment says its UUID is the base identifier for every domain and "can be same with any other UUID domains e.g. user". Khayyam has no alias form, so carrying the same concept into this domain under a second name would be two abstractions claiming one thing — the architecture error rule 3 names, and the one `qualified-names` answers with one declaration the other module includes. So `dt-uuid.kh` includes the thing domain's declaration and keeps only what the time domain owns: the requirement that a time can be named, `Field_TimeID` with its accessor `TimeID` (body generated under rule 2).
  - This is the same concept as the user domain's pilot `UserUUID` and as the thing domain's `UUID`; one owner, one declaration, and this domain is not it.
  - Cost: the file refuses `name-not-declared` until that owner converts, and it assumes the conversion names the abstraction `ThingUUID` (bare `UUID` stays claimed by the record and memory modules).
- **`ttl` names a span, not a unit.** `TTL() duration.NanoSecond` became `TimeToLive mt (self Field_TimeToLive) () (d Duration)`. An abstraction-owned method may name only abstractions, and `Duration` is one while `NanoSecond` is a capsule; separately, a contract that fixed the unit would pin every realization to nanoseconds for no gain in meaning.
- **The getter surface is a `Field_*` abstraction and its accessor keeps the field's name.** `Field_TimeToLive` + `TimeToLive` matches every `Field_X` accessor in the corpus (`Field_CountUnitID` → `CountUnitID()`, `Field_ThingUUID` → `ThingUUID()`) and leaves rule 2's generator able to produce the body from the field's name. `method-verb-phrases` discourages a noun-only method name and leaves field-accessor naming open, so the corpus convention was followed and the tension is recorded rather than resolved here.
- **No explanatory comments above the Khayyam** (rule 5). The one Go comment in the domain — the TTL definition — became content in [`edges/ttl/ttl.md`](edges/ttl/ttl.md).

## Ambiguities Resolved

- **The time domain declares no `Time` at all — did that source live in another repository, or was it never written?** — answered (2026-10-08): it lived in memar. `memar/modules/time/protocol/time.kh` declares `tp Time ab` (with `Observer_Epoch`); `utc_epoch.DayInWeek` is `memar/modules-plugable/time/utc/epoch/day-in-week.kh` (`var DayInWeek = day_in_week{}`); `duration.Second` is `memar/modules/time/duration/protocol/second.observers.kh` (`Observer_Duration_Second`, `GetDuration`). A conversion imports them the way [`edges/ttl/protocol/ttl.kh`](edges/ttl/protocol/ttl.kh) already imports `Duration` from `memar/modules/time/duration/protocol/duration.kh`. What is genuinely absent stays open below: the `Field_*` accessors.

## Open Questions

- **`dt-signal_data` is not in this domain.** `git ls-files modules/identity/time` returns six files, none of them a signal file. `dt-signal_data.kh` and the three `service-signal-*.kh` files live in `modules/computer/device/protocol/`, and what they declare is not a vocabulary of signal states either: `SignalData() []byte` — the payload a device sends from an output or receives at an input, with a note that large formats belong to the content and object modules. That is the device domain's work and it was not touched here.
- **`Field_Epoch` and `Field_Time` are declared in neither repository.** The `Time` surface resolves to memar (see Ambiguities Resolved), but these two accessors — named by consumer requirements across the tree — appear in no converted protocol here and in no memar declaration (the only memar hit is a changelog example). Requirements are re-modelled at conversion, so the open question is what replaces them, not where to import them from.
- **`Field_TimeID` has no consumer.** Nothing in the tree composes it or calls it, and `time_p.UUID` is referenced nowhere. If the surface is not wanted, deleting it is cheaper than converting it; if it is wanted, the domain needs to say which records carry it and why a time's identity is not simply `Field_ThingUUID`.
- **Span or instant?** [`edges/ttl/ttl.md`](edges/ttl/ttl.md) models the edge as `(time)-[:TTL]->(thing)` — an absolute instant — while the Go surface is a span held by a record. Both cannot be the edge. Settling it needs the `Time` above.
- **`TTL` is claimed by two different concepts.** `modules/computer/instance_of/edges/health/protocol/business-services.kh` declares `BS_Ping_Request.TTL() duration.NanoSecond` — a network ping timeout, not a record's expiry. Different receivers, so no method collision today, but under `qualified-names` one of the two wants its module's path in the name. Not this domain's file to change.
- **The memar module's name may still move.** Both files here address the memar module by URI, and `ttl.kh` imports `Duration` from `memar/modules/time/duration/protocol/duration.kh`, which declares it bare. `qualified-names` says a name in `time/duration` carries its module (`Time_Duration`). If the memar module renames it, this import breaks by name.
- **`Duration` may be the wrong concept here.** `memar`'s `Duration` is an int64 nanosecond count whose own comment fixes its largest span at roughly 290 earth years. A TTL contract that may be exceeded by that bound, or that wants a calendar-aware span, is asking for a different concept. Naming it is the memar module's decision, not this file's.

## Related Artifacts

| Artifact | Relation | Action |
| --- | --- | --- |
| [`time.md`](time.md) | Domain document | Keep in sync |
| [`edges/ttl/ttl.md`](edges/ttl/ttl.md) | The edge's document — TTL definition and its open questions | Keep in sync |
| [`protocol/dt-uuid.kh`](protocol/dt-uuid.kh) | Identity surface; includes the thing domain's declaration | None |
| [`edges/ttl/protocol/ttl.kh`](edges/ttl/protocol/ttl.kh) | The edge's surface | None |
| `modules/identity/thing/protocol/dt-uuid.kh` | The declaration this domain includes | Convert it, naming the abstraction `ThingUUID` (Review) |
| `modules/identity/user/protocol/dt-uuid.kh` | The pilot whose shape this domain follows | Fix its accessor (Review) |
| `modules/computer/device/protocol/dt-signal_data.kh` | Where the signal vocabulary actually lives | None (read) |
| [`../../../Khayyam.practice.md`](../../../Khayyam.practice.md) | Governing rules 1–7 for this conversion | None (read) |

## Notes

- **Frontend results.** `edges/ttl/protocol/ttl.kh` — accept. `protocol/dt-uuid.kh` — refuse `name-not-declared` against the tree as it stands; accept when `modules/identity/thing/protocol/dt-uuid.kh` declares `ThingUUID`, verified by supplying that file as an override. Nothing was suppressed; the one refusal is a true statement about a file another domain still owns.
- **The frontend resolves one root**, so neither this repository's `org/...` URIs nor a cross-module `memar/...` URI can be checked from this repository's root alone. Both files were checked from a junction root carrying `org/` → this repository, `memar/` → the memar repository and `modules/` → the memar repository's own module path, so every URI resolved to the real file it addresses. Where those roots come from is the manifest's business under the import-address rule, and no manifest exists yet.
- **Tooling defect.** `memar-documentation.py edit --newline crlf` (and `write`) writes the literal word `crlf` into the file: the argparse choice is handed to `write_utf8` as the replacement string instead of being mapped to `\r\n`. It corrupted `protocol/dt-uuid.kh` mid-conversion; the file was restored and rewritten without the flag, letting `detect_newline` read the file's own ending. Worth reporting to whoever owns the script.
- **Pilot check.** `modules/identity/user/protocol/dt-uuid.kh` refuses `declaration-form` at its line 15: the accessor writes `(UserUUID)` where the grammar wants a name and a type, `(id UserUUID)`. Not this domain's file, but it is the shape this conversion copies, so the copied shape is the corrected one.

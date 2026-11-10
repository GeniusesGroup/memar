---
Title: "Codec Rule — Format Adjuncts"
Labels: Draft
Start Date: 2026-11-10
ID: 498420
---
# Codec Rule — Format Adjuncts
Rules for [Codec](../../codec.md) live one rule per folder under [`modules/computer/codec/rules/`](../README.md). This rule says how a Memar module publishes encode/decode for a storage or wire **format** as Khayyam companions, so [Memory Store](../../../memory/store/store.md) stays a thin contract over addresses and batches and never owns “how a type looks as bytes.”

## The rule

### Companion naming and placement
- A type that publishes encode/decode for a named format does so in a companion beside the type’s protocol file: `<base>.codec.<format>.kh` next to `<base>.kh` (same `protocol/` folder).
- Naming follows the existing companion pattern (dot separates facet from base): `<base>.eng.kh`, `<base>.observers.kh`, `<base>.mutators.kh`, `<base>.bindings.kh`.
- Facet key is `codec`. The third segment is the **format** identity — in the spirit of a [Media Type](../../../mediatype/mediatype.md) codec suffix (`syllab`, `json`, `xml`, `protobuf`, `flatbuf`, …): it names a real encoding, not a UI face or UI module. Short forms are fine (`json`, `argv`). A name that means a face (e.g. `command` for the command UI) is refused as a format segment.
- One format per companion file. The companion holds that format’s encode/decode (and its refusals) for this type and nothing else.
- Adjuncts are optional at the Type level: a type with no `.codec.<format>.kh` remains a valid Type. Whether a **consumer** may still use that format without the adjunct is governed by [Missing adjunct: compile vs runtime (manifest key)](#missing-adjunct-compile-vs-runtime-manifest-key) below — not by inventing parse code inside a service.

### What a format codec may and may not own
A format codec is [Codec](../../codec.md): value ↔ form; it says nothing about what the value means.

**May**
- Encode the type’s value into that format; decode it back; refuse undecodable forms (`Codec_Error_NotDecodable` or a mapped refusal).
- Use only structure the type (or the owning abstraction) already declares — including TypeUUID maps the type already states.

**Must not**
- Own addresses, batch ordering, compare-and-swap, or any other store-contract concern.
- Invent domain or graph vocabulary on the wire. Graph concept rules (TypeUUID for Node, relation keys, side envelopes, typed edge fields) stay in **graph abstractions**; the codec only packs and unpacks the structure those abstractions already fix. It does not move those rules into memory or into the codec module.
- Own adjacency, match, path, expand, or graph refusal policy.
- Own presentation for eyes, or medium path/bind/batch policy.

### Three seams that must not be collapsed
Same family as [Memory Display → Four-way split](../../../../../modules-plugable/computer/memory/display/display.md#four-way-split-binding) and [Graph → What Graph frames vs what a medium adapter does](../../../../../modules-plugable/computer/memory/store/graph/graph.md#what-graph-frames-vs-what-a-medium-adapter-does):

| Seam | What it converts | Owner today / direction |
| --- | --- | --- |
| **(a) Type ↔ value-bytes / layout-value** | Typed value (or graph layout state) ↔ **value-bytes** of the memory contract | Type’s `.codec.<format>.kh`; today’s `Graph_Layout_Value_Codec` is this seam for graph layout (follow-on moves it into the base graph module’s adjuncts — not this rule’s implement step) |
| **(b) Medium body correspondence** | Address-scoped part-bytes map ↔ one medium **body** (envelope) | Medium adapter parameter, e.g. `Files_Body_Codec` (`files-body-codec`) |
| **(c) Display text** | Already-obtained service answers → text for eyes/logs | `Display_Text_Codec`; **one-way** (no Unpack into store) |

Collapsing any two is a design error. Faces and VUI widgets must not collapse (c) into (a): e.g. ErrorUUID → locale text → speech is widget composition of other services, not the Request codec.

### No format is mandatory
No codec — including [Syllab](../../syllab/syllab.md) — is required of every type, every project, or every seam. An organization may choose Syllab, JSON, FlatBuffers, protobuf, or another format. Syllab remains a **first-class** high-volume path (Goals: small size, little heap, high encode/decode performance; Not Goals: human-easy decode — display owns eyes), beside JSON and others; first-class means documented and supported as a peer, not that it is locked in. JSON is not mandatory on any seam either.

### Compile-time value format vs runtime medium bind
- **Value format (seam a):** which format adjuncts an application links for durable/wire values is fixed when the application is composed/compiled. Store stays thin: addresses and batches of **bytes**; it applies codecs the artifact was built with and does not grow a product that owns type shapes.
- **Medium body (seam b):** which body codec a project binds is an organization choice on the medium adapter. The adapter consumes already-encoded part bytes (or calls into seam-a codecs without owning their shape). Domains never name the body codec or inspect the body.

### Missing adjunct: compile vs runtime (manifest key)
A format may offer a **runtime-generic** path (JSON’s historical point: decode/encode without per-type source). Whether that path is allowed is declared by [`Codec_Format_Policy`](../../protocol/codec-format-policy.kh) / [`Codec_Adjunct_Mode`](../../protocol/codec-adjunct-mode.kh) on [`Format_Name`](../../protocol/format-name.kh):

- **Manifest key** (under `memar:`): `codec-format-policy`
- **Value form:** `format=mode` pairs, comma-separated; `mode` is `runtime` ([Runtime_Generic](../../protocol/codec-adjunct-mode.kh)) or `adjunct` ([Adjunct_Required](../../protocol/codec-adjunct-mode.kh)).
- **Example:** `codec-format-policy: json=runtime,syllab=adjunct,argv=adjunct`
- **Default:** a format not listed is **Adjunct_Required**.
- Agents do not load the manifest; the compiler and Memar tools read it (same discipline as other `memar:` keys). The setting is part of the composed artifact ([immutable infrastructure](../../../runtime/immutable_infrastructure/immutable_infrastructure.md)).

If the type lacks `.codec.<format>.kh`, a consumer needs that format, and the mode is **Adjunct_Required** → **compile error**. If the mode is **Runtime_Generic** → the format’s runtime path may run; services still must not embed face-specific parse as a substitute.

### Format modules provide a generator service
Every Memar format module must offer [`Generate_Format_Adjunct`](../../services/generate-format-adjunct/protocol/generate-format-adjunct.kh) so adjunct methods are produced into `<base>.codec.<format>.kh` — see [Format Module Provides Generator](../format-module-provides-generator/format-module-provides-generator.md).

### Request / Response face decode
`Process_Request` / `Process_Response` (and service Request/Response types) may publish the same adjunct shape so a face supplies a buffer and the server builds a typed Request without argparse inside the service. Cover at least one structured format (`json`, `syllab`, …) and an argv / token-stream format; the short format name for that stream is **`argv`** (media-type-like format identity, not a face name). Parent ruling: timeline `20261105-T112743Z-5676` (types unaware of fill path; codec adjuncts for parse).

## Why it exists
Without a settled adjunct method, JSON-on-FS, Syllab, layout-value pack, and face parse drift into separate ad-hoc bridges; store risks growing a second product for “how bytes look.” Owner (2026-11-10), from task `20261107-T065221Z-19384` and sibling need on `20261105-T112743Z-5676`.

## What this rule does not claim
- It does not implement faces, the memar router, MCP, Syllab-as-`Files_Body_Codec`, or the move of `Graph_Layout_Value_Codec` into a single base graph module.
- It does not force every type to ship every format adjunct.
- It does not move graph concept rules into memory or into codec.

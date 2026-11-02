---
Title: "Memory Display"
Labels: Draft
Start Date: 2026-11-01
ID: 498207
---
# Memory Display

## Abstract
A memory display is a **presentation projection**: it turns Graph and store service answers already obtained through the general APIs (`list_sides`, `get_side`, store part maps, …) into text a human or agent can read (JSON, YAML, or another bound text form). It is not storage, not Path encoding, not a medium adapter, and not [Memory View](../store/view/view.md). Domain Fields and part bytes stay opaque; the projection must not invent dump wrappers (`domains`, `placements`, sibling `relation` / `reverse` metadata). Its contract is Khayyam, [`protocol/display.kh`](protocol/display.kh) and the files beside it, with refusals in [`errors/errors.kh`](errors/errors.kh). Realization and a Memar verb are owed by an implement task after this design is approved.

## Explanation

### Placement
Owner correction on task `20261101-T152238Z-24960` (2026-11-01): home is `modules-plugable/computer/memory/display/` — a **sibling of `store/`**, not a child of it. Display is presentation for eyes; placing it under `store/` would suggest it is a storage concern, which G1 forbids. It is a pluggable consumer of Graph and of store part maps ([Placement](../../../../modules/knowledge/modularity/rules/placement/placement.md#the-rule)). [Memory View](../store/view/view.md) stays under `store/view/` (record-folder builder). Umbrella `memory/adaptors` and a bind-time family of graph-json **storage** codecs are rejected (parent `20261101-T142056Z-8280`).

Kernel-neutrality: the subject is formatting service answers for eyes. Which text form (JSON, YAML, …) is an organization choice exposed as [`Display_Text_Codec`](protocol/display-text-codec.kh); one default realization may ship with the capsule. That codec is not [`Files_Body_Codec`](../store/files/protocol/files-body-codec.kh) and not [`Graph_Layout_Value_Codec`](../store/graph/protocol/graph-layout-value-codec.kh).

### What display is (and is not)
- **Is:** a general projection of **typed** Graph/store answers into text for chat, UI, or logs.
- **Is:** Field- and part-opaque: opaque bytes appear only as an encoding token (for example base64 with length), never as interpreted domain schema.
- **Is not:** [Memory View](../store/view/view.md) — View builds a read-only **editor folder** from committed **record** state; no verb reads the view; domains register node presentations. Display formats **live service answers** and may be read by the caller that asked for the text.
- **Is not:** a second on-disk body shape, Path encoding, or a medium adapter.
- **Is not:** an owner of Graph adjacency or match — callers still call Graph/store; Display only formats what those services return (a thin Memar verb may compose call + format without moving ownership).

### Four-way split (binding)
Same split as [Graph → What it is to the memory contract](../store/graph/graph.md#what-it-is-to-the-memory-contract) (presentation item under Graph frames / medium):

1. Domain Fields / part bytes — opaque; owning domain gives meaning.
2. Graph layout framing — `Graph_Layout_Value_Codec`.
3. Medium body — `Files_Body_Codec` (or other medium).
4. **Presentation** — this module.

### One-way text
Display text is an output for eyes and logs only. No Graph, store, Files, or domain service takes display text as an input. Round-tripping display text into the store is Path encoding by another name and is refused by absence of any Unpack on [`Display_Text_Codec`](protocol/display-text-codec.kh).

### Forbidden output shapes
A display text must not introduce aggregating dump wrappers that pretend to be storage or Path encoding, including maps keyed `domains` or `placements`, or sibling `relation` / `reverse` metadata invented for inspection. There is no protocol method that takes a homemade dump map as input.

### Enforcement (binding)
The rules bind on every `Pack*` of [`Display_Text_Codec`](protocol/display-text-codec.kh). [`Display`](protocol/display.kh) `Format*` methods delegate to the bound codec and return the same refusals; they add no second packing path.

| Error | Raised by | Testable trigger |
| --- | --- | --- |
| `Error_Display_DumpShape` | `PackSides` / `PackSide` / `PackGetSide` / `PackParts` (and the `Format*` that called them) | The would-be text introduces an aggregating wrapper key `domains` or `placements`, or invents sibling `relation` / `reverse` dump metadata that is not a field of the typed Graph/store answer being formatted |
| `Error_Display_InterpretFields` | same Pack/Format methods | Opaque Field or part bytes are expanded into structured domain keys or schema instead of a single [`Display_Opaque_Token`](protocol/display-opaque-token.kh) |

### Minimum content of each Format (v1)
Opaque buffers use exactly one token form: [`Display_Opaque_Token`](protocol/display-opaque-token.kh) with encoding name the ASCII run `base64`, the base64 bytes, and the original length. A text form (JSON, YAML, …) may rearrange labels; it may not drop the members below or replace the token with interpreted schema.

- **`FormatSides` / `PackSides`** — for each side in the answer: `to` bytes, `side_ref`, and `fields` as one opaque token (empty Fields → token of length 0). Include paging cursor members when the answer carries them.
- **`FormatSide` / `PackSide`** — `to`, `side_ref`, `fields` token; include store token when the side carries one.
- **`FormatGetSide` / `PackGetSide`** — `found`; when found, `side_ref` if `given`, `fields` token if `given`, store token if `given`. When not found, only `found`.
- **`FormatParts` / `PackParts`** — every entry of [`Files_Parts`](../store/files/protocol/files-parts.kh): domain-key bytes and part value as one opaque token. **Coupling:** this method’s input type is the Files capsule’s `Files_Parts`; Display does not redefine the parts map.

### Protocol surface (v1)
[`Display`](protocol/display.kh) holds a bound [`Display_Text_Codec`](protocol/display-text-codec.kh) and exposes:

- `FormatSides` — `Graph_ListSidesAnswer` → text
- `FormatSide` — `Graph_Side` → text
- `FormatGetSide` — `Graph_GetSideAnswer` → text
- `FormatParts` — `Files_Parts` → text

**Out of v1:** formatting of Graph `match` / `path` / `expand` rows. Those stay callable on Graph; a later change in this capsule may add Format methods without moving MATCH ownership out of Graph.

### Concept challenge (recorded)
| Question | Answer |
| --- | --- |
| Equivalent already? | View is folder-via-record; no general answer→text projection exists. |
| Contextual view only? | Projection of answers, yes — but dump-refusal and Field opacity in text need an owner separate from Graph and Files. |
| New responsibility? | Yes: presentation of service answers for eyes. |
| Independent lifecycle? | Yes: text forms evolve without changing Graph layouts or View. |
| Rules no one else owns? | Forbidden dump shapes; opaque Field/part rendering in text. |
| Clarity if removed? | Agents reinvent storage-shaped dumps (G1 hole). |

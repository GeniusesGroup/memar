# Memory Address Handoff

## Topic & Purpose
The abstraction that mints a new address, asked for by the making of a task (task 20261030-T163545Z-10624).

## Status
Active — `services/mint-address` and `errors/` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **A new identifier is minted as a memory address, not as a ThingUUID (Decided, owner 2026-11-01).** Every domain follows one abstraction for minting; the concrete way to mint is each organization's choice. A machine reads the identifier as bytes, and its human string is shown by the text domain and is never what is kept. `Address_Mint.Mint` returns a `MemoryAddress`; a later mint never precedes an earlier one. - reason: the owner found a shared `ThingUUID` for every identifier wrong from the start.

## Open Questions
- **Does `MemoryAddress` need the order the mint promises?** `address-order.kh` declares `Precedes` on it; the mint states the promise in prose only. Blocks: a test that decides a mint.
- **What shows an address to a person?** The text domain is assumed; no abstraction there takes a `MemoryAddress` today. Blocks: the readable form of a task id in folder names and notes.
- **Task and thing still declare their identifiers as `ThingUUID`** (`Field_TaskID`). The task domain imports `MemoryAddress` instead once this is approved.

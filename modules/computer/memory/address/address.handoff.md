# Memory Address Handoff

## Topic & Purpose
The abstraction that mints a new address, asked for by the making of another abstraction (record 20261030-T163545Z-10624).

## Status
Active — `services/mint-address` and `errors/` written 2026-11-01, accepted by the Khayyam analyzer; no realization.

## Decisions
- **A new identifier is minted as a memory address, not as a ThingUUID (Decided, owner 2026-11-01).** Every domain follows one abstraction for minting; the concrete way to mint is each organization's choice. A machine reads the identifier as bytes, and its human string is shown by the text domain and is never what is kept. `Address_Mint.Mint` returns a `MemoryAddress`; a later mint never precedes an earlier one. Lenses on one thing share that one address (a thing ≡ what is placed on it ≡ its members, and like cases). Normative home: [Identifiers Are Memory Addresses](rules/identifiers-are-memory-addresses/identifiers-are-memory-addresses.md). - reason: the owner found a shared `ThingUUID` for every identifier wrong from the start; sharing across lenses must not mint a second id.

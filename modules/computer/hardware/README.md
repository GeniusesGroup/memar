# Hardware

## Idea backlog from edge code comments

Raw proposal from comment note inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Hardware status - edges/hardware-status.go
- **Idea**: flag-based states: Readys, Shutdown, DiskPressure, MemoryPressure, ProcessPressure, GPUPressure, TPUPressure, NetworkUnavailable - with an open TODO to add more status.
- **Review questions**: are pressure states computed observations (analytics) or stored states? Is the flag layout the right shape vs a status domain edge?
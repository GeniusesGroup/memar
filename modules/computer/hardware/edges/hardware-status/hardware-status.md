# Hardware status

## Model

- Candidate (unconfirmed): bit-flag status space on the hardware node (iota flags in package `label`): `Readys`, `Shutdown`, `DiskPressure`, `MemoryPressure`, `ProcessPressure`, `GPUPressure`, `TPUPressure`, `NetworkUnavailable`.

## Policies (rules)

- The set is open — source carries `// TODO::: add more status`.

## Placement

- **Core `hardware` keeps the stored status flags.** Node state is core-by-necessity (removing it would force another concept to carry hardware liveness), and flag values are parameters in one module (parameters vs semantics ⇒ one module + configuration).
- If pressure states turn out to be computed observations rather than stored state, the computation is pluggable analytics (analytics is always pluggable) while the stored flag stays here — no split of edge from processing.

## Open questions

- Are pressure states computed observations (analytics) or stored states?
- Is the flag layout the right shape vs a status domain edge?


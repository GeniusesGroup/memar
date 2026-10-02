# Net address types

## Model

- Candidate (unconfirmed): address-type label space on a net address — `DomainName`, `HostName`, `IPv4`, `IPv6`, `GP` (iota `Type_*` flags in package `label`).

## Policies (rules)

- None recorded beyond the type list; source TODO questions its own purpose (`WHY? NS system??`).

## Placement

- **Uncertain (create now, decide later) — address-type vocab stays core `instance_of` at the node/address entry point while it is only labels (a type flag is a parameter inside one module).** If name/address resolution with an NS system carries processing, that is a distinct capability (pluggable candidate), not more labels here — edge vs module flips only with independent semantics.

## Open questions

- Is this the placement for name/address resolution (URI domain overlap)?
- Relation to the sibling [](../address/) concept folder (typed `Address` payload) — one concept or two?


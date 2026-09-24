# Thing-organization relation (Producer / Consumer)

## Model

- Candidate (unconfirmed): triple sketch `[Thing, Organization, Label]` / `[Channel, Organization, Label]` — labels `Producer`, `Consumer` between a thing (or its channel) and an organization, e.g. `(thing)-[:org_role]->(org)` with Producer/Consumer as the label. Property-triple vs named edges unconfirmed.

## Policies (rules)

- Producer/Consumer mark which end of the thing/channel exchange an organization plays.

## Placement

- **Uncertain (create now, decide later).** Structural labels may stay at the thing/channel entry point (this module), but producer/consumer semantics that intersect the economics product chain are a pluggable candidate: a relationship needing processing semantics keeps edge + processing in one module, and economics product-chain processing would install/remove as a whole — not bare labels in core device.
- No new core module either way: while the labels are only vocab, they are parameters; the verdict flips only when supply-chain processing appears.

## Open questions

- Is Producer/Consumer an edge to Organization or a label?
- Where does it intersect the economics product chain?


# URI Edges
Some labels use just to find a vertex in better human manner and don't add any other useful information in any way e.g. `username` is just a way to find a `user` vertex not anymore information.

 Any label that use for identifier of any quiddity in the system like `username` or `iban` or ...

## URI protocols

Use related edges to save those protocols output to `identify` any quiddities in system e.g. identify `user` by `username`.

## Idea backlog

### National ID (government-iran-nin)
- **Idea**: URI-protocol pattern `[text, user, gov_iran_nin] >>` — store the Iranian national identification number as text identifying a `user`, alongside the other identifier protocols.
- **Review questions**: graduate to its own protocol folder + doc like [iban](iban/iban.md) / [government-passport-number](government-passport-number/government-passport-number.md), or stay a pattern line here? Validation/status rules for the NIN (checksum, issuing authority) and who enforces them — no bare edges?

# Ownership
Any `thing` that can be own by any `user` (`person`, `organization`, `group`, ...) have some responsibility for the `owner`!

## Contributor relations
A relation between a `thing` of any domain and a `user` with a role (who requested a record, who rewrote it, who confirmed it) is this domain's and is written once here; no other domain keeps an edge of its own for it (owner, 2026-10-30).

- **Each role is its own edge, in its own folder under `edges`:** [creator](./edges/creator/creator.md), [claimer](./edges/claimer/claimer.md), [requester](./edges/requester/requester.md), [rewriter](./edges/rewriter/rewriter.md), [reviewer](./edges/reviewer/reviewer.md), [tester](./edges/tester/tester.md), [arguer](./edges/arguer/arguer.md) and [confirmation](./edges/confirmation/confirmation.md). A role the changelog's open vocabulary adds later is a folder added, defined once.
- **What is searched by is part of the edge's key; what is only shown is in its value.** An edge is a value under an address and its reverse side is written in the same atomic batch, so "which things did this user confirm" is one read of the reverse edge only when the role is the edge's name. The tool a user worked through and the effort are the edge's value. A node per contribution is refused for this: it costs a second step and a read of every node of the user to answer the same question.
- **The kind of user is the identity domain's** ([user type](../../identity/user/protocol/dt-type.kh)); an edge never holds it. That a thing has only model or tool contributors, or that a person confirmed it, is read from the user at the other end of its edges.
- **A rule over the edges is not an edge.** That a confirmer did not do the work is read by the reader of the edges, not stored in them.
- These edges hang on the `thing`. The same key rule holds for every edge that relates a node to many, and a ruling here binds those too.

## Origin of ownership
Rights come first: ownership and legal relations arise from rights, and ownership is not the primitive that grants them. Ownership is not specific to any kind of thing; anything can be owned, so it lives here.

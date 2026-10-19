# Social connections
[Social connections](https://en.wikipedia.org/wiki/Social_connection) are the relationships you have with the people around you. They may be close, like family, friends, and co-workers. Or they may be more distant, like people you know casually. They can be as close as next door or so far away that you only connect with them by phone or online.

## Six degrees of separation

[Six degrees of separation](https://en.wikipedia.org/wiki/Six_degrees_of_separation) is the idea that all people are six or fewer social connections away from each other. As a result, a chain of "friend of a friend" statements can be made to connect any two people in a maximum of six steps.

## Connection-degree edges are precomputed, derived labels

Answering "how is user A related to user B?" (the LinkedIn-style question) by traversing the friendship graph on every profile view is too expensive. The resolved direction (modeling discussion, 2025-01-16; general principle in [`modules/storage/graph`](../../../../storage/graph/README.md)):

- The `connection-1st`, `connection-2nd`, `connection-3rd` edges ARE the precomputed answer: **derived shortcut edges** over the authoritative friendship/connection base edges, giving O(1) degree reads on profile pages.
- They are **automatic labels** - users cannot assign them (see [connection](connection/README.md)) - maintained by the system when base relations change; each friendship add/remove invalidates and recomputes the affected degree edges (write-time cost accepted for read-time O(1)).
- They are **caches, not truth**: always re-derivable from the authoritative base edges, never the source of truth, never authoritative for authorization decisions.
- Depth is bounded (1st/2nd/3rd) rather than arbitrary - beyond that, read-time traversal or approximation is acceptable. The exact depth cutoff and the incremental-update strategy are engine/implementation concerns (see the graph README's algorithm inventory).

## The circles of friendship

Many article like [this](https://kottke.org/21/06/the-circles-of-friendship) introduce deeply.
- **1stFriendshipCycle:** Ego, Usually < 2, The innermost layer of 1.5 is [the most intimate]; clearly that has to do with your romantic relationships.
- **2stFriendshipCycle:** Close Friends. Usually < 5, The next layer of five is your shoulders-to-cry-on friendships. They are the ones who will drop everything to support us when our world falls apart.
- **3stFriendshipCycle:** Best Friends. Usually < 15, The 15 layer includes the previous five, and your core social partners.
They are our main social companions, so they provide the context for having fun times.
They also provide the main circle for exchange of child care.
We trust them enough to leave our children with them.
- **4stFriendshipCycle:** Good Friends. Usually < 50, The next layer up, at 50, is your big-weekend-barbecue people.
- **5stFriendshipCycle:** Friends. Usually < 150, And the 150 layer is your weddings and funerals group who would come to your once-in-a-lifetime event.
- **Acquaintances:** Usually < 500, a relationship less intimate than friendship
- **KnownNames:** Usually < 1500
- **KnownFaces:** Usually < 5000

## Model

- Candidate (unconfirmed) social-graph label set from this folder's relation file: Follow (thing's [follow](../../../thing/edges/follow/follow.md), not a label of its own here), Blocked, Muted; ReferentUser or Introducer; DelegateTo / DelegateFrom (user delegation to this app in other apps); notification Reason labels keyed to friendship cycles (`Reason_1stFriendshipCycle` ... `Reason_UserFollow`).
- Nothing ratified: endpoints, direction, and which of these are stored edges vs annotations are open (see below).

## Policies (rules)

- Follow is "used to make or start making friendship".
- `Reason_1stFriendshipCycle`: "new comment from friend of user".
- `Reason_UserFollow`: "just user follow other, not any friend relationship".

## Placement

- **Correct here** — the social-graph relation labels belong to the social-connections family this folder owns: entry point is creating a user–user relation (Follow starts the same capability as [friendship](friendship/friendship.md)), and the derived connection-degree caches ([connection-1st](../../edges-shortcut/connection-1st/connection-1st.md) ...) recompute from these base relations — labels and that maintenance stay together (a module keeps its complete capability; prefer this existing home).
- **Follow is defined once, on thing:** a person following a person is thing's [follow](../../../thing/edges/follow/follow.md) with a person as the followed thing, under the same authentication, authorization, and accounting. This family keeps only its rules on it — that a follow is "used to make or start making friendship", and what `Reason_UserFollow` notifies.
- **DelegateTo / DelegateFrom are the exception under review**: "user delegation to this org(app) in other orgs(apps)" overlaps the existing [rights/delegate](../../../../rights/delegate/delegate.md) machinery — if delegation is real, its complete capability already has a home there; do not fork it here (prefer existing homes).
- Cycle `Reason_*` labels: notification keys without recorded triggers must not become bare edges — either they are annotations on events (no edge) or they need who-emits/what-it-triggers semantics first (no bare edges).

## Open questions

- Do DelegateTo/DelegateFrom duplicate the rights/delegate machinery? Do Blocked/Muted collide with the group module's blocked edge? Do cycle `Reason_*` labels duplicate the derived connection-1st/2nd/3rd edges?
- Separate edges vs purpose labels on one relation (parameters vs semantics)?
- Direction and naming unconfirmed — nothing ratified.


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

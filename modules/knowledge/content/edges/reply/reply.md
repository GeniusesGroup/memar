# Reply

## Model

- `(reply)-[:reply_to]->(parent)`
- `(parent)-[:reply_of]->(reply)`

Each edge relates one reply content to one parent content; a given pair has at most one edge. A content may have many `reply_to` edges and many `reply_of` edges, so the relation is many-to-many. A content with no outgoing `reply_to` edge is a root. The reverse `reply_of` side permits reading direct replies from a parent, including replies that have no timeline placement.

## Policies (rules)

- A reply edge relates content identities. It does not require either content to be placed on a shared audience or timeline.
- Adding each `reply_to` edge through `Add_Reply_To` is a separate relation operation and a separate Request. Adding the `has_text` edge and placing Content on a Timeline are separate operations with their own services and Requests.
- A content may be reused as a reply to many parents. Content imposes no fixed maximum number of reply edges; an organization may apply its own limit in a policy service or in the caller that coordinates the operation.
- `List_Reply_Of` pages only the `reply_of` relations from one parent; `List_Reply_To` pages only the `reply_to` relations from one reply. Neither service hydrates Content or chooses display order. Consumers choose how to order replies. Each newly added edge carries the `Request_UUID` of its `Add_Reply_To` operation; `asked_at` and `recorded_at` remain on that Request. If one content replies to several parents, each edge has its own Request and times. A consumer reads the exact edge's Request by the ID carried in that relation, through a Request-owned read service; Content does not aggregate Request reads into the relation read. Timeline placement numbers supply neither time. After an offline interval, the caller retries with the same `Request_UUID` and original `asked_at`, and the server records `recorded_at` when it first receives the request. `Request_UUID` identifies the attempt; consumers use Request times when they want time ordering.
- The model prescribes no order for equal timestamps; a consumer may choose a stable tie-breaker or leave ties unordered.
- A migrated reply may have no Request_UUID or client-declared time when its provenance cannot be recovered. Retain an old placement timestamp only as placement provenance; do not treat it as a Request timestamp or invent a client time.

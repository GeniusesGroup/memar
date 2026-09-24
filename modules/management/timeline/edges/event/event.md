# Event

## Model

- `(timeline)-[:event_is]->(thing)` (note: LogActivity, ...)
- `(thing)-[:event_of]->(timeline)`
- `(timeline)-[:event_is]->(comment)` (note: `user tweet`, `user home timeline`)
- `(timeline)-[:event_is]->(form)`
- `(timeline)-[:event_is]->(question)`
- `(timeline)-[:event_is]->(product)`
- `(timeline)-[:event_is]->(invoice)` (note: `support`, `judge case`, ...)
- `(timeline)-[:event_is]->(object)` (note: income `SMTP` email, ...)
- Event requests carry a reason: `Service_SetEvent_Request` exposes `Reason` and `ReasonUserID` — "it can be the owner of comment or any other user base on reason" ([protocol/service-set_event.go](protocol/service-set_event.go)).
- Reason vocabulary (in code): `Reason_UserMentioned`; friendship-cycle reasons 1st–6th; `Reason_UserFollow`; `Reason_FriendForward`, `Reason_FriendReaction`, `Reason_FriendReplied`, `Reason_FriendReceivedAReply`, `Reason_FollowByFriend`; recommendation reasons `Reason_BaseOnUserReaction` / `Reason_BaseOnUserFollow` / `Reason_BaseOnUserTopics` / `Reason_BaseOnUserFeedback` / `Reason_UserMightLike` ([protocol/dt-reason.go](protocol/dt-reason.go)).

## Policies (rules)

- `Reason_1stFriendshipCycle` — "new comment from friend of user".
- `Reason_UserFollow` — "just user follow other, not any friend relationship".
- `Reason_FriendForward` — "retweet or forward other comment to the user timeline".
- `Reason_FriendReaction` — "interest domain: Liked, ...".
- `Reason_FriendReplied` — "new comment to a user comment".
- `Reason_FriendReceivedAReply` — "a friend of user received a reply".
- `Reason_FollowByFriend` — "usually 1stFriendshipCycle".
- Recommendation reasons (`BaseOnUser*`, `UserMightLike`) carry no recorded comments.

## Placement

- **Correct here — the timeline's event-reason vocabulary stays with the event edge this folder owns** (module skeleton: `timeline/edges/event/`; reasons classify why an event appears on a timeline; prefer existing homes over inventing new modules).
- Friendship-cycle reasons key off the social graph owned by [social_connections](../../../../identity/person/edges/social_connections/social_connections.md) — if they merely *mirror* derived connection-degree caches they are annotations, not timeline-owned semantics (flagged, not moved).
- Recommendation reasons smell like pluggable analytics (why-would-you-like-this is recommendation machinery, never core timeline) — flagged open.
- Who may set a reason on whose event is policy → rules (core never knows Rule); the enum as recorded is classification only.

## Open questions

- Do the friendship-cycle reasons duplicate the derived connection-1st/2nd/3rd edges (see [social_connections](../../../../identity/person/edges/social_connections/social_connections.md))?
- Is the recommendation-reason set pluggable analytics rather than core timeline?
- Reasons as a fixed enum in code vs data labels (a new reason kind — Code change or data addition? Code/Rule boundary)?
- `ReasonUserID` vs owner-of-comment — one reason per event, and who is "reason user" when several people are involved ("TODO::: node details??" in [service-set_event.go](protocol/service-set_event.go))?

## Source

> Source: `modules/management/timeline/edges/event/protocol/dt-reason.go` (in code) and [protocol/service-set_event.go](protocol/service-set_event.go) (in code).


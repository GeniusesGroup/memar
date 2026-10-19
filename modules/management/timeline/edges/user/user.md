# User relation group (per-user timeline kinds)

## Model

- Candidate (unconfirmed): the per-user timeline is a group node typed by kind labels — reading from the example `[User, Group, Label] >> ["Omid", "123", "Life TimeLine"]`: user `Omid` relates to group `123` with label `Life TimeLine` (source was a label-only file, no edge code). Reading B: distinct edge kinds per timeline type — unconfirmed.
- Kinds: `PrivateTimeLine`, `PublicTimeLine`, `LifeTimeLine`, `UserNotificationTimeline`.

## Policies (rules)

- `PrivateTimeLine` — "It is use to feed for user itself / home timeline feed".
- `PublicTimeLine` — "It is use for others to see a user feed".
- `LifeTimeLine` — carried in the worked example as the label on the user's group.
- `UserNotificationTimeline` — notification feed kind; no further comment recorded.

## Placement

- **Correct here — the timeline kind vocabulary is the timeline capability's own** (module skeleton: `timeline/edges/`; only timeline gives these labels meaning; prefer existing homes over inventing new modules).
- The edge itself is user-to-group ([edges-loop/timeline](../../edges-loop/timeline/timeline.md) already models `(group)-[:---]->(timeline)` and ChannelID use) — this file records *which kinds* of timeline feeds exist; keep kind vocabulary beside the timeline capability, not in [group](../../../group/group.md).
- Who may read a Private vs Public feed is access policy → rules (core never knows Rule); the labels alone record no audience set (no bare edges).

## Open questions

- Is a timeline a group node with kind labels, or distinct edge kinds?
- Do the kinds overlap the knowledge/content domain (feeds are content streams — [knowledge/content](../../../../knowledge/content/content.md))?
- Relation to `UserNotificationTimeline`: notifications as timeline rows vs a separate notification capability?
- Direction/naming unconfirmed — nothing ratified.


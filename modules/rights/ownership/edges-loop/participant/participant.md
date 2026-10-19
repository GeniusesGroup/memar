# Content relation user

## Model

- Candidate (unconfirmed): `(content)-[:content_participant]->(user)` — the source was `package label` holding only "ContentParticipant" label comments grouped by content topic, no edge code.

## Policies (rules)

ContentParticipant labels grouped by content topic:

- **ContentTopic_Music**: SongWriter, Composer, Regulator, MusicSupplier.
- **ContentTopic_Movie**: Director.
- **ContentTopic_Game**: SportTeam.

## Placement

- **Not an edge of ownership; strip.** Participation in content grants no ownership: rights come first and ownership arises from rights ([rights.md](../../../rights.md)) — participant roles must not become ownership primitives. Removing it distorts nothing in ownership (core-by-necessity fails).
- Existing home: [content](../../../../knowledge/content/content.md) — content already reviews its own relation comment notes in its backlog; topic-specific participant roles (SongWriter, Director, …) are content-type semantics, and the capability that assigns them must own the labels together with their processing (pluggable owns complete capability; no bare edges).
- Not a new module: the label set alone carries no who-may-assign and no what-it-triggers — without processing semantics it must not stand as an edge anywhere.

## Open questions

- Are Music/Movie/Game participant labels content-type configuration inside content (parameters vs semantics), or does each topic need its own capability?
- Relation to the [content](../../../../knowledge/content/content.md) backlog entry on content-to-content Discussion — one participant surface or separate edges?
- Loop-edge shape and direction unconfirmed — the source held labels only; nothing is ratified.


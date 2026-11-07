# Group relation group (group chat timelines)

## Model

- Candidate (unconfirmed): `(group)-[:relation]->(group)` (name/direction unconfirmed) carrying chat-channel labels `Chats_Staff`, `Chats_Customer` — source was a label-only file, no edge code.
- Purpose recorded as comment use: "Use for Comments, ..." — a group-to-group channel that stores/retrieves comments in time order (see [edges-loop/timeline](../../edges-loop/timeline/timeline.md): ChannelID, time-ordered comments).

## Policies (rules)

- `Chats_Staff` — staff chat channel between groups.
- `Chats_Customer` — customer chat channel between groups.
- Both marked "use for comments and similar content".

## Placement

- **Correct here as recorded — the file is a timeline-module edge file and the labels are chat-timeline channels** (module skeleton: `timeline/edges/`; prefer existing homes over inventing new modules).
- **Cross-flag: [role/edges/group](../../../role/edges/group/group.md) is a different module's edge with the same folder name `group`** — same historical source family, different capability (role's `Default` + role TODO vs these chat labels); keep both docs, do not merge (each module keeps its capability), and converge only if inspection shows one edge.
- Not [knowledge/content](../../../../knowledge/content/content.md): the *channel* (which groups talk) is structural here; the discussion threads themselves are content — flagged open, not moved.

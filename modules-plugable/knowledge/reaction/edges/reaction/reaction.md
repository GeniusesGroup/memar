# Reaction
## Model
- `(thing)-[:get_reaction_by]->(user)`
- `(user)-[:reaction_to]->(thing)`
- The record: `UserID` is the PrimaryNode and `ReactionTo` the SecondaryNode ("any domain") — graph data that also stores a time series when the reaction changes.

## Policies (rules)
- "DataModel store user reaction to any content in the application such as laws, comments, products, ..." — the target is any domain.
- One unified `Type()` rune: "any unicode emoji character as old fashion rate(5 star) or like||dislike or ..." — old-fashioned rates (a 5-star score saved as a normal number), like/dislike, and any unicode emoji share one field.
- "It is also time series data that store user reaction in time if any changes to reaction occurred."

## Placement
- **Correct here — `modules-plugable/knowledge/reaction/edges/reaction` (already its home)** — the reaction record is this module's core edge; edge and its storage travel together (pluggable owns complete capability), as already filed in [reaction.md](../../reaction.md).
- **Not core knowledge:** reaction is an optional overlay on content/users — Question/Answer/Text hold the graph without it; removing it must not disturb them.
- **Time series stays attached to the reaction record for now;** whether an analytics module later mirrors it is an availability question (analytics is always pluggable — [analytics](../../../../../modules-plugable/economics/analytics/analytics.md)), not a reason to move the source of truth.

## Source
> Source: `modules-plugable/knowledge/reaction/edges/reaction/protocol/data_model.kh` (in code).

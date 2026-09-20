## Reaction

## Dictionary

reaction  [rɪ'ækʃn]

n.
1. a response that reveals a person's feelings or attitude
2. a bodily process occurring due to the effect of some foregoing stimulus or agent
3. (chemistry) a process in which one or more substances are changed into others
4. an idea evoked by some experience
5. doing something in opposition to another way of doing it that you don't like
6. extreme conservatism in political or social matters
7. (mechanics) the equal and opposite force that is produced when any force is applied to a body

## Idea backlog from edge code comments

Raw proposal from comment note inside edge .go files (comments remain in code as source). Review discipline per modules/management/vocabulary-discipline.handoff.md. Nothing below is ratified.

### Reaction model - edges/reaction/protocol/data_model.go
- **Idea**: one unified Reaction() rune field covering old-fashioned rates (5-star saved as a normal number), like/dislike and any unicode emoji; stored as graph data (UserID primary node, ReactionTo secondary node) and as a time series when the reaction changes. Open comment: query by day?
- **Review questions**: one unified reaction edge vs typed reaction edges; time-series placement per analytics-is-always-pluggable (economics criteria).
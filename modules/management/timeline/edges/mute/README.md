# Mute

## Model

- `(timeline)-[:mute]->(thing)`
- `(thing)-[:mute_in]->(timeline)`
- `(timeline)-[:mute]->(user)`
- `(timeline)-[:mute]->(comment)`

## Policies (rules)

- It is preferences data.
- User will not get notification for this comment for any reason e.g. `get a reply`, `get reactions`, ...

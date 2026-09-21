# Timeline

## Model

- `(group)-[:---]->(timeline)`

## Policies (rules)

- CAN use as ChannelID. Use to store and retrieve comments in time order. It can be UUID, URL hash or any random id.
- Related `Widget` for that domain will show to user in the group of comments.

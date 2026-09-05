# Username

## Model

- `(uri(text))-[:username_for]->(user)`
- `(user)-[:username_is]->(uri(text))`

## Policies (rules)

- Username or UniqueName
- Username is not limit to `person`, It CAN use for any other `user` such as `group` or even `product` identifier too.
- User CAN be any type such as person, group, organization, bot, ...
- It is not replace of user (person, group, ...) ID. It usually use to find the user in more human friendly manner.

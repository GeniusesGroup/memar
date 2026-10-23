# Username

## Model

- `(uri(text))-[:username_for]->(user)`
- `(user)-[:username_is]->(uri(text))`

## Policies (rules)

- Username or UniqueName
- Username is not limit to `person`, It CAN use for any other `user` such as `group` or even `product` identifier too.
- User CAN be any type such as person, group, organization, bot, ...
- It is not replace of user (person, group, ...) ID. It usually use to find the user in more human friendly manner.
- Username can assign more than one to a thing usually in "pro subscription" roles.

## Idea backlog

### Widget status
- **Idea**: a username status vocabulary starting from `Reserved` — a name held before it is usable.
- **Review questions**: is `Reserved` one status of the general status domain, or a username-private lifecycle (reserve → verify → release)? Who may reserve, and what does a Reserved name block in resolution/registration (no bare edges)? Does it connect to the registration flow in [service-register.kh](protocol/service-register.kh)?

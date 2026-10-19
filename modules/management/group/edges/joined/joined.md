# Joined

## Model

- `(group)-[:joined]->(user)`

## Policies (rules)

- It can be more than just one label for associated users to a group
- e.g. `Member`, `Honorary Members`, `Supporter`, ...
- Associated
- Accepter User ID
- e.g. Accept user join request if user is 1st friendship cycle of any member.

## JoinWay

- JoinByRule
- RequestID of making relation is made by inviter user.
- Invited user CAN check who invite itself to this group
- Invited

# User-assigned object labels

## Model

- Candidate (unconfirmed): user-assigned labels on the user's own object that grant others access to see it — candidates `UserPicture`, `UserPrimaryPicture` (source was a thing-to-label edge file).
- Access may be scoped by social relation level: a user preference can limit a label to some relation level (e.g. only `1stFriendshipCycle`).

## Policies (rules)

- "When users assign any below labels to their objects, They allow others to get and see them."
- "Also user can set a preference to limit access to its some relation level e.g. \"1stFriendshipCycle\""
- "Some rule CAN limit user to use these labels for some reason, e.g. governments FORCE user face MUST be clear enough in picture."

## Placement

- **Correct here** — which depiction *is* the object's picture is object identity, and this module owns object labels (same family as [icon](../icon/icon.md)); the label attachment stays with the thing it marks.
- **The access semantics are not thing's.** The source itself says "Some rule CAN limit user to use these labels" — core never knows Rule: who may read/assign the label is a rule evaluation over the social graph (a government-style override is policy), decided outside this module; thing carries only the structural label.
- Not analytics: the assignment is stored state on the object, not a discovered/derived query (analytics is always pluggable — does not apply here).
- Not a bare edge: who may assign `UserPicture` vs `UserPrimaryPicture`, and what assignment triggers, must exist before ratification (no bare edges).

## Open questions

- Converge with the existing [picture](../picture/picture.md) edge folder — is `UserPicture` a typed picture assignment (one edge + parameter) rather than a second edge (parameters vs semantics)?
- Is label-driven access an authorization rule evaluation over the social graph (rights domain), or a property of the label edge? (Moved from the `thing.md` backlog into this doc.) — Placement above answers the *label's* home (here); the evaluation stays with rules/rights.
- The relation-level preference (`1stFriendshipCycle`) keys off the social graph — evaluated in person's [social connections](../../../person/edges/social_connections/social_connections.md), or by the rules engine?
- `UserPicture` vs `UserPrimaryPicture`: one label with a primary flag, or two edges?


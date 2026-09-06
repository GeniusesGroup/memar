# User
[User](https://en.wikipedia.org/wiki/User_(computing)) in user-centered design, personas are created to represent the types of users. It is sometimes specified for each persona which types of user interfaces it is comfortable with (due to previous experience or the interface's inherent simplicity), and what technical expertise and degree of knowledge it has in specific fields or disciplines.

## Scope: application layer only
A `User` is known only at the application layer, not at the OS layer. `User` sits under the `identity` domain (see [Organization vs. Group](../organization/README.md#organization-vs-group-conceptual-level)). How a `User` relates to an OS-level account, if at all, is out of scope for this module.

## User authentication
Each user must have a valid public key. New CPU structures have a unique immutable key that we use to improve security.

### Open questions
- The "unique immutable CPU key" claim is stated but not designed: how is it provisioned, verified, and revocable, and what happens to a `User`'s identity when the hardware key is the root of trust but the hardware is lost or replaced? Not yet resolved.
- How user authentication connects to the `rule`/Code-vs-Rule model (is an authentication requirement Code or a per-organization Rule?) is not yet decided here.

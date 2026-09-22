# User
[User](https://en.wikipedia.org/wiki/User_(computing)) in user-centered design, personas are created to represent the types of users. It is sometimes specified for each persona which types of user interfaces it is comfortable with (due to previous experience or the interface's inherent simplicity), and what technical expertise and degree of knowledge it has in specific fields or disciplines.

## Scope: application layer only
A `User` is known only at the application layer, not at the OS layer. `User` sits under the `identity` domain (see [Organization vs. Group](../organization/organization.md#organization-vs-group-conceptual-level)). How a `User` relates to an OS-level account, if at all, is out of scope for this module.

## User authentication
Each user must have a valid public key. New CPU structures have a unique immutable key that we use to improve security.

## Discussion

### Drawbacks

- Hardware-rooted trust is fragile: if the immutable CPU key is the root of trust, losing or replacing the hardware directly threatens the `User`'s identity, so a recovery/rotation story is mandatory, not optional.
- Keeping `User` application-layer-only means there is no guaranteed binding to an OS-level account; anything that assumes such a binding must not rely on this module.

### Rationale and alternatives

- Public-key authentication is chosen over shared secrets (passwords) as the baseline; the CPU-unique-key idea strengthens it with a hardware root, but is recorded here as intent, not design.
- Scoping `User` to the application layer avoids coupling identity to any particular OS account model, which varies across `computer`/`device` deployments.

### Prior art

- WebAuthn / passkeys and TPM-backed keys implement hardware-rooted public-key identity; the "unique immutable CPU key" claim aligns with that family but is not yet specified here.

### Unresolved questions

- The "unique immutable CPU key" claim is stated but not designed: how is it provisioned, verified, and revocable, and what happens to a `User`'s identity when the hardware key is the root of trust but the hardware is lost or replaced? Not yet resolved.
- How user authentication connects to the `rule`/Code-vs-Rule model (is an authentication requirement Code or a per-organization Rule?) is not yet decided here.

### Future possibilities

- A key-recovery/multi-device design (threshold or delegated recovery) so identity survives hardware loss.
- Reconciling `User` with `rights/delegate` for authority that persists across devices.

# Quiddity states

## Model

- Candidate (unconfirmed): quiddity status states — Expired; Locked/Closed (quiddity must not be used or edited for some reason); Failure; PermanentInactivated; TemporaryInactivated; Revoked.
- Candidate (unconfirmed): provenance states — ManuallyAdded (data belongs to another app/org, added by users via GUI) and ManuallyVerified (manually added data verified in some way); CreationTime/CreatorId fields noted.

## Policies (rules)

- Locked/Closed: the quiddity must not be used or edited, for some reason. The other names are recorded without a transition rule.
- ManuallyAdded: data that belongs to another app or org, entered by users through the GUI. ManuallyVerified: that data checked in some way.

## Placement

- Candidate home is this status module. [status.md](../../status.md) says every quiddity, even a label, can carry a status, and these names were filed here.
- Whether Locked, Closed, and Failure collapse into one suspended state, and whether the provenance pair belongs on an audit record, is open below.

## Open questions

- are Locked/Closed/Failure distinct states or one Suspended with a reason? Do provenance states belong to audit-log?


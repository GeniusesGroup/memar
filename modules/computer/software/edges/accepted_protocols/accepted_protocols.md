# Accepted protocols

## Model

- `Field_AcceptedProtocols` composes three observers — `GetAcceptedEmail()`, `GetAcceptedSMS()`, `GetAcceptedPhoneCall()` — each returning a `Boolean`. No data model composes the field itself.
- The Go carried one bitmask over a `uint8` (`AcceptedProtocols_Unset = 0`, then `AcceptedProtocols_Email | AcceptedProtocols_SMS | AcceptedProtocols_PhoneCall`) with the comment "user domain accepted protocols"; the conversion split it into three booleans.

## Policies (rules)

- The source states which channels are accepted, not by whom, for what, or with what effect. The bitmask's zero sentinel went with the bitmask; absence now needs an explicit contract if it is wanted.

## Placement

- Filed under `computer/software`'s `edges/`, but the Go comment calls it the *user domain's* accepted protocols, and no second node is named anywhere — so neither bucket is proven. Not moved: placement follows whose facet it is.

## Source

> Source: `modules/computer/software/edges/accepted_protocols/protocol/dt-ap.kh` (in code).

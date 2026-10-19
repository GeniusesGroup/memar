# Accepted protocols

## Model

- `Field_AcceptedProtocols` composes three observers — `GetAcceptedEmail()`, `GetAcceptedSMS()`, `GetAcceptedPhoneCall()` — each returning a `Boolean`. No data model composes the field itself.
- The Go carried one bitmask over a `uint8` (`AcceptedProtocols_Unset = 0`, then `AcceptedProtocols_Email | AcceptedProtocols_SMS | AcceptedProtocols_PhoneCall`) with the comment "user domain accepted protocols"; the conversion split it into three booleans.

## Policies (rules)

- The source states which channels are accepted, not by whom, for what, or with what effect. The bitmask's zero sentinel went with the bitmask; absence now needs an explicit contract if it is wanted.

## Placement

- Filed under `computer/software`'s `edges/`, but the Go comment calls it the *user domain's* accepted protocols, and no second node is named anywhere — so neither bucket is proven. Not moved: the contradiction is recorded here and in `software.handoff.md`, and placement follows the answer.

## Open questions

- Whose facet is it — user's or software's? Every other facet of this shape composes an identity field; this one composes none, so nothing says what record carries the accepted channels.
- Three booleans versus one flag word: whether the channels are independent requirements (booleans) or one protocol set (flag) is the same question `instance_of/edges/audit-log`'s `log_p.Level` flag answers differently.

## Source

> Source: `modules/computer/software/edges/accepted_protocols/protocol/dt-ap.kh` (in code).

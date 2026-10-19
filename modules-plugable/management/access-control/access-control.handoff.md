# Access Control Handoff

## Topic & Purpose

Conversion state of `modules-plugable/management/access-control` from Go to Khayyam (2026-10-03), and
the open questions its three access models leave unanswered.

## Status

Partial - the two protocol files are converted; the three source files that hold the access models and
the error catalogue are unconverted, each for a stated reason. Nothing here declares an application
identity, and the domain document's "Nothing below is ratified" was honoured.

## Decisions

- **`AccessControl` composes memar's `Authorize`, and this domain declares no `Authorize` of its
  own.** `protocol/authorization.kh` was `package ac_p` with
  `AccessControl interface { Authorize() (err error_p.Error) }`. memar already owns that operation at
  `memar/modules/process/operation/protocol/authorization.kh` (`Authorize ab` + `authorize mt`), so
  the conversion imports and composes it instead of declaring a rival. It also removes a name
  collision the Go created for free: memar's `Authorize` is a declaration and this domain's `Authorize`
  would have been a bare method name, and Khayyam has no way to separate the two.
- **`GroupUserAccessControl` composes `AccessControl` rather than declaring a `Field_AccessControl`
  accessor.** The Go read `AccessControl() protocol.AccessControl` - a *data* value out of
  `libgo/protocol`, a library this repository does not have. Declaring `tp AccessControl mt (self
  Field_AccessControl) () (ac AccessControl)` would also have put a method and an imported type in
  one file under one name, which the qualified-names rule cannot separate. The reading kept instead
  is that the record *is* the access control granted to that group-user pair and answers `Authorize`
  for it - the stored allow/deny payload lives on the record. This is a disagreement with the Go,
  recorded below.
- **`Time()` is `Observer_Time_Creation`, not `Observer_Time_Request`.** The Go comment says
  `// Save time`; memar spells that concept "Time of the data is created"
  (`Observer_Time_Request` is "the time user call related service"). Both live in
  `memar/modules/process/time/protocol/`.
- **`RequestID()` is memar's `Observer_RequestID`,** whose accessor is `GetRequestID`. The Go's
  `UserRequestUUID` is an undefined type in a `package org` that has no such declaration.
- **`UserRole_StorageServices` became `GroupUserAccessControlStorage`.** The Go interface operates on
  `UserRole` - a type the file never declares, and a name left over from an earlier model of this
  domain. `Save`, `Get` and `Last` all take the record the file actually declares. Bare `Storage` was
  not used: the domain's storage surface is not a generic one, and `DelegateStorage` in
  `rights/delegate` sets the qualified form.
- **`numbers uint64` became `NumberOfVersion` and `versionOffset uint64` became `VersionOffset`,**
  both memar's, because the storage contract is already versioned by its own parameter names;
  `offset, limit` became `Container_Offset`/`Container_Limit` and `[][16]byte` became the imported
  `Array_ThingUUID` rather than a second array abstraction.
- **Nothing was converted from the three access models.** The domain document records all three as
  unratified Ideas and asks whether they are "one model, two capabilities, or competing sketches to
  converge". Converting any of them would have ratified the sketch that the document defers.

## The `Field_ApplicationID` question

**This domain has no application identity to own, and none was invented.**

The migration record for this wave states that access-control's `access_control.kh` imports
`modules/computer/instance_of` and that `Field_ApplicationID` therefore has no owner. That does not
hold for this domain, and the check was made directly:

- `internal/access_control.kh` (the former `_____zero_trust.go`) imports only `fmt`. No
  `modules/computer/instance_of`, no `modules/computer/app`, no application type.
- A repository-wide search for `ApplicationID`, `Application_UUID` and `Field_Application` finds five
  hits, none of them in this domain: `computer/connection/protocol/data_model.kh` (a commented-out
  `// ApplicationID() ID`), `computer/instance_of/edges/node/protocol/data_model.kh`, and three lines
  of `computer/instance_of/instance_of.handoff.md`.
- The actual blocker lives in **`computer/instance_of`**, not here: `edges/node/protocol/data_model.kh`
  requires `app_p.Field_ApplicationID` from `modules/computer/app/protocol`, and
  `modules/computer/app/` does not exist in this repository at all. That domain's handoff already
  records it. It is not this domain's to solve, and it does not touch the files converted here.

The one place an application identity is *discussed* in this domain is
[access-control.md](access-control.md)'s "Zero-trust application inventory" idea, which is explicitly
unratified and asks whether an application catalog even belongs to this module. No `Application` type,
`Field_ApplicationID`, or UUID was declared for it.

## Open Questions

- **The three access models are still three.** `app-connection.kh` (allow/deny over where / when /
  which), `internal/access_control.kh` (ContextGraph / Matcher / Policy / AccessGrant, allow-deny over
  matchers), and the ZTNA policy engine in the document's backlog (Policy / Rule / Group / Selector)
  remain three shapes with no ratified winner. Which one survives is the document's open question and
  is not settled by this conversion.
- **The where/when/which vocabulary has no owner either.** `utc.Weekdays`, `utc.DayHours`,
  `operation_p.ActionType` and the society/router identifiers in `app-connection.kh` are the access
  model's own types. `Operation_ActionType` is memar's
  (`memar/modules/process/operation/protocol/action.kh`, already converted); the week/day-hour
  vocabulary is `memar/time/utc`, which this repository has no import site for, and a society UUID
  needs an `identity/society` domain that does not exist (the same gap `computer/instance_of`
  records).
- **`GroupUserAccessControl`'s identity is not stated.** The Go keys storage on one `[16]byte` for a
  record that identifies a group *and* a user *and* an access control. Whether that is one record id,
  a composite of the three, or a rule id borrowed from `computer/rule` is undecided.
- **`GroupUserAccessControl` overlaps `management/authorization`.** That domain's
  [authorization.md](../authorization/authorization.md) documents `(group)-[:group_rule_authorization]->(rule)`
  and its own review questions ask which module owns group access semantics. Two domains now both
  hold a group-scoped authorization record. One home is needed; neither document claims it.
- **The record and the abstraction may be the same thing or two.** The Go read the access control out
  of the record; the conversion makes the record answer `Authorize`. If the record is only ever a
  pointer to a stored policy, `Field_AccessControl` is the right shape and the collision the
  qualified-names rule cannot separate has to be solved by renaming one of the two declarations
  instead.
- **The `errors/` catalogue has sixteen names and no method writes their text.** `UserNotAllow`,
  `UserNotOwnRecord`, the society and router pairs, the day and hour pairs, the service pair, the
  CRUD pair and the two delegate errors are Go `var Error` values initialized in `init()` and
  detailed in `locale.eng.kh` / `locale.per.kh` under `//go:build` tags. No `Error` method on any
  type writes human-readable text in this repository yet, so the same reason `knowledge/text` and
  `computer/software` were left in this shape applies. Note the domain name inside every error id is
  `package=authorization`, not `access-control` - the error catalogue was never migrated with the
  folder.

## Left unconverted

| File | Why |
| --- | --- |
| `app-connection.kh` | The concrete allow/deny table: a Go `struct` with a 60-byte syllab layout, `//memar:impl` generated codecs for Syllab and JSON, a `GiveFullAccess` mutator and three `Authorize*` stubs carrying `// TODO::: can be implement?`. One of three unratified access models; a concrete capsule with generated codecs, which is Phase 3 (re-modeling) and Phase 4 (generator). |
| `internal/access_control.kh` | The ZTNA sketch: `package ztna`, nine structs, a `main()` that only `fmt.Printf`s, and five unexported helpers. Its own `// TODO:` on `AccessControlResource` and the `// ...` in `isSatisfiedMatcher` mark it unfinished. Its provenance is the unverifiable one the migration record names. Recorded as an unratified Idea in the domain document. |
| `errors/errors.kh`, `errors/locale.eng.kh`, `errors/locale.per.kh` | Sixteen error values and their English and Persian detail text, written by build-tag-gated `init()`. No method on a type writes human-readable text yet; `locale.per.kh` carries an empty detail slot for every error. |

**What finishing these needs from elsewhere:** an `identity/society` domain with a UUID for the
where/where lists; a decision on which access model survives, which decides whether `app-connection.kh`
is re-modelled or deleted; and a text-writing method on `Error` before any error catalogue can be
converted.

## Related Artifacts

- [`README.md`](README.md)
- [access-control.md](access-control.md)
- [`../authorization/authorization.md`](../authorization/authorization.md) - the overlapping group
  authorization record
- `memar/modules/process/operation/protocol/authorization.kh` - the `Authorize` this domain composes
- `memar/modules/process/time/protocol/dt-creation.observers.kh` - `Observer_Time_Creation`
- [`../../../modules/computer/instance_of/instance_of.handoff.md`](../../../modules/computer/instance_of/instance_of.handoff.md)
  - where the `Field_ApplicationID` blocker actually is

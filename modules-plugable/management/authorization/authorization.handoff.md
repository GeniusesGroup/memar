# Authorization Handoff

## Topic & Purpose

Conversion state of `modules-plugable/management/authorization` from Go to Khayyam (2026-10-03), and the
open questions its two flag spaces leave.

## Status

Complete for the three protocol files - all three converted and accepted by the frontend. The flag
*values* were not converted, for a reason recorded below.

## Decisions

- **`Policy` became `GroupPolicy`.** Bare `Policy` is too generic to declare: no module in either
  corpus declares it, but [access-control](../access-control/access-control.md)'s unratified ZTNA
  policy-engine idea claims a `Policy`, and this module's own package is `group_authorization` whose
  every flag is about who may see a group (`JustOwner`, `GroupManagers`, `GroupMembers`,
  `Mentioned`, `AnyOne`, and the friendship-cycle set). The identifier-naming rule asks for the domain
  concept, so the name says whose policy it is.
- **`GetPolicy()` became `GetGroupPolicy`, and `SetPolicy()` was dropped.** `GetPolicy` is the Go's own
  name; renaming it to `GetGroupPolicy` keeps the accessor naming the value it returns after the
  value's own rename, which is the observer-accessor shape (`GetRequestID`, `GetCreationTime`). The
  Go's `SetPolicy() Policy` declares no influencing variable at all - it cannot set anything - so it is
  a broken signature rather than a contract. No mutator surface is declared instead: no `Field_*` in
  this repository has one, and there is no `Mutator_*` declaration anywhere in the organization tree
  yet. That is a gap, not a decision - see Open Questions.
- **`Access` became `ContentAccess`.** Every one of its four constants is spelled
  `Content_Access_*` in the Go (`UserList`, `Public`, `RegisteredUser`, `PremiumUser`), so the flag
  space is a *content* visibility level, not a group access level. Naming it `ContentAccess` also
  keeps it clear of the sibling `management/access-control` module. `ContentAccess` was free in both
  corpora.
- **Both flag spaces compose memar's width abstraction** - `U16` for `GroupPolicy`, `U8` for
  `ContentAccess` - as `computer/instance_of`'s `ResourceType` composes `U8`. A flag space's width is
  its capacity (eleven flags in sixteen bits, four in eight), so stating it is part of the contract.
- **The data model is `GroupAuthorizationDataModel`, and it composes the two ends of the edge the
  document names.** The Go's `DataModel` declared only the policy. The domain document's Model
  section is the newer intent and it says the domain is
  `(group)-[:group_rule_authorization]->(rule)`, so the record identifies the group
  (`Field_GroupID`, imported from the converted `management/group` protocol) and the rule
  (`Field_RuleID`, imported from the converted `computer/rule` protocol) as well as carrying the
  policy. Both `Field_*` are imported, never re-declared.

## Open Questions

- **The flag values have no Khayyam form.** Eleven `Policy_*` and four `Content_Access_*` constants
  remain only in the Go clue blocks. The converted corpus has no precedent either way -
  `computer/software`'s `accepted_protocols` edge left its three constants unconverted too. Variable
  inclusion (`vr {name} in "{path}"`) is the candidate, but whether a flag constant is a module
  constant, a value on the flag type, or a set of named `Boolean` observers is not settled, and this
  is not this domain's decision. **Neither flag space has a set/check surface,** which is what makes
  the values unusable: memar's own `Operation_ActionType`
  (`memar/modules/process/operation/protocol/action.kh`) declares `Operation_ActionType_Set` and
  `Operation_ActionType_Check` as body-less signatures, and that pair is the shape these two need.
- **Both `iota` blocks skip bit 0.** `Policy_Unset Policy = 0` and `Content_Access_Unset Access = 0`
  are the first specs of their `const` blocks, so the `(1 << iota)` that follows starts at `iota == 1`
  - the first real flag is `2`, and bit 0 is never assigned. This is in the Go and was carried
  unchanged; whether "unset" was meant to be bit 0 is a question for whoever writes the flag values.
- **`Policy`'s two halves are one type or two.** The Go comment `// Below policies are person type
  authorization` separates `Policy_AnyOne` from the six friendship-cycle flags. A friendship cycle is
  a different concept from a visibility level - it needs the ordering the cycle names and a
  definition of what "cycle" counts - yet it shares one `uint16`. One flag space with two meanings,
  or a `GroupPolicy` composed with a `FriendshipCycleDepth`, is undecided.
- **`ContentAccess` has no user in this module.** No `Field_*` here reads it, and the Go's `DataModel`
  did not either. It is a content-visibility vocabulary filed in a group-authorization package; the
  document's review questions ask how it relates to the four proposed group access types (Public,
  Private, PrivateInDepartment, PrivateInRole) and neither it nor they have a home yet.
- **Group access types remain an unratified idea.** [authorization.md](authorization.md)'s backlog
  proposes Public / Private / PrivateInDepartment / PrivateInRole and asks whether they belong here or
  in [access-control](../access-control/access-control.md). Nothing was declared for them.
- **This record overlaps `access-control`'s.** The neighbouring module now holds
  `GroupUserAccessControl`, a group-scoped authorization record with a policy reference, a request id
  and a save time. Both modules hold a group-scoped authorization record and neither document claims
  the single home. One of them should go.
- **The mutator side of a policy is unowned.** If the policy is set after creation, the surface that
  does it does not exist in this repository at all - no `Mutator_*` and no `Set*` method is declared
  anywhere in the organization tree.

## Left unconverted

Nothing. All three protocol files are converted; the flag constants stay in their Go clue blocks
because the flag space has no value form yet, which is recorded above rather than treated as work
left undone in this domain.

## Related Artifacts

- [`README.md`](README.md)
- [authorization.md](authorization.md)
- [`../access-control/access-control.md`](../access-control/access-control.md) and its
  `access-control.handoff.md` - the overlapping record and the three unratified access models
- [`../../../modules/computer/rule/edges-loop/access_control/access_control.md`](../../../modules/computer/rule/edges-loop/access_control/access_control.md)
  - `(rule)-[:access_control]->(___)`, the other half of this domain's edge and still an empty
  document
- `memar/modules/process/operation/protocol/action.kh` - the `Set`/`Check` pair a flag space needs
- `org/modules/management/group/protocol/dt-uuid.kh`, `org/modules/computer/rule/protocol/dt-uuid.kh`
  - the two `Field_*` this domain's data model imports

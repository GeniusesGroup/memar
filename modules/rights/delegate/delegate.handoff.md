# Delegate Handoff

Open state for [delegate.md](./delegate.md). See the repository's documentation-handoff practice for what a handoff is.

## Topic & Purpose

Converting this domain's four protocol files from the Go they carry to Khayyam, and recording what the conversion could not finish because the rule domain it depends on is not converted.

## Status

Active - all four `.kh` files accept under the Khayyam frontend, but the domain's data model is **incomplete**: a delegation record does not yet say what was delegated.

## Converted

- `protocol/dt-user-given_delegate.kh` - `Field_GivenDelegateUserID` + `GivenDelegateUserID () (u UserUUID)`
- `protocol/dt-user-gotten_delegate.kh` - `Field_GottenDelegateUserID` + `GottenDelegateUserID () (u UserUUID)`
- `protocol/data_model.kh` - `DelegateDataModel`
- `protocol/storage.kh` - `DelegateStorage` with `Save`, `Count`, `Get`, `ListRoles`, `ListGottenUsers`, `ListGivenUsers`, `ListGottenDelegateUsers`, `ListGivenDelegateUsers`

## Blocking finding

**`DelegateDataModel` cannot name what was delegated.** The Go composed `rule_p.Field_RuleUUID` and its own comment says `RoleID == Null` means "given delegate was given back" - the rule is the centre of the record. [computer/rule/protocol/dt-uuid.kh](../../../computer/rule/protocol/dt-uuid.kh) is not converted, so `Field_RuleID` is declared nowhere in Khayyam. Declaring it here would be a second abstraction claiming a concept another domain owns, which the qualified-names rule calls an architecture error, so it was left out and is recorded here instead.

**What is needed elsewhere:** `computer/rule/protocol/dt-uuid.kh` declares

    tp Field_RuleID ab
    tp RuleID mt (self Field_RuleID) () (t ThingUUID)

importing `ThingUUID` from `identity/thing`. `DelegateDataModel` then adds `Field_RuleID` to its composition block, and nothing else in this domain changes.

`storage.kh` uses `ThingUUID` for the rule reference in method parameters rather than a rule-domain type. That is the same identifier concept - the Go's `rule_p.UUID` is `record_p.UUID` - so no new type was declared, but the storage surface does not reference the rule domain's abstraction. The same fix above makes the link explicit if the reviewer wants it.

## Decisions

1. **Both user fields return `UserUUID`** from [identity/user/protocol/dt-uuid.kh](../../../identity/user/protocol/dt-uuid.kh), which declares that name itself. Nothing was added to that fork.
2. **The Go's given/gotten names are kept verbatim.** Reading the storage signatures - `ListGivenDelegateUsers(givenUserID) (gottenUserID)` and `ListGottenDelegateUsers(gottenUserID) (givenUserIDs)` - "given" is the user who delegates and "gotten" the user who receives. In English "given delegate" more naturally reads as the delegate that was handed over, so the pair reads backwards to an English reader. [delegate.md](./delegate.md) does not settle it, and `DelegateTo`/`DelegateFrom` versus `rights/delegate` is an open placement item in the migration map. Resolving the spelling belongs to a repository-wide sweep, not to this domain.
3. **The three collection types live in `storage.kh`.** `Array_GivenDelegateUserUUID`, `Array_GottenDelegateUserUUID` and `Array_DelegateRoleUUID` compose `Array_Dynamic` because a Go `[]T` is not `Array_Dynamic T`. They are declared where they are returned, which is the only place this domain uses them. When `identity/user/protocol/dt-uuid.kh` grows an `Array_UserUUID` beside the `Array_ThingUUID` that `identity/thing/protocol/dt-uuid.kh` already declares, the two user collections should become its uses and the delegate-specific pair can go.
4. **`DelegateDataModel` is a bundle, not a designed record.** It composes four field abstractions and nothing else. [delegate.md](./delegate.md) defines a delegate as someone "elected or chosen to speak, vote, or take decisions for a group" and says power is role access in software; that is the whole of what the record has to carry today, and it is legal content, so it stayed in the document.

## Extracted from the Go comments

- "Persons can delegate to things(as a user type)", on both user fields - already in [delegate.md](./delegate.md) under Tips.
- "User delegate means transfer power to someone. power is role access in softwares.", above the package in `protocol/data_model.kh` - the same statement, now [delegate.md](./delegate.md)'s opening definition.
- "Service: delegate user can delegate its role to other. blocked this service by default." - **not extracted, and it is a decision this domain has not made.** The claim that the delegation service is blocked by default is a policy about who may delegate and under what authority, which is the open `Authority != Permission` question in [delegate.md](./delegate.md). It needs an answer there before it belongs anywhere.

## Open Questions

1. **Given vs gotten, and `DelegateTo`/`DelegateFrom`** - the direction of the pair, and whether the edges are named at all rather than left as two fields.
2. **Whether delegate owns the authority side** - the `Authority != Permission` question [delegate.md](./delegate.md) already carries, and which the attorney and representative edges both depend on.
3. **Whether "blocked by default" survives** - see the third extracted item above.
4. **Whether a delegation is one record or a lifecycle.** `storage.kh` keys every read on `(givenUserID, gottenUserID, ruleID)` and its `Get` takes a `VersionOffset`, so revocation is modelled as a version rather than as an event; nothing says which of those the domain means.
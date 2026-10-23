# Ownership Handoff

Open state for [ownership.md](./ownership.md). See the repository's documentation-handoff practice for what a handoff is.

## Topic & Purpose

Converting this domain's three remaining protocol files from the Go they carry to the Khayyam the domain's documents describe, and settling what the folder's edge documents imply for those declarations.

## Status

Active - the three `.kh` files under this domain accept under the Khayyam frontend; the model's central question (bare edge or node) is still open in [ownership.md](./ownership.md), and one declaration depends on its answer.

## Converted

- `protocol/dt-uuid.kh` - `Field_OwnershipID` + `OwnershipID () (t ThingUUID)`
- `edges/issuer/protocol/dt-uuid.kh` - `Field_IssuerID` + `IssuerID`, and `Field_OrganizationIssuerID` + `OrganizationIssuerID`
- `edges/owner/protocol/dt-uuid.kh` - `Field_OwnerID` + `OwnerID () (u UserUUID)`

## Decisions

1. **Ownership is treated as a node.** [ownership.md](./ownership.md) still asks "Bare edge or node?", but every edge document in this folder is already written against an `ownership` node - `owner.md` `(ownership)-[:owner_is]->(user)`, `issuer.md` `(ownership)-[:issuer_is]->(organization)`, `heir.md`, `creator.md`, `reserved.md`. The edge documents are the newer intent on this point, so `Field_OwnershipID` is declared. **If the review answers "bare edge", this declaration has nowhere to live and `protocol/dt-uuid.kh` is the file to delete.**
2. **`ownership/protocol/dt-uuid.kh` takes `ThingUUID`** from [identity/thing](../../identity/thing/protocol/dt-uuid.kh), the single owner of the identifier concept. The Go said `thing_p.UUID` directly.
3. **Nothing was added to the `UserUUID` fork.** `owner` returns `UserUUID` because the owner *is* a user, and [identity/user/protocol/dt-uuid.kh](../../identity/user/protocol/dt-uuid.kh) declares that name itself. `issuer` also returns `UserUUID`, because [identity/organization/protocol/dt-uuid.kh](../../identity/organization/protocol/dt-uuid.kh) already states an organization's identity as `OrganizationID () (u UserUUID)` - the Go's `org_p.UUID` was itself `user_p.UUID`. Two fields, one value type, no competing abstraction.

## Findings

1. **`Field_IssuerID` and `Field_OrganizationIssuerID` are one concept at two placements.** Both convert to `(u UserUUID)`. The Go comment draws the distinction - the first is the issuer of an ownership, the second is for "issuer of a record in a data model" - but [issuer.md](./edges/issuer/issuer.md) documents only the first, and a general "issued by" field has no home inside an ownership edge folder. Placement of relations that still have two homes is an open item in the migration map. Both are kept, so no intent is lost; if the review confirms one declaration serves both, the second goes and its home moves.
2. **The `edges-loop/` five are a kind error, and four of their documents already say so.** `assigner`, `group`, `participant`, `staff`, `user` are task-assignment, HR and content-participation relations. `group.md`, `participant.md`, `staff.md` and `user.md` each carry a Placement section reading "Not an edge of ownership; strip." Nothing was written for them and nothing should be: they are also label vocabulary, which is data and not a type. `assigner.md` ("Assigned") is the one without that verdict.
3. **Legal meaning sits in `owner.md`, not in the declaration.** "Just owner MUST edit the related record in any domain; others CAN fork or update if owner allow" is a policy about what an owner may do. It is recorded here and left in the document; it is not a method on any field abstraction.

## Open Questions

1. **Bare edge or node** - the standing question in [ownership.md](./ownership.md). `Field_OwnershipID` is the only declaration in this domain that depends on it.
2. **Where the general "issuer of a record" field belongs** - not under an ownership edge; not yet claimed by any domain.
3. **Should `assigner` join the strip verdict** its four folder-mates already carry.
4. **Whether an ownership node needs more than an identity** - `owner.md` and `heir.md` and `creator.md` all hang off it, and `ownership.md` lists fraction, scope, start/end, restrictions, origin and transferability as candidate content. None of that is modelled; the node currently has an identity and nothing else.

## Pointer: Contract Research 001
[Contract Research 001](../contract/contract.research.001.md) (unratified, task `20261018-T195816Z-15768`) analyses this domain with contract and delegate. Its proposals, none decided:
- Ownership is a node: a title declared by an authority (the existing `issuer`), with a scope (the bundle of rights, reading "rights first"), holders with kind and fraction, an origin, and status events (finding 2). Answers open 1 and 4 above by default.
- "Owner" names two things: title, and record stewardship ("just the owner MUST edit the related record", [owner.md](./edges/owner/owner.md)). Stewardship is a rule over standings, not an edge (contradiction 1; its question 4).
- Mapping (finding 5): `heir` to succession of title, `creator` to attribution, `belongs_to-org` and `belongs_to-module` to the thing's declarer and registering domain, `reserved` to a reservation capability, `assigner` joins the strip verdict (answers open 3 above), the other loop folders stay stripped.

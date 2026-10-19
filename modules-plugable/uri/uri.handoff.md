# URI Handoff

## Topic & Purpose

Conversion state of `modules-plugable/uri` from Go to Khayyam (2026-10-03). The domain is a bundle of
fifteen identifier protocols rather than one module; this records what each of them now declares,
what was left out, and the naming collisions the bundle forced.

## Status

Twenty-one protocol files converted across ten sub-domains, all accepted by the frontend. Two
sub-domains are blocked on domains this repository does not have, three are documentation-only, and
six files were left unconverted for stated reasons.

## Decisions

- **One naming rule ran through the whole bundle: a value type and the accessor that returns it
  cannot share a name.** Go says `type Username string` beside `Username() Username`, and Khayyam has
  no way to separate a method from a type under one name. Where the collision arose the accessor
  took the `Get<Concept>` shape already used by `knowledge/text`'s `Field_Text` / `GetText`:
  `GetUsername`, `GetNumber`, `GetDomainName`, `GetShortID`, `GetIBAN`. The record-level fields kept
  a distinct word instead - `Field_AccountIBAN` / `AccountIBAN` beside the `IBAN` type,
  `Field_CardNumber` / `CardNumber` beside `Card`, `Field_InternalID` / `InternalID` beside
  `AccountInternalID`.
- **`[]T` is never re-declared.** Every id array imports `Array_ThingUUID` from
  `modules/identity/thing/protocol/dt-uuid.kh`. `internet-domain-name` is the one place a
  domain array was genuinely needed, so `Array_DomainName ab { Array_Dynamic }` is declared there
  beside `DomainName` - the shape `rights/delegate` uses for its own arrays.
- **Flag spaces compose memar's width abstraction.** `DomainStatus ab { U8 }` and
  `CardMII ab { U8 }`, matching `computer/instance_of`'s `ResourceType`. `Number`, `Username`,
  `DomainName`, `AccountInternalID`, `ShortID` and `IBAN` each compose memar's `String`, which is
  how `knowledge/text`'s `Text ab { String }` states a named string. **Abstractions only:** no
  capsule (`W16`, `W32`, `W64`) appears in any signature, because an abstraction's method may name
  only abstractions.
- **`uint16` in the card register request became `U16`, not `W16`.** The Go's `CVC() uint16` sits in
  a `BS_*` request abstraction; `W16` is a capsule and is illegal there.
- **Storage method names were kept as the Go wrote them,** including the shouting
  `FIND_AccountIDs_BY_ID`, `FIND_AccountIDs_BY_IBAN`, `FIND_FinancialCardIDs_BY_UserID`,
  `FIND_FinancialCardIDs_BY_CardNumber`. Three sub-domains share that family and a rename in one
  would break the pattern the others establish; the style is recorded below as a finding for the
  repository-wide sweep rather than fixed in four places at once.
- **Every storage contract imported its record's data model rather than re-declaring it,** the shape
  `rights/delegate` and `identity/uri/widgets/quiddity-uri` already use.
- **The `Field_UserUUID` on the register requests was kept even where the Go flagged it.** Both
  `internet-domain-name` and `username`'s register requests carry
  `user_p.Field_UserUUID // TODO::: get user id from connection??`; the field was converted and the
  question is recorded below rather than resolved by deleting a requirement.
- **`username/protocol/service-register.kh` composes `Field_TextID`,** the converted name from
  `knowledge/text/protocol/dt-uuid.kh`. The Go said `Field_TextUUID`, whose accessor is declared
  `TextID`; `in` resolves the name *declared* in the target file.

## Open Questions

- **A duplicate of `computer/software`'s accepted-protocols surface.** `internet-domain-name`'s
  `UserDomain_AP` (`Unset`, `Email`, `SMS`, `PhoneCall`) is the same concept as the already-converted
  `Field_AcceptedProtocols` in
  [`modules/computer/software/edges/accepted_protocols/protocol/dt-ap.kh`](../../modules/computer/software/edges/accepted_protocols/protocol/dt-ap.kh),
  which declares three observers for exactly those three protocols. Two abstractions, one concept.
  This is the qualified-names rule's "one concept declared twice" case, and the answer is one
  declaration the other module includes. Which module owns it is not this domain's to decide, so
  `dt-ap.kh` was left unconverted.
- **`Field_InventoryID` has no owner, and there are two claimants with different import paths.**
  `number-serial/protocol/data_model.kh` imports `modules/economics/inventory/protocol`, but the
  only `Field_InventoryID` in the whole tree is the commented-out Go interface in
  `modules-plugable/gui/page-inventory/protocol/dt-uuid.kh`. The import path and the claimant
  disagree about which inventory is meant, and neither is converted. This is the single blocker for
  that file.
- **`shaparak-hex` is blocked on a domain that does not exist.** Its data model and storage contract
  need `card_p.Field_CardID` and `fcp.UUID` from `modules/vertices/card/protocol`;
  **`modules/vertices/` is empty in this repository** - not unconverted, absent. Shaparak's own card
  hex has no other home: `shaparak-hex/protocol/data_model.kh` carries a bank card, and the card
  identity it points at is the missing one.
- **Three sub-domains have no document and two have no code.** `account-internal-id`,
  `internet-domain-name`, `number-serial` and `staff-id` have protocol files but no `<name>.md`;
  `government-passport-number`, `imei`, `isbn`, `net-address`, `title` and the seven `name-*`
  folders have documents but no protocol file at all. The Phase 0 rule is one folder per edge with
  its own document, and thirteen of these twenty folders do not have both halves.
- **The status vocabulary of a domain name is empty.** `dt-status.kh` declares
  `Status uint8` with its whole `const` block commented out
  (`// Status_ = Status(Status_FreeFlag << iota)`), so `DomainStatus` names a width and nothing else.
  `BS_ChangeStatus_Request` in both `internet-domain-name` and `username` therefore has nothing to
  set. `username`'s version does not even name a status - the Go has `// Field_Status` commented out.
- **`address` is a flat sixteen-field record with no country model behind it.** `AddressDataModel`
  carries `Country`, `State`, `Province`, `Region`, `City`, `District` as independent strings and
  `Postal`/`ZipCode` as bare `U32`, while the same bundle holds `iso-3166/location.kh` (the ISO
  country table) and `postal_code/` as separate domains. Whether an address names a country or
  carries its code, and whether a postal code is a number or a record, is unstated. `address.md`
  says only that it is a cache data module.
- **`CardMII`'s vocabulary has no form.** Ten `CardMII_*` constants and the `ToString()` that names
  them in both English and the industry wording stay in the Go block, for the reason recorded in
  [authorization.handoff.md](../management/authorization/authorization.handoff.md): a flag constant
  has no Khayyam form in this repository yet. The Go's own `// TODO::: detect card type??` (debit /
  credit / prepaid) is still unanswered, and `bank/iran.kh` maps 40-odd Iranian BIN prefixes to
  issuer names - a data table with no place to live.
- **`shortenerPath = "/s"` is a configuration value under `protocol/`.** Rule 1 makes `protocol/`
  abstraction-only, so where the shortener's path prefix belongs (a configuration domain, or the
  implementation layer) is the same open question `computer/instance_of`'s `CNF_LogMode` raised.
- **`StaffIDDataModel`'s `ID() uint32` is unnamed in the domain.** The Go carries
  `// TODO::: user-number??`. It was converted as `Field_InternalID` / `InternalID` returning `U32`,
  deliberately neutral: a staff *employee number* and a staff *system number* are different
  concepts and the Go does not say which this is.
- **`number-itu`'s `FindByNumber` takes a `uint64` where the type is a string.** The Go's
  `FindByNumber(number uint64, ...)` contradicts its own `type Number string`. It was converted with
  `Number`; the Go defect is recorded rather than reproduced.
- **`username`'s storage keys an organization by a user UUID.** `Count(userID, orgID user_p.UUID)`
  types `orgID` as a user UUID. The conversion keeps `UserUUID` for both because that is what the
  organization domain's declared accessor returns (`Field_OrganizationUUID` -> `UserUUID`), so the
  Go's typing was honest about the identity and misleading about the name.
- **`BS_Get_Response = DataModel` is a Go type alias and has no Khayyam form.** Five files declare
  one - `account-internal-id`, `iban`, `internet-domain-name`, `username`, and `iso-7812` (which
  splits it further into `BS_Get_Response1` and `BS_Get_Response2`, the second being `Error`). A
  response *is* the data model in each case, so nothing was lost, but the alias has no declaration
  and the services that are supposed to return one are named only in the Go.

## Left unconverted

| File | Why |
| --- | --- |
| `_import/passport/connect-foreign-platform.kh`, `get-cached-data.kh`, `set-foreign-detail-manually.kh` | Rule 8: an `_import/` tree is a legacy shim over a deleted library - all three import `libgo/achaemenid`, and each function body is `return nil`. |
| `internet-domain-name/protocol/dt-ap.kh` | `UserDomain_AP` duplicates the converted `Field_AcceptedProtocols` in `computer/software`; one concept must have one declaration and the owner is undecided. |
| `iso-3166/location.kh` | A Go `struct` holding the ISO 3166 country table (`Alpha2`, `Alpha3`, `Num`, `Name`) with a commented-out currency relation. Reference data, not a contract. |
| `iso-4217/currency.kh` | The same shape: the ISO 4217 currency table (`Code`, `Num`, `DS`, `Name`) with a commented-out location relation. Note it declares `package iso4217` while `iso-3166/location.kh` declares `package ar_p`, so neither package name matches its folder. |
| `iso-7812/bank/card.kh` | A concrete `Card string` capsule with four slicing accessors, an `IsValid()` that calls `memar/validators`, and `// TODO::: how to return 8 number length IIN??`. Implementation layer; the *contract* is `protocol/card.kh`. |
| `iso-7812/bank/iran.kh` | A 40-case `switch` from BIN prefix to Persian issuer name. The Persian text is mojibake in the file as it stands. A reference table with no home, and its data is already damaged. |
| `number-serial/protocol/data_model.kh` | Needs `Field_InventoryID`, whose owner is unconverted and whose two claimants disagree on the import path. |
| `shaparak-hex/protocol/data_model.kh`, `dt-card-hex.kh`, `storage.kh` | Need `Field_CardID` and `UUID` from `modules/vertices/card/protocol`; `modules/vertices/` does not exist in this repository. |
| `username/errors/errors.kh` | A `const` block whose only member is a commented-out string prefix. Comment-only, and the edge-vocabulary-is-data ground the repository has already taken twice. |
| `username/internal/validator.kh` | A compiled regexp and a `ValidateUsername` function. Implementation; the regex belongs in the domain document as the validation rule, not in source. |
| `uri-shortener/protocol/data_model.kh` (partly) | Converted. Its `const shortenerPath = "/s"` stayed in the Go block: a configuration value under `protocol/` has no Khayyam form under rule 1. |

## Related Artifacts

- [`README.md`](README.md)
- [uri.md](uri.md) - the bundle's own statement that these labels are ways to find a vertex, not
  information
- [`../management/authorization/authorization.handoff.md`](../management/authorization/authorization.handoff.md)
  - why the flag constants have no Khayyam form
- [`../management/access-control/access-control.handoff.md`](../management/access-control/access-control.handoff.md)
  - the sibling domain whose name collides with this bundle's `Field_AccountID` consumers
- `modules/computer/software/edges/accepted_protocols/protocol/dt-ap.kh` - the duplicate of
  `UserDomain_AP`
- `modules/identity/organization/protocol/dt-uuid.kh` - declares `Field_OrganizationUUID` but no
  `OrganizationUUID` type; its accessor returns `UserUUID`
- `modules/identity/user/protocol/dt-uuid.kh` - declares `Field_UserUUID` but no `Array_UserUUID`
- `memar/modules/computer/adt/container/protocol/pagination.kh` - `Pagination_Offset_Request` and
  `Pagination_Response`, which two of the service files here compose

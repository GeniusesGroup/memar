# Request Handoff

## Topic & Purpose
Org service-surface addressing policy inherited from the sRPC / URL critique sessions: four-identity decomposition, address carries only destination, and Official ≠ standard. Migrated from the Organization ideas backlog second pass (2026-09-16). This file also carries the Khayyam conversion state of `modules/computer/request` (converted 2026-10-03).

## Status
Active — direction/decided principles recorded; org-side operationalization of Official≠standard still open.

## Decisions

### From Organization ideas backlog — sRPC / URL critique (`sRPC - chatgpt.md`)

- **Four-identity decomposition for any org service surface:** routing identity, service identity,
  operation identity, and request identity are distinct concepts; HTTP collapsed them into one string
  and the ecosystem pays in cache-key ambiguity, authorization variance, and non-canonical resources.
  Org-internal service addressing should keep them separate (ServiceID fields, per-request stream
  identity) and never build user-facing URLs that double as internal service addresses. *(direction;
  recorded in memar as an sRPC design-rationale open item — the org should inherit it as policy)*
- **An address carries only destination information; request data never rides in the routing address.**
  The org's API design rule for every exposed surface (internal sRPC or external HTTP): the path/route
  names the destination; parameters are request data; "two optional places for one concept" is the
  smell to forbid — one concept, one representation, decided once per resource class. *(decided
  direction in the session; candidate org engineering rule)*
- **"Official" ≠ "standard": conformance is never inferred from a label.** When the org evaluates a
  vendor library, framework, or protocol, the check is against the rules themselves, not the
  implementation's origin, market share, or the fact that it ships by default — Memar already records
  the principle (protocol.md); the org's procurement/evaluation practice should operationalize it.
  *(decided principle; org-side operationalization open)*

### Khayyam conversion (2026-10-03)

- **The request identity is memar's, not this repository's.** `protocol/dt-uuid.kh` declared
  `Field_RequestID` and a local `UUID`, which are `Observer_RequestID` and `Request_UUID` in
  `memar/modules/process/request/protocol/`. A second declaration of one concept across two
  repositories is the architecture error the qualified-names rule names, so both files are left
  unconverted and every converted file here imports memar's names. The Go source's own
  `// type UUID request_p.UUID` shows the author had already decided this. **Recommended follow-up
  for the main session: delete `protocol/dt-uuid.kh` and `protocol/uuid.kh` once it is agreed that
  memar owns the identity** — nothing in this repository imports them.
- **The audit request time is memar's too.** `audit_time_p.Field_Request` is
  `Observer_Time_Request` (`memar/modules/process/time/protocol/dt-request.observers.kh`), imported
  by the other six converted domains already; nothing to decide, recorded so the request domain is
  not searched for it again.
- **`UserRequestUUID` is the same concept under a retired name.** It was an alias of the record
  UUID for the retired `user-request` domain. It is not declared here; the current spelling of that
  identity is memar's `Request_UUID`.
- **`Storage_Key_Primary` and `Storage_Key_Cluster` are qualified to `Request_Storage_Key_Primary`
  / `Request_Storage_Key_Cluster`.** The bare `Storage_*` spelling is already claimed by
  `identity/thing/protocol/storage.kh`, and this repository's rule 3 requires the full
  domain-qualified name.
- **The `SS_FIND_…` Go spellings are re-spelled `Service_ListRequestIDsByUserID_*`.** `SS_` and
  `FIND_…_BY_…` are Go residue; `identity/thing/protocol/service-get.kh` already sets
  `Service_Get_Request` / `Service_Get_Response` as the shape.
- **The `data` and `signature` edges type their byte payloads as an `Array_Dynamic` composition**
  (`RequestData`, `Signature`) rather than a Go `[]byte`, and their accessors are
  `GetRequestData` / `GetSignature`. The `Get` prefix is the escape
  `knowledge/text/protocol/dt-text.kh` already uses where the field's value type and its Go
  accessor share one name (`Text` / `GetText`); the bare method name would have collided with the
  declaration in the same file.
- **`edges/conditional/protocol/dt-authorized-by.kh` imports `Field_AuthorizedBy` from the rule
  domain** (`org/modules/computer/rule/edges/authorization/protocol/dt-authorized-by.kh`) rather
  than declaring it again — the two Go interfaces were identical down to the comment. See the open
  question on the two homes of that edge.
- **The media-type identity does not belong to this domain.** See below.

## Open Questions

- Org-side operationalization of Official ≠ standard (procurement/evaluation practice). *(decided principle; org-side operationalization open)*
- **What distinguishes the primary key from the cluster key.** `Request_Storage_Key_Primary` and
  `Request_Storage_Key_Cluster` have identical requirements (both are `Observer_RequestID`); the
  Go source said only "indicates the domain storage primary key" / "cluster key". Either the
  request domain should state what the storage layer does differently with them, or one of the two
  should go.
- **`Observer_RequestIDs` returns memar's untyped `Array_Dynamic`.** Every other list in this
  repository has a named array (`Array_ThingUUID` in `identity/thing/protocol/dt-uuid.kh`,
  `Array_ContractTermsData` in `rights/contract/edges/terms/protocol/dt-data.kh`), and the
  qualified-names rule says a bare name that is claimed is not reused. A named
  `Array_Request_UUID` belongs in `memar/modules/process/request/protocol/` beside
  `Request_UUID`; it was **not** created here, because that would be the cross-repository
  duplicate again.
- **Where the media-type identity lives.** `identity/thing/protocol/storage.kh` and
  `service-register.kh` want `DomainID() protocol.MediaTypeID`. Memar declares
  `Identifier_MediaType` (`memar/modules/identifier/mediatype/protocol/media-type.kh`) and
  `Observer_MediaType` / `GetMediaType`, but **no identity for a media type** — no
  `Field_MediaTypeID`, no UUID beside `Identifier_MediaType`. The request domain does not own media
  types and did not invent one; the missing abstraction belongs in memar's
  `identifier/mediatype/protocol/` (an identity file beside `media-type.kh`, composing
  `Identifier_MediaType`). That is a memar change and is recorded here rather than made.
- **Two homes for the `authorized_by` edge.** `rule/edges/authorization` models
  `(thing)-[:authorization_by]->(rule)` and `request/edges/conditional` models
  `(request)-[:authorized_by]->(rule)`; both carried a `Field_AuthorizedBy` Go interface
  returning a rule UUID, and the two differ only in label spelling. The migration map's Phase 0
  review already carries "relations that still have two homes" as an open item; this is one of
  them. This domain imported the rule domain's declaration rather than starting a third name.
- **`SS_FILTER_RequestIDs_BY_DomainID` (`TODO:::` in the Go source).** The commented-out pair asks
  whether it is a GUI service that finds by service id and filters by other data, and would have
  keyed on `bm_p.Field_ModuleID`. Left uncommented in the Go block; not designed here.
- **The retired `user-request` trees.** See "Left unconverted" below; the recommendation is
  deletion, which the main session should own.
- **The request chain number.** `widget/protocol/data_model.kh` carried
  `// With this number we can show user how many changes // ChainNumber() container_p.NumberOfElement`
  and the widget folder is named `widget` rather than an edge name. Whether the chain number is a
  field of the request record or a derived value of the graph is not stated anywhere in the domain.

## Left unconverted

| File | Why |
| --- | --- |
| `protocol/dt-uuid.kh` | `Field_RequestID` and `UUID` are memar's `Observer_RequestID` and `Request_UUID`; declaring them again is the cross-repository duplicate the qualified-names rule names. |
| `protocol/uuid.kh` | `UserRequestUUID` is the retired `user-request` domain's name for memar's `Request_UUID`. |
| `widget/protocol/data_model.kh` | Needs the graph record abstraction from `modules/storage/graph/protocol/data_model.kh`, which is not converted. |
| `widget/protocol/storage.kh` | Same, plus `Field_ServiceID` from `modules/computer/service/protocol/dt-uuid.kh`, also not converted. |
| `edges/connection/protocol/data_model.kh` | Needs `Field_ConnectionID` from `modules/computer/connection/protocol/dt-uuid.kh`, not converted. |
| `edges/service/protocol/data_model.kh` | Needs `Field_ServiceID` from `modules/computer/service/protocol/dt-uuid.kh`, not converted. |
| `internal/storage/storage.kh` | Implementation layer (a Go struct with methods), which the migration map places in Phase 3, not Phase 2. |
| `_import/user-request*/protocol/storage.kh` (4 files) | The retired `org/modules/user-request*` domains, excluded from every build by the leading underscore and importing a tree this repository no longer has. |

**What the conversion of the blocked files needs from elsewhere:** `Field_ServiceID` in
`modules/computer/service/protocol/dt-uuid.kh`; `Field_ConnectionID` in
`modules/computer/connection/protocol/dt-uuid.kh`; a graph record abstraction in
`modules/storage/graph/protocol/data_model.kh`; and, for the media-type identity, a memar change
in `identifier/mediatype/protocol/`. None of these is this domain's to declare.

**What still held from the retired trees**, recorded so it is not lost with them: a request record
stores the connection or app-instance that set or changed it, the signature proving the user asked
for the change, the service that handled it, and the time of the request (which is the request's
own save time, not the created record's); a request may chain to a past request that created or
updated the same record; a request carries a compression id with its payload; and a request metric
carries a duration and one of five statuses — unset, completed, failed, pending, drop.

## Related Artifacts

- [`README.md`](README.md)
- [`request.md`](request.md)
- Memar `protocol.md` / sRPC design-rationale open item
- `memar/modules/process/request/protocol/dt-uuid.kh`, `dt-uuid.observers.kh`
- `org/modules/computer/rule/edges/authorization/protocol/dt-authorized-by.kh`

## Notes

- Provenance: Organization ideas backlog → second-pass From `sRPC - chatgpt.md` (2026-09-16 migration).
- Khayyam conversion 2026-10-03: 4 files written, frontend `accept` on all four.

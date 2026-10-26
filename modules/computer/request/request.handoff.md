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
  domain** (`modules/computer/rule/edges/authorization/protocol/dt-authorized-by.kh`) rather
  than declaring it again — the two Go interfaces were identical down to the comment. See the open
  question on the two homes of that edge.
- **The media-type identity does not belong to this domain.** See below.

### Decisions taken by the memory-port design (2026-10-23)
Taken by task 20261023-T074641Z-5420 so that the first storage of Requests and the migration guess nothing; each is **Tentative**, open to the owner's ruling on the question it answers, and says what changing it costs. The evidence is the question-by-question table in that task's `docs/storage-forced-questions.md` (kept on the records branch). The rule that uses them is [Recording a change of state](request.md#recording-a-change-of-state).
- **Question 1 (what the domain is).** A Request is stored as a node, the memory of an asking, as the change plan rules; the opening of request.md is not rewritten here. Reversing it later copies requester and time into every domain record.
- **Question 2 (a thing or not).** A stored Request is named by the id of its node, minted by the service that composes the batch; whether that id is also a `ThingUUID` is a matter of the identifier modules and renames no stored node, since the bytes are the same. Memar's `Request_UUID` is not stored; if the owner rules that the identity stays `Request_UUID`, it is added as a field of the `request` part, which rewrites nothing.
- **Question 3 (what is recorded).** Every change of the current value of an acquired part, as the rule says, and no refusal. This is the one irreversible choice here: a refused asking not recorded cannot be recorded later. The cost accepted is that a refused claim leaves no trace; recording refusals later is a Request with an empty list of changes and breaks no stored record.
- **Question 4 (one instant or two).** Both, `asked_at` and `recorded_at`. The record contract stamps neither; the composing service does.
- **Question 5 (requester).** `requested_by` is required and holds an identity; a record migrated from an old log whose author was never kept carries the explicit marker that it was not recorded, which no new record may carry.
- **Question 6 (signature).** The field exists on every Request. Until the token domain issues keys it holds the digest of the canonical `request` part and names no key; the key is added when it exists. A past asking cannot be signed afterwards, so records written before keys exist are digest-only for good. Owed: `request.signing-key`.
- **Question 7 (erasure).** The payload is a part of its own, `request-data`, beside the fact, so a rule of erasure can reach it alone. The rule itself is the owner's open question in [Memory Handoff](../memory/memory.handoff.md#what-is-the-retention-and-erasure-rule-for-preserved-history-and-where-do-a-records-versions-live); no adapter erases until it is ruled.
- **Question 8 (outcomes).** A Request records a committed change. The outcomes of a call (received, refused, answered, failed) are not stored by this design; adding them later appends facts and rewrites none.
- **Question 9 (chain relation).** The edge that chains a change to the one it follows is stored on the Request as the field `follows` of each change, since one Request may change several parts, and the Request cites the nodes it changed; the node cites nothing but the head. The name `sub-request` is not used, because [sub-request](edges/sub-request/sub-request.md) models decomposition (a transaction's sub-requests) and a stored edge with two meanings would have to be rewritten to separate them. The last Request of a part is kept in a part `request-head` of the changed node, written with the Request, because tokens repeat and ids carry the minting instant, so the last Request cannot be derived. `caused_by`, with a role, remains the research's candidate for a causal edge across domains and is added beside `follows`, not instead.
- **Question 12 (retry).** A batch retried after an outcome that is not known keeps its Request id, and the expectation that the Request is absent tells a repeat from a conflict; a batch rewritten after a Conflict takes a new id.
- **Question 14 (petitions).** The text of a plan's Request section is a content and never a Request node.
- **Question 16 (audit log).** No Request of a recorded change is left unsaved by a rule; the memory and the audit log may share a listener.
- **Question 17 (operation identity).** The `operation` field names the verb asked; the service's identity is not stored.
- **Not blocking storage, left open as they stand:** questions 10, 11, 13 and 15. A node can be stored with them open, and answering them adds an edge or a field beside the record.

Facts verified on 2026-10-23: the four wrong imports listed under the contradictions below are fixed, so that pointer is stale; the Memar file names cited in request.md and above are still wrong (`dt-uuid.kh`, `dt-uuid.observers.kh` and `dt-request.observers.kh` are `uuid.kh`, `uuid.observers.kh` and `request.observers.kh` under `modules/process/request/protocol/` and `modules/process/time/protocol/`); and "not declared by this repository" is stale, since `modules/process/request/protocol/uuid.kh` is in this checkout.

### Past Requests are never converted; old shapes are read only in history (Tentative, owner's working answer, 2026-10-25; deeper task 20261025-T140526Z-16944)
- Decided: a Request's two parts are never converted. Each Request states the shape version of its payload, every release carries a reader for each shape version that history may hold, and a conversion converts only current values, each converted value written by a Request of its own whose `requested_by` names the release; the immutable-infrastructure rule then reads "the system writes only the new shape and reads old shapes only in history". Cost: readers of old shapes kept in every release, and a stated exception to "reads only the new".
- Reasons: [Immutable Infrastructure → A change carried to a site with no network](../runtime/immutable_infrastructure/immutable_infrastructure.md#a-change-carried-to-a-site-with-no-network) has a release that changes how something is stored carry a script that converts the old shape to the new, so that the system reads only the new ([Software → No Hidden Inputs](../../process/software/software.md#no-hidden-inputs)); but a Request is written once and never edited ([The write](request.md#the-write)), its `request` part carries the digest of its data and its signature, and its `request-data` holds the new values of the changed parts in the shape they had when written ([The Request node](request.md#the-request-node)). Converting the payloads of past Requests breaks their digests and signatures, which the plant repair-work requirements register requires to stay valid (immutable signed records, approvals signed), and a history widget that shows before and after reads exactly those payloads.
- Rejected: a conversion that rewrites past payloads and re-signs them with the release's own key, keeping the original digest beside the new, which leaves a signature that is no longer the asker's, against signed approvals; never changing a shape in place, a changed shape being a new part under a new key, which has domains carry every past shape's key and a reader of history follow keys across versions.
- Standing: the owner accepted the recommended option on 2026-10-25 as a working answer, to be studied in depth in task 20261025-T140526Z-16944, which may change it. It is an exception to a stated rule, that the system reads only the new shape, and stays visibly a working answer until that task settles it; `request.md` keeps its mark `Owed: memory.stored-shape`. The conversion tooling of the release task 20261024-T161049Z-20560 and the history widget of the console task 20261024-T161057Z-20560 build on it. It replaces the open entry "How does an update convert stored shapes when past Requests are signed and never edited?".

## Open Questions

### Does the Request domain need more of `record` than the reference to an address?
- State: "Recording a change of state" in `request.md` is written in `record`'s terms: a domain's current value is a part on a node, a Request is a node with the parts `request` and `request-data`, `request-head` is a map from a domain key to the last Request, a Request is found by `scan` on its labels, and the batch needs a class whose adapter declares `atomic_batch`. Its identifier is now stated as an address (the memory module's reference to an address, [Memory Address](../memory/address/address.md)), which is all the owner's ruling of 2026-10-24 leaves a kernel module. Parts, domain keys, labels, `scan` and the binding of classes to adapters are only `record`'s, a pluggable capsule; the section is load-bearing for every change of state, so it was not edited and its links to `record.md` stay.
- Options: (1) Recommended: the chain of Requests is stated over the memory contract alone (an address, `get`, `list`, an atomic `batch` under expectations), with `request-head` as a value under an address that the Request domain names, and the parts, labels and `scan` are the composition's use of `record`, moved to the pluggable side of this domain; cost: a rewrite of the section and of the Request node's description. (2) The section stays as how a project binds the Request class to `record`, stated as that choice. (3) The Request domain needs parts and labels as its own subject, and the ruling is revised.
- Anchor: [Recording a change of state](request.md#recording-a-change-of-state), [The Request node](request.md#the-request-node).
- Blocks: the move of the `record` capsule and the build of the verbs that write Requests. Assumption meanwhile: option 2.
- Asked: 2026-10-24, Claude (task `20261024-T160312Z-25344`), for Omid Hekayati.

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
- **Invoices delivered between organizations as requests (2026-10-10, open).** A purchase is one
  invoice that must reach every organization it involves, like a purchase request; delivering it is
  a request to a party that did not follow it, not a
  [follow](../../identity/thing/edges/follow/follow.md). It needs AAA: the sender authenticated,
  the receiver's rule deciding which senders' invoices it accepts, each delivery metered. Is it a
  request to the receiving organization's service surface, is a rejection on price mismatch that
  request's process error, and is it carried by the same mechanism as a follow's delivery? —
  [invoice exchange](../../economics/invoice/invoice.handoff.md#open-questions).

### From Request Research 001 (2026-10-19, agent proposals, nothing ratified)
Each entry: the question, the recommended default, what it blocks. Ordered by what they change: those that change what the domain is first. Reasoning, ten scenarios and six rival models are in [Request Research 001](request.research.001.md#open-questions).
1. **Is the request the durable memory of one asking (an acquired fact cited by the registration facts of other domains), or only Memar's runtime request with each domain restating requester and time?** Default: the memory of an asking. Blocks: the rewrite of the opening of [request.md](request.md), thing's registration event shape, the 125 files that mention a request id.
2. **Is a request a thing (`ThingUUID`), or the root of provenance whose identity stays Memar's `Request_UUID`?** Default: not a thing, one stated exception to the "all ids return ThingUUID" rule, because thing's registration cites a request and a request that is a thing would need one (regress). Blocks: retiring `protocol/dt-uuid.kh` and `uuid.kh`, the A1 sweep, thing TH2.
3. **What is recorded: every call, state-changing calls, or state-changing, refused and boundary-crossing calls plus any a rule chooses?** Default: the last; ping and time-sync frames and ordinary reads are not requests. Blocks: volume, connection stream counters, quota, audit of sensitive reads.
4. **Is the request time one instant or two (asked-at as signed, received-at by the organization)?** Default: both. Blocks: `Observer_Time_Request`'s two-layer meaning, offline sync, replay tolerance.
5. **Must a request name its requester; may an anonymous caller be recorded?** Default: required, as an identity; anonymity stated explicitly and only where a rule admits it. Blocks: the missing `requested_by` edge, `Service_ListRequestIDsByUserID`, guest limits.
6. **What does a signature cover and which key signs?** Default: a digest of payload, target and asked-at, by a key from the token domain, required for state-changing requests of an admitted user. Blocks: erasure, admission bootstrap, relay.
7. **May a payload be erased while fact, digest, signature and outcome stay?** Default: yes, by the shared erasure. Blocks: `user-request-data` `Delete`, retention rules.
8. **Are request outcomes only the call's (refused, answered, failed, dropped), the work's status being its domain's?** Default: yes; drop `pending`. Blocks: the status vocabulary (R4), the retired metric.
9. **Is the chain one relation `caused_by` with a role field, `retry_of` a separate one, and the three `logic-*` folders and `widget` retired?** Default: yes; `last-chain` stays a shortcut with its sources named. Blocks: the edges-loop folders, the widget record, `ChainNumber`, the rule's `made_request`.
10. **Does the request–connection relation live only in the request domain?** Default: yes; retire `connection/edges/request`. Blocks: connection edge cleanup, the `Field_ConnectionID` conversion.
11. **Is the connection edge optional and does it carry the stream coordinate; may the connection domain accept a non-software channel (counter, telephone, paper)?** Default: optional with the coordinate; the channel question goes to connection. Blocks: drafts, relay, `connection_to`.
12. **Is a retry a new request that refers back, and a third kind beside X2's replaces and offsets?** Default: yes. Blocks: the outbox, idempotency, X2's wording.
13. **Is exercised permission one evidence relation `permitted_by` (far end a rule or a delegation), apart from standing permission (`condition_is`)?** Default: yes. Blocks: the three `conditional` homes, X3, the unresearched delegate.
14. **Is this domain only the call occurrence, with petitions (formal asks to an authority, join requests, payment demands, searches) owned by their domains?** Default: yes. Blocks: the opening of request.md, group's `request_to_join`, transaction's "a request, not an operation".
15. **When a request crosses to another organization, are the two records counterparts, the receiver's citing the sender's as `caused_by`?** Default: yes. Blocks: the invoice-exchange question above, follow delivery.
16. **Are the request memory and the node's operational audit log two things that may share a listener?** Default: yes. Blocks: the instance_of `audit-log` shape, Memar's `Observer_RequestID` comment.
17. **Where is the operation identity recorded?** Default: on the service edge beside the service identity. Blocks: the `edges/service` data model.

### Contradictions between this domain's documents and its neighbours (reported by Request Research 001, not resolved)
See [Contradictions found](request.research.001.md#contradictions-found). One finding to act on first: this file and [request.md](request.md) cite Memar files that do not exist (`dt-uuid.kh`, `dt-uuid.observers.kh`, `dt-request.observers.kh`; Memar has `uuid.kh`, `uuid.observers.kh`, `request.observers.kh`), and four `.kh` files in other domains import the wrong paths (`economics/account/edges/bookkeeping`, `knowledge/text/edges/duration`, `knowledge/text/edges-loop/query`, `management/group/edges/membership-term-member_limit`).

## Left unconverted

| File | Why |
| --- | --- |
| `protocol/dt-uuid.kh` | `Field_RequestID` and `UUID` are memar's `Observer_RequestID` and `Request_UUID`; declaring them again is the cross-repository duplicate the qualified-names rule names. |
| `protocol/uuid.kh` | `UserRequestUUID` is the retired `user-request` domain's name for memar's `Request_UUID`. |
| `widget/protocol/data_model.kh` | Needs the graph record abstraction from `modules-plugable/computer/memory/store/graph/protocol/data_model.kh`, which is not converted. |
| `widget/protocol/storage.kh` | Same, plus `Field_ServiceID` from `modules/computer/service/protocol/dt-uuid.kh`, also not converted. |
| `edges/connection/protocol/data_model.kh` | Needs `Field_ConnectionID` from `modules/computer/connection/protocol/dt-uuid.kh`, not converted. |
| `edges/service/protocol/data_model.kh` | Needs `Field_ServiceID` from `modules/computer/service/protocol/dt-uuid.kh`, not converted. |
| `internal/storage/storage.kh` | Implementation layer (a Go struct with methods), which the migration map places in Phase 3, not Phase 2. |
| `_import/user-request*/protocol/storage.kh` (4 files) | The retired `modules/user-request*` domains, excluded from every build by the leading underscore and importing a tree this repository no longer has. |

**What the conversion of the blocked files needs from elsewhere:** `Field_ServiceID` in
`modules/computer/service/protocol/dt-uuid.kh`; `Field_ConnectionID` in
`modules/computer/connection/protocol/dt-uuid.kh`; a graph record abstraction in
`modules-plugable/computer/memory/store/graph/protocol/data_model.kh`; and, for the media-type identity, a memar change
in `identifier/mediatype/protocol/`. None of these is this domain's to declare.

**What still held from the retired trees**, recorded so it is not lost with them: a request record
stores the connection or app-instance that set or changed it, the signature proving the user asked
for the change, the service that handled it, and the time of the request (which is the request's
own save time, not the created record's); a request may chain to a past request that created or
updated the same record; a request carries a compression id with its payload; and a request metric
carries a duration and one of five statuses — unset, completed, failed, pending, drop.

## Proposed Next Steps
1. After the owner answers Request Research 001 questions 1, 2 and 14 (what the domain is, whether the request is a thing, the petition fence): rewrite the opening of [request.md](request.md); decide model M2 versus M3 ([rival models](request.research.001.md#3-rival-models)).
2. Correct the Memar file names cited in [request.md](request.md) and in this file, and the four wrong imports listed above, in one pass by the domains that own those files.
3. Apply the folder mapping ([finding 5](request.research.001.md#5-how-the-existing-edge-folders-map)) one area at a time: the Placement and Open questions sections every edge lacks, then reshape `conditional`, `signature`, `data`, `connection`, `service`; retire the `logic-*` folders after question 9.
4. Design the missing pieces ([finding 6](request.research.001.md#6-missing-edges-and-modules)): `requested_by`, `permitted_by`, `retry_of`, outcome events, then `quota` and `outbox`; check `quota` against interaction-limits of the synthesis.
5. Ask the connection, software and instance_of domains for the pointers recorded in their handoffs (retire `connection/edges/request`; app kind as the answer to "official GUI or SDK"; audit log versus request memory).
6. Turn the [test scenarios](request.research.001.md#7-test-scenarios) into tests once questions 1 to 8 are answered.

## Related Artifacts

- [`README.md`](README.md)
- [`request.md`](request.md)
- [`request.research.001.md`](request.research.001.md) — Request Research 001 (2026-10-19): the questions above and the folder mapping
- [`request.changelog.md`](request.changelog.md)
- Memar `protocol.md` / sRPC design-rationale open item
- `memar/modules/process/request/protocol/dt-uuid.kh`, `dt-uuid.observers.kh`
- `modules/computer/rule/edges/authorization/protocol/dt-authorized-by.kh`

## Notes

- Provenance: Organization ideas backlog → second-pass From `sRPC - chatgpt.md` (2026-09-16 migration).
- Khayyam conversion 2026-10-03: 4 files written, frontend `accept` on all four.

# Node Handoff

## Topic & Purpose

Conversion state of `modules/computer/instance_of` from Go to Khayyam (2026-10-03), and the
open questions the node protocol and its edges left unanswered.

## Status

Active — ten files converted across the keystone protocol and five edges; the node protocol
itself, the cluster contract, the audit-log configuration constant and every implementation file
are unconverted, each for a stated reason.

## Decisions

- **`Field_InstanceUUID` resolves to `ThingUUID`.** The Go `type UUID thing_p.UUID` is the same
  record identity the rest of the repository shares; a second node UUID would be the
  architecture error the qualified-names rule names. The accessor is
  `InstanceID mt (self Field_InstanceUUID) () (i ThingUUID)`, the shape `Field_UserUUID` /
  `Field_InstanceUUID`'s sibling `UserID` already has.
- **The health ping's TTL is the time domain's, not a second one.** `BS_Ping_Request` required a
  `TTL()` method, and the time agent recorded the name collision as a finding. `BS_Ping_Request`
  now composes `Field_TimeToLive` from `modules/identity/time/edges/ttl/protocol/ttl.kh`,
  which is already converted (`Field_TimeToLive ab` / `TimeToLive mt (self Field_TimeToLive) () (d Duration)`).
  **No `TTL` is declared in this domain.**
- **The ping's RTT became `Observer_RoundTripTime`.** `RTT()` returned `duration.NanoSecond`, and
  there is no field abstraction anywhere for a round trip time; the observer-mutator rule's shape
  is `Observer_X` with a `Get<Concept>` accessor, so `Observer_RoundTripTime` /
  `GetRoundTripTime` returning memar's `Duration`. Note the Go said `duration.NanoSecond` while the
  time domain's field returns memar's `Duration` — same elapsed-time concept, one spelling.
- **`Address` is a named `String`,** the shape `knowledge/text/protocol/dt-text.kh` already takes
  for a named string. Its binary wire form is `AddressBinary ab { Array_Dynamic }` in the address
  edge's data model, read by `Observer_Node_AddressBinary`.
- **`ResourceType` composes memar's `U8`.** It is a bare `uint8` in the Go with no constants and no
  domain document; composing `U8` states the width and domain-izes the name without inventing a
  vocabulary. The vocabulary question is recorded below.
- **`log_p.Event` is memar's `ProcessLog_Event`.** `AuditLogDataModel` composes it from
  `memar/modules/process/log/protocol/log-event.kh`. The Go's own `TODO::: other condition` is
  carried as a question, not as an invented requirement.
- **`Field_Type` on the label domain is `Field_LabelType`** as converted at
  `modules/knowledge/label/protocol/dt-uuid.kh`.
- **The empty `BS_*` shapes were not declared.** `BS_RegisterNodeAddresses_Req` / `_Res` and
  `BS_GetNeighborAddresses_Req` are `interface{}` in the Go. Rule 6 forbids converting an empty Go
  interface into an empty `ab`, so only `BS_GetNeighborAddresses_Response` — which has a real
  requirement — is declared.

## Ambiguities Resolved

- **Four edge folders have no domain document** — answered (2026-10-08): the documents exist now — [`address/address.md`](edges/address/address.md), [`health/health.md`](edges/health/health.md), [`resource/resource.md`](edges/resource/resource.md), [`language-human/language-human.md`](edges/language-human/language-human.md), and also [`node-metric/node-metric.md`](edges/node-metric/node-metric.md) — each with a one-line README, extracted from the protocol sources and the domain document's settled sections in the Edge folder shape (Model, Policies, Placement, Open questions). The bucket doubts the sources surfaced are recorded in those documents' Open questions: address and resource do not prove their far end is a node at all, and node-metric holds no relation — it held two source files, not three — and is flagged for the wrong-kind-folder pass.

## Open Questions

- **`Status()` on the node↔language-human data model returns nothing.** The identical shape exists
  in `computer/software/edges/language-human/protocol/data_model.kh` and is recorded in that
  domain's handoff; it is one question in two places.
- **The node data model needs an application identity that this repository does not have.**
  `edges/node/protocol/data_model.kh` requires `app_p.Field_ApplicationID` from
  `modules/computer/app/protocol`, and **`modules/computer/app/` does not exist in this
  repository at all** — not as an unconverted module, not as a folder. The node record therefore
  cannot be converted until that domain exists or the requirement is dropped. This is the single
  biggest blocker in this domain.
- **The cluster contract is blocked behind it.** `edges/node/protocol/distributed-cluster.kh`
  declares `Cluster` over `DataModel`, so it waits on the same application identity. It also
  declares `var CLU Cluster` — a package-level global that the Go comment says the application
  must assign on its `main.go` ("CLU is default global protocol.Cluster like window global
  variable in browsers"). A mutable global in a protocol file is not something this repository's
  rule 1 (abstraction-only under `protocol/`) can hold; where the cluster singleton should live is
  a placement question.
- **`Node` in `edges/node/protocol/storage.kh` declares `NodeID()` and `Addr()` with no results.**
  The Go comment on `Addr()` is `// TODO::: IP, GP`. Both are rule-6 cases; what a node's storage
  surface answers is unstated.
- **`ResourceType` has no vocabulary.** The resource edge has no domain document, and the only
  recorded resource labels in this domain are the desired/actual duality in
  [edges/node-resource](edges/node-resource/node-resource.md), which is a label on the edge, not a
  value of `ResourceType`. What resource kinds exist (CPU, RAM, GPU, storage, network?) is
  unrecorded.
- **`edges/audit-log/protocol/config.kh` is a configuration constant, not an abstraction.** It
  declares `CNF_LogMode log_p.Level = log_p.Level_AllSet`, whose policy is now in the domain
  document. Rule 1 makes `protocol/` abstraction-only, so a module-level configuration *value*
  filed there has no Khayyam form; where a node's log-mode configuration should be declared (a
  configuration domain, or the implementation layer) is undecided. `log_p.Level` is itself a
  fifteen-value bit flag over a `uint32` — the same shape `AcceptedProtocols` had in
  `computer/software` — and memar owns it, so it was not re-modelled here.
- **`ReplicationID()` on the node record binds an edge whose processing is undecided.**
  [edges/replication](edges/replication/replication.md) asks whether replication becomes a
  capability; the record already carries a `replicationID` byte.
- **Node lookup is inconsistent-hash-by-hand.** `internal/node/nodes.kh` finds the responsible node
  for a record by binary-searching `primaryIndexRanges` on the first eight bytes of the record id,
  and `GetNodeByObjectID` walks replications to find a node whose connection is open. The Go
  carries `// TODO::: change to Giti network when it is ready to serve lookup domain to GP address`,
  and `OrderZones` (`orderZones`) is an empty `TODO:::`. Which node owns a record is a stated
  contract somewhere; it is not here.

### From Request Research 001 (2026-10-19): the node end of the request chain
Pointer only; the reasoning is in [Request Research 001](../request/request.research.001.md#1-what-the-domain-is-for) and nothing in this domain changed.
- The node that served a request is the far end of the request's connection (`connection_to`, instance to instance); the proposal stores no node field on the request. On a client instance, [`user-active`](edges/user-active/user-active.md) is the default requester, derivable and not stored.
- [`audit-log`](edges/audit-log/audit-log.md) is the node's operational log, selective by mode; the request record is the organization's provenance memory and must not be selectively dropped. The proposal keeps them two things that may share a listener (request handoff question 16); the audit-log Khayyam shape (`ProcessLog_Event` alone) should wait for that answer.
- The peer services (ping, sync time) carry no requester and change no recorded state; the proposal says they are not requests in the request domain's sense (request handoff question 3).
- [`node-metric`](edges/node-metric/node-metric.md)'s `NetworkInfo` rate limits by owner type are the policy the proposed `quota` pluggable of the request domain would evaluate.

## Left unconverted


| File | Why |
| --- | --- |
| `edges/node/protocol/data_model.kh` | Needs `Field_ApplicationID` from `modules/computer/app/protocol`, which does not exist in this repository. |
| `edges/node/protocol/distributed-cluster.kh` | Depends on the node data model above; also declares a mutable package-level global under `protocol/`. |
| `edges/node/protocol/storage.kh` | `NodeID()` and `Addr()` declare no results and no types. |
| `edges/audit-log/protocol/config.kh` | A configuration value under `protocol/`; rule 1 leaves it no Khayyam form. |
| `edges/user-active/users.kh` | Needs `society_p.UUID` from `modules/identity/society/protocol`, which does not exist in this repository. `user_p.UUID` is available as `UserUUID`. |
| `edges/node-metric/manifest.kh`, `edges/node-metric/make-main-file.kh` | Go structs with bodies (`init` deriving the app id from a hash) and a `text/template` plus `go/format` generator. Implementation layer; Phase 3 / Phase 4. The settled content is in the domain document. |
| `edges/health/services/ping/frame-ping.kh` | A network frame capsule with a syllab accessor and `//memar:impl` methods. Implementation layer. |
| `edges/audit-log/services/listener/logic.kh`, `…/internal/event.kh`, `…/internal/log.kh` | The listener registry, the log event capsule and the logger. Implementation layer; Phase 3. The event capsule is nearly all stubs — `Decode`, `Encode`, `Unmarshal`, `Marshal`, `Len` and `CheckSyllab` all return nothing, and `Init` carries `// TODO::: set NodeID???`. |
| `errors/errors.kh`, `errors/locale.eng.kh`, `errors/locale.per.kh` | One error (`ErrNoNodeAvailable`) and its English and Persian detail text, written by build-tag-gated `init()`. No method on a type writes human-readable text yet — the same reason `knowledge/text` and `computer/software` were left in this shape. `locale.per.kh` has an empty `init()` body. |
| `init.kh` | `DomainName`, a `RequestType` flag pair (standalone, broadcast) and `registerServices()`. Phase 4 entry point. |
| `internal/node/*.kh` (5 files) | `Node`, `NodeDataStructure`, `Nodes`, `replication`, `replications` — the in-memory cluster with its hashing, ordering and connection logic. Implementation layer; Phase 3. |
| `services/*.kh` (5 files) | Service metadata records, sRPC handlers and syllab codecs. Phase 3 / Phase 4. Their specified behaviour is in the domain document. |

**What the conversion of the blocked files needs from elsewhere:** a `computer/app` domain with a
`Field_ApplicationID`; an `identity/society` domain with a UUID; and `edges/node/protocol/storage.kh`
and `edges/node/protocol/distributed-cluster.kh` need their own domain's design settled. None of
these is this domain's to declare.

## Related Artifacts

- [`README.md`](README.md)
- [`instance_of.md`](instance_of.md)
- `modules/identity/time/edges/ttl/protocol/ttl.kh` — the `Field_TimeToLive` this domain imports
- `memar/modules/process/log/protocol/log-event.kh` — `ProcessLog_Event`
- [edges/replication](edges/replication/replication.md),
  [edges/node-status](edges/node-status/node-status.md),
  [edges/node-resource](edges/node-resource/node-resource.md),
  [edges/net-address](edges/net-address/net-address.md),
  [edges/user-active](edges/user-active/user-active.md),
  [edges/hardware](edges/hardware/hardware.md),
  [edges/audit-log](edges/audit-log/audit-log.md)

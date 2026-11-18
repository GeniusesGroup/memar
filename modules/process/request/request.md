# Request
Request is a formal message requesting something that is submitted to an authority or an act of asking politely or formally for something.

## Usages
- Application service request domain use to store requests to prove how other records created as a chain to other records or standalone data.
- It can also use to store user requests as drafts for users to send later
- Prove how this a request created in the chain of other requests.

## Request–response
In computer science, [request–response](https://en.wikipedia.org/wiki/Request%E2%80%93response) or request–reply is one of the basic methods computers use to communicate with each other in a network, in which the first computer sends a request for some data and the second responds to the request. More specifically, it is a message exchange pattern in which a requestor sends a request message to a replier system, which receives and processes the request, ultimately returning a message in response. It is analogous to a telephone call, in which the caller must wait for the recipient to pick up before anything can be discussed. This is a simple but powerful messaging pattern which allows two applications to have a two-way conversation with one another over a channel; it is especially common in client–server architectures.

## Identity
The audit request's own identity is **not** declared by this repository. Memar declares
`Request_UUID` in `memar/modules/process/request/protocol/dt-uuid.kh`, and
`Observer_RequestID` / `GetRequestID` and `Observer_RequestIDs` / `GetRequestIDs` in
`memar/modules/process/request/protocol/dt-uuid.observers.kh`. This domain imports those
names wherever a record carries a request identity; it declares no rival. The audit time of a
request is likewise memar's `Observer_Time_Asked` / `GetAskedAt`.

The Go source of `protocol/dt-uuid.kh` carried

```
type UUID thing_p.UUID

// type UUID request_p.UUID
```

— the author had already written and commented the line that makes the identity memar's, and
this conversion records that decision rather than reverting it.

A Request retained through the memory contract is named by the address through which it is retained ([Memory Address](../../computer/memory/address/address.md), the reference to an address; [Recording a change of state](#recording-a-change-of-state) says how it is written); whether that address is also the identity above is decision 2 of the handoff's memory-port decisions, taken Tentatively.

## Storage
A request record is stored under two keys of the same identity, which the Go source named
`Storage_Key_Primary` and `Storage_Key_Cluster`: the primary key places the record, the cluster
key groups it. Both are satisfied by the request identity alone, so the two contracts carry the
same requirement today; what distinguishes them in the storage layer is not yet stated (see the
handoff).

A request record is also found by the user who made it, paged. The find-by-service-id pair
exists in the Go source and is not converted here, because `Field_ServiceID` belongs to the
`process/service` domain; `Field_ServiceID` still lives as a stub in `protocol/dt-uuid.kh` there.

## Request data and signature
The `data` edge carries the encoded payload of the request: `RequestData` decodes by the service
request structure and the compression type it was stored with, so the record must be read
together with the service that wrote it.

The `signature` edge carries the evidence that the user asked for the change: a byte sequence
kept on the record so that a later reader can prove the request was not invented after the fact.

## Services from retired user-request sources
`services/` holds four service stubs moved from the retired `modules/user-request*` domains
(`user-request`, `user-request-chain`, `user-request-data`, `user-request-metric`). Their Go
bodies remain under `TODO(go-migrate)` until converted; their Go import paths
(`modules/user-request/protocol`) name a tree this repository no longer has. This domain
supersedes those domains. Development of the stubs continues here.

## Recording a change of state
A domain holds the current value of what it is about, as a part on its node ([Memory Record → Definition](../../../modules-plugable/computer/memory/store/record/record.md#definition)). A change to that value is recorded by a Request, a node of its own that holds the change; the domain holds nothing of it. No domain keeps a history, the chain of its Requests is the history, and that chain is the audit trail; it is not a [log](../log/log.md), which is a service's record of what it did and saw.

### What is a change of state
A change of state is a change to the current value of a part whose value is acquired data ([Modeling → Acquired Data vs. Discovered Data](../../../modules/knowledge/modeling/modeling.md#acquired-data-vs-discovered-data)): a primary fact that nothing else in the model can recompute. Every such change is recorded, by the rule below. These are not changes of state by themselves:
- **A discovered value.** Whether a thing is blocked by the things it depends on, the order of a queue, a count, an index: each is recomputed from acquired data and is never stored as acquired.
- **A liveness signal.** A heartbeat has no use after the interval it covers, so it is held in volatile memory with a lease and never in the store ([Memory → Volatility: the real classifier](../../computer/memory/memory.md#volatility-the-real-classifier)). No claim has one today, since a claim older than a day is taken as a dead agent's. If one is introduced, the change recorded is the takeover of the claim it failed to keep, which changes the holder.
- **The value of an immutable node.** The node carries its own value, author and creation time. A service may still have a separate Request for the operation that created that node; the Request records the asking, not a duplicate of the node's value.
- **A reading, and a refusal.** A listing or a read changes nothing. A refused asking changed no value, so this rule records none.

The recorded changes of such a part include its creation, a claim, a release and the takeover of a lapsed claim, every move of its Status, a change of rank, a dependence added or dropped, a label added or removed, a change of parent, a member joining, and the move of a pointer to a current content. The tool's session log from 2026-10-07 to 2026-10-23 holds 1,440 events, 290 on its busiest day, which is a batch every few minutes at most, so recording each change costs no more than the ordinary work does.

### The write
The SDK owns the client-side Request cache. Before sending a side-effecting call, it creates the Request identity and client-declared `asked_at`, then persists that service call's exact request envelope in the caller's local Request node. Each call to a different service, or each separate relation operation, has its own Request identity and cache entry. A retry after a timeout, disconnect, app restart or ordinary offline interval resends that exact envelope with the same identity and `asked_at`; it never creates a sibling Request for the same intent. `recorded_at` is set by the server-side Request domain when it first records receipt. Consumers may choose either time for ordering; `Request_UUID` remains the stable identity and tie-breaker.

Each service handles only its own requested operation and its own Request identity. If that operation needs multiple Store reads or writes, its service-level coordinator may use a queue, lock, sequencer or recovery process; the Store exposes individual reads and writes and neither promises an atomic batch nor owns concurrency policy. A service's contract states how it handles partial completion, retry with the same Request identity, a conflicting identity and an unavailable Store. A workflow that calls several services retains and reports each call's independent Request and outcome; one call's success does not imply another call succeeded.

### The Request node
The Request is named by its `Request_UUID`, created by the client SDK before the call and retained in the SDK's local Request node. Its `asked_at` comes from that same cached envelope; `recorded_at` is assigned by the server-side Request service on first receipt. Its parts:
- **`request`**, the fact, in a canonical encoding: who asked (`requested_by`, an identity written `person:<name>` or `agent:<model or tool name>`, or the explicit marker `unrecorded`, which only a migrated record may carry); the verb asked (`operation`); the instant it was asked (`asked_at`) and the instant it was recorded (`recorded_at`); the changes, each a node id, a domain key, the token of the value replaced or its absence, the token of the new value, and the Request it follows (`follows`) for that key or none; the digest of its data; and its signature.
- **`request-data`**, the payload: the new values of the changed parts. It is a part of its own so that a rule of erasure, if the owner makes one, can reach the payload while the fact, the digest and the signature stay.
- **Labels.** The label of Requests, and the id of each node the Request changed.

A third part belongs to the Request domain and sits on the changed node, **`request-head`**: a canonical map from a domain key to the id of the last Request that changed that part. The Request coordinator updates this part as a separate write while serializing changes to the same key. It is stored rather than derived because a value that returns to an earlier value returns to its token, and Request identities do not order by commit time. `follows` of a change is the entry the head held for its key when the service read it, or none when the part is created, so a Request that changes several keys follows a different Request for each. Competing writers are sequenced by the coordinator, which rereads the head when another writer has advanced it.

The history of a part is walked from the head along `follows`, each Request stating the tokens it replaced and produced, which a reader can check against its neighbours. The finding of Requests by the node they changed, or by anything else a label carries, is `scan` by the node's id and the label of Requests, answered by the adapter's derived index ([Memory Record → What every adapter guarantees](../../../modules-plugable/computer/memory/store/record/record.md#what-every-adapter-guarantees)); no index is written into the store, and no walk of a history needs one. The part `request-head` is itself not recorded by a Request: it is written with the Request it names and is the record's own bookkeeping, and a rule that recorded it would record the record of the record.

The fields above are named once, in code, when the Request is built.

Owed: memory.stored-shape

Until the token domain issues keys, `signature` holds the SHA-256 digest of the canonical `request` part without the signature and names no key.

Owed: request.signing-key

## Client-held Request identity
A caller that may not learn whether a side-effecting verb finished — an agent whose tool call timed out, a client whose connection dropped — must not mint a second Request with the same intent. The SDK persists the complete request envelope in its local Request node before transmission. On an unclear outcome it resends that same envelope, preserving its Request_UUID and `asked_at`; the server's Request service re-examines the same identity and may continue or reconcile it. It never creates a sibling Request for that intent. A device reset may destroy the local node; recovery after loss of the device's durable storage is outside the guarantee.

This is not the same as [Process → Continuation and Retry](../process.md#continuation-and-retry). A process-level retry is a new interaction that refers back to an earlier one. Re-examining the same Request identity preserves one intent and one audit record while the coordinator resolves an uncertain outcome. The status words a Request may carry are named in [Request states](labels/request-status.md); their transition rules and the agent-facing create / status / re-examine services are owed.

A conversation-post guard that refuses a text identical to the latest of its kind ([Timeline_Error_SameContent](../../management/timeline/errors/placement.kh)) is a local defence when the caller held no Request id; it is not a substitute for Request identity on verbs whose duplicate effect is costly.

## Other resources
- [abp](https://docs.abp.io/en/abp/latest/Entities#auditing-interfaces)

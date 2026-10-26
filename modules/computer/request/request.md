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
request is likewise memar's `Observer_Time_Request`.

The Go source of `protocol/dt-uuid.kh` carried

```
type UUID thing_p.UUID

// type UUID request_p.UUID
```

— the author had already written and commented the line that makes the identity memar's, and
this conversion records that decision rather than reverting it.

A Request retained through the memory contract is named by the address through which it is retained ([Memory Address](../memory/address/address.md), the reference to an address; [Recording a change of state](#recording-a-change-of-state) says how it is written); whether that address is also the identity above is decision 2 of the handoff's memory-port decisions, taken Tentatively.

## Storage
A request record is stored under two keys of the same identity, which the Go source named
`Storage_Key_Primary` and `Storage_Key_Cluster`: the primary key places the record, the cluster
key groups it. Both are satisfied by the request identity alone, so the two contracts carry the
same requirement today; what distinguishes them in the storage layer is not yet stated (see the
handoff).

A request record is also found by the user who made it, paged. The find-by-service-id pair
exists in the Go source and is not converted here, because `Field_ServiceID` belongs to the
`computer/service` domain, which is not converted yet.

## Request data and signature
The `data` edge carries the encoded payload of the request: `RequestData` decodes by the service
request structure and the compression type it was stored with, so the record must be read
together with the service that wrote it.

The `signature` edge carries the evidence that the user asked for the change: a byte sequence
kept on the record so that a later reader can prove the request was not invented after the fact.

## Retired sources
`_import/` holds four copies of the retired `modules/user-request*` domains
(`user-request`, `user-request-chain`, `user-request-data`, `user-request-metric`). They are
excluded from every build by the leading underscore and their Go import paths
(`modules/user-request/protocol`) name a tree this repository no longer has. This domain
supersedes them. Their content is not converted here; what they held that still reads as current
intent is recorded in the handoff.

## Recording a change of state
A domain holds the current value of what it is about, as a part on its node ([Memory Record → Definition](../../../modules-plugable/computer/memory/store/record/record.md#definition)). A change to that value is recorded by a Request, a node of its own that holds the change; the domain holds nothing of it. No domain keeps a history, the chain of its Requests is the history, and that chain is the audit log. The timeline is for discussion and is not where a change of state is recorded.

### What is a change of state
A change of state is a change to the current value of a part whose value is acquired data ([Modeling → Acquired Data vs. Discovered Data](../../../docs/modeling.md#acquired-data-vs-discovered-data)): a primary fact that nothing else in the model can recompute. Every such change is recorded, by the rule below. These are not changes of state, and no Request records them:
- **A discovered value.** Whether a task is blocked by the tasks it depends on, the order of a queue, a count, an index: each is recomputed from acquired data and is never stored as acquired.
- **A liveness signal.** A heartbeat has no use after the interval it covers, so it is held in volatile memory with a lease and never in the store ([Memory → Volatility: the real classifier](../memory/memory.md#volatility-the-real-classifier)). No task has one today, since a claim older than a day is taken as a dead agent's. If one is introduced, the change recorded is the takeover of the claim it failed to keep, which changes the holder.
- **The creation of an immutable node.** A content, a text, a placement or a Request is written once and carries its own author and time; the node is its own record.
- **A reading, and a refusal.** A listing or a read changes nothing. A refused asking changed no value, so this rule records none; whether the Request domain records refusals is its own open question ([Request Handoff](request.handoff.md#decisions-taken-by-the-memory-port-design-2026-10-23)).

For a task, the recorded changes are: its creation, a claim, a release and the takeover of a lapsed claim, every move of its Status, a change of priority, a dependence added or dropped, a label added or removed, a change of parent, a person joining the Task's group, and the move of a pointer to a current content. The tool's session log from 2026-10-07 to 2026-10-23 holds 1,440 events, 290 on its busiest day, which is a batch every few minutes at most, so recording each change costs no more than the ordinary work does.

### The write
The service that applies a verb to a domain is the layer that composes the domain, the Request domain and the port, and it writes the new value and the Request as one batch. The domain's own types know neither the Request nor the port. The batch holds:
- **Expectations,** in this order. That the Request's own part is absent, so a Request is written once and never edited, and a conflict on it means the change was committed before. For each changed part, that it still holds the token the service read, or is absent when the change is the part's creation. For each changed node, that its part `request-head` still holds the token the service read, or is absent when the node has none.
- **Writes.** The nodes the change creates, a content, its text and its placement when it places one, each with an expectation that its part is absent, in the same batch as the pointer move, so that a pointer never names a content that is missing after a crash; each changed part with its new value; each changed node's `request-head` with the new Request's id set for the keys it changed; the Request's two parts, `request` and `request-data`; and the Request's labels.

The batch is applied atomically, which needs a class whose adapter declares `atomic_batch`; the class that records state changes is refused otherwise ([Memory Record → Binding adapters to classes](../../../modules-plugable/computer/memory/store/record/record.md#binding-adapters-to-classes)). On Conflict the service first reads the Request by its id, since a retried batch may find its own earlier commit: present, the change was committed and the verb is done. Absent, it reads again, decides again, and writes a new batch with a new Request id. When the answer is Unavailable with the reason Failed or Unreachable, the port's rule is that the batch can no longer commit, so the service writes the same batch again with the same Request id, which only this case reuses, and gives up after three tries; with the reason NotHeld it does not retry, since the node is not this store's to write.

### The Request node
The Request is named by the id of its node, minted by the service before the batch. Its parts:
- **`request`**, the fact, in a canonical encoding: who asked (`requested_by`, an identity written `person:<name>` or `agent:<model or tool name>`, or the explicit marker `unrecorded`, which only a migrated record may carry); the verb asked (`operation`); the instant it was asked (`asked_at`) and the instant it was recorded (`recorded_at`); the changes, each a node id, a domain key, the token of the value replaced or its absence, the token of the new value, and the Request it follows (`follows`) for that key or none; the digest of its data; and its signature.
- **`request-data`**, the payload: the new values of the changed parts. It is a part of its own so that a rule of erasure, if the owner makes one, can reach the payload while the fact, the digest and the signature stay.
- **Labels.** The label of Requests, and the id of each node the Request changed.

A third part belongs to the Request domain and sits on the changed node, **`request-head`**: a canonical map from a domain key to the id of the last Request that changed that part. It is written in the same batch as the Request and guarded by the same kind of expectation, and it is stored and not derived because a derivation cannot give it: a value that returns to an earlier value returns to its token, and ids order Requests by the instant they were minted and not by the order they were committed, so no search of the Requests can tell which one is last. `follows` of a change is the entry the head held for its key when the service read it, or none when the part is created, so a Request that changes several keys follows a different Request for each, and two writers cannot both extend one chain: the second fails its expectation on the head and reads again.

The history of a part is walked from the head along `follows`, each Request stating the tokens it replaced and produced, which a reader can check against its neighbours. The finding of Requests by the node they changed, or by anything else a label carries, is `scan` by the node's id and the label of Requests, answered by the adapter's derived index ([Memory Record → What every adapter guarantees](../../../modules-plugable/computer/memory/store/record/record.md#what-every-adapter-guarantees)); no index is written into the store, and no walk of a history needs one. The part `request-head` is itself not recorded by a Request: it is written with the Request it names and is the record's own bookkeeping, and a rule that recorded it would record the record of the record.

The fields above are named once, in code, when the Request is built.

Owed: memory.stored-shape

Until the token domain issues keys, `signature` holds the SHA-256 digest of the canonical `request` part without the signature and names no key.

Owed: request.signing-key

## Other resources
- [abp](https://docs.abp.io/en/abp/latest/Entities#auditing-interfaces)

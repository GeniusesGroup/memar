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

`_import/` holds four copies of the retired `org/modules/user-request*` domains
(`user-request`, `user-request-chain`, `user-request-data`, `user-request-metric`). They are
excluded from every build by the leading underscore and their Go import paths
(`org/modules/user-request/protocol`) name a tree this repository no longer has. This domain
supersedes them. Their content is not converted here; what they held that still reads as current
intent is recorded in the handoff.

## Other resources

- [abp](https://docs.abp.io/en/abp/latest/Entities#auditing-interfaces)

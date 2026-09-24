---
Title: "sRPC — Application Protocol"
Status: Draft
Start Date: 2020-05-10
ID: 441408
---

# sRPC — Application Protocol

## Abstract
sRPC (Syllab Remote Procedure Call) is Memar's application protocol: frames that ride in a [Networking](./networking.md) packet — with lower-layer frames such as [Chapar](./chapar.md) or [GP](./giti.md), or on older Internet transports — and supply the fields needed to select a service, identify a call, carry a payload, open and close a stream, and agree an acknowledgement scheme. It decides that routing, service, operation, and request are independent identities, none of them a path segment or a query key; that service lookup and protocol-forced data stay minimal; that peers may agree an acknowledgement scheme rather than transmit blindly; and that durable-delivery machinery belongs in a library wrapping the application's own store, not in a standalone message broker. Frame type numbers are registered in [Networking](./networking.md); this document is the contract for those frames' fields and peer behavior.

## Introduction

### Motivation
Application-layer calls fail when the protocol itself is the cost: finding a service among a server's services requires extra lookup work, and the protocol forces extra data onto every exchange. They fail again when routing, handler, operation, and request instance share one representation, so none of them can be addressed, matched, or adapted on its own. This protocol exists to keep lookup and forced exchange small, and to keep those four as distinct fields. Human readability of the wire is not a goal.

### Methodology
Frame type numbers live in the [Networking](./networking.md) registry; this document specifies field layout and peer rules for those frames. Guest-adaptation forms — the HTTP URI multiplexer under [Service ID](#service-id), an HTTP `Error-ID` header under [Error ID](#error-id) — are consumed contracts with [HTTP](./http.md), not this protocol's addressing model. Implementations are not listed here; Memar's implementation modules live under [`modules/`](../../modules/) in this repository.

## Explanation

### Independent identities
sRPC models routing, service, operation, and request as distinct representations: the underlying packet's addressing determines the destination; [Service ID](#service-id) selects the handler; [Stream ID](#stream-id) (and the [Service Frame](#service-frame)'s `Time` field for non-stream calls) identifies the instance; [Payload](#payload-request-or-response) carries the request or response. None of these is a path segment or a query key. Older Internet protocols may carry this protocol as transport or as an adapter — the http-uri form under [Service ID](#service-id) is that adapter, not this protocol's addressing model. Memar's position on depending on HTTP is [HTTP](./http.md).

### Goals and non-goals
1. Minimum overhead to find a service among a server's services.
2. Minimum data exchange forced by the protocol.
3. Easy understanding by a human is not a goal.

### Frames
Each packet may carry many frames, as long as the packet respects the network MTU. Every frame has a fixed first field named `Type`, a signed 8-bit integer. `Type` occupies the same identification role as [MediaTypeID](./media-type.md) but is not a 64-bit unsigned integer: it is one byte here, to keep per-frame overhead small. Frame numbers are registered in the [Networking](./networking.md) document.

#### Packet Sequence Number Frame
An incremental number used to detect a failed packet, and similar conditions. Use even numbers (0, 2, 4, 6, …) for the client (who starts the connection) and odd numbers (1, 3, 5, 7, …) for the server (who receives the connection). Separation of the packet identifiers ensures that peers can send packets without the latency imposed by negotiating for an identifier.

```go
type PacketSequenceNumber struct {
    SequenceNumber uint64
}
```

#### Ping Frame
Ping carries no fields besides the common `Type`.

```go
type Ping struct {
}
```

#### Service Frame
Call a service without opening a stream. `Time` matches the request to the response and is used to drop the call if its TTL has passed.

```go
type Service struct {
	Length     uint16
	ServiceID  uint64
	CompressID uint64
	Time       int64 // It is used to match the request and response and drop if TTL
	Payload    []byte
}
```

#### Open-Stream
Opens a stream.

```go
type OpenStream struct {
    ProtocolID     uint64
    ServiceID      uint64
    CompressTypeID uint64
    DataLength     uint64
    Weight         protocol.Weight
}
```

#### Close-Stream Frame
Closes a stream. `Reason` is a `uint64` field. Whether `Reason` is an Error ID is unsettled.

```go
type CloseStream struct {
    Reason   uint64
}
```

#### Data Frame
Carries a stream's payload at a given offset.

```go
type Data struct {
    Length   uint16
    StreamID uint64
    Offset   uint64
    Payload  []byte
}
```

#### Error
Reports an error on a stream.

```go
type Error struct {
    StreamID uint64
    ErrorID  uint64
}
```

#### Data Signature Frame
Carries a signature over stream data.

```go
type DataSignature struct {
	Length    uint16
	StreamID  uint64
	Signature []byte
}
```

### Frame fields
Fields shared across frames, and fields whose meaning is stated once for every frame that carries them.

#### Length
Length is the length of the whole frame excluding the common `Type` field. It must respect the data-link protocol's limits: fragmentation is not supported. Prefer not to exceed 8192 bytes (octets), or 8 KB.

#### Stream ID
Use even numbers for the client (who starts the connection) to start a stream, e.g. 0, 2, 4, 6, …. Use odd numbers for the server (who receives the connection) to start a stream, e.g. 1, 3, 5, 7, …. Separation of the stream identifiers ensures that client and server can open streams without the latency imposed by negotiating for an identifier.

#### Offset
A single stream can transmit at most 4.72 TB with a 1.18 KB payload Length, as a limit to 1.5 KB Ethernet frames.

#### ProtocolID
ProtocolID is suggested to indicate the protocol in making each stream process. Even ProtocolID values are suggested as a port number to listen, receive, respond, or serve; odd numbers for send, request, or client.

#### Service ID
Service ID routes to a service and calls the handler. It is the same as the [MediaTypeID](./media-type.md) of the service media type. Other protocols may use it as an adapter, e.g. http-uri: `/m?{{.ServiceID}}`, where `m` is short for multiplexer (mux). That form is guest interoperability, not this protocol's addressing model.

#### Error ID
Error ID indicates that calling the service produced an error. It is the same as the [MediaTypeID](./media-type.md) of the error media type. Other protocols may carry it as an adapter, e.g. http-header: `Error-ID: {{.ErrorID}}`.

#### Payload (Request or Response)
Payload may be any data, including another application protocol (e.g. HTTP, sRPC). Stream payload is stored in order by packet sequence number ([Packet Sequence Number Frame](#packet-sequence-number-frame)) so the stream can be reassembled. Payload length is whatever the called service's specification requires. The default codec is [Syllab](./syllab.md). Other codecs and protocols (including HTTP and JSON) are possible; they are not suggested.

### Acknowledgement Scheme
sRPC peers may agree to use any acknowledgement scheme, such as selective negative acknowledgement (SNACK), negative-acknowledgement (NAK or NACK), or [acknowledgement (ACK)](https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)) as used in many protocols such as TCP. Unlike IP, UDP, and similar protocols, this is not [blind transmission](https://en.wikipedia.org/wiki/Blind_transmission).

### Position on Message Brokers
The standalone message broker — MQTT, AMQP, and kin deployed as a separate service — is an external protocol surface Memar does not adopt as a default, and the reason is arithmetic, not taste. The honest-delivery pattern the broker serves (at-least-once, exactly-once semantics, its QoS levels) requires the broker to persist messages to non-volatile storage before acknowledging them. An application that itself must durably record what it sends then pays for that persistence twice: once in the application's own storage, once in the broker's — plus the network hop between them — per message, at layers that did not need the duplication. At IoT volumes this cost dominates the system's storage budget; at any volume it buys a guarantee the application's own store could have provided directly.

Memar's stance: **the broker's mechanism belongs in a library inside the application's own architecture, not in a separate standalone service.** Where durable delivery is the requirement, the durable store is the application's own; the delivery machinery (the acknowledgement discipline this protocol already defines, persistent queues, retries initiated by whichever participant this framework's retry rules allow) wraps that store rather than shadowing it. This is the same judgment [Networking](./networking.md#memars-position-on-the-traditional-network-stack) records for protocol logic generally: middleware logic is application-relevant logic, and its placement is a decision to be made, not an OS-shaped default to be inherited.

Two further notes are attached to this position:

- The sync/async client models brokers offer are both cost-irrational in the same way: either the client's logic is structured around the broker's session (sync), or the broker is trusted to have persisted before the client continues (async) — losing data precisely when the acknowledgement meant nothing. Both models are artifacts of the broker being a separate process; a library-owned broker dissolves the trade-off by letting the application's own storage be the durability point.
- The producer-consumer independence principle ([Process → Events](../process.md#events)) is untouched by this position: making the broker mechanism a library does not couple producers to consumers — it only relocates who runs the machinery.

Open work on this protocol — the wire-level cancellation contract, and the wire-shape agreement this position's delivery machinery needs — is tracked in the paired [handoff](./sRPC.handoff.md).

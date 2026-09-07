# sRPC - Application Protocol
sRPC (Syllab Remote Procedure Call) is a RPC(remote procedure call) protocol. It is develope to introduce frame structure that can use in any network packet to add full functionality to base protocols frames e.g. [Chapar](./chapar.md) or [GP](./giti.md) protocols.

It can also use to be a messaging protocol among with other older Internet protocols like IP, TCP, UDP, HTTP, ...

## Goals
- Minimum overhead to find service from server services
- Minimum data exchange forces by protocol

## Not Goals
- Easy to understand by human

## Frames - Internal Services
Each packet can carry many frames until respect network MTU. All frames have fixed first field name `Type` with `signed 8bit` length that is same as [MediaTypeID](./media-type.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead.

Frame numbers register in the [Networking](./networking.md) document.

### Packet Sequence Number Frame
Incremental number use to detect failed packet, ... Use even number e.g. 0,2,4,6,... for client(who start connection) and Use odd number e.g. 1,3,5,7,... for server(who receive connection). Separation of the packet identifiers ensures that peer are able to send packets without the latency imposed by negotiating for an identifier.
```go
type PacketSequenceNumber struct {
    SequenceNumber uint64
}
```

### Ping Frame
```go
type Ping struct {
}
```

### Service Frame
Call a service without need to open any stream.
```go
type Service struct {
	Length     uint16
	ServiceID  uint64
	CompressID uint64
	Time       int64 // It is used to match the request and response and drop if TTL
	Payload    []byte
}
```

### Open-Stream
```go
type OpenStream struct {
    ProtocolID     uint64
    ServiceID      uint64
    CompressTypeID uint64
    DataLength     uint64
    Weight         protocol.Weight
}
```

### Close-Stream Frame
```go
type CloseStream struct {
    Reason   uint64 // ErrorID??
}
```

### Data Frame
```go
type Data struct {
    Length   uint16
    StreamID uint64
    Offset   uint64
    Payload  []byte
}
```

### Error
```go
type Error struct {
    StreamID uint64
    ErrorID  uint64
}
```

### Data Signature Frame
```go
type DataSignature struct {
	Length    uint16
	StreamID  uint64
	Signature []byte
}
```

## Frames Fields

### Length
- Length of whole frame exclude `Type` common filed.
- must respect data-link protocol due to not Fragmentation supported. Better not over of 8192 Byte(octets) or 8KB

### Stream ID
Use even number for client(who start connection) to start a stream e.g. 0,2,4,6,... . Use odd number for server(who receive connection) to start a stream e.g. 1,3,5,7,... . Separation of the stream identifiers ensures that client and server are able to open streams without the latency imposed by negotiating for an identifier.

### Offset
Max 4.72TB can transmit in single stream with 1.18KB payload Length as limit to 1.5KB of ethernet frames

### ProtocolID
Suggest to indicate protocolID in making each stream process. Also suggest to use even ProtocolID as a port number to listen||receive||response||server and odd numbers for send||request||client.

### Service ID
- Use to route service and call the handler.
- Same as [MediaTypeID](./media-type.md) of service media type.
- Can use by other protocols e.g. http-uri: "/m?{{.ServiceID}}" that m use to be short and abbreviation for multiplexer(mux).

### Error ID
- Use to show if calling service occur an error.
- Same as [MediaTypeID](./media-type.md) of error media type.
- Can transfer by other protocols e.g. http-header: "Error-ID: {{.ErrorID}}"

### Payload (Request or Response)
- Payload can be any data like application protocol e.g. HTTP, sRPC, ... . It must store in order by PacketID to make whole a stream data
- Payload with any length that service force to accept it on its specs usually is [Syllab](./Syllab.md) codec.   
- *Just for your information, payload can be any other protocols and codecs like http, json too but it is not standard and not suggest from us.*

## Acknowledgement Scheme
sRPC peers can have agreement to use any acknowledgement scheme like selective negative acknowledgement (SNACK), negative-acknowledgement (NAK or NACK) or [acknowledgement(ACK)](https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)) use in many protocols like TCP, .... So unlike IP, UDP, ... is not [blind transmission](https://en.wikipedia.org/wiki/Blind_transmission)

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language. We implement it on some language like [C](), [Go](https://github.com/GeniusesGroup/libgo/blob/master/srpc), [JavaScript](https://github.com/GeniusesGroup/libjs/blob/master/polyfills/http.js) and more in progress ...

## Inspired of
- [ICMP -Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
- [QUIC](https://en.wikipedia.org/wiki/QUIC) - [RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000)

## Position on Message Brokers
The standalone message broker — MQTT, AMQP, and kin deployed as a separate service — is an external protocol surface Memar does not adopt as a default, and the reason is arithmetic, not taste. The honest-delivery pattern the broker serves (at-least-once, exactly-once semantics, its QoS levels) requires the broker to persist messages to non-volatile storage before acknowledging them. An application that itself must durably record what it sends then pays for that persistence twice: once in the application's own storage, once in the broker's — plus the network hop between them — per message, at layers that did not need the duplication. At IoT volumes this cost dominates the system's storage budget; at any volume it buys a guarantee the application's own store could have provided directly.

Memar's stance: **the broker's mechanism belongs in a library inside the application's own architecture, not in a separate standalone service.** Where durable delivery is the requirement, the durable store is the application's own; the delivery machinery (the acknowledgement discipline this protocol already defines, persistent queues, retries initiated by whichever participant this framework's retry rules allow) wraps that store rather than shadowing it. This is the same judgment [Networking](./networking.md#memars-position-on-the-traditional-network-stack) records for protocol logic generally: middleware logic is application-relevant logic, and its placement is a decision to be made, not an OS-shaped default to be inherited.

Two further notes are attached to this position:

- The sync/async client models brokers offer are both cost-irrational in the same way: either the client's logic is structured around the broker's session (sync), or the broker is trusted to have persisted before the client continues (async) — losing data precisely when the acknowledgement meant nothing. Both models are artifacts of the broker being a separate process; a library-owned broker dissolves the trade-off by letting the application's own storage be the durability point.
- The producer-consumer independence principle ([Process → Events](../process.md#events)) is untouched by this position: making the broker mechanism a library does not couple producers to consumers — it only relocates who runs the machinery.

Open work on this protocol — the wire-level cancellation contract, and the wire-shape agreement this position's delivery machinery needs — is tracked in the paired [handoff](./sRPC.handoff.md).

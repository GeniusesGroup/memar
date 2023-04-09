# sRPC - Application Protocol
sRPC (Syllab Remote Procedure Call) is a RPC(remote procedure call) protocol. It is develope to use by [Chapar](./Chapar.md) and [GP](./Giti-Network.md) protocols, But it can also use to be a messaging protocol among with other protocols like IP, TCP, UDP, HTTP, ...

We combine OSI layer 4 to layer 6 requirements as Transport+Session+Presentation protocols to have one protocol and remove all overhead data.

## Goals
- Minimum overhead to find service from server services
- Minimum data exchange forces by protocol

## Not Goals
- Easy to understand by human

## Frames - Internal Services
Each packet can carry many frames until respect network MTU. All frames have fixed first field name `Type` with `signed 8bit` length that is same as [MediaTypeID](./media-type.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead. frame numbers will be the same as appear in below order e.g. PacketSequenceNumber=0, padding=1, ping=2, ...

Negative frame type reserved and use to extend types to int16 (or int64) length.

### Packet Sequence Number Frame
Incremental number use to detect failed packet, ... Use even number e.g. 0,2,4,6,... for client(who start connection) and Use odd number e.g. 1,3,5,7,... for server(who receive connection). Separation of the packet identifiers ensures that peer are able to send packets without the latency imposed by negotiating for an identifier.
```go
type PacketSequenceNumber struct {
    SequenceNumber uint64
}
```

### Padding Frame
```go
type Padding struct {
    Length   uint16
    Padding  []byte
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

## Special Signature Frame (MAC, Tag, ...)
This is special frame that don't need `Type` field and always appear in the end of a packet(or a frame). Due to carry on end of each packet(or frame) it must be in reverse to read its fields. Depend on crypto mode it use to authenticate data transmitted and check packet(or frame) healthy in any network hop, But usually just first router and receiver check packet(or frame) signature.
```go
type PacketSignature struct {
    Signature       []byte
    SignatureScheme uint16 // SignatureScheme identifies a signature algorithm supported by TLS. See RFC 8446, Section 4.2.3.
    Length          uint16 // including the header fields
}
```

## Frames Fields

### Length
- Length of whole frame exclude `Type` common filed.
- must respect data-link protocol due to not Fragmentation supported. Better not over of 8192 Byte(octets) or 8KB

### Padding
If block cipher use, add some random data to have fix size packet

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
- [QUIC](https://en.wikipedia.org/wiki/QUIC) - [RFC](https://datatracker.ietf.org/doc/html/rfc9000) 

# sRPC - Application Protocol
sRPC (Syllab Remote Procedure Call) is a RPC(remote procedure call) protocol. It is develope to use by [Chapar](./Chapar.md) and [GP](./Giti-Network.md) protocols, But it can also use to be a messaging protocol among with other protocols like IP, TCP, UDP, HTTP, ...

We combine OSI layer 4 to layer 6 requirements as Transport+Session+Presentation protocols to have one protocol and remove all overhead data.

## Goals
- Minimum overhead to find service from server services
- Minimum data exchange forces by protocol

## Not Goals
- Easy to understand by human

## Frames - Internal Services
Each packet can carry many frames until respect network MTU. All frames have fixed first field name `Type` with `8bit` length that is same as [ServiceID](./Service.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead. frame numbers will be the same as appear in below order e.g. padding=0, ping=1, ...

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
    ProtocolID     uint16
    ServiceID      uint64
    CompressTypeID uint64
    DataLength     uint64
}
```

### Close-Stream Frame
```go
type CloseStream struct {
}
```

### Data Frame
```go
type Data struct {
    Length   uint16
    StreamID uint32
    Offset   uint32
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

### Signature Frame
```go
type Signature struct {
	Length    uint16
	StreamID  uint32
	Signature []byte
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
- Read more about [ServiceID](./Service.md)
- Can use by other protocols e.g. http-uri: "/m?{{.ServiceID}}" that m use to be short and abbreviation for multiplexer(mux).

### Error ID
- Use to show if calling service occur an error.
- Read more about [ErrorID](./Error.md)
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

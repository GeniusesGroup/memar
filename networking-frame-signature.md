# Special Signature Frame (MAC, Tag, ...)
This is special frame that don't need `Type` field and always appear in the end of a packet(or a frame). Due to carry on end of each packet(or frame) it must be in reverse to read its fields. Depend on crypto mode it use to authenticate data transmitted and check packet(or frame) healthy in any network hop, But usually just first router and receiver check packet(or frame) signature.

```go
type PacketSignature struct {
    Signature       []byte
    SignatureScheme uint16 // SignatureScheme identifies a signature algorithm supported by TLS. See RFC 8446, Section 4.2.3.
    Length          uint16 // including the header fields
}
```

## Padding Frame
If block cipher use, add some random data to have fix size packet in random location of the frame.

```go
type Padding struct {
    Length   uint16
    Padding  []byte
}
```

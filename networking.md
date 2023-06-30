# Networking
All requirements in networking response with `frame` idea. Each network packet contains many frames in desire order that read by devices in a network to do some desire logic in each device, e.g. switching, routing, multiplexing, ...

## Packet
Strongly suggest respect OSI network model and order frames in any packet in OSI layers order. Strongly suggest **Frames** after layer 3 always encrypted.
A packet at least have two(always the special signature frame appear at the end) or more frames in [sRPC format](./sRPC.md)

## Frames
Frames indicate in each protocol RFC or in [sRPC Protocol](./sRPC.md).

### Fields
As describe in [sRPC](./sRPC.md) too, Each packet can carry many frames until respect network MTU. All frames have fixed first field name `FrameID` with `unsigned 8bit` length, that is same as [MediaTypeID](./media-type.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead.

```go
type Frames struct {
    FrameID byte
}
```

### Frames Number
frames number will be register here in this table and must be respect by all. Number greater than 240 (FrameID > 240) use for experimental protocols and SHOULD ignore by any device that don't want to process them.

| Num.  | Frame name   | Doc   |
| :---: | :---:        | :---: |
| 0     | Unset        | -------- |
| 1     | Asb          | [Protocol](./networking-osi_1-Asb.md) |
| 2     | Chapar       | [Protocol](./networking-osi_2-Chapar.md) |
| 3     | GP           | [Protocol](./networking-osi_3-Giti-Network.md) |
| 4     |              |  |
| 5     |              |  |
| 127   |              |  |
| 128   | Padding      | [Protocol](./networking-frame-signature.md) |
| 129   | PacketSequenceNumber | [Protocol](./sRPC.md) |
| 130   | Ping         | [Protocol](./sRPC.md) |

#### Suggested experimental protocols
Below frames can't use directly and must wrap inside a frame with `FrameID` in declared number. Some other can be find on [EtherType](https://en.wikipedia.org/wiki/EtherType).

| Num.  | Frame name   | Doc   |
| :---: | :---:        | :---: |
| 241   | ARP          | [ARP - Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) |
| 242   | VLANs        | [VLANs](https://en.wikipedia.org/wiki/IEEE_802.1Q) |
| 243   | IPV4         | [IPv4 - Internet Protocol v4](https://en.wikipedia.org/wiki/IPv4) |
| 244   | IPV6         | [IPv6 - Internet Protocol v6](https://en.wikipedia.org/wiki/IPv6) |
| 245   | NDP          | [NDP - Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) |
| 246   | NTP          | [NTP - Network_Time_Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol) |

### Methods
Due some frames can work without need to have `Length` field, instead All frames handler must provide `NextFrame() []byte` method.

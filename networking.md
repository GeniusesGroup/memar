# Networking
Networking is make connection between computer systems. It means we will need it almost in all computer parts e.g. two computer hardware connection, GPU to CPU network (by some protocols like PCIe, ...).

All requirements in networking response with `frame` idea. Each network packet contains many frames in desire order that read by devices in a network to do some desire logic in each device, e.g. switching, routing, multiplexing, ...

## Packet
Strongly suggest respect OSI network model and order frames in any packet in OSI layers order. Strongly suggest **Frames** after layer 3 always encrypted.
- A packet at least have two(always the special signature frame appear at the end) or more frames in [sRPC format](./sRPC.md)
- Packet size can be up to 8192 Byte or 8KB. Enough to stream 1.5Mbps video call in each 40ms frames (`1.5/8*1024/1000*40=7.68KB`).

## Frames
Frames indicate in each protocol RFC e.g. [GP](./networking-osi_3-Giti-Network.md), [sRPC Protocol](./sRPC.md), ...

### Fields
As describe in [sRPC](./sRPC.md) too, Each packet can carry many frames until respect network MTU. All frames have fixed first field name `FrameType` with `signed 8bit` length, that is same as [MediaTypeID](./media-type.md) but not use 64bit unsigned integer and standard here as a byte to minimize packet unnecessary overhead.

```go
type Frames struct {
    frameType byte
}
```

### Frames Number
frames number will be register here in this table and must be respect by all.
Some rules:
- Number greater than 100 (FrameType > 100) use for experimental protocols and SHOULD ignore by any device that don't want to process them.
- Signed bit use to extend one byte Frame Number to 8 byte signed (63 bit number range) and support more frame types. It will 

| Num.  |      Frame name      |                                    Doc                                    |
| :---: | :------------------: | :-----------------------------------------------------------------------: |
|   0   |        Unset         |                                 --------                                  |
|   1   |         Asb          |                   [Protocol](./networking-osi_1-Asb.md)                   |
|   2   |        Chapar        |                 [Protocol](./networking-osi_2-Chapar.md)                  |
|   3   |          GP          |              [Protocol](./networking-osi_3-Giti-Network.md)               |
|   4   |                      |                                                                           |
|   5   |                      |                                                                           |
|   6   |                      |                                                                           |
|  ...  |                      |                               [Protocol]()                                |
|  96   |       Padding        |                [Protocol](./networking-frame-signature.md)                |
|  97   |       Security       |                [Protocol](./networking-frame-signature.md)                |
|  98   | PacketSequenceNumber |                           [Protocol](./sRPC.md)                           |
|  99   |                      |                               [Protocol]()                                |
|  100  |                      |                          experimental protocols                           |
|  ...  |                      |                          experimental protocols                           |
|  128  |    Extended Frame    | Use to extend number to 63 bit range frame numbers as it is signed number |

### Suggested experimental protocols
A way to process all old protocols e.g. Ethernet, ATM, IPv4, IPv6,

#### Internet protocol suite
Suggest Internet protocol suite use `FrameType == 100` and a sub frame type to indicate many different protocols e.g. Ethernet, IP, TCP, UDP, ... .

- Ethernet protocol
It CAN support and carry many protocols with `EtherType` that is 2 octet number. Some other can be find on [EtherType wikipedia page](https://en.wikipedia.org/wiki/EtherType).

|  Num.  | Frame name |                                              Doc                                               |
| :----: | :--------: | :--------------------------------------------------------------------------------------------: |
| 0x0806 |    ARP     | [ARP - Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol) |
| 0x8100 |   VLANs    |                       [VLANs](https://en.wikipedia.org/wiki/IEEE_802.1Q)                       |
| 0x0800 |    IPV4    |               [IPv4 - Internet Protocol v4](https://en.wikipedia.org/wiki/IPv4)                |
| 0x86DD |    IPV6    |               [IPv6 - Internet Protocol v6](https://en.wikipedia.org/wiki/IPv6)                |

- NDP
[NDP - Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol) is base on `IPv6` protocol.

- NTP
[NTP - Network_Time_Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol) is base on `UDP` protocol.

### Methods
Due some frames can work without need to have `Length` field, instead All frames handler must provide `NextFrame() []byte` method.

## Other protocols
- https://enlightra.com/

# Chapar - Data Link Protocol
Chapar is introduced to improve [layer 2 of OSI](https://en.wikipedia.org/wiki/Data_link_layer) that can transmit frames at or near speed of the physical layer (Computing & Networking) limiting and not depend on any devices internal bus speed like RAM, CAM, ... due to it doesn't need any state manager in switching devices (intermediate nodes). It use and combine good specs of [datagrams](https://en.wikipedia.org/wiki/Datagram) and [virtual circuits](http://www.telecomabc.com/v/virtual-circuit.html) to make most efficient protocol.  
Chapar is a switching protocol that store switch state just in frames and just in two connected peer that can be treated as [stateless protocol](https://en.wikipedia.org/wiki/Stateless_protocol). Other protocols usually need to store some states in all hop switches devices (setup information mechanism) other than on frames and peers e.g. other protocols that use and store [MAC](https://en.wikipedia.org/wiki/MAC_address) in frames and each switching device in the network, that must translate to some data in each switch devices to switch frames.

For the full rationale behind these design choices — including comparison with Ethernet's state model and cost structure — see [related document](./chapar-vs-ethernet-rationale.md).

## Inform
Anywhere in this document talk about [Ethernet](https://en.wikipedia.org/wiki/Ethernet), means ethernet in [layer two](https://en.wikipedia.org/wiki/Ethernet_frame#Frame_%E2%80%93_data_link_layer) not including layer one. Ethernet in layer one has its frame header and dedicated specs that usually engineers mix ethernet for two layer almost because they use and think to TCP/IP model instead of OSI model.

Goals, explicit Non-Goals, and worked topology-capacity examples are recorded in [related document](./chapar-introduction-goals-and-topology.md) rather than here, to keep this document limited to wire format and normative behavior.

## Frame architecture
- Ports number can be mutable due to physical link limits. The endpoint must beware of this aspect.
- Each switch interface in any location of link can be wired or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bit   | Length(byte-Octet) | Data                          |
| :---: | :---:              | :---:                         |
| 0     | 1                  | FrameType                     |
| 8     | 1                  | Hop Count                     |
| 16    | 1                  | Next Hop                      |
| 24    | 1                  | First Hop Port Number         |
| ...   | ~                  | x Hop Port Number (Optional)  |

- FrameType: Indicate by [networking rules](./networking.md).
- [Hop Count](https://en.wikipedia.org/wiki/Hop_(networking)#Hop_count): The hop count refers to the number of intermediate network devices through which data must pass between source and destination, and also indicate frame length.
- [Next Hop](https://en.wikipedia.org/wiki/Hop_(networking)#Next_hop): Indicate hop number that frame must send on indicate port by that hop.
- First Hop Port Number: Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- x Hop Port Number: Up to 255 hop port number can be in a frame.

## Frame Types
Chapar support **UniCast** and **BroadCast** frame and not support **AnyCast** or **MultiCast**. We strongly suggest use broadcast frames just in network discoverable mechanism like find GP network coordinators. Also to broadcast emergency messages service, not to use to broadcast video channels, ...

Chapar itself carries a Broadcast frame without interpreting why it was sent — the actual Discovery or Emergency semantics live in an [sRPC](./sRPC.md) service call (identified by `ServiceID`) elsewhere in the same packet, not a dedicated FrameType. See [related document](./chapar-broadcast-scope-and-known-risks.md) for why Broadcast is restricted this way.

## Discovery
A device announces itself with a one-way Broadcast frame (`HopCount == 0x00`) — a fire-and-forget [sRPC](./sRPC.md) call with no defined response, the same whether it's a first announcement or a routine re-announcement on a self-configured interval. As it floods hop by hop, the existing port-rewrite [Rule](#rules) causes the frame to accumulate its own reverse path.

Chapar has no persistent, stable device address (see [related document](./chapar-vs-ethernet-rationale.md)); where an upper layer needs to identify a sender, this accumulated reverse path is what serves that role — ephemeral, and relative to whoever holds it, not a portable identifier (see [related document](./chapar-discovery-and-path-establishment.md)).

Any node may react (optional); ChaparKhane always must. Reacting means independently initiating a fresh Unicast frame to the new device using the accumulated path, reversed — not a coupled RPC response. Re-establishing a path after a topology change likewise relies on an ordinary upper-layer timeout triggering a fresh announcement, not a dedicated Chapar mechanism. See [related document](./chapar-discovery-and-path-establishment.md) for the full mechanism, device-to-device path composition, and open questions — Discovery is also likely not the only service built this way; see that document for why the full space is left to ChaparKhane's own service design.

## Switching

### Blocking Switch
Transmitting will block sender until frame transmitted successfully. Sender can be sure frame transmitted.

### Non blocking Switch
Transmitting will not block caller to be non blocking and queue frames for congestion situations.
A situation might be occur that a port available when a frame queued but when the time to send is come, the port broken and sender don't know about this.

## Rules
- HopCount encoding: `0x00` is reserved exclusively as the Broadcast sentinel, carrying the full 255-slot hop-port space with zero-length data in each slot. Values `0x01`–`0xFF` indicate a Unicast frame with 1 to 255 intermediate hops respectively — since a Unicast frame must have at least one hop, `0x00` would otherwise be unused by Unicast, so it is repurposed for Broadcast instead of adding a dedicated field.
- BroadCast frame must have all hop port number space with 0-byte data in the header, otherwise other frames in the packet manipulates(rewrite) by switches devices.
- When two peer connect by two different port number, one of them must be as switching adaptor. That means **usually higher hop** must add virtual switch hop to switching road. It will add one more hop port number in each chapar frame.
- In each hop, the Switch device must rewrite the received port number on the frame. The reasons are:
    - BroadcastFrame: To improve performance, the previous switch just sends a frame without declaring the next port.
    - UnicastFrame: To be sure receive port is the same with declaration one in a frame.
    - Rule&Security: To be sure the physical network port is the same on the sender and receiver switch.

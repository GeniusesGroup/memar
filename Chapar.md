# Chapar - Data Link Protocol
Chapar is a switching protocol that store switch state in frames as [stateless protocol](https://en.wikipedia.org/wiki/Stateless_protocol) instead of devices unlike other protocols that use and store [MAC](https://en.wikipedia.org/wiki/MAC_address) in frames and each switching device in the network that must translate to some data in each switch devices like [Ethernet](https://en.wikipedia.org/wiki/Ethernet) in [layer two]((https://en.wikipedia.org/wiki/Ethernet_frame#Frame_%E2%80%93_data_link_layer)) to switch frames in the real [stateless manner](https://en.wikipedia.org/wiki/Connectionless_communication). Chapar is introduced to improve [layer 2 of OSI](https://en.wikipedia.org/wiki/Data_link_layer) that can transmit frames in almost speed of the physical layer (Computing & Networking) limiting.

## Why (Ethernet disadvantages)
- High price & have limits to make layer 2 networks without getting help from layer 3. The best switch has up to 512000 CAM record limit for query MAC to the port.
- High power usage and limit speed in CAM tables(CAM, TACM, ...).
- Close source complicated hardware and switching algorithms.

## Goals
- **Simple** networking by eliminate complexity
- **Decrease** switch products & network **price**
- **Improve** network **bandwidth** & **latency** without increase networking price
- **Make a big layer 2** network approximately 255^256(2^2048) node if respect port numbers are same on both peer or approximately 255^128(2^1024) node if you don't want to respect this hard work **without need upper layer** and of course switches devices must count as node.
- **Make networking greener** by reduce direct(switch devices) and indirect(cooling) power usage

## Non Goals (Non Considering)
- **Security**: Layer 2 is more related to physical layer networks that need physical security to eliminate device access from the network. Any undesired connectivity on a layer 2 network gets physical ports or some frequency on layer 1. So the security of a network must handle in physical with help from ChaparKhane as network coordinator.
- **Error detection** requirement is more related to the physical link (OSI layer 1) to check the healthy of transmitted data between endpoints. Maybe a layer one protocol can guarantee to transmit data without the need to have error detection. And Also related to the upper layer than the Data-Link layer to check the health of data in the destination.
- **Fragmentation**: MTU is not enough to send all types of data on a network, but layer two is not where it must handle.
- **Switching loop**: Due to the suggested structure that a frame can switch just up to 255 hop, so this problem does not exist in Chapar.
- **Backup links** or have more than one physical link between two nodes to providing fault tolerance if an active link fails not to consider or handle by Chapar switches and Endpoints must handle multiple paths to each other with help of network coordinator if exist. We have good reason that layer 2 is not good for this requirements is that this logic need state and why we store states in all path.
- **Bandwidth management** or [Quality of service](https://en.wikipedia.org/wiki/Quality_of_service) is a complicated feature that we decide to handle on layer one and layer three. It is easy to control endpoint devices layer one bandwidth on the connection point to help [ChaparKhane](./ChaparKhane.md) to coordinate network better, but in layer one, you can't distinguish between inbound and outbound traffics.

## Still considering
- **Frames congestion** on any ports force still use cache on ports interfaces that can drop up to 50% efficiency. Suggest use computer hardware studies e.g. PCI-Express(PCIe), ...  to handle this consideration in best effort.

## Frame architecture
- This Frame structure will transport by physical layer so it is payload of desire frame and that frame have its header and structure like StartDelimiter, EndDelimiter, CheckSequence, ...
- Ports number can be mutable due to physical link limits. The endpoint must beware of this aspect.
- Each switch interface in any location of link can be wired or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bit   | Length(byte-Octet) | Data                          |
| :---: | :---:              | :---:                         |
| 0     | 1                  | Next Hop                      |
| 8     | 1                  | Hop Count                     |
| 16    | 1                  | Next Header                   |
| 24    | 1                  | First Hop Port Number         |
| ...   | ~                  | x Hop Port Number (Optional)  |
| ...   | ~                  | Payload                       |

- [Next Hop](https://en.wikipedia.org/wiki/Hop_(networking)#Next_hop): Indicate hop number that frame must send on indicate port by that hop.
- [Hop Count](https://en.wikipedia.org/wiki/Hop_(networking)#Hop_count): The hop count refers to the number of intermediate network devices through which data must pass between source and destination and also indicate payload location.
- Next Header: Indicate upper layer protocol equal EtherType.
- First Hop Port Number: Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- x Hop Port Number: Up to 255 hop port number can be in a frame.
- Payload: Can be any upper-layer packet data that type indicates by the next header.

## Frame Types
Chapar support **UniCast** and **BroadCast** frame and not support **MultiCast**

## Frame Switch

### Blocking
transmitting will block sender until frame transmitted successfully. Sender can be sure frame transmitted.

### Non blocking
transmitting will not block caller to be non blocking and queue frames for congestion situations.
A situation might be occur that a port available when a frame queued but when the time to send is come, the port broken and sender don't know about this.

## Rules
- Frame size can be up to 8192 Byte or 8KB. Enough to stream 1.5Mbps video call in each 40ms frames (1.5/8*1024/1000*40=7.68KB).
- Due to the frame must have at least one hop, Use unused HopCount==0 for broadCast frames to all ports. So both HopCount==0x00 & HopCount==0xff have 255 hop port number space in frame header.
- BroadCast frame must have all hop port number space with 0-byte data in the header, otherwise frame payload rewrite by switches devices.
- In each hop, the Switch device must rewrite the received port number on the frame. The reasons are:
    - BroadcastFrame: To improve performance, the previous switch just sends a frame without declaring the next port.
    - UnicastFrame: To be sure receive port is the same with declaration one in a frame.
    - Rule&Security: To be sure the physical network port is the same on the sender and receiver switch.

## Next-Header Standard Supported Protocols
- 0 : [sRPC - sRPC Protocol](./sRPC.md)
- 1 : [GP - Giti Protocol](./Giti-Network.md)
- 2 : [IPv4 - Internet Protocol v4](https://en.wikipedia.org/wiki/IPv4)
- 3 : [IPv6 - Internet Protocol v6](https://en.wikipedia.org/wiki/IPv6)
- 4 : [ICMP -Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
- 5 : [NTP - Network_Time_Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol)

### Non supported [EtherType](https://en.wikipedia.org/wiki/EtherType)
- [ARP - Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
- [NDP - Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol)
- [VLANs](https://en.wikipedia.org/wiki/IEEE_802.1Q)

## WireLess
Like other wireless technology, We must provide some dedicate channel:
- Broadcast control channel (BCCH) to manage broadcasting for all user equipment
- Paging control channel (PCCH) to manage paging messages --- why not page device by DTCH?????
- Common control channel (CCCH) and dedicated control channel (DCCH) for common messages for all user equipment in the same cell
- Dedicated traffic channel (DTCH) to send data to the specific user equipment in a cell

Each Chapar wireless switch device handles two hops of the frame instead of regular one hop in each switching hop. It means each wireless hot-spot can serve more than 2^16(65536) devices.
Use channel 49 (694-790 MHz) in [UHF](https://en.wikipedia.org/wiki/Ultra_high_frequency) frequency range to broadcast available 

## Inspired of
- https://guifi.net/
- https://en.wikipedia.org/wiki/Telephone_exchange
- https://en.wikipedia.org/wiki/Fast_packet_switching
- [SDU](https://en.wikipedia.org/wiki/Service_data_unit) vs [PDU](https://en.wikipedia.org/wiki/Protocol_data_unit)
- [ETSI](https://www.etsi.org/) standards
- https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode
- (IEEE 802)[https://www.ieee802.org/]

## Articles
- https://www.dropbox.com/sh/51l4x1p2e8lub5x/AABVgFyJ0fuia8QZt7SEZgBWa?dl=0

## Chapar word meaning
["The Chapar"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers who were provided with fresh supplies and horses at each station along the way, allowing them to quickly complete their way without having to procure supplies on their own or wait for their horse to rest.

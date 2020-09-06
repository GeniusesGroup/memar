# Chapar - Data Link Protocol
Chapar is a switching protocol that store switch state in frames as [stateless protocol](https://en.wikipedia.org/wiki/Stateless_protocol) instead of devices unlike other protocols that use and store [MAC](https://en.wikipedia.org/wiki/MAC_address) in frames that must translate to some data in each switch devices like [Ethernet](https://en.wikipedia.org/wiki/Ethernet) in [layer two]((https://en.wikipedia.org/wiki/Ethernet_frame#Frame_%E2%80%93_data_link_layer)) to switch frames in the real [stateless manner](https://en.wikipedia.org/wiki/Connectionless_communication)! Chapar is introduced to improve [layer 2 of OSI](https://en.wikipedia.org/wiki/Data_link_layer) that can transmit frames in almost speed of physical layer (Computing & Networking) limiting!

## Why (Ethernet disadvantages)
- High price & have limit to make layer 2 network without get help from layer 3! The best switch have up to 512000 CAM record limit for query MAC to the port!
- High power usage and limit speed in CAM tables(CAM, TACM, ...)!
- Close source complicated hardware and switching algorithms!

## Goals
- **Decrease** switch products & network **price**
- **Improve** network **bandwidth** & **latency** without increase networking price!
- **Make big layer 2** network approximately 256^128(2^1024) node **without need upper layer**!!
- **Make networking greener** by reduce direct(switch devices) and indirect(cooling) power usage!
- **Bandwidth management** or [Quality of service](https://en.wikipedia.org/wiki/Quality_of_service) is complicated feature that can handle on layer one and layer three too! But it is easy to control endpoint devices bandwidth on the connection point to help [ChaparKhane](./ChaparKhane.Md) to coordinate network better, but in this layer you can't distinguish between inbound and outbound traffics!

## Not Goals or Considering
- **Security**: Layer 2 is more related to physical layer network that need physical security to eliminate access a device from desire network! So security of a network must handle in upper layer than layer 2.
- **Error detection**: Due to simplicity of protocol and quality of todays hardwares it is better to check healthy of data just in destination not in every switch device!
- **Fragmentation**: MTU is not enough to send all type of data on a network, but layer two is not where it must handle!
- **Switching loop**: Due to suggested structure that a frame can switch just up to 255 hop, so this problem is not exist in Chapar.
- **Backup links** or have more than one physical link between two node to providing fault tolerance if an active link fails not consider or handle by Chapar switches and Endpoints must handle multiple path to each other with help of network coordinator if exist!

## Still considering
- **Frames congestion** on any ports force still use cache on ports interfaces that can drop up to 50% efficiency!

## Frame architecture
- StartDelimiter, EndDelimiter & CheckSequence may add to this structure due to physical layer rules!
- Ports number can be mutable due to physical links limits. Endpoint must beware of this aspect!
- Each switch interface in any location of link can be wire or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bits  | data type                     |
| :---: | :---:                         |
| 0     | Next Hop                      |
| 8     | Hop Count                     |
| 16    | Next Header                   |
| 24    | First Hop Port Number         |
| ...   | x Hop Port Number (Optional)  |
| ...   | Payload                       |

- [Next Hop](https://en.wikipedia.org/wiki/Hop_(networking)#Next_hop) : Indicate hop number that frame must send on indicate port by that hop!
- [Hop Count](https://en.wikipedia.org/wiki/Hop_(networking)#Hop_count) : The hop count refers to the number of intermediate network devices through which data must pass between source and destination and also indicate payload location!
- Next Header : Indicate upper layer protocol equal EtherType!
- First Hop Port Number : Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- x Hop Port Number : Up to 255 hop port number can be in a frame!
- Payload : Can be any upper layer packet data that type indicate by next header!

## Frame Types
Chapar support **UniCast** and **BroadCast** frame and not support **MultiCast**!

## Rules
- Frame size can be up to 8192 Byte or 8KB. Enough to stream 1.5Mbps video call in each 40ms frames (1.5/8*1024/1000*40=7.68KB).
- Due to frame must have at least one hop, Use unused HopCount==0 for broadCast frames to all ports! So both HopCount==0x00 & HopCount==0xff have 255 hop port number space in frame header!
- BroadCast frame must have all hop port number space with 0 byte data in header otherwise frame payload rewrite by switches devices!
- In each hop, Switch must rewrite received port number on the frame! The reasons are:
    - BroadcastFrame : To improve performance, previous switch just send frame without declare next port!
    - UnicastFrame : To be sure receive port is same with declaration one in frame!
    - Rule&Security : To be sure physical network port is same on sender and receiver switch!

## Next-Header Standard Supported Protocols
- 0 : [sRPC - sRPC Protocol](./sRPC.md)
- 1 : [GP - Giti Protocol](./GP.md)
- 2 : [IPv4 - Internet Protocol v4](https://en.wikipedia.org/wiki/IPv4)
- 3 : [IPv6 - Internet Protocol v6](https://en.wikipedia.org/wiki/IPv6)
- 4 : [ICMP -Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
- 5 : [NTP - Network_Time_Protocol](https://en.wikipedia.org/wiki/Network_Time_Protocol)

### Non supported [EtherType](https://en.wikipedia.org/wiki/EtherType)
- [ARP - Address Resolution Protocol](https://en.wikipedia.org/wiki/Address_Resolution_Protocol)
- [NDP - Neighbor Discovery Protocol](https://en.wikipedia.org/wiki/Neighbor_Discovery_Protocol)
- [VLANs](https://en.wikipedia.org/wiki/IEEE_802.1Q)

## Inspired of
- https://guifi.net/
- https://en.wikipedia.org/wiki/Telephone_exchange
- https://en.wikipedia.org/wiki/Fast_packet_switching

## Chapar word meaning
["The Chapars"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers who were provided with fresh supplies and horses at each station along the way, allowing them to quickly complete their way without having to procure supplies on their own or wait for their horse to rest.

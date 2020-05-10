# Chapar - Data Link Protocol
A real stateless switching protocol! This protocol can transmit frames in almost speed of physical layer limiting! It is all about improve [layer 2 of OSI](https://en.wikipedia.org/wiki/Data_link_layer)! The introduced [switch design](https://en.wikipedia.org/wiki/Stateless_protocol) isn't like Ethernet switch that must store MAC address state in each switch and will switch frames in [stateless manner](https://en.wikipedia.org/wiki/Connectionless_communication).

## Ethernet disadvantages
- High price & have limit to make layer 2 network without get help from layer 3! The best switch have up to 512000 TCAM record limit for query MAC to the port!
- High power usage and limit speed in TCAM tables!
- Close source complicated hardware and switching algorithms!

## Goals
- Decrease switch products & network price
- Improve network bandwidth & latency without increase networking price!
- Make big layer 2 network as 256^256(2^2048) node without need upper layer!!
- Make networking greener by reduce direct(switch devices) and indirect(cooling) power usage!

## Not Goals
- Security : Layer 2 is more related to physical layer network that need physical security to eliminate access a device from desire network! So security of a network must handle in upper layer than layer 2.
- Error detection : Due to simplicity of protocol and quality of todays hardwares it is better to check healthy of data just in destination not in every switch device!

## Still considering
- Still need cache on ports! Frames congestion that force use cache on ports interfaces can drop up to 50% efficiency!

## Packet architecture
- StartDelimiter, EndDelimiter & CheckSequence may add to this structure due to physical layer rules!
- Ports number can be mutable due to physical links limits. Endpoint must beware of this aspect!
- Each switch interface in any location of link can be wire or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bits  | data type                 |
| :---: | :---:                     |
| 0     | Next Hop                  |
| 8     | Total Hop                 |
| 16    | Next Header               |
| 24    | Switch 1 PortNum          |
| ...   | Switch x PortNum(Optional)|
| ...   | Payload                   |

- Next Hop : Indicate switch port number use on next switch device!
- Total Hop : Total hop numbers and also indicate payload location!
- Next Header : Indicate upper layer protocol equal EtherType!
- Switch 1 PortNum : Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- Other Ports : Up to 256 switch port number can be here in frame!
- Payload : Up to 8192 Byte or 8KB. Enough to stream 1.5Mbps video call in each 40ms frames (1.5/8*1024/1000*40=7.68KB)

## Inspired of
- https://guifi.net/
- https://en.wikipedia.org/wiki/Telephone_exchange

## Chapar word meaning
["The Chapars"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers who were provided with fresh supplies and horses at each station along the way, allowing them to quickly complete their way without having to procure supplies on their own or wait for their horse to rest.

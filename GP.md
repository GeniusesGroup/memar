# GP - Giti (Network) Protocol
We combine OSI layer 3 to layer 6 requirements as Network + Transport + Session + Presentation protocols to have one protocol and remove all overhead data. This protocol needs in the IoE era (Internet of Everything) for connecting things, people, data, ...!
It has some differences in internal service call, security, pipelining, multiplexing, ... . It will introduce huge advantage and improve app network performance! We will implement this protocol in [PersiaOS](./PersiaOS.md).

## IP disadvantages
- IP Routers can just be gateway!
- Registering system is centralized and manual human base!
- IP leases fee is high!
- IP addresses can't (or very hard to) register by end user and usually register by ISP!
- IP addresses can't prove their ownership to use in authentication process due to above problem!
- IP address can easily spoofing! Spoofing can be used as part of a DoS attack and Can't determine source of attack!

## Goals
- Decentralized and automatic process to register routers in any layer!
- Free, automate and floating to lease new GP address!
- Make GP routers as coordinator in network along side be a gateway!

## Still considering
- How and when to allow new XP register in XP networks!

## Packet Architecture
| bits          | Length(byte-Octet)| data              |
| :---:         | :---:             | :---:             |
| 1 ... 128     | 16                | Destination GP    |
| 129 ... 256   | 16                | Source GP         |
| 257 ... 272   | 2                 | Payload Length    |
| 273 ... 304   | 4                 | Stream ID         |
| 305 ... 336   | 4                 | Packet ID         |
| 337 ... __    | __                | Payload           |
| __            | __                | Padding           |
| __            | __                | Checksum          |

- **Payload Length** : Always encrypted and must respect data-link protocol due to not Fragmentation supported. Better not over of 8192 Byte(octets) or 8KB! Not include headers, padding or checksum!!
- **Stream ID** : Always encrypted. Use even number for client(who start connection) to start a stream e.g. 0,2,4,6,8,10,... . Use odd number for server(who receive connection) to start a stream e.g. 1,3,5,7,9,11,... 
- **Packet ID** : Always encrypted. Max 4.72TB can transmit in single stream with 1.18KB payload Length as limit to 1.5KB of ethernet frames! 
- **Payload** : Always encrypted, Payload can be any application protocol e.g. HTTP, sRPC, ... . It must store in order by PacketID to make whole a stream data
- **Padding** : If block cipher use, add some random data to have fix size packet!
- **Checksum** : Depend on mode it use to authenticate data transmitted and check packet healthy!

### Extended header
It introduces an internal service call instead of data in each header!

### Versioning
Unlike existing Internet Protocol as IP, we don't offer any versioning for this protocol as we believe if we need fundamentally change any part of a protocol after the official release, we will already make new protocol! So we respect data link layers protocols like Ethernet and use their solution like [Ethertype](https://en.wikipedia.org/wiki/Ethertype) in [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header and don't reinvent other solution!

## GP Address
GP address lengths is 128 bit(16 byte) that contain 32+32+32+16+16bit as XPs + GP Routers + OSs + Apps + Protocols!
This protocol unlike IPv6 regard each bit of a GP address. We suggest use below rules but just XP part must always respect these rules and each XP network can have own rules about routing protocol in their networks!
- **XP(Exchange Points)**: *0 to 31 bit* >> *32bit length* >> Each civilization like exiting country can tell others and get a 4 byte unique immutable identifier. We know some considering exist and we must have some rules to allow new members in XPs!
- **Routers**: *32 to 63 bit* >> *32bit length* >> Each XP must delegate its range to some routers to do routing for improve performance & consistency of its own network. So each Router always have 4 byte unique mutable identifier.
- **Users**: *64 to 96 bit* >> *32bit length* >> Each user on each device can get 4 byte unique mutable identifier from router. This range usually get by OS and route them to register app by user in OS. So an OS can host one or more users!
- **Apps**: *97 to 112 bit* >> *16bit length* >> Each user app can get 2 byte unique mutable identifier from OS. Same app but for different user always get dedicate unique range.
- **Protocol**: *113 to 128 bit* >> *16bit length* >> Each App have 2 byte address range that usually use to detect payload data structure some thing like TCP||UDP port number purpose!

## Routing Architecture

### Mobile GP
The [Mobile GP](https://en.wikipedia.org/wiki/Mobile_IP) allows for location-independent routing of the GP packet on the Internet! We don't have rules for mobility implementation in this spec! You can achieve mobility just by have proper topology in your XP and data link layer!

### Quality of Service
It must be handled in routers, not protocol packet!

### Local Network
When no GP router exists in a network, Nodes can set the first 64bit of GP to zero and broadcast their-selfs to each other!

### Multi-cast & Any-cast
Due to the nature of this spec that must be decentralized, and we believe this type of requirement must handle at the app layer to protect user privacy, So we don't offer any way to multi-cast or any-cast a packet in Giti networks!

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/GP), [JavaScript]() and more in progress ...

## Inspired of
- [QUIC](https://en.wikipedia.org/wiki/QUIC)
- [IPv6](https://en.wikipedia.org/wiki/IPv6)
- https://www.semanticscholar.org/paper/Blockchain-models-for-universal-connectivity-Navarro-Castro/788b7a634b369d98e72ed37c5fdf71f7fd62ef0b
- https://pdfs.semanticscholar.org/788b/7a634b369d98e72ed37c5fdf71f7fd62ef0b.pdf?_ga=2.260489549.1562006812.1569054619-1995410782.1569054619

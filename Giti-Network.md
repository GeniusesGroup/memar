# GP - Giti Network Protocol
We combine OSI layer 3 to layer 6 requirements as Network + Transport + Session + Presentation protocols to have one protocol and remove all overhead data. This protocol needs in the IoE era (Internet of Everything) for connecting things, people, data, ...!
It has some differences in internal service call, security, pipelining, multiplexing, ... . It will introduce huge advantage and improve app network performance! We will implement this protocol in [PersiaOS](./PersiaOS.md).

## IP disadvantages
- IP Routers can just be gateway!
- Registering system is centralized and manual human base!
- IP leases fee is high!
- IP addresses can't (or very hard to) register by end user and usually register by ISPs!
- IP addresses can't prove their ownership to use in authentication process due to above problem!
- IP address can easily spoofing! Spoofing can be used as part of a DoS attack and Can't determine source of attack!

## Goals
- Decentralized and automatic process to register routers in any layer!
- Free, automate and floating to lease new GP address!
- Make GP routers as coordinator in network along side be a gateway!

## Packet Architecture
| bit     | Length(byte-Octet)| Data                  |
| :---:   | :---:             | :---:                 |
| 0       | 16                | Destination GP        |
| 128     | 16                | Source GP             |
| 256     | 2                 | Payload Length        |
| 272     | 2                 | Stream ID             |
| 288     | 2                 | Packet ID             |
| 304     | ~                 | Payload               |
| __      | ~                 | Padding  (optional)   |
| __      | ~                 | Signature (Checksum)  |

- **Payload Length** : Always encrypted and must respect data-link protocol due to not Fragmentation supported. Better not over of 8192 Byte(octets) or 8KB! Not include headers, padding or checksum!!
- **Stream ID** : Always encrypted. Use even number for client(who start connection) to start a stream e.g. 0,2,4,6,... . Use odd number for server(who receive connection) to start a stream e.g. 1,3,5,7,... . Separation of the stream identifiers ensures that client and server are able to open streams without the latency imposed by negotiating for an identifier.
- **Packet ID** : Always encrypted. Max 4.72TB can transmit in single stream with 1.18KB payload Length as limit to 1.5KB of ethernet frames! 
- **Payload** : Always encrypted, Payload can be any application protocol e.g. HTTP, sRPC, ... . It must store in order by PacketID to make whole a stream data
- **Padding** : If block cipher use, add some random data to have fix size packet!
- **Signature** : or Checksum, MAC, Tag, ... Depend on mode it use to authenticate data transmitted and check packet healthy!

### Extended header
It introduces an internal service call instead of data in each header!

### Versioning
Unlike existing Internet Protocol as IP, we don't offer any versioning for this protocol as we believe if we need fundamentally change any part of a protocol after the official release, we will already make new protocol! So we respect data link layers protocols like Ethernet and use their solution like [Ethertype](https://en.wikipedia.org/wiki/Ethertype) in [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header and don't reinvent other solution!

## GP Address
| bit    | Length(byte-Octet)| Data            |
| :---:  | :---:             | :---:           |
| 0      | 2                 | Planet ID       |
| 16     | 4                 | Society ID      |
| 48     | 4                 | Router ID       |
| 80     | 4                 | User ID         |
| 112    | 2                 | App ID          |

GP address lengths is 128 bit(16 byte) as below describe! This protocol unlike IPv6 regard each bit of a GP address. We suggest use below rules in all levels and layers, But just PlanetID & SocietyID part must always respect suggested structure and each society network can have own rules about other routing part of protocol in their networks! **All IDs are temp IDs** and each Society, Router(thing), User & App actually own 32byte unique identifier!
- **Planet ID**: Each planet in universe get a 2 byte unique immutable identifier until exist!
- **Society ID**: Each society civilization like exiting country can tell others and get a 4 byte unique immutable identifier until exist.
- **Router ID**: Each society must delegate its range to some routers to do routing for improve performance & consistency of its own network. So each Router always have 4 byte unique mutable identifier until exist.
- **User ID**: Each user on each device get unique mutable identifier from router. This ID usually get by OS and route them to register app by user in OS. So an OS can host one or more users until exist!
- **App ID**: Each user app get unique mutable identifier from OS. Same app but for different user always get dedicate unique ID until exist.

## Routing Architecture

### Mobile GP
The [Mobile GP](https://en.wikipedia.org/wiki/Mobile_IP) allows for location-independent routing of the GP packet on the Internet! We don't have rules for mobility implementation in this spec! You can achieve mobility just by have proper topology in your society network and data link layer!

### Quality of Service
It must be handled in routers, not protocol packet!

### Local Network
When no GP router exists in a network, Nodes can set the first 64bit of GP to zero and broadcast their-selfs to each other!

### Multi-cast & Any-cast
Due to the nature of this spec that must be decentralized, and we believe this type of requirement must handle at the app layer to protect user privacy, So we don't offer any way to multi-cast or any-cast a packet in Giti networks!

### ProtocolID usage
Suggest to indicate protocolID in making each stream process. Also suggest to use even ProtocolID as port number to listen||receive||response||server and odd numbers for send||request||client.

### Acknowledgement Scheme
Giti network use negative-acknowledgement (NAK or NACK) instead of [acknowledgement(ACK)](https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)) use in many protocols like TCP, ...! So unlike IP, UDP, ... is not [blind transmission](https://en.wikipedia.org/wiki/Blind_transmission)
selective negative acknowledgement (SNACK)

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/SabzCity/libgo/blob/master/GP), [JavaScript]() and more in progress ...

## Inspired of
- [QUIC](https://en.wikipedia.org/wiki/QUIC) - [RFC](https://tools.ietf.org/html/draft-ietf-quic-transport-31) 
- [HTTP2]() - [RFC](https://tools.ietf.org/html/rfc7540)
- [IPv6](https://en.wikipedia.org/wiki/IPv6) - [RFC]()
- [Blockchain models for universal connectivity](https://www.semanticscholar.org/paper/Blockchain-models-for-universal-connectivity-Navarro-Castro/788b7a634b369d98e72ed37c5fdf71f7fd62ef0b) - [PDF](https://pdfs.semanticscholar.org/788b/7a634b369d98e72ed37c5fdf71f7fd62ef0b.pdf?_ga=2.260489549.1562006812.1569054619-1995410782.1569054619)

## Articles
- https://datatracker.ietf.org/doc/html/rfc1106

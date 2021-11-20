# GP - Giti Network Protocol
We combine OSI layer 3 to layer 6 requirements as Network + Transport + Session + Presentation protocols to have one protocol and remove all overhead data. This protocol needs in the IoE era (Internet of Everything) for connecting apps to apps as the goal of computer networks.
It has some differences in internal service call, security, pipelining, multiplexing, ... . It will introduce huge advantage and improve app network performance! We will implement this protocol in [PersiaOS](./PersiaOS.md).

## IP disadvantages
- IP Routers can just be gateway or can't be as network coordinator
- Registering system is centralized and manual human base
- IP leases fee is high
- IP addresses can't (or very hard to) register by end user and usually register by ISPs
- IP addresses can't prove their ownership to use in authentication process due to above problem
- IP address can easily spoofing! Spoofing can be used as part of a DoS attack and Can't determine source of attack

## Goals
- Decentralized and automatic process to register routers in any layer
- Free, automate and floating to lease new GP address
- Make GP routers as coordinator in network along side be a gateway

## Packet Architecture
| bit     | Length(byte-Octet)| Data                  |
| :---:   | :---:             | :---:                 |
| 0       | 16                | Destination GP        |
| 128     | 16                | Source GP             |
| 256     | 8                 | Packet Number         |
| 320     | 4                 | Frames                |
| ~       | ~                 | Signature             |

- **Packet Number** : Always encrypted. Incremental number use to detect failed packet, ... Use even number e.g. 0,2,4,6,... for client(who start connection) and Use odd number e.g. 1,3,5,7,... for server(who receive connection). Separation of the packet identifiers ensures that peer are able to send packets without the latency imposed by negotiating for an identifier.
- **Frames** : Always encrypted. one or more frame in [sRPC format](./sRPC.md)
- **Signature** : (or Checksum, MAC, Tag, ...) depend on crypto mode it use to authenticate data transmitted and check packet healthy in any network hop, But usually just first router and receiver check packet signature.

### Extended header
It introduces an internal frames to be service call instead of data in the header!

### Versioning
Unlike existing Internet Protocol as IP, GP don't offer any versioning for the protocol as we believe if we need fundamentally change any part of a protocol after the official release, we will already make new protocol! So we respect data link layers protocols like Ethernet and use their solution like [Ethertype](https://en.wikipedia.org/wiki/Ethertype) in [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header and don't reinvent other solution!

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
- **Router ID**: Each society must delegate its range to some routers to do routing for improve performance & consistency of its own network. So each Router always have 4 byte unique mutable identifier until exist. Usually each organization that claim a land (physical location) like complex building own one router ID.
- **User ID**: Each user on each device get unique mutable identifier from router. This ID get by OS and route them to register app by user in OS. So an OS can host one or more users until exist.
- **App ID**: Each app get unique mutable identifier from OS. It means same app but for different user has same ID.

### Compare with IPv6 addr
IPv6 and GP addresses are interchangeable, e.g. [Persia Society](persia.giti) register its block address range by [RIPE NCC](https://www.ripe.net/publications/docs/ripe-744).

- **Routing Prefix** with 48bit length has very common with GP addr. Same as IPv6 first 48bit of addr that is site prefix (global unicast address) in GP addr we have 48bit (PlanetID+SocietyID) to route packets to any global society.
- **SubNet ID** with 16bit length can be same in some way to RouterID but with 32bit length
- **Interface ID** with 64bit length not has any common with GP addr. Unlike IPv6 that has no good rule for 64bit end of addr and suggest use of [EUI-64](https://en.wikipedia.org/wiki/Organizationally_unique_identifier#64-bit_extended_unique_identifier_(EUI-64)), GP suggest (strongly advice) a better rule for its 48bit in end of addr.

Some Other IPv6 addr renumbering suggestion:
- **Type** with 3bit length
- **Registry ID** with 5bit length can be same in some way to PlanetID
- **Provider ID** with 16bit length as Internet access provider can be same in some way to SocietyID
- **Subscriber ID** with 24bit length has no any common with GP addr
- **SubNet ID** with 32bit length can be same in some way to RouterID
- **Interface ID** with 48bit length has no any common with GP addr

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
It is so simple protocol that can easily encode and decode in any programming language! We implement it on some language like [C](), [Go](https://github.com/GeniusesGroup/libgo/blob/master/GP), [JavaScript]() and more in progress ...

## Inspired of
- [QUIC](https://en.wikipedia.org/wiki/QUIC) - [RFC](https://datatracker.ietf.org/doc/html/rfc9000) 
- [HTTP2]() - [RFC](https://tools.ietf.org/html/rfc7540)
- [IPv6](https://en.wikipedia.org/wiki/IPv6) - [RFC]()
- [Blockchain models for universal connectivity](https://www.semanticscholar.org/paper/Blockchain-models-for-universal-connectivity-Navarro-Castro/788b7a634b369d98e72ed37c5fdf71f7fd62ef0b) - [PDF](https://pdfs.semanticscholar.org/788b/7a634b369d98e72ed37c5fdf71f7fd62ef0b.pdf?_ga=2.260489549.1562006812.1569054619-1995410782.1569054619)

## Articles
- https://datatracker.ietf.org/doc/html/rfc1106

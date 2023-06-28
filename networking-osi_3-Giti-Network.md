# GP - Giti Network Protocol
In the IoE (the Internet of Everything or IoT as the Internet of Things) era, we need connecting Applications as the main goal of computer networks, instead of connecting OSs and devices. IP(v6) is a good protocol but it is designed to connect devices in a very manual manner. GP has some differences in internal services call, security, pipelining, multiplexing, ... . GP will introduce a huge advantage and improve app network performance. We will implement this protocol in [PersiaOS](./PersiaOS.md) but it can use by any other device and OSs due to its very simple specs.

## IP (Internet Protocol) disadvantages
- IP Routers can just be a gateway or can't be as network coordinator
- Registering system is centralized and manual human base
- IP leases fee is high
- IP addresses can't (or very hard to) register by end-user and usually register by ISPs
- IP addresses can't prove their ownership to use in the authentication process due to the above problem
- IP addresses can easily be spoofed. Spoofing can be used as part of a DoS attack and Can't determine the source of an attack
- IP packets want to be multi frame carrier, but almost always carry just one main frame by each packet indicate by [Next Header](https://en.wikipedia.org/wiki/IPv6_packet#Fixed_header) and use extension headers just for some internal protocol mechanism, not all connecting applications requirements. And unfortunately frames introduce by previous frame instead introduce by itself. 

## Goals
- Connect users by applications instead of OSs
- Connect users anywhere in the universe (different planets)
- Best use of addressing space allocation and assignment
- Decentralized and automatic process to register routers in any layer
- Free, automated, and floating to lease new GP address
- GP routers can be network coordinators alongside being a gateway

## Packet Architecture
**Frames** are Always encrypted. at least two(always the special signature frame appear at the end) or more frames in [sRPC format](./sRPC.md)

| bit     | Length(Byte-Octet)| Data                  |
| :---:   | :---:             | :---:                 |
| 0       | 16                | Destination GP        |
| 128     | 16                | Source GP             |
| 256     | ~                 | Frames                |

### Compare with IPv6 packet
- **Versioning**: Unlike IP, GP don't offer any versioning for the protocol as we believe if we need fundamentally change any part of a protocol after the official release, we will already make new protocol. So we respect data link layers protocols like Ethernet and use their solution like [Ethertype](https://en.wikipedia.org/wiki/Ethertype) in [Ethernet frame](https://en.wikipedia.org/wiki/Ethernet_frame) header and don't reinvent other solution.
- **Flow Label**: Almost same as Packet Number in sRPC PacketSequenceNumber frame.
- **Payload Length**: Due to a GP packet isn't chain of related frames and haven't primary frame, Each frame has its own length if need it.
- **Next Header**: Due to a GP packet isn't chain of related frames and haven't primary frame, Each frame has its own *Type* to introduce itself.
- **Extended header**: GP uses standalone frames instead of chain of frames as primary frame and extended headers.
- **Hop Limit**: GP suggest some mechanism in [ChaparKhane](./ChaparKhane.md) as its network router||coordinator to reach this requirement.

## GP Address
| bit    | Length(byte-Octet)| Data            |
| :---:  | :---:             | :---:           |
| 0      | 2                 | Planet ID       |
| 16     | 4                 | Society ID      |
| 48     | 4                 | Router ID       |
| 80     | 4                 | User ID         |
| 112    | 2                 | App ID          |

GP address lengths is 128 bit(16 bytes) as below describe. This protocol unlike IPv6 regard each bit of a GP address. We suggest use below rules in all levels and layers, But just PlanetID & SocietyID part must always respect suggested structure and each society network can have own rules about other routing part of protocol in their networks. **All IDs are temp IDs** and each Society, Router(thing), User & App actually own 32 bytes unique identifier.
- **Planet ID**: Each planet in universe get a 2 bytes unique immutable identifier until exist.
- **Society ID**: Each society civilization like exiting country can tell others and get a 4 bytes unique immutable identifier until exist.
- **Router ID**: Each society must delegate its range to some routers to do routing for improve performance & consistency of its own network. So each Router always have 4 bytes unique mutable identifier until exist(society scope). Usually each organization that claim a land (physical location) like complex building own one router ID.
- **User ID**: Each user on each device get unique mutable identifier from a router(router scope). This ID get by the OS of each device and route them to register app by user in the OS. So an OS can host one or more users until exist.
- **App ID**: Each app get unique mutable identifier from OS. It means same app but for different user has same ID.

### Compare with IPv6 addr
IPv6 and GP addresses are interchangeable, but need some contract with IANA to register /16 range for at least earth planet.

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

### Routers
We strongly suggest using [ChaparKhane](./ChaparKhane.md) for the routers mechanism with [Chapar](./Chapar.md) as link layer protocol to carry GP packets instead of Ethernet frames.

### Mobile GP
The [Mobile GP](https://en.wikipedia.org/wiki/Mobile_IP) allows for location-independent routing of the GP packet on the Internet. We don't have rules for mobility implementation in this spec. You can achieve mobility just by have proper topology in your society network and data link layer.

### Quality of Service
It must be handled in routers, not protocol packets.

### Local Network
When no GP router exists in a network, GP protocol can't use properly. Anyway, nodes can set the first 10 bytes (PlanetID, SocietyID, RouterID) of GP to any data and send packets to other nodes, But peers can't prove their identities strongly to each other.

### Multicast & Anycast & Broadcast
Due to the nature of this spec that must be decentralized, and we believe this type of requirement must handle at the app layer to protect user privacy, So we don't offer any way to multi-cast or any-cast or broad-cast a packet in Giti networks.

## Supported programming languages
It is so simple protocol that can easily encode and decode in any programming language. We implement it on some language like [C](), [Go](https://github.com/GeniusesGroup/libgo/blob/master/GP), [JavaScript]() and more in progress ...

## Inspired of
- [Application-Layer Traffic Optimization (ALTO) Protocol](https://www.rfc-editor.org/rfc/rfc7285.html)
- [QUIC](https://en.wikipedia.org/wiki/QUIC) - [RFC](https://datatracker.ietf.org/doc/html/rfc9000) 
- [HTTP2]() - [RFC](https://tools.ietf.org/html/rfc7540)
- [IPv6](https://en.wikipedia.org/wiki/IPv6) - [RFC]()
- [Blockchain models for universal connectivity](https://www.semanticscholar.org/paper/Blockchain-models-for-universal-connectivity-Navarro-Castro/788b7a634b369d98e72ed37c5fdf71f7fd62ef0b) - [PDF](https://pdfs.semanticscholar.org/788b/7a634b369d98e72ed37c5fdf71f7fd62ef0b.pdf?_ga=2.260489549.1562006812.1569054619-1995410782.1569054619)
- [Matrix, An open network for secure, decentralized communication](https://matrix.org/)

## Other projects
- [Homa](https://github.com/PlatformLab/HomaModule/)

## Articles
- https://datatracker.ietf.org/doc/html/rfc1106

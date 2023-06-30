# Chapar - Data Link Protocol
Chapar is introduced to improve [layer 2 of OSI](https://en.wikipedia.org/wiki/Data_link_layer) that can transmit frames at or near speed of the physical layer (Computing & Networking) limiting and not depend on any devices internal bus speed like RAM, CAM, ... due to it doesn't need any state manager in switching devices (intermediate nodes). It use and combine good specs of [datagrams](https://en.wikipedia.org/wiki/Datagram) and [virtual circuits](http://www.telecomabc.com/v/virtual-circuit.html) to make most efficient protocol.   
Chapar is a switching protocol that store switch state just in frames and just in two connected peer that can be treated as [stateless protocol](https://en.wikipedia.org/wiki/Stateless_protocol). Other protocols usually need to store some states in all hop switches devices (setup information mechanism) other than on frames and peers e.g. other protocols that use and store [MAC](https://en.wikipedia.org/wiki/MAC_address) in frames and each switching device in the network, that must translate to some data in each switch devices to switch frames.

## Inform
Anywhere in this document talk about [Ethernet](https://en.wikipedia.org/wiki/Ethernet), means ethernet in [layer two](https://en.wikipedia.org/wiki/Ethernet_frame#Frame_%E2%80%93_data_link_layer) not including layer one. Ethernet in layer one has its frame header and dedicated specs that usually engineers mix ethernet for two layer almost because they use and think to TCP/IP model instead of OSI model.

## Why (Ethernet disadvantages)
- Ethernet is not a [connection-less](https://en.wikipedia.org/wiki/Connectionless_communication) protocol, Unlike all think or say it. You may think, Why?. Because it must make a MAC table in each switch device as setup information, So it is [connection-oriented](https://en.wikipedia.org/wiki/Connection-oriented_communication) protocol, that need state in three location as frames, peer devices and in each network switch hop.
- High price. Bandwidth is important, but cost per bit transferred is more important
- Limits to make layer 2 networks without getting help from layer 3. The best switch has up to 512000 CAM record limit for query MAC to the port.
- High power usage and limit speed in CAM tables(CAM, TACM, ...).
- Close source complicated hardware and switching algorithms.

## Goals
- **Simple** networking by eliminate complexity
- **Decrease** switch products & network **price**
- **Improve** network **bandwidth** & **latency** without increase networking price
- **Make a big layer 2** network approximately 255^256(2^2048) node if respect port numbers are same on both peer or approximately 255^128(2^1024) node if you don't want to respect this hard work **without need upper layer** and of course switches devices must count as node.
- **Make networking greener** by reduce direct(switch devices) and indirect(cooling) power usage

## Non Goals (Non Considering that can be treated as disadvantages)
- **Security**: Layer 2 is more related to physical layer networks that need physical security to eliminate device access from the network. Any undesired connectivity on a layer 2 network gets physical ports or some frequency on layer 1. So the security of a network must handle in physical with help from ChaparKhane as network coordinator.
- **Error detection** requirement is more related to the physical link (OSI layer 1) to check the healthy of transmitted data between endpoints. Maybe a layer one protocol can guarantee to transmit data without the need to have error detection. And Also related to the upper layer than the Data-Link layer to check the health of data in the destination.
- **Fragmentation**: MTU is not enough to send all types of data on a network, but layer two is not where it must handle.
- **Switching loop**: Due to the suggested structure that a frame can switch just up to 255 hop, so this problem does not exist in Chapar.
- **Backup links** or have more than one physical link between two nodes to providing fault tolerance if an active link fails not to consider or handle by Chapar switches and Endpoints must handle multiple paths to each other with help of network coordinator if exist. We have good reason that layer 2 is not good for this requirements is that this logic need state and why we store states in all path.
- **Bandwidth management** or [Quality of service](https://en.wikipedia.org/wiki/Quality_of_service) is a complicated feature that we decide to handle on layer one and layer three. It is easy to control endpoint devices layer one bandwidth on the connection point to help [ChaparKhane](./ChaparKhane.md) to coordinate network better, but in layer one, you can't distinguish between inbound and outbound traffics.
- **VLAN** or [Virtual Local Area Network](https://en.wikipedia.org/wiki/Virtual_LAN) like "bandwidth management" need state to switch each frame, so it is break our goal to have a very simple switching mechanism. Network segmentation can handle on layer three by help from [ChaparKhane](./ChaparKhane.md) to coordinate local network better.
- **Memory usage in peers**. Theoretically if two peer have more than one path to each other, peers can store each path separately for a connection unlike MAC that need just one value. But be aware that very limited ethernet switch devices support multi path to switch frames, So you can just store one path for each connection. And remember support switching in multi path manner in ethernet is very huge performance drop.

## Still considering
- **Frames congestion** on any ports force still use cache on ports interfaces that can drop up to 50% efficiency. Suggest use computer hardware studies e.g. PCI-Express(PCIe), ...  to handle this consideration in best effort.

## Topology Example
- [Some diagrams](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#R7V1Lk5s4EP4te3Btcpgp3tjHzCTZpCqp3aqp2k2OMsigHYxYkF%2F59SuBZCOEsT3GwIx9GUPrAfT3davVEszIfJyv%2F0hBEn7HPoxGhuavR%2BbHkWGMxxr9ywSbQmCzMyYIUuQXIn0neEK%2FIBfydsEC%2BTCTKhKMI4ISWejhOIYekWQgTfFKrjbDkXzVBARQETx5IFKl%2FyCfhPyxDHcn%2FwJREIor686kKJkDUZk%2FSRYCH69KIvPTyHxMMSbF0Xz9CCOmO6GXot3nPaXbG0thTI5p8DWZLZdfn0P7aakB68fi8e%2Fg%2B92Y3xvZiAeGPn1%2BfopTEuIAxyD6tJM%2BpHgR%2B5D1qtGzXZ1vGCdUqFPhv5CQDQcTLAimopDMI14K14j8YM3vXZuf%2FuS9seOP6%2FLJRpzEJN0UrWxx%2BrNctmuWn4l2GQEp%2BcCYQAVeBLIMeUL8GUXingo9sIffq14uyvAi9WCDTgVNQRpA0lDP2JKAGg%2FEc0hvm7ZLYQQIWsr3ATiNg229HdL0gIN9AvCTfoF%2FEe7uGwHePBP4vCl9MrApVUgwiklW6vkvJqAV1sKhclvnjpj7qc97qttmU3V6UFx%2FR8Dtg7yckzb3lEsQLbgWknBDYQOsaUIJ1y9pjTJr9UbW9kS%2Bc0ml0MCVWbAdlkUPBdd5o4pLaoERukqInAXafLFWuEAH2IQdJin2YEZv8GEVIgKfEpArbkXjExnZKfCeg5wffy5IhGIoobKEKYHrZlxUffMGlqw3XeP%2BdrWLIXQRGISl%2BMHR9iN0lr8XwN1G%2BhZtzujI4Z%2BFvDW5edXzEG7dq%2FbtVo3X6lYH6FdrdHmzriOtq5VAWLEuq2frMl%2BrdVmDsy5LUaVhO1TwDqf0r2PbJj2jXWv39%2FfvVUOLfUHnGDNFPfggC3O70mWlMvlfgBCYxrnE0Myc%2BSl%2B3qZ9DMUwj7UEVeElhdo1%2BhSyMw3BHlfwNCdyF4WBKoZQMws40NGlpwGOwoNFkkDGgQhs2G%2F3Lvbl4HOlaveO47itAG25Ewkf8ziHd9Bznk4YURHPZhmU6pyar1DuxWhOWByof5mMhW6%2BLuqdmw1oh2YvZNmpDKpcxm3mT2PtC7FHHd4Ou7VvYAojmQ8gQgEbtzwKP21lPrAogEWgH3jBHPl%2BQT2YoV9gmvfHyMdVSDu3H0b2x6Ywgi%2Bw8Maj7bJGmXUNNtLgBl1duEGuexFBvZStYqlJbqC6pNZwtG%2FDU%2FN0tx2%2F0ZXjUK5zYOg5UF92HseMla0Rs9flPXGc5%2B62Kz5DmXvq7kWGSNNxZK5X50aXDpV7XdiTITeuFXPL7hRzo9fcvoT5dQBuTGTAjXHH%2BVu9T8BPWsx5O5g7PWNu9Iv5NUJu9gx5L9mFPWsH14K51jPmVq%2BYXx%2Fgutsz4PZgAL%2BagF3Xew7YneFgfq2QdzwvFxvGSznC4XDAvVYSuB3b%2FYDycdeCuZKc6Rrznnfau0PeANTRXN2yOt4BNJiE3LUAPukZ8J4Tctdo42bPkPecjxv0xs6OkjOdY95vQu5owIePZDXr0jWSujody1AcUMCGv023qjtThBu9bdM11Y1MfMtzvk%2B3eTMMVQSRdVfsu33EEW293bo7o46qIjp%2B31MdWHV7ec%2FCxVRwce9tBRm3Bphq%2Bqk9YNSdSVcIjKHpEjCGpRpMt7Co%2B5lvsOzGgN5gUQeFK4TFHJ4XGyu4jAwnYuqe0oOA5A9eCGY4DzN2wDj%2FLbAouMvyGOsDraBbybpoxstFR1R3TBkRDZYNbbrw2ZudtL8VIl7IYOfXTUV9WhAyhsTRJv%2BBeeNAvABG44U8YFDaoTgjEPhMh2AJt00LihW0qzYREqrE4jEVcUkdB%2BnZ5q5hFrQWuj2J%2BS2w1XbGFbqqTmS74bSbd5bUYEhBo4tZw563qLdlg3mL2jr2uxmWUU%2BFc%2BciYsVXfOpCfMLnwLbi1j57UfPCYPUVUi1ezOnfvFTrOfMw5MSD1ewt7rR7rryzt7RXOHPk%2FPXkr7YY9dfZvxW9sX5%2FW9GFkZdIXholS%2B%2FHatMUMSYMeQZeAcV2aibgdRHS5cYcdZ73xnzESz8K0qJvse1jx6kLvdduHRinLpwzs4wjxqmhJ8%2BEpYg55%2BTI3Fn1naXWTNeuyZ01j%2F497xgb9vh%2FGdPrari3Thm%2BW7NrNf58vUOzOT5ibB53OjZ3mb1YhTBmQ9QKS0kLzQPx7yTXQgrVxAJmbTIwh5LHme7SHbeMQznjIL%2BtbNdlHOqGEPtiQ4gaW1%2BOYSkMFhFIR4dzYg6YM7uPp1lu%2FqUsV7V%2B4V14rizPtd7SYCeSciyT0u3b69k1K0%2BvL1jU5cFkANGiunIkeJ8lIK61bK9gG7PqNJi%2B04ovJomf97mqtNz8Z2COok1R9QuMlpAZQqm85B507h54QXFRVhLjdA6iUtkSpAjQX2pOgCxS9jHvxnoeSPZVWXEVs0JLK6Z3WgTZd5vu6ON7KA7UljhNQhDzLo1CxtzAHbd8Jt4avyhDNFiO%2BZU08ah5CUlpZzPav7gSN2HGifxr46XLrHDqyze27Ys%2By%2FQZ0e5Yn4WjuOOskurt2H1XwdFgJsYgLB%2B8L92pDz2c0qgXx3ckRN5znJsTa45iRJDQT7VuCcvGeqXbkerNIgxIVTk%2BypIIbET13EwN7Tc0Z54AxKR2qEmY%2B82nO1vPXpC82bkf8Bct%2BIXK57AcTXULVo1XMC7mFepeLrh5hZtXeLteYeg%2BwRarOr35hP3TzptPuPmEm0%2FowCdYtryXpv9AQf0W%2BM0p3JzCW3YKA5w%2BWLbRVaxAT3f%2FYapYMNj9my7z0%2F8%3D)
- Two-tier network with core/edge. With just 1 core chapar switch and 256 edge chapar switches can connect 65280(65536-256) host to the network of course with just one physical link between core and edge switches. If we provide two core switches that have two physical link between cores and edges switches, the network can connect 65024(65536-256-256) host to the network.
- Three-tier network with core/distribution/access. With just 1 core chapar switch and 256 distribution chapar switches and 65280 access switches can connect 16,646,400(65280\*255) host to the network of course with just one physical link between core/distribution/access switches. If we want 2 core switch and each access switch connect to two distribution switches can connect 16,516,096(65024\*254) host to the network.    
A Chaparkhane device (router) with 32GB of ram easily handle all connections if one router outer network capacity satisfy the network nodes. Beware nodes just need Chaparkhane for outer network routing without support for anything bad like [NAT](https://en.wikipedia.org/wiki/Network_address_translation) and inner network connections just use Chaparkhane as coordinator with high secure connection by help of GP or IPsec.
- Three-tier network with core/distribution/[wireless-access](#Wireless). With just 1 core chapar switch and 256 distribution chapar switches and 65280 wireless-access switches can connect 4,261,478,400(65280\*65280) host to the network of course with just one physical link between core/distribution/wireless-access switches. If we want 2 core switches and each wireless-access switch connect to two distribution switches can connect 4,228,120,576(65024\*65024) host to the network.

## Frame architecture
- Ports number can be mutable due to physical link limits. The endpoint must beware of this aspect.
- Each switch interface in any location of link can be wired or wireless with any Energy||Frequency specs (e.g. Fiber, WiFi, LAN, Bluetooth, ...)

| bit   | Length(byte-Octet) | Data                          |
| :---: | :---:              | :---:                         |
| 0     | 1                  | FrameID                       |
| 8     | 1                  | Hop Count                     |
| 16    | 1                  | Next Hop                      |
| 24    | 1                  | First Hop Port Number         |
| ...   | ~                  | x Hop Port Number (Optional)  |

- FrameID: Indicate by [networking rules](./networking.md).
- [Hop Count](https://en.wikipedia.org/wiki/Hop_(networking)#Hop_count): The hop count refers to the number of intermediate network devices through which data must pass between source and destination, and also indicate frame length.
- [Next Hop](https://en.wikipedia.org/wiki/Hop_(networking)#Next_hop): Indicate hop number that frame must send on indicate port by that hop.
- First Hop Port Number: Source Port Number, also can be Destination Port Number in P2P(Point to Point) connection.
- x Hop Port Number: Up to 255 hop port number can be in a frame.

## Frame Types
Chapar support **UniCast** and **BroadCast** frame and not support **AnyCast** or **MultiCast**. We strongly suggest use broadcast frames just in network discoverable mechanism like find GP network coordinators. Also to broadcast emergency messages service, not to use to broadcast video channels, ...

## Switching

### Blocking Switch
Transmitting will block sender until frame transmitted successfully. Sender can be sure frame transmitted.

### Non blocking Switch
Transmitting will not block caller to be non blocking and queue frames for congestion situations.
A situation might be occur that a port available when a frame queued but when the time to send is come, the port broken and sender don't know about this.

## Rules
- Frame size can be up to 8192 Byte or 8KB. Enough to stream 1.5Mbps video call in each 40ms frames (`1.5/8*1024/1000*40=7.68KB`).
- Due to the frame must have at least one hop, Use unused HopCount==0 for broadCast frames to all ports. So both HopCount==0x00 & HopCount==0xff have 255 hop port number space in frame header.
- BroadCast frame must have all hop port number space with 0-byte data in the header, otherwise other frames in the packet manipulates(rewrite) by switches devices.
- When two peer connect by two different port number, one of them must be as switching adaptor. That means **usually higher hop** must add virtual switch hop to switching road. It will add one more hop port number in each chapar frame.
- In each hop, the Switch device must rewrite the received port number on the frame. The reasons are:
    - BroadcastFrame: To improve performance, the previous switch just sends a frame without declaring the next port.
    - UnicastFrame: To be sure receive port is the same with declaration one in a frame.
    - Rule&Security: To be sure the physical network port is the same on the sender and receiver switch.

## Hardwares
Chapar functions can add by switching fabric unit (SFU) in any devices by any interfaces like PCIe, .... It can have 1 to 256 wired port or 2^16(65536) wireless port. 

### Wireless Access Point
Chapar can help layer 1 protocols to made connections betweeen AP and clients. Suggest each Chapar wireless ap device handles two hops of the frame instead of regular one hop in each switching hop. It means each wireless ap can serve 2^16(65536) devices.

## Inspired of
- https://guifi.net/
- https://en.wikipedia.org/wiki/Telephone_exchange
- https://en.wikipedia.org/wiki/Fast_packet_switching
- [SDU](https://en.wikipedia.org/wiki/Service_data_unit) vs [PDU](https://en.wikipedia.org/wiki/Protocol_data_unit)
- [ETSI](https://www.etsi.org/) standards
- https://en.wikipedia.org/wiki/Asynchronous_Transfer_Mode
- [IEEE 802](https://www.ieee802.org/)
- [Frame Relay](https://en.wikipedia.org/wiki/Frame_Relay)

## Articles
- https://www.dropbox.com/sh/51l4x1p2e8lub5x/AABVgFyJ0fuia8QZt7SEZgBWa?dl=0

## Chapar word meaning
["The Chapar"](https://en.wikipedia.org/wiki/Chapar_Khaneh) (Persian: چاپار‎) were express couriers who were provided with fresh supplies and horses at each station along the way, allowing them to quickly complete their way without having to procure supplies on their own or wait for their horse to rest.

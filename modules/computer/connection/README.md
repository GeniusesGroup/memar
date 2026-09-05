# Connection
a “connection” is a very low level concept; it basically means the pipes are connected to each other.

## Model

- `(quiddity)-[:software_connection]->(---)`

## Connection-oriented communication

In telecommunications and computer networking, [connection-oriented communication](https://en.wikipedia.org/wiki/Connection-oriented_communication) is a communication protocol where a communication session or a semi-permanent connection is established before any useful data can be transferred. The established connection ensures that data is delivered in the correct order to the upper communication layer. The alternative is called connection-less communication, such as the datagram mode communication used by Internet Protocol (IP) and User Datagram Protocol (UDP), where data may be delivered out of order, since different network packets are routed independently and may be delivered over different paths.

## Communications system

A [communications system](https://en.wikipedia.org/wiki/Communications_system) is a collection of individual telecommunications networks systems, relay stations, tributary stations, and terminal equipment usually capable of interconnection and inter-operation to form an integrated whole. Communication systems allow the transfer of information from one place to another or from one device to another through a specified channel or medium. The components of a communications system serve a common purpose, are technically compatible, use common procedures, respond to controls, and operate in union.

## Communication protocol

A [communication protocol](https://en.wikipedia.org/wiki/Communication_protocol) is a system of rules that allows two or more entities of a communications system to transmit information. The protocol defines the rules, syntax, semantics, and synchronization of communication and possible error recovery methods. Protocols may be implemented by hardware, software, or a combination of both.

## Communication Channel

A [communication channel](https://en.wikipedia.org/wiki/Communication_channel) refers either to a physical transmission medium such as a wire, or to a logical connection over a multiplexed medium such as a radio channel in telecommunications and computer networking. A channel is used for information transfer of, for example, a digital bit stream, from one or several senders to one or several receivers. A channel has a certain capacity for transmitting information, often measured by its bandwidth in Hz or its data rate in bits per second.

## Session (computer science)

In computer science and networking in particular, a [session](https://en.wikipedia.org/wiki/Session_(computer_science)) is a time-delimited two-way link, a practical (relatively high) layer in the TCP/IP protocol enabling interactive expression and information exchange between two or more communication devices or ends – be they computers, automated systems, or live active users (see login session). A session is established at a certain point in time, and then ‘torn down’ - brought to an end - at some later point. An established communication session may involve more than one message in each direction. A session is typically stateful, meaning that at least one of the communicating parties needs to hold current state information and save information about the session history to be able to communicate, as opposed to stateless communication, where the communication consists of independent requests with responses.

### Session management
In human–computer interaction, session management is the process of keeping track of a user's activity across sessions of interaction with the computer system.
Typical session management tasks in a desktop environment include keeping track of which applications are open and which documents each application has opened, so that the same state can be restored when the user logs out and logs in later. For a website, session management might involve requiring the user to re-login if the session has expired (i.e., a certain time limit has passed without user activity). It is also used to store information on the server-side between HTTP requests.

## Policies (rules)

- A connection can use just by single app node, so user can't use same connection to connect other node before close connection on usage node. In the other words it means hardware MUST NOT let user copy tokens to other devices.

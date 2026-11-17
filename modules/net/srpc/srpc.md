---
Title: "sRPC — Application Protocol"
Labels: Draft
Start Date: 2020-05-10
ID: 441408
---
# sRPC — Application Protocol
## Abstract
sRPC (Syllab Remote Procedure Call) is Memar's application protocol: frames that ride in a [Networking](../net.md) packet — with lower-layer frames such as [Chapar](../chapar/chapar.md) or [GP](../giti/giti.md), or on older Internet transports — and supply the fields needed to select a service, identify a call, carry a payload, open and close a stream, and agree an acknowledgement scheme. It decides that routing, service, operation, and request are independent identities, none of them a path segment or a query key; that service lookup and protocol-forced data stay minimal; that peers may agree an acknowledgement scheme rather than transmit blindly; and that durable-delivery machinery belongs in a library wrapping the application's own store, not in a standalone message broker. The [protocol](protocol/) declares their structure and behavior.

## Introduction
### Motivation
Application-layer calls fail when the protocol itself is the cost: finding a service among a server's services requires extra lookup work, and the protocol forces extra data onto every exchange. They fail again when routing, handler, operation, and request instance share one representation, so none of them can be addressed, matched, or adapted on its own. This protocol exists to keep lookup and forced exchange small, and to keep those four as distinct fields. Human readability of the wire is not a goal.

### Methodology
The [protocol](protocol/) carries the frame contracts. [Networking](../net.md#frame-identity) owns frame identity.

## Explanation
### Goals
Service lookup and the data forced onto each exchange should stay small. Binary exchange saves bandwidth and parsing work at both ends; consumers receive the text they need through the service's delivered [SDK](../../process/service/rules/sdk/sdk.md).

### Frames
[Protocol](protocol/) declares the frames and their fields.

### Acknowledgement Scheme
sRPC peers may agree to use any acknowledgement scheme, such as selective negative acknowledgement (SNACK), negative-acknowledgement (NAK or NACK), or [acknowledgement (ACK)](https://en.wikipedia.org/wiki/Acknowledgement_(data_networks)) as used in many protocols such as TCP. Unlike IP, UDP, and similar protocols, this is not [blind transmission](https://en.wikipedia.org/wiki/Blind_transmission).

### Position on Message Brokers
The standalone message broker — MQTT, AMQP, and kin deployed as a separate service — is an external protocol surface Memar does not adopt as a default, and the reason is arithmetic, not taste. The honest-delivery pattern the broker serves (at-least-once, exactly-once semantics, its QoS levels) requires the broker to persist messages to non-volatile storage before acknowledging them. An application that itself must durably record what it sends then pays for that persistence twice: once in the application's own storage, once in the broker's — plus the network hop between them — per message, at layers that did not need the duplication. At IoT volumes this cost dominates the system's storage budget; at any volume it buys a guarantee the application's own store could have provided directly.

Memar's stance: **the broker's mechanism belongs in a library inside the application's own architecture, not in a separate standalone service.** Where durable delivery is the requirement, the durable store is the application's own; the delivery machinery (the acknowledgement discipline this protocol already defines, persistent queues, retries initiated by whichever participant this framework's retry rules allow) wraps that store rather than shadowing it. This is the same judgment [Networking](../net.md#memars-position-on-the-traditional-network-stack) records for protocol logic generally: middleware logic is application-relevant logic, and its placement is a decision to be made, not an OS-shaped default to be inherited.

Two further notes are attached to this position:

- The sync/async client models brokers offer are both cost-irrational in the same way: either the client's logic is structured around the broker's session (sync), or the broker is trusted to have persisted before the client continues (async) — losing data precisely when the acknowledgement meant nothing. Both models are artifacts of the broker being a separate process; a library-owned broker dissolves the trade-off by letting the application's own storage be the durability point.
- The producer-consumer independence principle ([Process → Events](../../process/process.md#events)) is untouched by this position: making the broker mechanism a library does not couple producers to consumers — it only relocates who runs the machinery.

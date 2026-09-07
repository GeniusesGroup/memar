---
Title: "Networking Connection"
Status: Draft
Start Date: 2026-09-06
ID: 496867
---

# Networking Connection

## Abstract
This document is the home of Memar's connection protocol: what a **connection** is between computing components in [Networking](./networking.md)'s packet model, where a connection's state lives and who owns it, what the connection's participants may and may not do with it, and how long-lived behavior (timeouts, keep-alives, half-open states) is governed. It exists because the ecosystem's dominant arrangement — connection state owned by the host's OS-embedded network stack, exposed to applications through a narrow, blocking socket API — repeatedly produces the same class of design failure, and the framework needs a stated alternative, not an implicit inheritance of that arrangement. The critique of that arrangement itself lives in [Networking → Memar's position on the traditional network stack](./networking.md#memars-position-on-the-traditional-network-stack); this document states the positive contract.

## Introduction

### Motivation
Two interface failures shape this document's direction. The first is the ecosystem's standard socket read: a blocking `Read` with no way to proceed when no data has arrived — the standard answers (spawning a reader thread, setting read deadlines) are workarounds around an interface that simply does not model "no data yet" as a first-class outcome. The second is the drift around connection *state*: HTTP is universally described as stateless, yet its own specifications define persistent state mechanisms (cookies, session lifetimes, keep-alive) — the layering has drifted so that state owned and needed at the Transport layer is re-created, badly, at the Application layer by every framework above it. Both failures trace to the same root: connection state and connection behavior were placed somewhere the application cannot see and cannot govern, so every layer above compensates in its own ad-hoc way. This document records where Memar places that state and behavior instead.

### Methodology
The positions here were formed alongside [Networking](./networking.md)'s position on the traditional network stack, checked against the HTTP cookie/session specifications and the Go socket API's actual behavior, and aligned with the packet/frame model of [Networking](./networking.md) — in particular its principle that no layer is mandatory and each layer's presence is justified per link. The connection contract below is stated at the framework level; the userspace TCP realization that will implement it is tracked under that position's unresolved questions.

## Explanation

### The connection concept
A **connection** is a persistent, stateful association between two components, established so that a series of exchanges can share context — negotiated capabilities, ordering guarantees, buffers, identity — instead of restating it per exchange. In the packet model, a connection is *not* a layer and *not* a packet element: it is an agreement between the endpoints, realized by whatever layers the participating links justify ([Layer presence](./networking.md#layer-presence)), that both endpoints maintain shared state for a span covering multiple packets.

This definition deliberately does not require any particular protocol to exist below: two components on a link with no data-link framing can still hold a connection; two components speaking Chapar over an Ethernet segment hold one; and an application-to-application conversation under GP holds one without any intermediate device participating in it at all.

### State ownership: the state lives with the protocol's logic
The load-bearing rule of this document: **a connection's state is owned by the component that runs the connection's protocol logic, and that component exposes the state to the layers above it.** The state includes what the protocol genuinely needs — sequence and acknowledgment tracking, buffers, timers, negotiated options, and the endpoint's own lifecycle position — and the component exposes an accurate view of it, not a shadow copy and not an opaque handle.

This rule is the direct inversion of the socket arrangement, where state lives in the kernel behind an API that exposes only bytes-in/bytes-out and a handful of file-descriptor operations. The failures that arrangement produces, and which this rule prevents:

- **The stateless-protocol myth.** A protocol is called "stateless" because its state is hidden from its users, and every user then rebuilds that state at a higher layer, inconsistently. Under this rule, a protocol's persistent state mechanisms are part of its exposed contract — [Chapar](./chapar.md)'s switching state, a connection's negotiated options — so no upper layer re-creates a private, divergent copy.
- **Re-creation of Transport state at the Application layer.** When connection health, liveness, and lifetime are invisible above the socket, frameworks re-implement them as application-level heartbeats, session timeouts, and retry heuristics — three different answers to one question, all worse than the one the Transport component could have given. Ownership with exposure removes the question.
- **Blocking reads as a modeling failure.** "Read blocks until data arrives" is an interface decision, not a property of networking. In Memar's model, checking for available data is a query against the connection's exposed state; waiting for arrival is one explicit mode of consuming that state among several — not the only operation the interface offers.

### Timeouts and liveness are budgets of the owning component
Consistent with [Process → Requests, Cancellation, and Timeout](../process.md#requests-cancellation-and-timeout): the timers that govern a connection — inactivity timeouts, retransmission budgets, keep-alive intervals — belong to the component that owns the connection's state, are configured through that component's configuration surface, and are not renegotiated by every caller of every operation. A per-operation deadline parameter handed down through every layer re-creates the socket arrangement's confusion in application code; the component-owned budget replaces it. Where an individual exchange genuinely carries a caller-meaningful bound, that bound is an explicit parameter of that exchange — modeled where it is meaningful, not threaded invisibly everywhere.

### Half-open and abandoned connections
A connection's endpoints can fail independently, so the protocol must define how an endpoint detects and resolves half-open states — the peer gone without a closing exchange — and what happens to in-flight work when it does. This document specifies the *rule* (detection and resolution are the owning component's responsibility, driven by its own budgets, and their outcome is exposed as connection state); the frame-level mechanics (which frames carry the probes and closes) belong to each protocol's own document — [Chapar](./chapar.md) for its links, and the userspace transport realization tracked in [Networking](./networking.md)'s position topic.

The ownership-with-exposure direction is validated by QUIC's userspace model (connection state in the library, visible and configurable) — existence proof that state ownership with exposure is implementable, not merely aspirational — and the "stateless HTTP" contradiction is visible in the HTTP cookie and session specifications themselves.

## Results
Insufficient time has passed since this document was drafted to report real, observed outcomes. It is a Draft whose positions await their first implementation in the userspace transport work.

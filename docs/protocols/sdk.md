---
Title: "SDK"
Status: Draft
Start Date: 2026-09-08
ID: 496912
---

# SDK
This document records the concept work behind Memar's SDK protocol — the working positions, boundaries, and open questions reached so far. It is a Draft: a dedicated design session will turn these positions into the protocol's actual specification. See [Protocol](../protocol.md) for the general concept of a protocol.

## Abstract
The SDK protocol defines a general abstraction for **service client delivery**: a service's own developer produces, alongside the service, the client-side realization of the service's declared interface, produced per consumer language — not a document other parties must implement from. The abstraction is defined independently of any transport, any serialization codec, any consumer language, and any interface style (RPC, resource-oriented, event). The core position: the SDK is the service's own deliverable, carrying in generated form everything a consumer needs to call the service correctly — request construction, response decoding, error mapping ([Error](./error.md)), caching strategy, and validation ([GUI](./gui.md)) — so the consumer writes no network code at all and never re-derives the declared interface from a specification. The SDK is further anchored to four framework concepts: it is part of the module's own realization of its protocol, not an accessory beside it ([Modularity](../modularity.md)); a module presents local and network invocation behind one call surface — network meaning the defined crossing out of one application's agency space into another's, not two machines ([Networking](./networking.md)); an SDK call invokes a process opaquely ([Process](../process.md)); and a network call is a delegation — the serving side executes as the requester's agent under the agreement the parties already hold ([Agency](../agency.md)). The industry's dominant alternative — publishing a textual or intermediate specification (OpenAPI, IDL) and leaving SDK production to every consumer — is examined and rejected as the default: it moves service-owner responsibility onto each consumer and produces the documented ecosystem failures below. What remains open — the delivery and versioning rules, generation mechanics, and the relationship to [Media Type](./media-type.md) and [sRPC](./sRPC.md) — is registered in the paired [handoff](./sdk.handoff.md).

## Introduction

### Motivation
The ecosystem's standing practice is to ship a service with a document — prose, or an intermediate specification such as OpenAPI (formerly Swagger) — and treat the client side as each consumer's problem. Every consuming organization then writes and maintains its own client code from that document. The failures are observable everywhere:

- **Responsibility transfer.** Correct behavior that only the service developer knows — how requests should be cached, how the service's errors map to consumer-side outcomes, which call sequences are valid — must be re-derived by every consumer from a description that does not carry it. The consumer's guess becomes their permanent liability.
- **Intra-organizational absence.** The failure is not only between organizations: within one organization, a backend team ships the specification and the frontend team generates or hand-writes its own client from it — the same responsibility transfer, one desk over. Even [gRPC](https://grpc.io), whose code generation is the ecosystem's closest approach to this protocol's position, did not displace the practice: OpenAPI-style textual specification delivery remains dominant.
- **Consumer-side drift.** N hand-written clients against one service evolve at N speeds; interface changes surface as runtime failures in some consumers and not others.

The position behind this protocol: the party that knows the service owns the client's correctness — the service developer delivers the SDK, and consumers consume it. Generated code is the delivery mechanism because the service's interface is already declared somewhere authoritative; producing the client from it is derivation, not authorship.

The responsibility rule also has a division-of-labor consequence the founding discussions stated explicitly: with a delivered SDK, a GUI developer can build against services as if calling local functions — never needing to know a network exists — and the backend team can add, remove, or replace network protocols ([Networking](./networking.md), [sRPC](./sRPC.md)) without the service or GUI developers noticing. Consumers of a correctly-delivered SDK are insulated from the transport layer by construction.

### Methodology
This document's content was arrived at across years of working discussions (2020 through 2024) in public developer communities — on GraphQL's aggregation cost, on frontend teams hand-generating clients from textual specifications, on error transmission across the SDK boundary, and on a prototype of automatically-generated SDK code for a Go service consumed from JavaScript (see the paired [changelog](./sdk.changelog.md) for the session-by-session provenance). The positions below were stated and defended in those discussions before this document existed; drafting examined them for what they presuppose rather than inventing them.

## Explanation

### What an SDK is
An SDK is **the client-side deliverable a service's developer provides, realizing the service's declared interface for one consumer language**. The general question the protocol answers is not "how do consumers write clients?" but: **what does a service owe its consumers, and in what form is that debt paid?** The debt is paid in code: a callable realization of the service's interface, carrying the service's own decisions about how it should be called.

```text
        Service developer (one)                    Consumers (many)
   ┌─────────────────────────────┐          ┌──────────────────────────┐
   │  Service implementation     │          │  GUI · other services ·  │
   │  + interface declaration    │──SDK──▶  │  tools · other teams     │
   │  (per-language SDKs         │          │  (call functions; no     │
   │   generated from it)        │          │   network code of their  │
   └─────────────────────────────┘          │   own)                   │
                                             └──────────────────────────┘
```

The SDK is *derived from the service's declared interface*, not authored beside it: the interface declaration — the callable signatures, the structure definitions, the error inventory — exists once as the service's own declaration, and each language's SDK is generated from it. Generation is the mechanism that keeps N deliverables consistent with one declared interface; hand-maintained client code per language is what the derivation replaces. The generation mechanics (where the interface declaration lives, what the generator consumes) are the design session's task — the position settled here is the *ownership and the direction of derivation*, not the tooling.

### Working positions
The discussions converged on the following statements. They are the settled core of the concept; each is elaborated below.

1. **The SDK is the service's own deliverable.** Responsibility for correct client behavior belongs to the service's developer, not to each consumer. This is the protocol's central position and the one the ecosystem's current default violates.
2. **A textual or intermediate specification is not a deliverable of this kind.** Publishing OpenAPI/Swagger-style documentation (or prose documentation) and leaving SDK production to consumers moves the service owner's responsibility onto every consumer; it is examined and rejected as the default — see [What an SDK is not](#what-an-sdk-is-not).
3. **The SDK carries the service's operational decisions, not just its message shapes.** How requests should be cached, how responses decompose, how errors map across the boundary ([Error](./error.md)), which validations apply ([GUI](./gui.md)) — decisions only the service developer holds — travel in the SDK, not in a document the consumer must interpret.
4. **The consumer writes no network code.** No part of a consumer communicates with the service except through SDK functions; the generated code is the only thing that knows a transport or serialization exists. This is the same position [GUI](./gui.md) states for graphical clients, generalized to every consumer.
5. **Aggregation is a consumer-side capability, not a service-side endpoint shape.** A service offers its operations at their natural granularity; consumers that need composed views compose them in the SDK from the delivered functions ([Aggregation and the cache](#aggregation-and-the-cache)).
6. **Error transmission across the boundary is numeric coding, not locale-bound text** ([Error](./error.md)) — the SDK carries the mapping, so consumers never parse error strings.
7. **The SDK is declaration-derived and identity-bearing per revision; the declaration binds no consumer language.** Deliverables are produced per consumer language where the module provides them; a consumer in a language the module does not serve consumes the same declared interface through FFI against the delivered realization, a port to its language, or another consumption path — without re-deriving the interface. Two deliverables derived from the same declaration revision are substitutable; a declaration change is a new revision and new deliverables, never a silent mutation of delivered code.
8. **Generation, where compilation allows, is compile-time.** In compiled languages the SDK is generated into source and compiled with the consumer, so violations of the declared interface surface at compile time (including error-code coverage); in dynamic languages the generation produces the same guarantee as far as the language permits.
9. **The SDK is part of the module's own realization of its protocol.** A module's protocol surface is complete only when its client side is delivered with it; a module that stops at its server-side realization leaves its own protocol half-realized, and the vacancy is filled by consumers re-deriving the declared interface — the founding violation ([Modularity → Module, Process, and Protocol](../modularity.md#module-process-and-protocol)).
10. **A module presents two invocation kinds — local and network — behind one call surface.** A local call executes within the consumer's own agency space; a network call traverses a defined path out of that space into the module's, and the process executes under the module's control. The separating boundary is agency space, not hardware and not instance topology ([Local and network invocation](#local-and-network-invocation)).
11. **An SDK call invokes a process opaquely.** The consumer states intent and data; the process's internal progression, participants, and mechanisms remain the service's — a plain function call into process invocation ([Invoking a process](#invoking-a-process)).
12. **A network SDK call is a delegation.** The requester delegates the process's execution to the serving side, which executes on the requester's behalf under the agreement the parties already hold; the delegation boundary is what protects the process's integrity against the requester's own interference ([The call as delegation](#the-call-as-delegation)).

### What an SDK is not
Two boundary cases fix the concept from its edges:

- **A specification is not an SDK.** A service's OpenAPI document, its prose API reference, its `.proto` file — each describes the service's interface; none realizes it. Consuming from a specification re-implements the declared interface per consumer, which is precisely the responsibility transfer this protocol rejects. See [Protocol vs API Specification](../protocol.md#protocol-vs-api-specification) for the general distinction; the SDK is the *realization* side of what a specification merely *records*.
- **An SDK is not a shared library of general utilities.** The SDK's subject matter is the one service's declared interface; a toolkit, a framework, or a general-purpose client library for a protocol (an HTTP client, a [Chapar](./chapar.md) implementation) is a different concept — reusable machinery, not one service's delivered interface. Where the machinery underneath an SDK comes from (an implementing repository's networking stack, for instance) is composition, not identity.

### The responsibility chain
The division of labor the SDK fixes, end to end:

- **The service developer** owns the service's declared interface and the correctness of its realization — including cache strategy, error mapping, and validation rules — and delivers them. The service developer knows how requests should be cached because the service developer knows the service's cost structure and consistency requirements; that knowledge must not be re-derived from outside.
- **The SDK (generated)** is the delivery vehicle — the only component on the consumer side that encodes transport, serialization, caching, error mapping, and validation.
- **The consumer** owns domain logic — what to call and what to do with results — and nothing below that line. A GUI team that writes fetching, retry, or serialization glue is doing the backend team's work over again, worse, from an incomplete description.

This chain is what makes intra-organizational delivery work the same as cross-organizational delivery: the frontend team is a consumer like any other, and the same deliverable discipline applies. The recurring ecosystem practice of a frontend team generating its own client from the backend's textual documentation is the chain's violation, not an acceptable variant of it.

### Part of the module, not beside it
[Modularity → Module, Process, and Protocol](../modularity.md#module-process-and-protocol) keeps three concepts distinct: a Module is a structural boundary for capabilities, a Process is progression over time, a Protocol is the declarative rules governing processes. The SDK position adds the delivery consequence for the module side: **the SDK is part of the module's own realization of its protocol**, generated from the same declaration the service side realizes — not an artifact a module publishes about itself. A module that delivers only its server side has not completed its protocol surface: the protocol's consumer face is unrealized, and the vacancy is filled by whichever consumer gets there first, re-deriving the declared interface from a description — exactly the responsibility transfer this protocol exists to end. Completing the surface is therefore a conformance obligation of the module, on the same footing as the service behavior itself, not a convenience feature.

### Local and network invocation
A module presents two invocation kinds behind one call surface:

```text
                 consumer code
                      │  one call surface — SDK functions
            ┌─────────┴────────────────┐
            ▼                          ▼
     local realization          network realization
     (executes within the       (traverses a defined path out of the
      consumer's own            consumer's agency space into the module's;
      agency space)             the process executes under the module's control)
```

- **Local invocation**: the service executes within the consumer's own agency space — no boundary is crossed.
- **Network invocation**: the call traverses a defined path out of the consumer's agency space into the module's, and the code executes under the module's control — deliberately, so that the process's processing stays out of the requester's hands (the processing-security reason; see [The call as delegation](#the-call-as-delegation)).

The separating boundary is therefore **the application's agency space, not hardware and not instance topology**. Two applications on one machine — including an application and the operating system hosting it — relate through network invocation exactly when one crosses into the other's space along a defined path. Android is the standing instance: the operating system delivers an SDK to the applications it hosts, and an app calling OS capabilities is consuming another application's SDK in the full sense, hardware co-location notwithstanding. What makes an exchange network communication is the defined crossing between agency spaces, not the distance between machines — consistent with [Networking → Scope](./networking.md#scope), where a GPU–CPU exchange over PCIe is as much a network as two computers over a cable.

Which realization backs a call is a delivery decision, not a consumer decision; the consumer writes one call either way. This is [Modularity Is Not Deployment](../modularity.md#modularity-is-not-deployment) expressed at the call level: deployment shape changes without consumer change, because the SDK is the layer that absorbed the difference. It is also the uniformity the founding prototype demonstrated — GUI developers work "completely local", calling plain functions, while a transport may sit underneath (see the paired [changelog](./sdk.changelog.md)).

### Invoking a process
What crosses an SDK call is a **process invocation**. The consumer states the intent — which capability, with which data — and the process's internal progression, participants, state transitions, and mechanisms remain the service's own knowledge. This follows [Process → Definition](../process.md#definition) directly: the defining question of a process is not "which mechanism executes this," and the SDK is the enforcement of that independence at the consumer boundary — a plain function call in, process invocation out. The consumer's knowledge of the process starts at the call signature and ends at the returned outcome and the [Error](./error.md) codes it may carry; everything between is the service's responsibility, delivered inside the SDK rather than exposed to the consumer.

### The call as delegation
A network SDK call is an agency relationship, and the [Agency](../agency.md) machinery names it precisely: the requester is the [Principal](../agency.md#principal); the serving side executes as the [Execution Agent](../agency.md#execution-agent) on the requester's behalf; the relationship is [delegation](../agency.md#delegation), and the delegation's content — responsibility, authority, boundaries, expected outcomes — is the agreed process the SDK realizes.

The security consequence the founding discussions stressed is **integrity, not access**: the delegation boundary is what keeps the process's precise execution out of the requester's control — conflict-of-interest management. The standing example: a request to transfer from one account to another must not be able to fail into debiting 1,000 units while crediting 10,000; the bookkeeping rule that prevents this is the process's own agreed rule, enforced at the executing side and never adjustable by the requester mid-call. Running such a process requester-side would put the ledger's integrity at the requester's mercy; delegating it to the module's control puts it under the party bound by the agreement — which is the point of the delegation.

The precondition is the agreement itself: a delegation is only trustworthy when the process has actually been agreed beforehand — the two parties hold the same declared process, and neither can redefine it during execution. The SDK is how that agreement travels: not as a promise in a document, but as the generated code both sides already conform to.

### Aggregation and the cache
The founding discussions fixed two capabilities the SDK carries, against a concrete alternative — pushing aggregation into a service-side endpoint (the GraphQL-style answer to over- and under-fetching):

- **Caching.** The SDK owns a cache strategy for the service's responses — the service's developer chooses it, because invalidation cost follows from the service's own consistency semantics. Pushing composition server-side forces the cache problem into the service layer: composed responses cache data from several sources of truth, so a change in one model invalidates composed caches through cross-model invalidation logic the service must now implement. With the cache in the SDK, invalidation follows the data's own source of truth, and each service's responses cache independently of every other's.
- **Composition.** What a GUI screen needs from several services is composed by that GUI's code calling several SDKs — or, where the same composition recurs across consumers, by a dedicated composing layer — not by the service growing aggregate endpoints. The service-side aggregate endpoint couples one view's needs into every service's implementation and re-opens the access-control and partial-failure questions at each aggregate ([the founding discussion's example](./sdk.changelog.md): an aggregated user model mixing viewable and non-viewable fields forces per-field access decisions into the aggregate, or error outcomes for whole calls).

The position is granularity, not machinery: a service may *additionally* offer coarse operations where its domain genuinely has them; what it may not do is treat consumer-side composition as the service's problem to absorb by default. The cache-strategy variables the SDK exposes (what to cache, for how long, against which invalidation signals) are a design-session question — the position settled here is placement, not the strategy vocabulary.

### Errors across the boundary
Error handling is part of the delivered interface, not consumer improvisation. The position: errors crossing the boundary are numeric codes ([Error](./error.md)), and the generated SDK maps them — to consumer-language error values, to typed outcomes — so no consumer ever parses error text, and error coverage is checked where it can be checked mechanically (at compile time in compiled languages). The concrete error's own fields stay service-side or route to logging per the [Error protocol](./error.md) discipline; the SDK's job is boundary mapping only. Error documentation for humans is a specification concern beside the SDK, never its substitute.

### Relationship to other protocols
- **[Media Type](./media-type.md)** — the media-type scheme (`domain/...` with `type`, `package`, `name` parameters) is the addressing layer the SDK's generated artifacts attach to: a service's structures are addressed canonically, and "easily generate SDK in any programming language" is that protocol's stated goal, with this document supplying the concept those generated artifacts realize.
- **[sRPC](./sRPC.md)** — a transport the generated SDK may target; the SDK consumer sees function calls, not frames. The SDK/transport split is what allows transports to change without consumer impact ([Working positions](#working-positions) 4).
- **[GUI](./gui.md)** — the GUI protocol's "the GUI does not speak the network" position is this protocol's consumer rule applied to the graphical case, with the accessor/setter pattern ([GUI](./gui.md)) as the validation-sharing mechanism the SDK's generation includes.
- **[Error](./error.md)** — the error-coding discipline the SDK's boundary mapping realizes.
- **[Modularity](../modularity.md)** — the SDK is part of the module's realization of its protocol ([Part of the module, not beside it](#part-of-the-module-not-beside-it)); the local/network realization split behind one call surface is [Modularity Is Not Deployment](../modularity.md#modularity-is-not-deployment) at the call level.
- **[Process](../process.md)** — an SDK call invokes a process opaquely ([Invoking a process](#invoking-a-process)); the SDK is the mechanism-independent process boundary made real for consumers.
- **[Agency](../agency.md)** — a network call is Principal–Agent delegation with the serving side as Execution Agent ([The call as delegation](#the-call-as-delegation)); integrity of the agreed process is the delegation's purpose.

## Results
Insufficient time has passed since these positions were adopted to report real, observed outcomes from implementing against them. This section will be filled in once there is such experience to draw on.

# SDK Changelog

## Changelog

### Founding positions recorded from public developer discussions
- Time: 2026-09-08T16:20:34Z
- Type: Added
- Cited:
  - [GUI](./gui.md) — Reference: the GUI protocol already states the consumer-prohibition rule for graphical clients and relies on SDK-mediated access; this document generalizes the rule to every consumer and grounds that assumption.
  - [Media Type](./media-type.md) — Reference: declares "Easily generate SDK in any programing language" as a goal; this document supplies the concept that goal points at.
  - [Error](./error.md) — Reference: the numeric error-coding discipline the SDK's boundary mapping adopts.
  - [Process](../process.md) — Reference: already names the SDK among legitimate retry initiators; consistent with the responsibility allocation recorded here, nothing changed there.
- Propagates to:
  - gui.md: Done — the broken SDK link in the architecture position corrected to `./sdk.md` (recorded in [gui.changelog.md](./gui.changelog.md)).
  - media-type.md: Pending — the "Easily generate SDK" goal line gains a forward link to this document when the SDK document stabilizes.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via ZCode) — extracted, recorded

#### What changed
- Created as the concept record of Memar's SDK protocol: what an SDK is (the client-side deliverable realizing the service's contract, derived from the contract declaration, one deliverable per consumer language) and what it is not (a specification; a general utility library).
- Eight working positions recorded: service-owned responsibility; specification is not a deliverable; operational decisions (cache, error mapping, validation) travel in the SDK; consumers write no network code; aggregation is a consumer-side capability; numeric error transmission; per-language derivation from one contract with revision identity; compile-time generation in compiled languages.
- Boundary topics recorded: the responsibility chain (service developer → generated SDK → consumer), aggregation and the cache (against service-side aggregate endpoints), errors across the boundary, and the relationships to Media Type, sRPC, GUI, and Error.
- The GUI architecture position's broken SDK link (`../sdk.md`, resolving to a nonexistent `docs/sdk.md`) corrected to `./sdk.md`.

#### Related work
- OpenAPI (formerly Swagger) — the dominant specification-first delivery the position rejects as the default: an interface document handed to consumers, leaving client production to every consuming organization — and, in the intra-organizational case, to the frontend team generating its own client from the backend's document.
- gRPC — the ecosystem's closest approach: stub code generated from interface definitions, delivered by the service side; assessed in the founding discussions as not having displaced specification-first delivery.
- GraphQL — service-side aggregation examined and rejected as the default answer to over-/under-fetching (see [Aggregation and the cache](./sdk.md#aggregation-and-the-cache) in the base document).
- Repository pattern — identified in the founding discussions as derived from the SDK pattern: the same independent-access-layer shape applied to data access.
- Vendor platform kits (hardware/OS vendors' toolsets) — the ecosystem's broad "SDK" usage, quoted as background in the founding discussions; a different sense from this protocol's subject.

#### Deliberation
- The positions were argued across public developer-community discussions spanning 2020 through 2024 — the Gommunity, gopherconf.ir, and Go Engineers groups (Omid Hekayati — claimed).
- Frontend teams' preference for human-readable protocols was diagnosed as a symptom of missing SDK delivery: with a delivered SDK, wire-format readability stops being the deciding factor (Omid Hekayati, Gommunity, 2020-09).
- GraphQL-style service-side aggregation was criticized as moving expensive work that belongs in the SDK into the backend (Omid Hekayati, Gommunity, 2020-09).
- A prototype SDK — an automatically generated JavaScript client for a Go backend service — was demonstrated: no part of the GUI software communicates with the backend directly; everything calls the generated functions (Omid Hekayati, gopherconf.ir, 2021-11).
- Numeric error-code transmission, covered by the SDK at compile time, was argued against monolingual error text on the wire (Omid Hekayati, gopherconf.ir, 2021-12).
- The absence of delivered SDKs was named the ecosystem's visible failure whenever consumer and service are developed in different languages (Omid Hekayati, gopherconf.ir, 2022-06).
- Runtime-reflection-based client production was rejected for compiled languages; code generators preferred (Omid Hekayati, gopherconf.ir, 2022-07).
- Handing over an OpenAPI JSON instead of an SDK was named the ecosystem's default deferral — "the problem is everyone else's" (Omid Hekayati, gopherconf.ir, 2022-07).
- The repository pattern was identified as derived from the SDK pattern (Omid Hekayati, gopherconf.ir, 2023-05).
- The CQRS aggregation debate was resolved for this protocol's purposes by cache placement: with the right cache strategy in each module's delivered SDK, the module stays the responder of its own capability, and composed models avoid cross-model cache invalidation (Omid Hekayati, 2023-06; the accompanying diagrams live only in the chat exports — see the handoff).
- Client-side process composition was claimed: business rules stay in their own services; the processes relating to a domain (the invoice example) take shape in the GUI or the SDK (Omid Hekayati, gopherconf.ir, 2024-10).
- The missing topic was identified on 2026-09-08 while consolidating the Telegram-sourced idea migration into the documentation set: the other ideas had landed; the SDK had not (Omid Hekayati — claimed). Super Z (GLM-5.3-Flash via ZCode) extracted the founding claims from the author's own messages only and structured the document under the current documentation method.

#### Considered and not done
- Renaming the protocol (candidates considered: Client, Binding, Service Client) — not done: gui.md, media-type.md, process.md, and the founding discussions all use SDK, and the word's general sense covers the concept; the narrowed meaning is defined in the base document. Final naming stays an open question in the handoff.
- Drafting the normative generation and tooling specification now — not done: generation mechanics (the contract declaration's location, the generator's input) need a dedicated design session; this document fixes ownership and the direction of derivation only.
- Restating the CQRS/cache analysis as a critique section in the body — not done: it serves the audit reader, so it lives here (Related work, Deliberation) per the relevance discipline; only the settled placement position entered the body.

---

### Four framework anchorings added: module conformance, dual invocation, process opacity, delegation
- Time: 2026-09-08T18:10:35Z
- Type: Expanded
- Cited:
  - [Modularity](../modularity.md) — Depends_on: this entry's module-conformance and invocation positions rely on Modularity's Module/Process/Protocol distinction and its Modularity-Is-Not-Deployment position, linked rather than restated.
  - [Process](../process.md) — Reference: the mechanism-independence of a process ([Definition](../process.md#definition)) is the grounding for the process-opacity position.
  - [Agency](../agency.md) — Depends_on: the delegation position is stated through Agency's Principal, Delegation, Execution Agent, and Contracts machinery.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via ZCode) — recorded

#### What changed
- Four working positions added (9–12): the SDK as part of the module's own protocol realization; two invocation kinds (local, network) behind one call surface; opaque process invocation; the network call as delegation under a pre-existing agreement.
- Four topic sections recorded: [Part of the module, not beside it](./sdk.md#part-of-the-module-not-beside-it), [Local and network invocation](./sdk.md#local-and-network-invocation), [Invoking a process](./sdk.md#invoking-a-process), [The call as delegation](./sdk.md#the-call-as-delegation) — the last carrying the founding transfer example (debit 1,000 / credit 10,000) as the integrity test case.
- The relationships section now covers concept documents as well as protocols; Modularity, Process, and Agency entries added. The Abstract updated to carry the four anchorings.

#### Deliberation
- The SDK is part of the module's protocol and implementation — without the client-side face, the module's protocol surface stays incomplete, and the vacancy is filled by consumers re-deriving the contract (Omid Hekayati — claimed).
- Modules present two kinds of API: local invocation, needing no other application instance; and network invocation, whose code execution must happen under another node's control, for the security of the process's processing (Omid Hekayati).
- The SDK's essential act is invoking a process without the consumer knowing much about the process itself — a plain function or method call (Omid Hekayati).
- The network call is a request to another agent to perform a process on the requester's behalf; the reason is again processing security — managing the conflict of interest so the requester cannot alter the process mid-flight. The founding example: an account-transfer request must not fail into debiting 1,000 while crediting 10,000, violating the transaction/bookkeeping process agreed in advance; the agreement's actual existence is the precondition (Omid Hekayati).
- The four claims were anchored to the framework's existing positions — Modularity's Module/Process/Protocol distinction and deployment independence, Process's mechanism-independence, Agency's Principal/Delegation/Execution Agent machinery — rather than introducing new terms (Super Z — recorded).

---

### Vocabulary corrected: contract rejected; invocation reframed as agency-space crossing
- Time: 2026-09-09T05:34:47Z
- Type: Expanded
- Cited:
  - [Protocol](../protocol.md) — Depends_on: the [Protocol vs Contract](../protocol.md#protocol-vs-contract) distinction grounds the vocabulary rejection — a contract is a legal concept carrying parties and obligations; the SDK's subject is a declared interface, and calling it a contract imports obligations that do not exist here.
  - [Networking](./networking.md) — Depends_on: the invocation reframing relies on Networking's scope position — a network exists wherever two computing entities exchange data ([Scope](./networking.md#scope)), not only between machines.
- Propagates to:
  - gui.md: Pending — the architecture position's "keeps the service contract in exactly one place" phrase may adopt the declaration vocabulary when the SDK document stabilizes.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash via ZCode) — recorded

#### What changed
- The word "contract" removed from the base document's current vocabulary — replaced by the service's declaration / declared interface — throughout: the definition, the derivation paragraph, positions 7–9, the responsibility chain, the specification boundary, and the error topic.
- Position 7 rewritten: the declaration binds no consumer language — a consumer in a language the module does not serve consumes the same declared interface through FFI against the delivered realization, a port to its language, or another consumption path, without re-deriving it (the founding example: a Go caller consuming a module whose SDK is delivered in Khayyam).
- Local and network invocation reframed: the separating boundary is the application's agency space, not hardware and not instance topology — with the standing instance that an operating system such as Android delivers an SDK to the applications it hosts, and an app calling OS capabilities is consuming another application's SDK in the full sense.
- The paired handoff's question titles and states moved to the new vocabulary ("declaration artifact", "delivery and versioning"), and a new open question registered: correctness ownership of non-generated consumption paths (FFI, ports).
- Relation labels in the previous entry corrected from Depends_for to Depends_on (this document relies on Modularity and Agency, not the inverse).

#### Deliberation
- "Contract" was rejected as the delivery vocabulary: like entity and object in the software ecosystem, the word distorts more than it carries — not unrelated to the intent, but transferring too few of the ideas behind it to be worth using; the Protocol-vs-Contract distinction (parties and obligations) makes the attribution wrong (Omid Hekayati — claimed).
- Language mismatch was named a non-problem: a caller wanting Go while the module delivers its SDK in Khayyam consumes via porting or FFI without any violation — so the declaration cannot be said to bind languages (Omid Hekayati).
- "Network" was reframed per networking.md: not two applications on two different machines — the defined path out of one application's agency space into another's; Android's OS-delivered SDK named as a genuine SDK instance (Omid Hekayati).
- The two critiques were applied the same session (Super Z — recorded).

#### Considered and not done
- Rewriting the two earlier entries' vocabulary — not done: changelog entries are append-only history recording the artifact's state when made; this entry records the correction instead. The one exception applied: relation labels in the previous entry (authored in this same working thread, uncommitted) were corrected in place and disclosed above.

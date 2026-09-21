---
Title: "Reevaluating HTTP as a Default Application Protocol"
Status: Draft
Start Date: 2026-09-21
ID: 497223
---

# Reevaluating HTTP as a Default Application Protocol
This document deconstructs the default validity of HTTP as an application, session, and addressing model; shareable locators remain a real job and are not the target of the deconstruction.

## Abstract
HTTP is a protocol surface owned outside Memar, not a concept Memar defines, and not the default primitive for application calls, session handoff, or addressing in systems Memar governs. Its URL is asked to be a shareable locator, a carrier of request data, and a carrier of credentials at once; the protocol also leaves a second optional place for the same request (the payload) while already providing non-locator credential channels (`Authorization`, `Cookie`). Navigational primitives are GET-shaped, so session handoff that rides them inherits locator leakage — history, `Referer`, access logs, caches keyed on the URI — which are correct behaviors of a locator and therefore the wrong channels for a secret. Cookies reconstruct, at the application layer, connection state the protocol's "stateless" slogan had hidden. This document does not ban HTTP and does not retire shareable locators; a locator remains needed even when the consumer is a native application. It performs the same check [filesystem](./filesystem.md) performs for storage: set aside the default that a system is an HTTP application, and decide, concern by concern, whether HTTP is the surface wanted. The companion [HTTP Practice](./http.practice.md) turns that check into criteria.

## Introduction

### Motivation
Systems continuously default to HTTP as the application protocol and to the URL as the place every parameter belongs — including the credential that establishes a session on another origin. That default is inheritance from a document-retrieval protocol, not an examination of the jobs being performed. The friction is then treated as a hygiene list (do not put tokens in query strings; set `Referrer-Policy`; call `replaceState`) that patches instances while the generating rule survives: the locator, the request, and the session are still one string. A short credential lifetime does not restore a clean model; a mental model that treats TTL as permission to overload the locator will keep producing the same class of leak, because the locator's channels do not consult TTL before recording. We must ask which of HTTP's jobs are still jobs, and which are inherited collisions.

### Methodology
The analysis reads HTTP as its own specifications describe it — URI syntax ([RFC 3986](https://www.rfc-editor.org/rfc/rfc3986)), HTTP semantics ([RFC 9110](https://www.rfc-editor.org/rfc/rfc9110)), cookies ([RFC 6265](https://www.rfc-editor.org/rfc/rfc6265)), Bearer tokens ([RFC 6750](https://www.rfc-editor.org/rfc/rfc6750)), caching keyed on the request target ([RFC 9111](https://www.rfc-editor.org/rfc/rfc9111)) — and asks which jobs those rules actually serve. Claims about locator leakage rest on behaviors those specifications and deployed clients already define, not on a replacement protocol. This document specifies Memar's position on depending on HTTP; it does not specify a replacement application protocol. The positive counterparts it presupposes live in [Content](../content.md) (reference versus locator), [sRPC](./sRPC.md) (independent identities), and [Networking Connection](./networking-connection.md) (connection state owned by protocol logic). The Networking-layer rule that an address carries only destination information appears here only as its HTTP instance.

## Explanation

### Memar's Stance on the HTTP Protocol Surface
HTTP is not a concept Memar defines: it is a protocol surface owned outside Memar, with stable, externally specified rules. Memar's own stack is expected to be able to speak that surface where interoperability with the existing Internet requires it, rather than inherit it as the shape of every application call. This is why this document lives in [`protocols/`](./README.md): it does not answer "what is HTTP?" (the general meaning governs — see [Terminology → The Default Meaning of an Unreferenced Term](../terminology.md#the-default-meaning-of-an-unreferenced-term)); it answers "what is Memar's position on depending on HTTP?"

That stance has one content: **in Memar's stack, HTTP is a high-level interoperability library — a guest protocol from the inherited Internet, whose inclusion is a decision — not the foundation of application, session, or addressing models.** The prevailing default inverts this: because browsers, gateways, and teaching materials present HTTP as how programs talk, developers design services, session handoff, and even new RPC protocols as if the URL were the addressing model. This document is a deep critique of that inheritance; the topics below supply the evidence. Its function toward the builder is a warning with an action attached: **set aside the old default that you necessarily need HTTP as the application protocol, and actually check whether you want the need** — for a shareable locator a human can pass, for a document a browser must fetch, for a peer that only speaks HTTP, the surface may well be the right answer. What is not acceptable is choosing it by default, without the check, or designing a new application protocol as a re-encoded URL. The check itself is operationalized in the companion [HTTP Practice](./http.practice.md).

### Three Jobs Collapsed into One String
The URL is asked to do three different jobs:

1. **Locator** — a shareable address for retrieval. This job is real. [Content → Reference vs. Locator](../content.md#reference-as-a-relation-not-a-property) already separates a semantic reference from a retrieval mechanism; a native application still needs a locator when a person or another system must point at a resource. Retiring HTTP would not retire this job.
2. **Request data** — parameters of a call (what to do, with which arguments). This is RPC content. It belongs in a payload whose representation is decided once per resource class.
3. **Credential** — the secret or ticket that establishes who the caller is, or that hands a session to another origin. This is session content. HTTP already has non-locator channels for it: the `Authorization` header ([RFC 6750](https://www.rfc-editor.org/rfc/rfc6750)) and the `Cookie` header ([RFC 6265](https://www.rfc-editor.org/rfc/rfc6265)). A credential belongs in one of those, in a payload, or in a session mechanism of the destination origin — not in the locator.

The security failure of a session token in a query string is a special case of this collapse, not a separate hygiene topic. UTM parameters, UI mode flags, and similar request context sitting in the same string are the same architectural smell at lower severity: they are not secrets, but they are still request data living in a locator. Patching only the secret leaves the generating rule in place.

A short-lived credential does not split the jobs. Locator channels record what they are given; they do not honor the issuer's TTL. A model that says "the token expires in minutes, so the URL may carry it" has decided that uncertainty in the locator is acceptable. That is the mental model this document rejects, independent of any one token's lifetime.

This cut is by *job*. A different cut — by *identity* of destination, handler, operation, and request instance — is [Four Identities Collapsed into One String](#four-identities-collapsed-into-one-string). A credential stuffed into a query string is both: job 3 living in the locator, and request identity living in the routing address.

### Four Identities Collapsed into One String
Routing identity (which destination), service identity (which handler), operation identity (which kind of call), and request identity (which instance of the call) are four distinct concepts. HTTP's URL commonly encodes all four in one path-and-query string for convenience — a host and path for routing, further path segments or query keys for the service and operation, and more query keys for the instance (session tokens, request ids, user ids). Convenience is not a decomposition.

[sRPC](./sRPC.md#independent-identities) is the positive counterpart at the application-protocol layer: Service ID, Stream ID, the Service Frame's `Time` field, and Payload are separate representations, and none of them is a path segment. That independence is sRPC's own design; this document records the inherited collapse it separates from. HTTP may still *carry* sRPC as an adaptation — the http-uri multiplexer form recorded on [sRPC → Service ID](./sRPC.md#service-id) is that adapter, not sRPC's addressing model.

### Two Optional Places for One Concept
HTTP allows request data in the query string, in the payload, or in both. That is two optional places for one concept. The smell to forbid is not "query strings exist"; it is leaving the representation of a resource class undecided, so each caller invents a split. One concept, one representation, decided once per resource class.

Query-as-locator-modifier (which document, which projection) and payload-as-request are a legitimate split only when the two actually are two concepts — [locator versus call](#three-jobs-collapsed-into-one-string) — not when they are two encodings of the same arguments. Headers are not a third optional encoding of the same request: `Authorization` and `Cookie` are the protocol's decided credential channels, which is why moving a secret out of the locator and into them is a split of jobs, not a second optional place for the same arguments.

This is the HTTP appearance of a Networking-layer rule: an address contains only the information required to determine the destination; request data does not belong in the routing address.

### Navigation Is GET-Shaped; Payload Handoff Still Exists
Links, address-bar entry, and typical `Location` redirects cause the consumer to issue GET. GET's content is not well-defined in HTTP semantics; user agents do not send a payload when following a link. A session handoff that uses those primitives therefore has nowhere to put a credential except the locator — unless it stops using those primitives for the credential.

HTTP still offers payload-bearing and header-bearing handoff. A top-level form POST to the destination origin is a first-party navigation: the destination may establish its own session (`Set-Cookie` on itself, or an `Authorization` exchange) and answer with `303` to a locator that carries no credential. A dedicated exchange service that accepts the credential in a request payload, then returns a locator or sets a destination-origin session, is the same split. Two documents that already share a browsing context can pass a credential in a message between origins without placing it in either locator. A one-time, tightly bound code in a locator, consumed once and followed by `303` to a clean address, is a degraded fallback for when GET is unavoidable — the code is still locator leakage, accepted only because its reuse window is closed by the issuer, not because the URL became a correct place for secrets.

Treating "the browser navigates with GET" as "the only HTTP solution is a query string" is the inherited default this document suspends. Cross-origin `fetch` plus `Set-Cookie` is not a reliable substitute: third-party cookie rules increasingly block a script on origin A from establishing a cookie on origin B. Top-level navigation to B, or a message into a document already on B, are the HTTP-era shapes that remain first-party.

### Locator Leakage Is a Property of the Locator Job
A locator is recorded because it is a locator. These are correct behaviors of a shareable address, not misconfigurations a careful application can fully close:

- Browser history, including after a later `replaceState` of only the current entry.
- The `Referer` header on subsequent requests.
- Server and intermediary access logs.
- Shared and private caches keyed on the request target ([RFC 9111](https://www.rfc-editor.org/rfc/rfc9111)): a credential in the query becomes part of the cache key and can be stored and replayed.
- Crash and analytics captures of the current address; sync of history across devices; human sharing.

The URI fragment ([RFC 3986](https://www.rfc-editor.org/rfc/rfc3986#section-3.5)) is not sent to the server and therefore does not appear in server logs, which is why the implicit OAuth flow put tokens there. It remains in history, is visible to script on the page, and is visible to anything that can read the current address. It is still a locator channel.

Putting a credential in a locator therefore publishes it through every channel locators correctly use. `history.replaceState` after the fact, `Referrer-Policy`, and log redaction are damage control around a locator that already received a secret; they are not a design that kept the secret out.

RFC 6750 already forbids Bearer tokens in page URLs for this class of leakage. The deeper rule this document adds is that the same channels make the locator the wrong home for any credential, including tickets marketed as short-lived, until the issuer has evidence the locator never held them.

### The Stateless Slogan and Cookie Reconstruction
HTTP is widely described as stateless. Its own specifications define persistent state mechanisms: cookies, session lifetimes, keep-alive. The slogan names the fact that request identity is not a first-class protocol field, not the fact that no state exists. Because that state is hidden from the layers that need it, frameworks reconstruct it at the application layer — cookie jars, session stores, replay of credentials on every call — inconsistently, and worse than a connection component that owned and exposed the state could have done.

[Networking Connection](./networking-connection.md) states the positive contract this reconstruction violates: a connection's state is owned by the component that runs the protocol logic and is exposed to the layers above. This document owns the HTTP instance of that failure.

### HTTP-Shaped Traffic Is a Deployment Constraint
Protocols riding on HTTP pass through filters that expect HTTP; other shapes get blocked. That is a deployment constraint of a specific era and region, not an architecture. Designing the stack around a current filter's expectation guarantees the architecture inherits that filter's lifetime. Where deployment reality forces HTTP-shaped traffic today, the dependence check — not dogma — decides, and the check may well say yes. [Networking → Memar's position on the traditional network stack](./networking.md#memars-position-on-the-traditional-network-stack) states the same rule for the OS-embedded stack generally; this topic is the HTTP-shaped case.

### Guest Use: HTTP as Interoperability, Not as Model
HTTP remains a justified surface when the check says so: a document a browser must fetch; a locator a person must share; a peer that only speaks the existing Internet; an adapter that carries a Memar protocol to such a peer. In those cases HTTP is a library and a projection — the way [filesystem](./filesystem.md) remains a justified projection over a richer store, and the way a file explorer is a UI over that store rather than the store's model. A shareable HTTP URL may project a Memar address; it must not become the address.

What guest use does not license is copying HTTP's collisions into Memar's own protocols: a new RPC that is a URL with a different encoding, a session model whose default handoff is a query parameter, or an address that carries request data because HTTP's address did.

### Implications
Adopting this position forces three consequences whether or not anyone wants them:

1. Session handoff across origins, if it uses HTTP at all, must use a payload-bearing or header-bearing exchange and land on a locator that holds no credential — [Navigation Is GET-Shaped; Payload Handoff Still Exists](#navigation-is-get-shaped-payload-handoff-still-exists).
2. A shareable locator may still be minted; it contains only destination information. Request data and credentials stay out of it — [Three Jobs Collapsed into One String](#three-jobs-collapsed-into-one-string).
3. A Memar application protocol is not specified as a URL. Independent identities are [sRPC](./sRPC.md)'s contract; this document only forbids copying the collapse.

---
name: http
description: replaces the default assumption that a system is an HTTP application — and that session handoff is a GET with query parameters — with an explicit, per-concern need-check and recorded decision
---

# HTTP Practice

> **Purpose:** This practice operationalizes [http.md](./http.md): it turns that document's warning — set aside the default that you necessarily need HTTP as the application protocol — into a followable check with explicit criteria. The critique and its arguments live in the base document and are not restated here; each criterion below links to the topic that argues it.

---

## The Default to Suspend

*"Every application is an HTTP API; cross-origin session handoff is a GET whose query string carries the token."*

Under Memar's stance ([http.md → Memar's Stance on the HTTP Protocol Surface](./http.md#memars-stance-on-the-http-protocol-surface)), HTTP is a high-level interoperability library whose inclusion is a decision. This practice is that decision procedure.

---

## When to Run the Check

Run it when any of these appears in the work:

- a new service, SDK, or application protocol is being designed and "the URL" or "the endpoint" shows up as the addressing model;
- session or identity must move from one origin or application to another without a second login;
- a shareable address (invite, deep link, QR, message) is being minted;
- a Memar protocol is being adapted to ride on HTTP for a browser or an existing-Internet peer;
- an HTTP dependency is being inherited from an existing project without examination.

---

## The Need Check

Answer each question about **one concern at a time** — the answer may differ per concern within the same system. Do not answer for "the system" as a whole.

1. **Which of the three jobs is this string doing?**
   Locator, request data, and credential are different jobs ([Three Jobs Collapsed into One String](./http.md#three-jobs-collapsed-into-one-string)). If the same string is doing more than one, split them. A shareable locator may remain HTTP; the request and the credential may not ride it.

2. **Must a human or another system share this address?**
   Yes → a locator is justified ([Content → Reference vs. Locator](../content.md#reference-as-a-relation-not-a-property)); mint one that holds destination information only, not request data or credentials ([Three Jobs Collapsed into One String](./http.md#three-jobs-collapsed-into-one-string)). No → do not invent a URL in order to have somewhere to put parameters.

3. **Is the consumer a browser document, a native process, or a machine protocol?**
   Browser document or existing-Internet peer → HTTP as guest surface may win ([Guest Use: HTTP as Interoperability, Not as Model](./http.md#guest-use-http-as-interoperability-not-as-model)). Machine protocol between Memar peers → do not copy URL structure into the new protocol ([Four Identities Collapsed into One String](./http.md#four-identities-collapsed-into-one-string), [sRPC](./sRPC.md)).

4. **Where does the request live?**
   One concept, one representation, decided once per resource class ([Two Optional Places for One Concept](./http.md#two-optional-places-for-one-concept)). If HTTP is the guest surface, pick payload or locator-modifier deliberately; do not leave both optional.

5. **How does session handoff travel?**
   Not by placing a credential on a locator. Prefer a destination-origin `Cookie` or `Authorization` exchange, a payload-bearing call, a top-level POST to the destination origin followed by `303` to a clean locator, or a message into a document already on that origin ([Navigation Is GET-Shaped; Payload Handoff Still Exists](./http.md#navigation-is-get-shaped-payload-handoff-still-exists)). A one-time code in a locator is a degraded fallback, not the default, and still requires an immediate `303` to an address without the code. Short TTL does not make the locator a correct channel ([Three Jobs Collapsed into One String](./http.md#three-jobs-collapsed-into-one-string)).

6. **Is HTTP-shaped traffic being chosen because a filter expects it?**
   Record that as a deployment constraint, not as the addressing model ([HTTP-Shaped Traffic Is a Deployment Constraint](./http.md#http-shaped-traffic-is-a-deployment-constraint)). The check may still say yes; the architecture must not inherit the filter.

---

## Recording the Decision

The outcome — HTTP as guest surface for named concerns, projection-only (locators and browsers), or none — must be an explicit, recorded decision, not a silent default: Memar's framework standard is that no aspect of the design space may be assumed by default; every assumption must be the outcome of an explicit decision ([Framework → Goal-Oriented Frameworks and Purpose Space](../framework.md#goal-oriented-frameworks-and-purpose-space)). Record it where the project's decisions live (a Task or Decision artifact), with the answers above as its rationale.

---

## Anti-patterns

- Putting a session token, Bearer token, or one-time ticket in a query string or URI fragment and calling the remaining risk "acceptable TTL."
- Putting a credential in a GET URI that caches will key on.
- Designing a new RPC as path segments plus query keys.
- Treating "user agents follow redirects with GET" as "the only HTTP handoff is a query parameter."
- Using cross-origin `fetch` plus `Set-Cookie` as the session bridge and discovering third-party cookie rules later.
- Banning HTTP, or banning shareable locators — the check may well conclude *yes, use them*. The error is the default, not the outcome.
- Encoding a Memar protocol as a URL and calling the result a new protocol.

# Reevaluating HTTP as a Default Application Protocol Changelog

## Changelog

### Initial draft — HTTP as guest protocol; URL overload; handoff without locator secrets
- Time: 2026-09-21T15:36:36Z
- Type: Added
- Cited:
  - [Reevaluating the Filesystem as a Fundamental Modeling Primitive](./filesystem.md) — Extends: this document is the same kind of protocol-folder member — Memar's position on an external protocol surface — applied to HTTP rather than to POSIX/VFS.
  - [sRPC](./sRPC.md) — Depends_for: the four-identity collapse and the "re-encoded URL" caution originated as lost sRPC design rationale; the HTTP critique moves here so sRPC can state its independent identities as a positive contract.
  - [Networking Connection](./networking-connection.md) — Depends_for: the "stateless HTTP" versus cookie reconstruction instance moves here so the connection document can state state-ownership without prosecuting HTTP.
  - [Networking](./networking.md) — Depends_for: the HTTP-shaped-traffic filter case moves here; Networking keeps the general rule that a deployment constraint is not an architecture.
  - [Content](../content.md) — Depends_on: Reference vs. Locator is the reason shareable addresses survive this critique.
  - [RFC 3986](https://www.rfc-editor.org/rfc/rfc3986) — Evidence: URI syntax as the locator job.
  - [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) — Evidence: HTTP semantics, including that GET content is not well-defined and that `303` exists for POST-to-GET handoff.
  - [RFC 6265](https://www.rfc-editor.org/rfc/rfc6265) — Evidence: cookies as specified persistent state against the "stateless" slogan.
  - [RFC 6750](https://www.rfc-editor.org/rfc/rfc6750) — Evidence: Bearer tokens must not be placed in page URLs because locators leak through logs and `Referer`.
- Propagates to:
  - protocols/README.md: Done — the second membership kind now names HTTP alongside filesystem.
  - networking.md: Done — HTTP-filter paragraph reduced to the general deployment rule plus a link here.
  - networking-connection.md: Done — HTTP cookie/session prosecution removed from Motivation, Methodology, and the closing evidence sentence; positive contract remains; HTTP instance linked here.
  - networking.handoff.md: Done — address-only-destination entry now points here for the HTTP instance and keeps Networking as owner of the general principle.
  - sRPC.md: Done — independent-identities rationale added as a positive contract; http-uri form framed as adapter.
  - sRPC.handoff.md: Done — URL-critique open question graduated into this document and into sRPC's positive rationale.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, decided, requested
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — argued, drafted

#### What changed
- Created `http.md` as Memar's position on depending on HTTP: guest interoperability library, not the foundation of application, session, or addressing models.
- Recorded the URL as three collapsed jobs (locator, request data, credential) and four collapsed identities (routing, service, operation, request); credentials in query strings are an instance of that collapse.
- Recorded that short credential TTL does not restore a clean model, because locator channels do not consult TTL.
- Recorded that navigation is GET-shaped and that payload-bearing HTTP handoff still exists (top-level POST plus `303`, exchange service, inter-document message); treating GET-plus-query as the only HTTP solution is the default being suspended.
- Moved the HTTP cookie/"stateless" reconstruction from networking-connection and the HTTP-filter deployment case from networking into this document.
- Added `http.practice.md` as the per-concern need-check.

#### Deliberation
- A filesystem-like HTTP document was proposed, with HTTP remaining necessary for shareable locators even in native applications, and with sRPC-adjacent HTTP remarks relocated here as a guest protocol under a critical view (Omid Hekayati).
- Direct mention of any one product's SSO URL was excluded from the documentation; the class is credential-in-locator handoff across origins (Omid Hekayati).
- Main protocol documents must not be written as "why we did not use HTTP"; they state what they recommend, and HTTP-related critique gathers here (Omid Hekayati).
- GET-with-query is not the only HTTP-era handoff; a payload exchange service, top-level POST, and one-time codes remain available (Omid Hekayati).
- A short-lived token does not excuse an overloaded locator: a bad mental model keeps producing dirty work (Omid Hekayati).
- The document was aligned with filesystem.md's membership kind and check-not-ban stance, Content's locator distinction, and the already-open networking/sRPC handoff items (Grok).

#### Considered and not done
- **Ban HTTP, or treat it as filesystem-like "usually omit"** (rejected): locators and browsers remain real jobs; the filesystem analogy is the *check*, not the omission rate. (Omid Hekayati)
- **Leave the URL critique in sRPC as that protocol's rationale** (rejected): sRPC's job is to state independent identities; prosecuting HTTP there makes sRPC look like "HTTP but binary." (Omid Hekayati)
- **Fold the whole HTTP critique into networking.md only** (rejected): Networking owns the address-only-destination principle; HTTP's overloaded URL, GET-shaped navigation, cookies, and guest-use check are an external-surface position of the filesystem kind. (Grok; decided by Omid Hekayati as the filesystem-like file)
- **Security-checklist document ("do not put tokens in URLs")** (rejected): that patches the instance and leaves the generating collapse in place. (Grok, following Cognition's conceptual-root rule as used in the session)

---

### Review pass: headers, fragment, cache; handoff leakage removed from the body
- Time: 2026-09-21T16:20:00Z
- Type: Changed
- Cited:
  - [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) — Evidence: caches key on the request target, so a credential in the query is stored and replayable.
  - [RFC 3986 §3.5](https://www.rfc-editor.org/rfc/rfc3986#section-3.5) — Evidence: the fragment is a locator channel that is not sent to the server.
- Propagates to:
  - http.practice.md: Done — criterion 2 no longer attributes "destination only" to Content; criterion 5 includes header-bearing handoff; cache-key anti-pattern added.
  - http.handoff.md: Rejected — no new open question; the additions are body claims, not unsettled work.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — reviewed, applied

#### What changed
- Abstract tightened around the claim (URL overload, non-locator credential channels, locator leakage, check-not-ban) rather than previewing every topic as a tour.
- Methodology no longer reports that the Networking address-only-destination rule is "not yet" in networking.md, and no longer points the current-state reader at a handoff. That rule appears here only as its HTTP instance; formalization remains on networking's handoff.
- `Authorization` and `Cookie` are recorded as HTTP's decided credential channels, distinct from query-versus-payload as two optional places for the same request.
- Locator leakage now includes cache keys (RFC 9111) and the URI fragment (not a server-log bypass).
- Three-jobs and four-identities cuts are cross-linked as two decompositions of the same collapse.
- Guest use states the filesystem-parallel explicitly: a shareable HTTP URL may project a Memar address; it must not become the address.
- Implications added as forced consequences of adopting the position.
- Inbound sRPC link now targets `#independent-identities` as well as `#service-id`.
- Content citations now target the real heading [Reference as a Relation, Not a Property](../content.md#reference-as-a-relation-not-a-property); `#reference-vs-locator` was not a heading.

#### Considered and not done
- **Leave the Networking-principle "not yet in the body" sentence in Methodology** (rejected): that is working state, not method. (Grok)
- **Treat fragment tokens as an acceptable HTTP-era fix** (rejected): the fragment is still a locator channel. (Grok)

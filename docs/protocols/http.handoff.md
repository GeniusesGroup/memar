# Reevaluating HTTP as a Default Application Protocol Handoff

Open work for `protocols/http.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../documentation-handoff.md) for what a handoff is.

## Topic & Purpose
Memar's position on depending on HTTP as an inherited application-protocol surface: the URL's collapsed jobs, the GET-shaped navigation constraint, cookie reconstruction of hidden connection state, and guest use for locators and the existing Internet.

## Status
Active

## Decisions

- HTTP critique lives in this document; other protocol documents state their positive contracts and link here for the HTTP instance rather than prosecuting HTTP in their own motivation. Confidence: Decided. Alternatives rejected: leaving HTTP remarks scattered in networking-connection and sRPC (those documents then narrate "why not HTTP" instead of stating what they recommend); treating HTTP as banned (locators and browsers remain real jobs).
- Credentials in locators are an instance of URL overload, not a standalone security appendix. Confidence: Decided.
- Shareable locators remain a job even for native applications; this document does not retire them. Confidence: Decided.
- Short credential TTL does not license overloading the locator. Confidence: Decided.

## Open Questions

### Where the address-only-destination principle is written in Networking
- State: the general rule (an address contains only destination information; request data does not belong in the routing address) remains a Networking-layer claim. This document owns the HTTP instance (query versus payload, URL overload). [networking.handoff.md](./networking.handoff.md) still tracks formalizing the principle in networking.md.
- Next: when networking.md next grows a principles section, write the positive rule there and keep this document as the HTTP appearance.

### Locators as Content versus a future locator protocol
- State: shareable locators are justified here and already distinguished in [Content → Reference vs. Locator](../content.md#reference-as-a-relation-not-a-property). Whether Memar later specifies a locator protocol of its own, or leaves locators as Content's URI preference plus guest HTTP, is not decided.
- Next: do not invent a locator protocol in this document; revisit if Content's addressability work demands a wire form.

### HTTP version independence
- State: HTTP/2 and HTTP/3 change framing, not the URL's jobs or cookie reconstruction. The claims in the base document are treated as version-independent; that reading has not been checked sentence-by-sentence against RFC 9113 and RFC 9114.
- Next: a dedicated pass only if a claim is challenged as version-specific.

## Anticipated Work

- Networking.md's principles section absorbs the positive address-only-destination rule; this document stays the HTTP instance.
- Guest-use adapters (sRPC over HTTP, locators minted for humans) accumulate as worked checks in the practice, not as a catalog in the base document.

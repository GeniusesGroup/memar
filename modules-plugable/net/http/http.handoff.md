# Reevaluating HTTP as a Default Application Protocol Handoff
Open work for `http.md`. Entries are mutable current state — revised as each item moves, removed when it resolves or is dropped. See [documentation-handoff.md](../../knowledge/documentation/handoff/handoff.md) for what a handoff is.

## Topic & Purpose
Memar's position on depending on HTTP as an inherited application-protocol surface: the URL's collapsed jobs, the GET-shaped navigation constraint, cookie reconstruction of hidden connection state, and guest use for locators and the existing Internet.

## Status
Active

## Open Questions

### Locators as Content versus a future locator protocol
- State: shareable locators are justified here and already distinguished in [Content → Reference vs. Locator](../../../modules/knowledge/content/content.md#reference-as-a-relation-not-a-property). Whether Memar later specifies a locator protocol of its own, or leaves locators as Content's URI preference plus guest HTTP, is not decided.
- Next: do not invent a locator protocol in this document; revisit if Content's addressability work demands a wire form.

### HTTP version independence
- State: HTTP/2 and HTTP/3 change framing, not the URL's jobs or cookie reconstruction. The claims in the base document are treated as version-independent; that reading has not been checked sentence-by-sentence against RFC 9113 and RFC 9114.
- Next: a dedicated pass only if a claim is challenged as version-specific.

### The status vocabulary has no live home, and the status contract has nothing to answer it
- State: the two observers the status protocol demands — `GetStatusCode` at `modules-plugable/net/http/protocol/status.observers.kh:6` and `GetReasonPhrase` at `:9` — have no declarations anywhere in the realization: everything `modules-plugable/net/http/const.kh` holds sits inside the archived Go block the file opens, and `protocol/version.kh` is one line. Both archives carry the vocabulary, so the subject is HTTP's own status surface, and this module's status protocol is the only document that states the surface rather than describing a consumer of it — [sRPC](../../../modules/net/srpc/srpc.md) carries HTTP as an adapter and is not the owner.
- Blocks continuation: nothing in the toolchain — no realization resolves the two observers today. It does block treating the status contract as realized: those two observers are the surface a status code would be reached through, and there is none.
- Next: owner ruling on whether the vocabulary belongs in `const.kh`, in the status protocol, or is deliberately left to each realization, then the declarations written where that ruling puts them. Nothing is written before it.
- Carried from: Go Target Research 001 → Live problems the two archives jointly expose (`bundles/khayyam/targets/go/target.research.001.md#live-problems-the-two-archives-jointly-expose--defects-in-the-sources-and-where-each-one-was-routed`), verified 2026-10-02 and routed here 2026-10-08.

## Anticipated Work
- Guest-use adapters (sRPC over HTTP, locators minted for humans) accumulate as worked checks in the practice, not as a catalog in the base document.

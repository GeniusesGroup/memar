# sRPC — Application Protocol Changelog

## Changelog

### Wire-level cancellation and message-broker position recorded as Open Questions / Position
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — the *Requests, Cancellation, and Timeout* topic added there in the same pass; its first unresolved question defers the wire-level cancellation contract to this document.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

#### What changed
- Added two new sections: *Position on Message Brokers* and *Open Questions* (the wire-level cancellation contract deferred from process.md's context critique).
- *Position on Message Brokers* records that the standalone message broker duplicates durable persistence per message (application store plus broker store plus the hop between them), which at IoT volumes dominates the storage budget, and that the broker's mechanism belongs in a library within the application's own architecture, with the application's own store as the durability point (Omid Hekayati).
- The section also records the observation that both broker client models (sync session-driven, async trust-the-broker) lose data or structure logic around the broker precisely because the broker is a separate process (Omid Hekayati).
- *Open Questions* records the cancellation position: the framework's application protocol will need an explicit wire-level cancellation contract, whose shape is not yet designed — recorded as an open question rather than an invented frame (Omid Hekayati).
- The broker position was placed in this document rather than chapar.md or a new document, since the delivery machinery it references (acknowledgement scheme, durable queues, retry initiation) is this protocol's own subject matter (Super Z).
- The position was verified against process.md's Events principle (producer-consumer independence) so the library-relocation is not misread as coupling producers to consumers (Super Z).
- The sync/async irrationality observation was kept as a supporting note rather than letting it expand into a redesign proposal (Super Z).

---

### Independent identities stated here; HTTP collapse moved to the HTTP position document
- Time: 2026-09-21T15:36:36Z
- Type: Changed
- Propagates to:
  - http.md: Done — owns the URL's four-identity collapse as prior-art critique.
  - sRPC.handoff.md: Done — the address/identity open question graduated.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- Added *Independent identities*: routing, service, operation, and request as distinct representations — the missing design rationale, stated as this protocol's positive contract rather than as a critique of HTTP.
- The http-uri multiplexer form is framed as a guest adapter, not as addressing.
- A consumed-contract link points at [http](./http.md) for Memar's position on depending on HTTP.

#### Considered and not done
- **Write the URL critique into this protocol document's rationale layer** (rejected): that was the previous handoff's next step; it would keep sRPC narrating HTTP. The critique belongs in http.md. (Omid Hekayati)

---

### Rewrote under the current Explanation-facet method
- Time: 2026-09-21T16:15:56Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../documentation-explanation.md) — Reference: the Explanation-facet skeleton, Relevance discipline, and Progressive migration this rewrite follows.
  - [Documentation](../documentation.md) — Reference: written surface, content rule (no derivative inventories), and citation direction used to drop the languages list and keep implementations out of the protocol body.
- Propagates to:
  - http.md: Done — inbound links `./sRPC.md#service-id` and `./sRPC.md` still resolve; heading texts that produce `#service-id`, `#service-frame`, and the Service Frame `Time` mention were kept; no edit required.
  - networking.handoff.md: Done — inbound link `./sRPC.md#independent-identities` still resolves; no edit required.
  - sRPC.handoff.md: Done — Close-Stream `Reason` / Error ID recorded as an open question; the cancellation contract and library-broker wire-shape questions kept; the Process cancellation link path corrected from `../../process.md` to `../process.md`.
- Contributors:
  - [Omid Hekayati](../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../CONTRIBUTORS.md#grok) (Grok 4.6 via Cursor) — applied

#### What changed
- `sRPC.md` was brought in line with the current Explanation-facet method: YAML front matter (Title, Status: Draft, Start Date, ID), then `# Title` / `Abstract` / `Introduction` (Motivation, Methodology) / `Explanation` topics only. Protocol mechanics were preserved: frames, fields, even/odd identifier split, acknowledgement scheme, message-broker position, independent-identities rationale, and the http-uri multiplexer as a guest adapter.
- Start Date is 2020-05-10 and ID is 441408, from this repository's first recorded commit for the file (the 2020-05-10 RFC merge). Any earlier drafting date in the source repositories is unrecorded here.
- Title is `sRPC — Application Protocol` (same concept; filename unchanged).
- `Inspired of` (ICMP, QUIC / RFC 9000) left the body and is recorded in this entry's `Related work`.
- `Supported programming languages` (empty `[C]()` link, old libgo/libjs paths) was dropped from the body as a derivative inventory; implementations live in `memar-{language}` repositories per `docs/protocols/README.md`.
- Close-Stream `Reason uint64` remains a field; the legacy `// ErrorID??` comment is not treated as specified. The topic states that whether `Reason` is an Error ID is unsettled; the question moved to the paired handoff.
- The informal payload aside is a present-state sentence: Syllab is the default codec; other codecs are possible and not suggested. The Syllab link targets `./syllab.md`.
- Open questions and anticipated wire work stay in `sRPC.handoff.md`; the broker topic keeps a single pointer to that handoff. No `sRPC.practice.md` was created (the base document has no followable procedure).

#### Related work
- [ICMP — Internet Control Message Protocol](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) and [QUIC](https://en.wikipedia.org/wiki/QUIC) ([RFC 9000](https://datatracker.ietf.org/doc/html/rfc9000)) were listed in the pre-method body as `Inspired of`. They are comparative prior art, not premise evidence for a current-state claim, so they live here.

#### Considered and not done
- **Specify Close-Stream `Reason` as an Error ID** (rejected): the `??` marked the identification unsettled; guessing would invent a wire rule. (Grok)
- **Keep the supported-languages inventory in the body** (rejected): empty and stale links are a derivative inventory; the protocol document is not an implementation catalog. (Omid Hekayati)
- **Create `sRPC.practice.md`** (rejected): the base document contains no followable procedure that must migrate. (Omid Hekayati)
- **Invent cancellation or library-broker wire frames in this pass** (rejected): documentation-method migration, not a protocol redesign. (Omid Hekayati)

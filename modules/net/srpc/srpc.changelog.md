# sRPC — Application Protocol Changelog

## Changelog

### Wire-level cancellation and message-broker position recorded as Open Questions / Position
- Time: 2026-09-06T00:00:00Z
- Type: Added
- Propagates to:
  - process.md: Done — the *Requests, Cancellation, and Timeout* topic added there in the same pass; its first unresolved question defers the wire-level cancellation contract to this document.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — claimed, argued
  - [Super Z](../../../CONTRIBUTORS.md#super-z) (GLM-5.3-Flash) — reviewed, rewrote

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
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — applied

#### What changed
- Added *Independent identities*: routing, service, operation, and request as distinct representations — the missing design rationale, stated as this protocol's positive contract rather than as a critique of HTTP.
- The http-uri multiplexer form is framed as a guest adapter, not as addressing.
- A consumed-contract link points at [http](../../../modules-plugable/net/http/http.md) for Memar's position on depending on HTTP.

#### Considered and not done
- **Write the URL critique into this protocol document's rationale layer** (rejected): that was the previous handoff's next step; it would keep sRPC narrating HTTP. The critique belongs in http.md. (Omid Hekayati)

---

### Rewrote under the current Explanation-facet method
- Time: 2026-09-21T16:15:56Z
- Type: refactor
- Cited:
  - [Documentation — Explanation](../../../modules-plugable/knowledge/documentation/explanation/explanation.md) — Reference: the Explanation-facet skeleton, Relevance discipline, and Progressive migration this rewrite follows.
  - [Documentation](../../../modules-plugable/knowledge/documentation/documentation.md) — Reference: written surface, content rule (no derivative inventories), and citation direction used to drop the languages list and keep implementations out of the protocol body.
- Propagates to:
  - http.md: Done — inbound links `./sRPC.md#service-id` and `./sRPC.md` still resolve; heading texts that produce `#service-id`, `#service-frame`, and the Service Frame `Time` mention were kept; no edit required.
  - networking.handoff.md: Done — inbound link `./sRPC.md#independent-identities` still resolves; no edit required.
  - sRPC.handoff.md: Done — Close-Stream `Reason` / Error ID recorded as an open question; the cancellation contract and library-broker wire-shape questions kept; the Process cancellation link path corrected from `../../process.md` to `../process.md`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested, decided
  - [Grok](../../../CONTRIBUTORS.md#grok) (Grok 4.6 via [Cursor](../../../CONTRIBUTORS.md#cursor)) — applied

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

---

### The wire serves every participant; a consumer's text is the delivered SDK
- Time: 2026-10-10T07:22:51Z
- Type: Added
- Propagates to:
  - service-sdk.md: Done — the consumer's side of the same ruling stands there as Working position 13 and under *Local and network invocation*, which links this goal.
  - service-sdk.handoff.md: Done — *The agent as an SDK consumer* no longer holds the position and points to its homes, this goal among them.
  - docs/comparisons/mcp.001.md: Done — each citation of the moved lines, the section 11 second-opinion record's included, now names the line its sentence sits at: `sRPC.md:135` as `:136` and `:141` as `:142`.
  - bundles/khayyam/targets/go/target.research.001.md: Done — its citations now name `sRPC.md:136` for `:135` and `:139` for `:138`.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided
  - Auto (model not recorded) via [Cursor](../../../CONTRIBUTORS.md#cursor) — applied

#### What changed
- *Goals and non-goals* gains goal 4: the wire serves every participant of an exchange and the network it crosses, not one consumer — its binary form saves bandwidth and the serialization and parse work at both ends of every exchange — and a consumer's need for text, a person's or an AI agent's, is met on its own side by the service's delivered [SDK](../../process/service/rules/sdk/sdk.md), not by the wire.
- Goals 1–3 are unchanged, so references to them by line or number still hold.

#### Decision
- The goal graduates by owner ruling (Omid Hekayati, 2026-10-10) from [SDK Handoff → The agent as an SDK consumer](../../process/service/rules/sdk/sdk.handoff.md#the-agent-as-an-sdk-consumer), where it had stood as his position: a protocol is designed for all its participants, not one; binary on the wire saves the whole network's resources, which at scale is not small, and the industry's move from REST to gRPC is the precedent that wire cost matters. The precedent stays in this record; the body states only the goal.

---

### Review of the uncommitted changes of 2026-10-12
- Time: 2026-10-12T09:45:50Z
- Type: Reviewed
- Contributors:
  - [Claude](../../../CONTRIBUTORS.md#claude) (Sonnet-5.5) — reviewed

#### What changed
- Reviewed; no change needed. The added handoff entry on `Error-ID`: `modules/lib/net/http/headers/const.kh` declares `Key_ErrorID = "Error-ID"` only inside the archived block that opens the file, and `const.kh` repeats it in a comment, so "comment-only" holds. The question is left to the owner; the `protocols/` to `modules/` and link corrections are mechanical.

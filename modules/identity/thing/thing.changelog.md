# Thing Changelog

## Changelog

### Follow added
- Time: 2026-10-10T14:10:00Z
- Type: added
- Cited:
  - [A Relation Several Domains Need Is Defined Once](../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once) - Depends_on: why the relation sits on thing rather than in each domain that needs it.
  - [Separating Structure (Code) from Policy (Rule)](../../../docs/modeling.md#separating-structure-code-from-policy-rule) - Depends_on: authorization and charging are the owner's rules, attached to the relation rather than built into it.
  - [Modeling State Change as Events, Not Destructive Updates](../../../docs/modeling.md#modeling-state-change-as-events-not-destructive-updates) - Depends_on: a revocation and a failed delivery are new facts, not deletions.
- Propagates to:
  - [price-index](../../../modules-plugable/economics/price-index/price-index.md): Done - its own `follow` edge was removed and its sharing semantics now rest on this relation.
  - [replacement-cost source](../../../modules-plugable/economics/replacement-cost/edges/source/source.md): Done - a source edge implies following the source product's price under the supplier's authorization and accounting.
  - [invoice handoff](../../economics/invoice/invoice.handoff.md): Done - the inter-organization invoice item asks whether delivering an invoice, a request rather than a follow, uses the same AAA mechanism.
  - [social connections](../person/edges/social_connections/social_connections.md): Done - its candidate `Follow` label points here.
  - [newsletter](../../knowledge/content/edges-loop/newsletter/newsletter.md): Done - an open question asks whether a subscription is this relation.
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the relation; the edge document is proposed

#### What changed
- [follow](edges/follow/follow.md) adds `(thing)-[:follow]->(thing)`: an organization or a person, by its identity, follows a thing for named edge kinds, and every new fact of those edges reaches it, across organizations. Its authentication, authorization by the owner's rule through `condition_is`, and per-delivery metering that the owner's rule may charge for are stated in the edge document; delivery by push or pull, and whether delivery and metering are a pluggable capability, are its open questions.

#### Deliberation
- The follow edge is a foundational concept that can take shape in thing, because how data moves between organizations for different edges has to be answered; even a product's price update is a kind of follow, like RSS, but authentication, authorization, and accounting must be observed (Omid Hekayati, translated).

#### Considered and not done
- Keeping a follow edge inside price-index and a second inside social connections — not taken: one concern, several edges; each domain keeps only its rules for when its records may be followed.
- Placing the relation in a pluggable module — not taken for the relation; whether its delivery and metering processing is pluggable is left open in the edge document.

### Follow: questions for separate sessions
- Time: 2026-10-10T14:20:00Z
- Type: changed
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the audit
  - An AI agent in Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — audited and drafted

#### What changed
- [follow](edges/follow/follow.md)'s question on revocation no longer asks what a source does after one, which source already states; it names where each edge resting on a follow keeps that rule, now including price-index's component, which implies a follow as source does. Whether an invoice uses the same AAA mechanism is left to invoice exchange, which asks it.
- Its Open questions gained questions for separate sessions: identifying and ordering deliveries (answered, unratified), missed versions and retries, use of versions after a revocation, billing a charged follow and failed deliveries, rate limits, who may see who follows a thing, things owned outside the platform, and identity proof across organizations.

### Count unit: questions from the pricing session
- Time: 2026-10-10T14:45:00Z
- Type: added
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — decided the lessons
  - An AI agent via Cursor (model not reported by the runtime; no CONTRIBUTORS.md entry) — drafted

#### What changed
- [count_unit](edges/count_unit/count_unit.md) gained an Open questions section: whether a compound unit (kg·km, t·km, passenger-km, per hour, per month) is a count unit node of its own, as a product may declare its price's display basis in one.
- [currency](edges/count_unit/labels/currency/currency.md)'s Open questions gained a note: evaluating a price against a currency or a basket is a price index, not a rate stored on the label; and the owner's reading that money's "Exchange rates rejected as stored facts" concerns the design of the project's own currency, still to be recorded in money.
- Nothing was removed or reworded.

### Research on what the thing domain is for, its kernel, and the owner's questions
- Time: 2026-10-18T18:30:00Z
- Type: added
- Cited:
  - [Modules → Placement](../../modules.md#placement) - Reference: the kernel and pluggable tests the research applies
  - [Classification Emerges From Rules and Relations](../../../docs/modeling.md#classification-emerges-from-rules-and-relations-not-from-intrinsic-labels) - Reference: the thing read as the unclassified base node
- Contributors:
  - [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — requested the work (2026-10-18, away)
  - An AI agent (Claude, model claude-sonnet-5-5 as reported by the runtime; no CONTRIBUTORS.md entry) — researched and drafted

#### What changed
- [thing.research.001.md](thing.research.001.md) is added: eleven scenarios from several cultures and industries; a proposal that a thing is an identity with a lifecycle and identity relations (five kernel elements) and that `ThingModel` requires only its identity; five rival-model choices; a mapping of every folder; pluggable sketches (follow, identity-resolution, erasure, measurement, evaluation); twenty test scenarios; a reconciliation with the product, task, content and text researches; thirteen contradictions reported, not resolved; and twenty-one owner questions with defaults.
- [thing.handoff.md](thing.handoff.md) gains the twenty-one questions with their defaults and what each blocks, seven Next Steps, and the research in Related Artifacts.
- Nothing in [thing.md](thing.md), in any edge document, or in any `.kh` file was changed; nothing was moved or deleted.

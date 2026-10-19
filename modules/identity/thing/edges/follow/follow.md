# Follow
This identity receives every new fact of these edges of that thing, across organizations, under the followed thing's owner's authentication, authorization, and accounting.

## Model
- `(thing)-[:follow]->(thing)` — the follower, an [organization](../../../organization/organization.md) or a [person](../../../person/person.md) by its identity, follows a thing — a product, a [price index](../../../../../modules-plugable/economics/price-index/price-index.md), an organization, a [law](../../../../rights/law/law.md) — for the edge kinds it names, so every new fact of those edges reaches the follower, in its own organization or another. It is what an RSS subscription does, under AAA.
- Fields:
  - Scope — the edge kinds followed, at least one: a product's [price](../../../../economics/product/edges/price/price.md), an index's composition, an organization's announcements. An edge kind is named by its identity, not its label.
  - Delivery — push to the follower, or pull by the follower; open below.
- AAA:
  - **Authentication** — the follower's identity is verified before the edge exists.
  - **Authorization** — the followed thing's owner decides, by rule, which identities may follow which edge kinds. The rule attaches through the generic `condition_is` attachment, so this relation never references the [rule](../../../../computer/rule/rule.md) domain; evaluating it is the authorization capability's work ([access-control](../../../../../modules-plugable/management/access-control/access-control.md), [authorization](../../../../../modules-plugable/management/authorization/authorization.md)).
  - **Accounting** — each delivery is metered, and the owner's rule may charge for it ([service charging](../../../../../bundles/government/modules/payment-rails-and-service-charging/payment-rails-and-service-charging.md)).
- A delivery carries the new version of the followed edge as the owner keeps it, not a copy that replaces it. A delivery, a failed delivery, and a revocation are each a fact with its time.

## Policies (rules)
- Created by the follower, only after its identity is authenticated and the owner's rule authorizes it for every edge kind in its scope. The owner may refuse it, limit its scope, price it, or revoke it.
- Removed by the follower at any time.
- Revoked by the owner: the revocation is a new fact that references the follow, not a deletion. Deliveries stop from its time; what was delivered before stays with the follower.
- Each new version of a followed edge produces one delivery to each follower whose scope names that edge kind.
- A failed delivery is recorded — follow, version, time, reason — and is not dropped.
- Each delivery is metered whether or not it is charged; a charge follows the owner's rule in force when the delivery was made.
- The follower never edits the followed thing; following is reading.
- Thing owns the relation. Each domain owns the rules for when its own records may be followed and which of their edge kinds may be named in a scope.

## Placement
- **On thing:** a product's price, a price index, an organization's announcements, a law's updates, and an invoice's status all need the same relation: how a fact moves from the organization that owns it to an identity in another organization that asked for it. [A relation several domains need is defined once](../../../../../docs/modeling.md#a-relation-several-domains-need-is-defined-once), in the domain that covers every record those domains are; copying it into each would be several edges for one concern. [Price index](../../../../../modules-plugable/economics/price-index/price-index.md) and replacement cost's [source](../../../../../modules-plugable/economics/replacement-cost/edges/source/source.md) read this relation rather than define their own.
- **Rule stays outside:** authorization and charging are rules of the owner, attached through `condition_is` and evaluated by the capabilities that own them ([Separating Structure from Policy](../../../../../docs/modeling.md#separating-structure-code-from-policy-rule)).
- **Not a second following relation:** the candidate `Follow` in [social connections](../../../person/edges/social_connections/social_connections.md) is this relation with a person as the followed thing; what a follow between persons starts there is that family's rule.
- **Not a request:** sending a fact to a party that did not ask to follow it — an invoice to the organizations it involves — is a request, not a follow ([invoice exchange](../../../../economics/invoice/invoice.handoff.md)).

## Open questions
- Delivery: push, pull, or both, and who chooses — the follower or the owner's rule?
- Is the delivery and metering processing a pluggable capability while the relation stays on thing? [Modules → Placement](../../../../modules.md#placement) keeps a capability's edge and its processing together, so either the relation alone is structural enough for thing, or the relation and its processing move together.
- Does revocation end the edge, or only refuse further deliveries? What an edge resting on a follow does after it is revoked is its own domain's rule: a [source](../../../../../modules-plugable/economics/replacement-cost/edges/source/source.md) falls back to quotes; it is open in [component](../../../../../modules-plugable/economics/price-index/edges/component/component.md#open-questions) for an index component, and in [price index](../../../../../modules-plugable/economics/price-index/price-index.md#unresolved-questions) for a product [evaluated against](../../../../../modules-plugable/economics/price-index/edges/evaluated-against/evaluated-against.md) a followed index.
- When a staff member creates a follow for an organization, is the organization the follower, with the staff member's authority checked through [delegate](../../../../rights/delegate/delegate.md)?
- Is a newsletter subscription a follow of the publishing organization, scoped to its [newsletter](../../../../knowledge/content/edges-loop/newsletter/newsletter.md) content?
- Is delivery to another organization carried as a [request](../../../../computer/request/request.handoff.md) to that organization's service surface? Whether an invoice sent to a party that did not follow uses the same AAA mechanism is asked in [invoice exchange](../../../../economics/invoice/invoice.handoff.md).
- Is each delivery identified by the follow and the version it carries, so that a redelivered version is recognized and applied once, and does the follower apply versions in the order of their time rather than of their arrival? Yes: a delivery carries a version as the owner keeps it, and a version is a fact with its own identity and time, not an overwrite, so a redelivered version is the same fact and changes nothing, and versions are ordered by the time the owner gave them. (answered 2026-10-10, unratified)
- A follower that was unreachable: does it receive every version it missed, in order, or only the latest, and for how long and how often is a failed push retried?
- What may a follower do with versions delivered before a revocation: keep them for its own audit only, or also keep using them in values it computes and states to others — an index, a sale price — and may the owner's rule limit that use?
- How is a charged follow billed — per delivery, per period, or prepaid — to which account of the follower, and is a failed delivery charged, and who bears the cost of retrying it?
- May the owner's rule limit the rate of deliveries or pulls, for example by sending only the latest version per period, and how does the follower's record then show the versions it never received?
- Who may see who follows a thing: the owner sees its followers, but may a follower see the others, and how is a supplier kept from showing a competitor its buyers through its follower list?
- How is a thing owned by an organization not on the platform followed: by an integration the follower authorizes that reads the outside owner's published facts and records them as the follower's own observations, like a [quote](../../../../../modules-plugable/economics/replacement-cost/edges/quote/quote.md), or not at all?
- How does an owner authenticate a follower from another organization: which proof of identity does the follower's organization present, and who issues it?

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
- **Not a request:** sending a fact to a party that did not ask to follow it — an invoice to the organizations it involves — is a request, not a follow (invoice exchange).

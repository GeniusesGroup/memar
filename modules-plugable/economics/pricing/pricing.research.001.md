# Pricing Research 001 — Who owns a price, and on what basis it is shown

## Table of Contents
- [Status](#status)
- [Question and Goals](#question-and-goals)
- [Participants](#participants)
- [Starting Evidence](#starting-evidence)
- [Methodology](#methodology)
- [Findings](#findings)
- [Recommendation (unratified)](#recommendation-unratified)
- [Open Questions](#open-questions)
- [Related Artifacts](#related-artifacts)

## Status
Active

## Question and Goals
- **Questions:**
  - Which node owns a sale price: the product, the batch, or a more general supply instance that covers goods, services, and transport? — Open (recommendation below, not ratified)
  - On what basis is a price shown to a user browsing the catalogue, and must every product show one? — Open (recommendation below, not ratified)
  - Which of the four candidate models below survives the scenarios and Memar's modeling criteria? — Answered as findings; the choice between them is the owner's
- **Goals:**
  - Work each scenario through: what is priced, who states the price, what it varies by, and what a browsing user sees. — Met
  - Evaluate the candidate models against Memar's modeling criteria and against how other systems separate a product from its price. — Met
  - Give the owner a recommendation, clearly unratified, and the questions only the owner can decide. — Met
- **Scope:** sale prices of goods, services, and transport, and how they are displayed. Out of scope: the invoice's own adjustment fields (`RulePrice` naming, open in [invoice.handoff.md](../../../modules/economics/invoice/invoice.handoff.md)), the basis a price is derived from (decided: [replacement cost](../replacement-cost/replacement-cost.md), [decision](edges/pricing/pricing.md#decisions-2026-10-10)), tax, and the data-model pass for any edge.

## Participants
- [Omid Hekayati](../../../CONTRIBUTORS.md#omid-hekayati) — Questioner, Goal-setter, Reviewer (Not yet reviewed)
- An AI agent working in Cursor — Researcher. The runtime did not report its model, and [CONTRIBUTORS.md](../../../CONTRIBUTORS.md) has no entry for it.

## Starting Evidence
The owner's statements of 2026-10-10, translated, are where the inquiry starts. They are a question's origin, not a conclusion:

- "After I put the price edge on product itself I changed my mind and forgot to write it down: price does not belong to product at all, it belongs to the batch of goods."
- "But I have problems: do we promote batch to services too? How does a barber who charges by time and place handle it?"
- "Do not assume price and pricing are finished at all; there are many scenarios you must work through yourself."
- "If we force every product in the system to have a price the user can refer to, should a transport-based service show kg per km travelled as its initial display basis?"

Earlier the same day the session decided that a price is derived from current stated prices, evaluated as replacement cost, and never from the purchase invoices of stock held. It left open which edge carries a rule-stated sale price ([pricing → Open questions](edges/pricing/pricing.md#open-questions)).

## Methodology
One reasoning pass by one agent. No second cognitive system was consulted, and no organization was asked how it prices.

1. **The model as it stands** was read: [product](../../../modules/economics/product/product.md) and its [price](../../../modules/economics/product/edges/price/price.md) edge with its [storage](../../../modules/economics/product/edges/price/protocol/storage.kh) and [data model](../../../modules/economics/product/edges/price/protocol/data_model.kh); [batch](../batch/batch.md) with [cost](../batch/edges/cost/cost.md), [price-settlement](../batch/edges/price-settlement/price-settlement.md), and [exist](../batch/edges/exist/exist.md); [service](../service/service.md) with [timing-interval](../service/edges/timing-interval/timing-interval.md), [item-seat](../service/edges/item-seat/item-seat.md), [number](../service/edges/number/number.md), and [multiple-use](../service/edges/multiple-use/multiple-use.md); [best_before](../good/edges/best_before/best_before.md); [pricing](edges/pricing/pricing.md); [trade](../matching_system/edges/trade/trade.md); task [negotiation](../../../modules/management/task/edges/negotiation/negotiation.md); [count_unit](../../../modules/identity/thing/edges/count_unit/count_unit.md); invoice [item](../../../modules/economics/invoice/edges/item/item.md); the legacy [product-auction storage](../../../modules/economics/product/_import/product-auction/storage.kh).
2. **Outside material** was fetched on 2026-10-10 and read where it bears on the question:
   - [schema.org UnitPriceSpecification](https://schema.org/UnitPriceSpecification): a price carries a `referenceQuantity` ("1 EUR per 4 kWh"), a `unitCode` from the UN/CEFACT Common Code, a `billingDuration` and `billingIncrement`, a `priceType` (list price, sale price, manufacturer's suggested retail price), and a validity (`validFrom`, `validThrough`) and `eligibleQuantity`.
   - [schema.org AggregateOffer](https://schema.org/AggregateOffer): "When a single product is associated with multiple offers (for example, the same pair of shoes is offered by different merchants), then AggregateOffer can be used", with `lowPrice`, `highPrice`, and `offerCount`. An offer is "an offer to provide this item — for example, an offer to sell a product, rent the DVD of a movie, perform a service, or give away tickets to an event". In this vocabulary the price sits on the offer, and the product is what is offered.
   - [Units of measurement in transportation](https://en.wikipedia.org/wiki/Tonne-kilometre): freight is measured in mass times distance. The kilogram-kilometre is "the service of moving one kilogram of payload a distance of one kilometre", and 1 t·km = 1000 kg·km. Passengers are measured in passenger-kilometres and containers in TEU-km.
   - [Unit price](https://en.wikipedia.org/wiki/Unit_price): a retail shelf tag shows the item price and, beside it, the price per unit of weight or volume.
   - [Dynamic pricing](https://en.wikipedia.org/wiki/Dynamic_pricing): Uber "measures supply (Uber drivers) and demand (passengers hailing rides …) and prices fares accordingly", and after public criticism it capped surge prices during emergencies from 2015.
3. **Memar's criteria** the candidates were judged by: [Concept Existence vs. Model Existence](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#concept-existence-vs-model-existence) (an abstraction needs an independent responsibility, lifecycle, or boundary), [Acquired Data vs. Discovered Data](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#acquired-data-vs-discovered-data), [One Authoritative Location per Concern's Data](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#one-authoritative-location-per-concerns-data), and [Separating Structure (Code) from Policy (Rule)](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule).
4. **Procedure.** Ten scenarios were worked through, each with four answers: what is priced, who states it, what it varies by, and what a browsing user sees. Then each candidate model was tested against every scenario and the criteria.

**Limits.** The scenarios are reasoning, not observation of organizations. The EU price-indication rules on unit prices could not be retrieved (the fetch timed out), so they are not cited. A statement below about what a buyer understands is the researcher's judgment, and is marked as such.

## Findings

### The word "price" carries four things
Every scenario separates them, and the model already holds three of them in different places (researcher):

1. **Cost basis** — what obtaining another unit costs today. It is discovered, per product: [replacement cost](../replacement-cost/replacement-cost.md). It stays per product whichever node carries the sale price, because it is the cost of obtaining another unit, not a property of any lot already held.
2. **Stated offer price** — a seller's commitment: "this, at this price, in this unit, valid until then, for these buyers". It is acquired: a person or a rule acting for the seller states it. The [price](../../../modules/economics/product/edges/price/price.md) edge is this today, keyed per product and currency and versioned.
3. **Agreed price** — what one sale was made at. It is acquired and historical, and lives on the invoice [item](../../../modules/economics/invoice/edges/item/item.md).
4. **Display price** — what a browsing user sees before choosing a lot, a slot, or a seller. In most scenarios it is discovered from the stated offers: the lowest, a range, a "from", or a rate per basis unit.

The owner's question is about the second, and the display question is about the fourth. The rest of the findings keep them apart.

### Scenarios

#### Goods held in several batches bought at different costs
- **Priced:** units of one product, held as lots in one or more warehouses ([exist](../batch/edges/exist/exist.md)).
- **States it:** the seller, through a pricing rule reacting to replacement cost.
- **Varies by:** not the lot's purchase cost. That would make the batch's history the basis, which the 2026-10-10 decision rejects. Two lots of the same tinned food bought at 2000 and 2600 sell at one price. A difference between lots is legitimate only where a buyer values it: remaining shelf life, the warehouse it ships from, a grade or condition.
- **Perishables:** [best_before](../good/edges/best_before/best_before.md) measures from production time, so the lot is the only node that knows how much life a unit has left. A "reduced, best before Friday" price belongs to the lot.
- **User sees:** one price for the product, and a lot's own price only where it differs (near expiry, another city).

#### Made-to-order goods
- **Priced:** a product that does not exist yet. Product identity precedes production ([product](../../../modules/economics/product/product.md)), and a [pre-order](../../../modules/economics/invoice/edges-shortcut/pre-order/pre-order.md) points at a future production time. There is no batch when the price is stated.
- **States it:** the seller, from the replacement cost of the materials plus conversion cost, and for a configured product ([customable](../../../modules/economics/product/edges/customable/customable.md)) per configuration.
- **Varies by:** configuration, delivery date, quantity.
- **User sees:** a price, or "from" a price, for the product or configuration. A batch is created later, at production.

#### A barber charging by time and place
- **Priced:** the service of one barber in one shop for one stretch of time. The deliverable is a slot: staff × place × time. Nothing in the model holds a slot as a node before it is sold. [timing-interval](../service/edges/timing-interval/timing-interval.md) holds how long the service takes, per product, and [item-seat](../service/edges/item-seat/item-seat.md) holds the occupied seat or person-slot on the invoice line.
- **States it:** the shop. Either per service ("haircut 300 at the city-centre shop, 250 in the suburb") or per time ("400 an hour with the senior barber").
- **Varies by:** place, barber, hour of day, weekday.
- **User sees:** per service and place, "haircut from 250". Where the shop charges by time, the rate per hour together with the expected duration from timing-interval gives an estimate. That estimate is discovered, not stated.
- A batch has no analogue here. What the batch is for goods, the slot is for this service: the specific thing delivered, with its own place and time.

#### Transport priced by weight × distance (kg·km)
- **Priced:** moving a load from A to B. The deliverable is a movement: route × time × load.
- **States it:** the carrier, as a rate card or a family of [pricing](edges/pricing/pricing.md) rules (city, hour, route, zone, demand), decided 2026-09-16 as a module family.
- **Varies by:** weight, distance, city, hour, route, demand, and minimum or fixed charges.
- **The final price is computed per movement.** Memar's own example says it: "A trip's price depends on traffic level and time window, but the relationship — a purchase of a transport product — is structurally identical across all trips" ([Separating Structure from Policy](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#separating-structure-code-from-policy-rule)). The computed price is discovered, from the stated rules and the movement's facts. It becomes acquired only when it is quoted with a validity, or agreed on an invoice.
- **kg·km as the display basis:** it is a standard freight unit (1 t·km = 1000 kg·km), and schema.org's `referenceQuantity` with a `unitCode` expresses exactly "this much per that quantity". So it is a sound basis for freight sold by weight and distance between businesses. As the only display it misleads where fixed charges dominate small loads, and where city, hour, or demand rules multiply the rate. A person ordering a taxi or sending one parcel expects a price for the trip, not a rate (researcher's judgment). The basis is therefore a per-product declaration, not a unit forced on all transport: kg·km or t·km for freight, passenger-km or per trip for passengers, per parcel and zone for couriers.
- **User sees:** a rate in the declared basis with its minimum charge, or an estimate for an example movement. The payable price comes at quote time.

#### A seat or slot service (event, cinema)
- **Priced:** one seat at one showing. The showing is the instance (time, hall). The seat zone qualifies it.
- **States it:** the venue.
- **Varies by:** showing (matinee, weekend), seat zone, how early it is bought (dynamic pricing in theme parks and events).
- **The model today:** the seat id sits on the invoice line ([item-seat](../service/edges/item-seat/item-seat.md)). Capacity and minimum sales are per product ([number](../service/edges/number/number.md)). A showing has no node.
- **User sees:** showings, each with its price per zone.

#### Subscriptions and multiple-use services
- **Priced:** a plan: a period of access, or a pack of N uses ([multiple-use](../service/edges/multiple-use/multiple-use.md) caps the uses per buyer).
- **States it:** the seller, once per plan and billing period. schema.org's `billingDuration` and `billingStart` express "per month" and "price rises after the first year".
- **Varies by:** period, tier, introductory terms.
- **No supply instance carries it.** No lot, slot, or movement exists before the sale. The plan itself is the product, and its price is per product per period. This scenario is the clearest case against removing price from product altogether.
- **User sees:** price per period, and the per-use price for a pack.

#### A marketplace where several sellers offer one product
- **Priced:** one product, for example the same sofa sold by several stores ([brand](../brand/edges/brand/brand.md) records "one product, many sellers").
- **States it:** each seller, separately.
- **The model today:** product price storage keys a price by product and currency only, and its data model says a price "can be register just by producer organization whom own the related quiddity". One shared product therefore holds one producer's price, not each seller's. [Replacement cost](../replacement-cost/replacement-cost.md) instead assumes each organization owns its own product node, pointing at the supplier's through `source`.
- **Outside practice:** schema.org puts the price on each seller's offer and aggregates them for the product (`AggregateOffer`: lowest, highest, count).
- **User sees:** "from X, N sellers" — a discovered value, never a second stored price.

#### Exchange-traded goods
- **Priced:** a quantity of a fungible good, through the [matching system](../matching_system/edges/trade/trade.md).
- **States it:** no one states a sale price. Each order states a limit, or none ("market price will choose for the deals"). The price is discovered by matching.
- **User sees:** the last deal and the best bid and ask, all discovered from the order book. A price stored on the product would be a derived copy with no re-derivation path.

#### Negotiated prices
- **Priced:** one deal ([negotiation](../../../modules/management/task/edges/negotiation/negotiation.md) is "for invoice price").
- **States it:** both parties. The agreed price is acquired at acceptance and lands on the invoice item.
- **User sees:** at most an indicative price or "negotiable". The catalogue cannot show the agreed price, because it does not exist before the negotiation.

#### Quote-only products with no public price
- **Priced:** one request: an industrial plant, a building, a bespoke service.
- **States it:** the seller, per request, as a quote with a validity. The sale-side counterpart of the replacement-cost [quote](../replacement-cost/edges/quote/quote.md).
- **User sees:** "price on request". The product is still a product: [product](../../../modules/economics/product/product.md) already says products may never be priced and stay products for asset management.

### What each scenario says about the candidates

| Scenario | (a) product | (b) batch | (c) supply instance | (d) reference on product |
|---|---|---|---|---|
| Lots at different costs | fits | fits | fits (batch) | fits |
| Perishables near expiry | fails | fits | fits (batch) | fits as reference |
| Made-to-order | fits | fails, no batch yet | fits only with a planned batch | fits |
| Barber by time and place | needs rules | fails, no batch | fits (slot), no node yet | fits |
| Transport kg·km | needs rules | fails | fits (movement), no node yet | fits |
| Seat or slot | needs rules | fails | fits (showing), no node yet | fits |
| Subscription | fits | fails | strained, no instance | fits |
| Several sellers | fails | fits per seller's stock | fits | fits, discovered |
| Exchange-traded | fails | fails | fits only if an order counts as an instance | fits, discovered |
| Negotiated, quote-only | fails | fails | fails | fits ("on request") |

"Needs rules" means a single stored product price cannot express it, and a pricing rule computing per sale can. That is already decided practice ([pricing → 2026-09-16](edges/pricing/pricing.md#decisions-from-organization-ideas-backlog-2026-09-16)).

### (a) Price on product, the status quo
Simple, and right for made-to-order goods, subscriptions, and a simple shop. It fails where the same product is sold at different prices for reasons the product cannot know: a lot near expiry, a branch, several sellers. Every such case then needs a pricing rule even when the seller only wants to state a price by hand. Searching by price range (`FIND_ProductIDs_BY_CurrencyID_AND_Price_RANGE`) only works because there is one price per product. Any model with several prices per product needs a discovered display price for that search.

### (b) Price on batch, the owner's leaning
Right for goods held in lots that differ in something a buyer values: freshness, place, grade. The model already resolves one money concern most-specific-first: [price-settlement](../batch/edges/price-settlement/price-settlement.md) reads "Priority order to prefer:: Batch >> Product >> POS >> Organization". A batch price as an override of a product price would follow the same pattern.

As the only owner it fails in four ways:

- **No batch exists** for made-to-order goods at sale time, for services, for transport, or for subscriptions. The owner's barber question is exactly this.
- **Duplication.** Identical non-perishable lots carry one price, because the price comes from replacement cost per product. Storing it on each lot puts one concern's data in many locations. Each lot then holds a copy with no re-derivation path, and a single price change must touch every lot ([One Authoritative Location](https://github.com/GeniusesGroup/memar/blob/main/docs/modeling.md#one-authoritative-location-per-concerns-data)).
- **Pull toward history.** A price per lot invites deriving it from the lot's [cost](../batch/edges/cost/cost.md), which is the historical basis the 2026-10-10 decision rejects.
- **No display.** A browsing user is not choosing a lot. A product-level display has to be discovered from the lots anyway.

### (c) A general supply instance: batch for goods, slot for services, movement for transport
Conceptually the strongest answer to the owner's question. A price belongs to the specific thing delivered, and the product is its kind. Each instance kind has an independent lifecycle, which is Memar's test for an abstraction. A lot is received, held, moved, recalled, and expires. A slot is opened, held, booked, served, or lapses. A movement is quoted, dispatched, delivered.

Against it, as of today:

- Only the batch exists as a node. A slot or a showing exists only as a seat id on an invoice line, and a movement not at all.
- [service](../service/service.md) records that a shared parent with good, a "tradable thing", is "deliberately not invented until requirements force it", and that a future `schedulable` module may unify seats, device channels, and estate spaces. The barber and the cinema are evidence for that module. They do not yet force one parent over batch, slot, and movement.
- Subscriptions, negotiated deals, and quotes have no instance before the sale. They need the product, the deal, or the quote to carry the price.
- Many instances repeat one price: every barber slot at the same shop, every showing on weekdays. Storing that price per instance is duplication, as in (b). The price stays stated once, on the product or as a rule, and is applied to the instance when it is sold. A price stored on an instance is right only where the seller commits that instance to a different price.

### (d) An indicative reference price on the product, in a declared basis unit
This separates display from commitment. The product declares the basis it is shown in: a [count_unit](../../../modules/identity/thing/edges/count_unit/count_unit.md), possibly compound (kg·km, passenger-km, per hour, per month), and a reference quantity. The reference price is either:

- **stated:** a list price or suggested retail price — schema.org's `priceType` keeps these apart from the sale price; or
- **discovered:** the lowest, a range, or "from", over the offers that exist. That is stored only as a cache, an `edges-shortcut` that names what it recomputes from.

It fits every scenario, including "on request" and exchange-traded goods. It does not answer which node holds the payable price. It is a display layer over (a), (b), or (c), not a model of its own. One risk: a stated reference price and the payable prices can drift apart and mislead. A discovered reference cannot.

### A seller's offer is the missing node in all four
In schema.org the price lives on the offer: seller, item, price, unit, validity, eligible buyers. The item may be a product or one specific instance. The legacy `ProductAuction` record in this repository was such an offer: organization, product, a discount "minus from product price", an authorization naming which users and groups may buy, a type, and a status. The current price edge keeps only the price. Whether an offer earns a node, or is the price edge's own record grown with validity and eligibility, is a modeling question for the owner. The scenarios show what it has to hold. (researcher)

### Must every product show a price?
No scenario supports forcing one. [product](../../../modules/economics/product/product.md) defines a product by being priceable, not priced, and keeps products that are never sold. Negotiated, quote-only, and exchange-traded products have no price to show before a sale. What every product can show is its state: a price, a "from", a rate in its basis, "on request", "negotiable", or "market". (researcher)

## Recommendation (unratified)
The owner has not reviewed this, and nothing in it is decided.

1. Keep four things apart: cost basis per product (replacement cost), stated offer price, agreed price on the invoice item, and display price.
2. A stated sale price attaches to the most specific node the seller commits it to: the product by default, a batch where lots differ in what the buyer values (shelf life, place, grade), and later a slot or movement. Resolution is most-specific-first, as price-settlement already reads (Batch >> Product >> POS >> Organization). A batch never carries a price because its acquisition cost differed.
3. Price stays possible on the product. Made-to-order goods, subscriptions, and services without instances have nothing else to carry it. The owner's "price belongs to the batch" is read here as the goods case of "price belongs to what is delivered". That reading still needs the owner's agreement.
4. No general supply-instance node yet. Slot and movement are recorded as candidate instance kinds for the `schedulable` module that [service](../service/service.md) anticipates. Until then service and transport prices are stated per product or computed by pricing rules at quote time, and the agreed price lands on the invoice item.
5. A computed price (transport, surge, a barber's rate × duration) is not stored before it is quoted. It is discovered from stated rules and the sale's facts. It becomes acquired as a quote with a validity, or as an invoice item.
6. Do not force every product to show a price. Each product declares its display basis: a count unit, compound where needed (kg·km, t·km, passenger-km, per hour, per month), and a reference quantity. The catalogue shows a discovered display price in that basis, or a state: "on request", "negotiable", "market". kg·km is the right basis for freight sold by weight and distance, not for every transport product.
7. Replacement cost stays per product, whichever node carries the sale price.

## Open Questions
Only the owner can decide these:

1. Does price leave the product entirely, so that every sale price sits on a batch or another instance, including made-to-order goods and subscriptions? Or does a batch price override a product price, most-specific-first?
2. For services, is the instance that carries a price a slot (staff × place × time), and is it made a node now? Or do service prices stay on the product, with pricing rules, until a `schedulable` module exists?
3. May two lots of one product carry different prices for any reason besides shelf life, place, and grade? Acquisition cost is excluded by the 2026-10-10 decision. Confirm that this holds for batch prices too.
4. Must every product show a price? If not, which displayed states are legitimate: "from", range, rate, "on request", "negotiable", "market"?
5. Who declares a product's display basis: the product's own count unit, or a separate display-basis edge? Is a compound unit such as kg·km a count unit node of its own?
6. Marketplace: one shared product with a price per seller, or one product node per seller linked through `source` or `brand`?
7. Does a seller's offer (seller, item, price, unit, validity, eligible buyers) become a node of its own, as the legacy `ProductAuction` was? Or does the price edge's record grow those fields?
8. Which price does the invoice item copy at issue? This is the first of [pricing → Open questions](edges/pricing/pricing.md#open-questions), now read together with question 1.

## Related Artifacts
- [edges/pricing/pricing.md](edges/pricing/pricing.md) — its open bullet links here (Update, done)
- [pricing.changelog.md](pricing.changelog.md) — entry for this research (Update, done)
- [product price](../../../modules/economics/product/edges/price/price.md) — changes if question 1 moves price off the product (Review)
- [batch](../batch/batch.md) — gains a price edge if the batch override is ratified (Review)
- [service](../service/service.md) — slot as a candidate instance for its future `schedulable` module (Review)
- [replacement cost](../replacement-cost/replacement-cost.md) — stays per product. Its open question on which edge carries a rule-stated price is the same question as question 1 (None)
- [invoice.handoff.md](../../../modules/economics/invoice/invoice.handoff.md) — the agreed price and an invoice reaching both organizations (Related)

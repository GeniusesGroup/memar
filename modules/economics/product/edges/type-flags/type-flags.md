# Type flags

## Model

- Live flag-space on the product record (not a graph edge): one `Type uint64` iota in [product.go](../product.go) splitting **Good vs Service** (`Type_Good` — "if flag not set means product is service"; `Type_Unset` — "usually for good kind").
- **Common flags:** `Type_ReserveValidity`, `Type_ReserveQuantity` (max one person can reserve before paying), `Type_PreSale` (marked `??` — unresolved), `Type_NeedApprove` (base on product-role), `Type_NeedPrescription` (medical goods; can't be added by users to invoice), `Type_InvoiceSell`, `Type_OrderSell`, `Type_SellLimit_Role` / `Type_SellLimit_Group` / `Type_SellLimit_User`.
- **Good flags:** `Type_Inventory` (owner-tracked capital goods: book, mobile, car), `Type_Custom` (made on buyer requirements, product-ingredient), `Type_BestBefore` (daily consumption goods), `Type_CustomIngredient`.
- **Service flags** (structure comment: TimeService — consultation in chat or real life; ActService — guarding, maintenance, cleaning; Transport): `Type_TimeValidity`, `Type_Transport` ("indicate InvoiceID use to retrieve coordinate domain"), `Type_Shipping`, `Type_Content` (digital data), `Type_Timing`, `Type_TimingInterval`, `Type_MultipleUse` (gym), `Type_Duration`, `Type_Number` (cinema, concert, transport), `Type_Area`, `Type_Place` (doctor-room, gym, station/bus/train/airport), `Type_Seat` (cinema, concert, transport), `Type_Provider_Staff`, `Type_Provider_Role`, `Type_Share` (panic-room ticket).
- Header note in source: "Cinema, Rent, Therapy, Consulting, Coaching, Mentoring, FixingService, the transportation of goods and passenger, ..." — service examples riding the same flag space.

## Policies (rules)

- Good/Service is a flag pair on one product record, not two node types — consistent with the multi-typing position in [product.md](../../product.md) (a product node can simultaneously be a `thing`, content, …).
- Sell-limit and provider flags are parameters already owned elsewhere: SellLimit → rule domain (answered in [sell-limit](../sell-limit/sell-limit.md)); Provider → service pluggable (see [provider](../provider/provider.md)).
- `Type_PreSale` semantics unresolved in code (`??`) — must converge with time-window eligibility ([buy-limit](../buy-limit/buy-limit.md)) before migration.

## Placement

- **Flags stay with the product record they flag** — a flag-space is a parameter list, not processing semantics (parameters-vs-semantics ⇒ no separate module; no new home invented).
- Flag *meanings* that leak other domains migrate with their owners when those capabilities migrate: SellLimit_* → rule configuration; Provider_* → service module; coordinate-by-role (on `Type_Transport`) is a lookup recipe to strip ([coordinate](../coordinate/coordinate.md)).
- **Not core-by-necessity as vocabulary:** an org without goods/services reconfigures flags; core keeps only the ability to carry org-chosen type bits.

## Open questions

- Is the Good/Service split a flag pair or two identity lenses (per the confirmed multi-typing position in [product.md](../../product.md))?
- Do SellLimit flags belong here or to the rule domain? ([sell-limit](../sell-limit/sell-limit.md) answers: rule domain.)
- PreSale semantics unresolved (marked `??` in code) — converge with [buy-limit](../buy-limit/buy-limit.md) open questions.
- Closed kernel set or organizational-open flag vocabulary?

## Source

> Source: `modules/economics/product/edges/product.go` (in code).

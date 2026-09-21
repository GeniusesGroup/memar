# Tax
A [tax](https://en.wikipedia.org/wiki/Tax) is a mandatory financial charge or some other type of levy imposed on a taxpayer (an individual or legal entity) by a governmental organization to collectively support government spending, public expenditures, or as a way to regulate and reduce negative externalities.

In economic terms, taxation transfers wealth from households or businesses to the government of a nation.

## VAT

VAT is just like any other product, but it is in such a way that the user is forced to purchase it in exchange for no service or goods!

## Idea backlog from edge code comments

Raw proposals from comment notes in `edges/*.go` (comments remain in code as source). Nothing below is ratified.

- **Tax label catalog** (`edges/tax.go`): VAT (the comment's editorial aside aside), CustomsDuties (import), and an environmental-tax family: Green, Carbon, Severance, Fuel duty, Waste disposal + refundable fees, Plastic bags, Environmental tariff, Energy taxes, License fees. Catalog semantics from comments: up to two tax labels per context, each with a rate; multiple rates per label; blank label = VAT-exempt.
- **Tax relations** (`edges/tax-relation-*.go`): IncomeTax (tax-budget), TaxDepositAccount (tax-financial_account), tax-product accepts all tax labels, tax-rule `Value` for logic exceeding a simple percentage calculation (e.g. charity-institution discounts).
- **Review questions**: closed vs organizational-open catalog? Does tax-rule duplicate the core rule mechanism ([rule.handoff.md](../../../modules/computer/rule/rule.handoff.md) §9: fees are rules producing transactions)?
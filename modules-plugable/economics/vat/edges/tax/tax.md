# Tax

## Model

- Candidate (unconfirmed): a tax-label catalog edge — labels attached to tax records; catalog semantics from source comments: "Define up to two tax labels and associate each of them with a specific tax rate", "Associate multiple tax rates with the same tax labels", "Associate a blank tax label with tax exempt items (considered non-value-added tax (VAT))".
- Catalog values: `VAT` ("VAT as Value-Added-Tax is bad name for a robbery!" — editorial aside in source), `CustomsDuties` ("When a product want to import a country"), plus an environmental-tax family: Environmental pollution taxes / Green tax / Carbon tax / Severance tax / Fuel duty / Waste disposal taxes and refundable fees / Plastic bags / Environmental tariff / Energy taxes / License fees.

## Policies (rules)

- "Setting tax labels allows you to perform the following actions:" — up to two tax labels per context, each with its own rate; multiple rates may share one label; a blank label marks tax-exempt items (VAT-exempt).
- Label list is the vocabulary for rates and exemptions — the comment frames it as configuration performed by users, not kernel behavior.

## Placement

- **Correct here — the tax module owns its own label catalog**.
- **Not core rights/law or law labels:** [law labels tax](../../../../rights/law/labels/tax/tax.md) is a *comment* label for laws — different subject (legal commentary vs fiscal rate labels); no overlap, no move (cross-reference only).
- **Not a new "catalog" module:** an enumerable label set with rates is tax configuration, not independent processing semantics.
- Blank-label exemption ties to tax rates — travels with this module (edge + rate semantics complete together).

## Open questions

- Closed kernel catalog or organizational-open (low-code extensibility)? Environmental family reads as jurisdiction-specific — likely open per-org.
- Are the catalog names edge/label *types* or free label *values* on one generic tax edge? (Source is `package label` — labels-on-edge vs distinct edges, same review as [form](../../../../../modules-plugable/knowledge/form/edges/form/form.md).)
- "up to two tax labels" — two labels per product? per invoice line? per jurisdiction? Scope unconfirmed.
- Editorial "robbery" aside — keep as source color, not policy? The catalog entry for VAT stands regardless.


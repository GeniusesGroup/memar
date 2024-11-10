/* For license and copyright information please see the LEGAL file in the code repository */

package isp

import (
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
	qcu_p "org/modules/identity/quiddity-count_unit/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is summary data that calculated to reduce fetch and calculate on each client device.
type DataModel interface {
	invoice_p.Field_InvoiceID
	ItemCount() qcu_p.Quantity
	ProductCount() qcu_p.Quantity
	SuggestedPrice() money_p.Amount  // Total should pay before any discount or auction
	DiscountedPrice() money_p.Amount // Directly assign by users with enough authorization access (usually org staff).
	RulePrice() money_p.Amount       // the sum of all rules(vouchers+discounts+gift+auctions) apply for this invoice
	PayablePrice() money_p.Amount    // Total price user pay to organization

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}

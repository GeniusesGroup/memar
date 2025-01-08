/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	request_p "memar/audit/request/protocol"

	product_p "org/modules/business/product/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
	qcu_p "org/modules/identity/quiddity-count_unit/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// Ship service can add as an item to invoice
// Each item must check for reserve validity and make action in end of validity
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	qcu_p.Field_Quantity
	SuggestedPrice() money_p.Amount  // Total should pay before any discount or auction
	DiscountedPrice() money_p.Amount // Directly assign by users with enough authorization access (usually org staff).
	RulePrice() money_p.Amount       // the sum of all rules(vouchers+discounts+gift+auctions) apply for this product.
	PayablePrice() money_p.Amount    // Total price user pay to organization

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}

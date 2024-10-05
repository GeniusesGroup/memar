/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	product_p "org/modules/business/product/protocol"
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	SuggestedPrice() money_p.Amount  // Total should pay before any discount or auction
	DiscountedPrice() money_p.Amount // user profit from this product purchase by auctions
	PayablePrice() money_p.Amount    // Total price user pay to organization

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}

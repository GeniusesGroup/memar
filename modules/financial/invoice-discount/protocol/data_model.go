/* For license and copyright information please see the LEGAL file in the code repository */

package idp

import (
	audit_p "org/modules/computer/audit/protocol"
	discount_p "org/modules/financial/discount/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	money_p "org/modules/financial/money/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	discount_p.Field_DiscountID
	Discounted() money_p.Amount

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}

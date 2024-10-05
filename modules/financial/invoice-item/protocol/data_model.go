/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	product_p "org/modules/business/product/protocol"
	audit_p "org/modules/computer/audit/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	qcu_p "org/modules/identity/quiddity-count_unit/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// each InvoiceItem is immutable record and so use version mechanism to chain InvoiceItem in InvoiceID group.
// Ship service can add as an item to invoice
// Each item must check for reserve validity and make action in end of validity
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	qcu_p.Field_Quantity

	audit_p.Field_RequestID
	storage_p.Field_SaveTime
}

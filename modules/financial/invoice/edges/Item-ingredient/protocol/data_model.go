/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	request_p "memar/audit/request/protocol"
	audit_time_p "memar/audit/time/protocol"
	decimal_p "memar/math/decimal/protocol"

	product_p "org/modules/business/product/protocol"
	ii_p "org/modules/financial/invoice/edges/item/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	label_p "org/modules/knowledge/label/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	label_p.Field_LabelID
	product_p.Field_ProductID

	ii_p.Field_InvoiceItemID
	IngredientID() product_p.UUID
	decimal_p.Field_Quantity
	Field_Status

	request_p.Field_RequestID
	audit_time_p.Field_SaveTime
}

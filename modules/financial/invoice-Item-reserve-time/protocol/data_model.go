/* For license and copyright information please see the LEGAL file in the code repository */

package iirtp

import (
	request_p "memar/audit/request/protocol"
	time_p "memar/time/protocol"

	product_p "org/modules/business/product/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	Start() time_p.Time
	End() time_p.Time

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}

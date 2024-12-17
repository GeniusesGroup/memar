/* For license and copyright information please see the LEGAL file in the code repository */

package iipp

import (
	request_p "memar/audit/request/protocol"

	product_p "org/modules/business/product/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	staff_p "org/modules/organization/staff/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	staff_p.Field_StaffID

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}

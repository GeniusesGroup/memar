/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	request_p "memar/audit/request/protocol"

	product_p "org/modules/business/product/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

// DataModel indicate the domain record data fields.
// It can also use to order buyers e.g. patient in doctor clinic.
type DataModel interface {
	invoice_p.Field_InvoiceID
	product_p.Field_ProductID
	Field_SeatID
	Field_Status

	request_p.Field_RequestID
	storage_p.Field_SaveTime
}

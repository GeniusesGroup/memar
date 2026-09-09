/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"

	ii_p "org/modules/economics/invoice/edges/item/protocol"
)

// DataModel indicate the domain record data fields.
// It can also use to order buyers e.g. patient in doctor clinic.
type DataModel interface {
	ii_p.Field_InvoiceItemID
	Field_SeatID

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	request_p "memar/process/request/protocol"
	audit_time_p "memar/process/time/protocol"
	record_p "memar/storage/record/protocol"

	product_p "org/modules/economics/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	product_p.Field_ProductID
	SeatCapacity() uint64 // max seat number
	Field_Type
	MapID() record_p.UUID // to show background and rows and seats. suggest use SVG format

	request_p.Field_RequestID
	audit_time_p.Field_Request
}

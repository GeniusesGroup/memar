/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// It can also use to order buyers e.g. patient in doctor clinic.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ProductID() pp.ProductUUID
	SeatID() SeatID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	op "org/modules/object/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	SeatCapacity() uint64 // max seat number
	Type() Type
	MapID() op.ObjectUUID // to show background and rows and seats. suggest use SVG format

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

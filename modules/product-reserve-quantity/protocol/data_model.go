/* For license and copyright information please see the LEGAL file in the code repository */

package prqp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProductID() pp.ProductUUID
	Quantity() uint64 // fix max reserve number
	Percent() uint64  // percent of the inventory

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

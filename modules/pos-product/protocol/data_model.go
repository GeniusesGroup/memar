/* For license and copyright information please see the LEGAL file in the code repository */

package ppp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	pp "org/modules/pos/protocol"
	prp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
// Save shortcut to regular products to easily add to invoice
type DataModel interface {
	PosID() pp.PosUUID
	ProductID() []prp.ProductUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

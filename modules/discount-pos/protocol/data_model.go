/* For license and copyright information please see the LEGAL file in the code repository */

package dpp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	PosID() pp.PosUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

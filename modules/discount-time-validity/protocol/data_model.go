/* For license and copyright information please see the LEGAL file in the code repository */

package dtvp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel or LiveUntil indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	Start() protocol.Time
	End() protocol.Time

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

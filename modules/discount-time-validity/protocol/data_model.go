/* For license and copyright information please see the LEGAL file in the code repository */

package dtvp

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
)

// DataModel or LiveUntil indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	Start() protocol.Time
	End() protocol.Time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

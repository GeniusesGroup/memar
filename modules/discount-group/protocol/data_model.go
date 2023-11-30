/* For license and copyright information please see the LEGAL file in the code repository */

package dgp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
	gp "org/modules/group/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	GroupID() gp.GroupUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/* For license and copyright information please see the LEGAL file in the code repository */

package dutp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	DiscountID() dp.DiscountUUID
	UserType() protocol.UserType

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

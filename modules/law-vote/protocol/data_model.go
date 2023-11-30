/* For license and copyright information please see the LEGAL file in the code repository */

package lvp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	lp "org/modules/law/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	LawID() lp.LawUUID
	UserID() up.UserUUID
	Vote() Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

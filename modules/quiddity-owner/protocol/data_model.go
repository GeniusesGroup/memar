/* For license and copyright information please see the LEGAL file in the code repository */

package qop

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	qp "org/modules/quiddity/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	QuiddityID() qp.QuiddityUUID
	OwnerID() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

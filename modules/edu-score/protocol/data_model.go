/* For license and copyright information please see the LEGAL file in the code repository */

package esp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	OrgID() org.OrgUUID
	UserID() up.UserUUID
	Score() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ProjectID() ProjectUUID
	UserID() up.UserUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

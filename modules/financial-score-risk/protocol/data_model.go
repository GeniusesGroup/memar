/* For license and copyright information please see the LEGAL file in the code repository */

package fsip

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

// DataModel
// Store user risk to prevent or detect frauds
type DataModel interface {
	UserID() up.UserUUID
	Score() int64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

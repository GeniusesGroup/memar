/* For license and copyright information please see the LEGAL file in the code repository */

package trup

import (
	"memar/protocol"

	tp "org/modules/task/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	TaskID() tp.TaskUUID
	UserID() up.UserUUID
	RelationType() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

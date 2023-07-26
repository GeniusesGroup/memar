/* For license and copyright information please see the LEGAL file in the code repository */

package cugsp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	GroupID() gp.GroupUUID
	ReadUntil() protocol.NumberOfVersion

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

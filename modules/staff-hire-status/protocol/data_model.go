/* For license and copyright information please see the LEGAL file in the code repository */

package shsp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

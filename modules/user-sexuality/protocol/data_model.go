/* For license and copyright information please see the LEGAL file in the code repository */

package usp

import (
	"memar/protocol"

	up "org/modules/user/protocol"
	usp "org/modules/user-sexuality/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	Sexuality() usp.Sexuality

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

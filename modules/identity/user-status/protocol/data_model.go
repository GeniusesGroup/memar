/* For license and copyright information please see the LEGAL file in the code repository */

package usp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	OrgID() up.UserUUID
	Status() Status

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

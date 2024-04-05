/* For license and copyright information please see the LEGAL file in the code repository */

package urup

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	SideID() up.UserUUID
	Relation() User_Relation

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

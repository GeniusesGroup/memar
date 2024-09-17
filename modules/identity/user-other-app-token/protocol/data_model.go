/* For license and copyright information please see the LEGAL file in the code repository */

package uoatp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	UserID() up.UserUUID
	OrgID() org.OrgUUID
	Token() Token

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

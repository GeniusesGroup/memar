/* For license and copyright information please see the LEGAL file in the code repository */

package urp

import (
	"memar/protocol"

	aap "org/modules/app-audit/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	ReferentUserID() up.UserUUID

	aap.AuditRequest
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

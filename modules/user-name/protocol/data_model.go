/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
// it is use in many other services like send email(email address), ...
type DataModel interface {
	UserID() up.UserUUID
	OrgID() org.OrgUUID
	Username() Username
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

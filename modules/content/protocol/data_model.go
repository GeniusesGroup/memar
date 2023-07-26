/* For license and copyright information please see the LEGAL file in the code repository */

package cp

import (
	"memar/protocol"

	ctp "org/modules/content-type/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	ContentID() ContentUUID
	UserID() up.UserUUID
	ContentTypeID() ctp.ContentTypeUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

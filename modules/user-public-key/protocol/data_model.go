/* For license and copyright information please see the LEGAL file in the code repository */

package upkp

import (
	"memar/protocol"

	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	PublicKey() PublicKey
	Issuer() org.OrgUUID //Use to get notify about status of the PK e.g. revoked notification, ...
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

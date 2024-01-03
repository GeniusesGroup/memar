/* For license and copyright information please see the LEGAL file in the code repository */

package cpkp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	PublicKeyID() PublicKeyUUID
	UserID() up.UserUUID
	Issuer() org.OrgUUID //Use to get notify about status of the PK e.g. revoked notification, ...
	PublicKey() PublicKey

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

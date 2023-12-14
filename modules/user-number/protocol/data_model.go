/* For license and copyright information please see the LEGAL file in the code repository */

package unp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

// TODO::: need domain or any fields here to support for Numbers Authority (GOD mode)? e.g. [IANA](https://iana.org/)

type DataModel interface {
	UserID() up.UserUUID
	OrgID() org.OrgUUID
	ProviderID() org.OrgUUID
	Number() Number
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

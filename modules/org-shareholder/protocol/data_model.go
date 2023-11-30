/* For license and copyright information please see the LEGAL file in the code repository */

package osp

import (
	"memar/math/per"
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	org "org/modules/org/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	OrgID() org.OrgUUID
	UserID() up.UserUUID
	Quantity() per.Trillion

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

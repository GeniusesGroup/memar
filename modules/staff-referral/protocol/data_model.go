/* For license and copyright information please see the LEGAL file in the code repository */

package srp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
	up "org/modules/user/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	ReferralID() up.UserUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

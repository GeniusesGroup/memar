/* For license and copyright information please see the LEGAL file in the code repository */

// User delegate means transfer power to someone. power is role access in softwares.
package udp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	rp "org/modules/role/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	GivenUserID() up.UserUUID
	GottenUserID() up.UserUUID
	RoleID() rp.RoleUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

// Service: delegate user can delegate its role to other. blocked this service by default.

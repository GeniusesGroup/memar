/* For license and copyright information please see the LEGAL file in the code repository */

package sip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

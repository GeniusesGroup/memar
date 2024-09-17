/* For license and copyright information please see the LEGAL file in the code repository */

package stlap

import (
	"memar/protocol"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel or staff replace
type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	PresentedID() sp.StaffUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

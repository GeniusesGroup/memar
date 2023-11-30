/* For license and copyright information please see the LEGAL file in the code repository */

package sop

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	DayHours() earth.DayHours

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/* For license and copyright information please see the LEGAL file in the code repository */

package stup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	osp "org/modules/org-shift/protocol"
	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	ShiftID() osp.ShiftUUID
	DayHours() earth.DayHours // what hours in a day this staff must active to provide services or do projects

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

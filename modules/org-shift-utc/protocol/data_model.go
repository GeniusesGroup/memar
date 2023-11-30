/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	sp "org/modules/org-shift/protocol"
)

type DataModel interface {
	ShiftID() sp.ShiftUUID
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours // what hours in day in utc time week this org active to provide services
	Type() sp.Type

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

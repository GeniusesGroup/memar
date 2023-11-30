/* For license and copyright information please see the LEGAL file in the code repository */

package rhup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	rp "org/modules/role/protocol"
)

type DataModel interface {
	RoleID() rp.RoleUUID
	Week() utc.WeekElapsed
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours // what hours in a day this role active to provide services

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

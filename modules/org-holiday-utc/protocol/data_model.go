/* For license and copyright information please see the LEGAL file in the code repository */

package ohup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	org "org/modules/org/protocol"
)

type DataModel interface {
	OrgID() org.OrgUUID
	Week() utc.WeekElapsed
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this org active to provide services
	DayHours() earth.DayHours // what hours in a day this org active to provide services

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

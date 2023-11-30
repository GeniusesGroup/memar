/* For license and copyright information please see the LEGAL file in the code repository */

package dtup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	arp "org/modules/app-request/protocol"
	dp "org/modules/department/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours // what hours in day in utc time week this department active to provide services

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

/* For license and copyright information please see the LEGAL file in the code repository */

package dhup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	dp "org/modules/department/protocol"
)

type DataModel interface {
	DepartmentID() dp.DepartmentUUID
	Week() utc.WeekElapsed
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours // what hours in a day this department active to provide services

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

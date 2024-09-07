/* For license and copyright information please see the LEGAL file in the code repository */

package rhup

import (
	"memar/time/earth"
	"memar/time/utc"

	aa_p "org/modules/app-audit/protocol"
	role_p "org/modules/role/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	role_p.Field_RoleID
	Week() utc.WeekElapsed
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours // what hours in a day this role active to provide services

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}

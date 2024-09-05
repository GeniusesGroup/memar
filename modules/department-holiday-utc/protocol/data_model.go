/* For license and copyright information please see the LEGAL file in the code repository */

package dhu_p

import (
	"memar/time/earth"
	"memar/time/utc"

	aa_p "org/modules/app-audit/protocol"
	department_p "org/modules/org-department/protocol"
	storage_p "org/modules/storage/protocol"
)

type DataModel interface {
	department_p.Field_DepartmentID
	Week() utc.WeekElapsed
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this department active to provide services
	DayHours() earth.DayHours // what hours in a day this department active to provide services

	aa_p.Field_AuditRequest
	storage_p.Field_SaveTime
}

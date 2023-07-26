/* For license and copyright information please see the LEGAL file in the code repository */

package rtup

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	rp "org/modules/role/protocol"
)

type DataModel interface {
	RoleID() rp.RoleUUID
	Weekdays() utc.Weekdays   // what days in weekday in utc time week this role active to provide services
	DayHours() earth.DayHours // what hours in day in utc time week this role active to provide services

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

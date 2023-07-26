/* For license and copyright information please see the LEGAL file in the code repository */

package stlp

import (
	"memar/protocol"
	"memar/time/earth"
	"memar/time/utc"

	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	DayHours() earth.DayHours
	Type() Type

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

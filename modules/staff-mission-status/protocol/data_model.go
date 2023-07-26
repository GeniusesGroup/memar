/* For license and copyright information please see the LEGAL file in the code repository */

package smsp

import (
	"memar/protocol"
	"memar/time/utc"

	sp "org/modules/staff/protocol"
)

type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

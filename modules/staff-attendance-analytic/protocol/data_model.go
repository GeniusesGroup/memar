/* For license and copyright information please see the LEGAL file in the code repository */

package saap

import (
	"memar/protocol"
	"memar/time/utc"

	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	Hours() uint64

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

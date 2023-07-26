/* For license and copyright information please see the LEGAL file in the code repository */

package sspp

import (
	"memar/protocol"
	"memar/time/utc"

	osp "org/modules/org-shift/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	StaffID() sp.StaffUUID
	Day() utc.DayElapsed
	ShiftID() osp.ShiftUUID

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

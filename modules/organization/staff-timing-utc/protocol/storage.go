/* For license and copyright information please see the LEGAL file in the code repository */

package stup

import (
	"memar/protocol"
	"memar/time/utc"

	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID sp.StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID sp.StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	// FIND_StaffIDs_BY_ShiftID(shiftID ShiftUUID, offset, limit uint64) (staffIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

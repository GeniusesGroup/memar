/* For license and copyright information please see the LEGAL file in the code repository */

package smp

import (
	"libgo/protocol"
	"libgo/time/utc"

	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID sp.StaffUUID, day utc.DayElapsed) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID sp.StaffUUID, day utc.DayElapsed, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_StaffIDs_BY_Day(day utc.DayElapsed, offset, limit uint64) (staffIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// we may need indexing based on mission type ??
	// FindByType(t Type, offset, limit uint64) (staffIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)

}

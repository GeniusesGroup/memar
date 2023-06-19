/* For license and copyright information please see the LEGAL file in the code repository */

package sep

import (
	"libgo/protocol"

	sp "org/modules/staff/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(staffID sp.StaffUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(staffID sp.StaffUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_StaffIDs_BY_EvaluatorIDs(evaluatorID sp.StaffUUID, offset, limit uint64) (staffIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_EvaluatorIDs_BY_StaffID(staffID sp.StaffUUID, offset, limit uint64) (evaluatorIDs []sp.StaffUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

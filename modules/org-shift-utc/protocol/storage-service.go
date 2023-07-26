/* For license and copyright information please see the LEGAL file in the code repository */

package osup

import (
	"memar/protocol"

	sp "org/modules/org-shift/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(shiftID sp.ShiftUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(shiftID sp.ShiftUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)

	// do we need indexing ??
	FIND_ShiftIDs_BY_Type(t sp.Type, offset, limit uint64) (shiftIDs []sp.ShiftUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

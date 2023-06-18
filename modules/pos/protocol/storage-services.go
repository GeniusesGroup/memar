/* For license and copyright information please see the LEGAL file in the code repository */

package pp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID PosUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FILTER_PosIDs_BY_Type(t Type, offset, limit uint64) (posIDs []PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

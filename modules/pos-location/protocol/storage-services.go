/* For license and copyright information please see the LEGAL file in the code repository */

package plp

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/pos/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(posID pp.PosUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(posID pp.PosUUID, vo protocol.VersionOffset) (dm DataModel, err protocol.Error)

	FIND_PosIDs_BY_BuildingLocationID(BuildingLocationID eblp.BuildingLocationUUID, offset, limit uint64) (posIDs []pp.PosUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

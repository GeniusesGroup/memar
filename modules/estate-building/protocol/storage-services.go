/* For license and copyright information please see the LEGAL file in the code repository */

package ebp

import (
	"libgo/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(buildingID BuildingUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(buildingID BuildingUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(areaID BuildingUUID, offset, limit uint64) (buildingIDs []BuildingUUID, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (buildingIDs []BuildingUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

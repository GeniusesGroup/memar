/* For license and copyright information please see the LEGAL file in the code repository */

package eblsp

import (
	"memar/protocol"

	eblp "org/modules/estate-building-location/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(buildingLocationID eblp.BuildingLocationUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(buildingLocationID eblp.BuildingLocationUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByStatus(status Status, offset, limit uint64) (buildingLocationIDs []eblp.BuildingLocationUUID, err protocol.Error)
}

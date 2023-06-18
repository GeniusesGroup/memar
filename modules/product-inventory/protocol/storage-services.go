/* For license and copyright information please see the LEGAL file in the code repository */

package pip

import (
	"libgo/protocol"

	eblp "org/modules/estate-building-location/protocol"
	pp "org/modules/product/protocol"
)

type StorageService interface {
	// Save(p ProductInventory) (nv protocol.NumberOfVersion, err protocol.Error)

	Lock(productID pp.ProductUUID, buildingLocationID eblp.BuildingLocationUUID) (dm DataModel, err protocol.Error)
	Unlock(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, buildingLocationID eblp.BuildingLocationUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, buildingLocationID eblp.BuildingLocationUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_BuildingLocationID(buildingLocationID eblp.BuildingLocationUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_BuildingLocationIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (buildingLocationIDs []eblp.BuildingLocationUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

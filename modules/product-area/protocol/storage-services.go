/* For license and copyright information please see the LEGAL file in the code repository */

package pap

import (
	"libgo/protocol"
	ep "org/modules/estate/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, estateID ep.EstateUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, estateID ep.EstateUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_EstateID(estateID ep.EstateUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_EstateIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (estateIDs []ep.EstateUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

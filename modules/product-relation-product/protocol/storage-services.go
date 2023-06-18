/* For license and copyright information please see the LEGAL file in the code repository */

package prpp

import (
	"libgo/protocol"

	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, relationID pp.ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, relationID pp.ProductUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_RelationID(relationID pp.ProductUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_RelationIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (relationIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

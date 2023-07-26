/* For license and copyright information please see the LEGAL file in the code repository */

package ptp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, tag string) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, tag string, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_Tags_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (tags []string, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ProductIDs_By_Tag(tag string, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

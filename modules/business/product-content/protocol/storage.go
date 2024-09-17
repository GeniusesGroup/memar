/* For license and copyright information please see the LEGAL file in the code repository */

package pcp

import (
	"memar/protocol"

	cp "org/modules/content/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, contentID cp.ContentUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, contentID cp.ContentUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_ContentID(contentID cp.ContentUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ContentIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (contentIDs []cp.ContentUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

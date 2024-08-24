/* For license and copyright information please see the LEGAL file in the code repository */

package psp

import (
	"memar/protocol"

	op "org/modules/object/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_ProductIDs_BY_MapID(mapID op.ObjectUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	FILTER_ProductIDs_BY_SeatType(t Type, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

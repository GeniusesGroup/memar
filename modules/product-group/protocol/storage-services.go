/* For license and copyright information please see the LEGAL file in the code repository */

package pgp

import (
	"libgo/protocol"

	gp "org/modules/group/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID pp.ProductUUID, groupID gp.GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID pp.ProductUUID, groupID gp.GroupUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (productIDs []pp.ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (groupIDs []gp.GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

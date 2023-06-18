/* For license and copyright information please see the LEGAL file in the code repository */

package dcp

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
	dp "org/modules/discount/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID dp.DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID dp.DiscountUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_DiscountIDs_BY_CategoryID(categoryID cp.CategoryUUID, offset, limit uint64) (discountIDs []dp.DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

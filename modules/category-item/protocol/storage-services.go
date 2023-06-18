/* For license and copyright information please see the LEGAL file in the code repository */

package cip

import (
	"libgo/protocol"

	cp "org/modules/category/protocol"
)

type StorageServices interface {
	Save(f DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID cp.CategoryUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID cp.CategoryUUID, priority uint64, vo protocol.VersionOffset) (f DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CategoryIDs_BY_ItemID(itemID [16]byte, offset, limit uint64) (categoryIDs []cp.CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_Priorities_BY_CategoryID(itemID [16]byte, categoryID cp.CategoryUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}

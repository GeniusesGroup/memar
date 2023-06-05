/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CategoryItem interface {
	CategoryID() CategoryUUID       //
	Priority() uint64               //
	ItemID() [16]byte               // any domain usually product, content, ... domain
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type CategoryItem_StorageServices interface {
	Save(f CategoryItem) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID CategoryUUID, priority uint64) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID CategoryUUID, priority uint64, vo protocol.VersionOffset) (f CategoryItem, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_CategoryIDs_BY_ItemID(itemID [16]byte, offset, limit uint64) (categoryIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_Priorities_BY_CategoryID(itemID [16]byte, categoryID CategoryUUID, offset, limit uint64) (priorities []uint64, nv protocol.NumberOfVersion, err protocol.Error)
}

// services:
// Last(categoryID [16]byte, priority uint64) (ci CategoryItem, nv protocol.NumberOfVersion, err protocol.Error)
// ListItems(categoryID [16]byte, offset, limit uint64) (items [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)

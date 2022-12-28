/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// Category indicate the domain record data fields.
// Category or Topic
type Category interface {
	CategoryID() [16]byte       // quiddity domain
	ParentID() [16]byte         // CategoryID, Exist if it isn't top category.
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type Category_StorageServices interface {
	Save(c Category) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, vo protocol.VersionOffset) (gs CategoryStatus, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

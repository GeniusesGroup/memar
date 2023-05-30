/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

type CategoryUUID = protocol.UUID

// Category indicate the domain record data fields.
// Category or Topic
type Category interface {
	CategoryID() CategoryUUID       // quiddity domain
	ParentID() CategoryUUID         // Exist if it isn't top category.
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type Category_StorageServices interface {
	Save(c Category) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID [16]byte, vo protocol.VersionOffset) (gs CategoryStatus, nv protocol.NumberOfVersion, err protocol.Error)

	GetIDs(offset, limit uint64) (categoryIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

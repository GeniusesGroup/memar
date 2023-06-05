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
	Save(dm Category) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(categoryID CategoryUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(categoryID CategoryUUID, vo protocol.VersionOffset) (dm CategoryStatus, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_CategoryIDs_BY_ParentID(parentID CategoryUUID, offset, limit uint64) (categoryIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_ParentIDs_BY_CategoryID(categoryID CategoryUUID, offset, limit uint64) (parentIDs []CategoryUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

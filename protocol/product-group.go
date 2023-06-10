/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductGroup indicate the domain record data fields.
type ProductGroup interface {
	ProductID() ProductUUID //
	GroupID() GroupUUID     //
	Status() ProductGroup_Status
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductGroup_StorageServices interface {
	Save(dm ProductGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID, groupID GroupUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, groupID GroupUUID, vo protocol.VersionOffset) (dm ProductGroup, nv protocol.NumberOfVersion, err protocol.Error)

	LIST_ProductIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
	LIST_GroupIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (groupIDs []GroupUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

type ProductGroup_Status Quiddity_Status

/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// ProductGroup indicate the domain record data fields.
type ProductGroup interface {
	ProductID() ProductUUID         //
	GroupID() GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type ProductGroup_StorageServices interface {
	Save(pg ProductGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(productID ProductUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(productID ProductUUID, vo protocol.VersionOffset) (pg ProductGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID GroupUUID, offset, limit uint64) (productIDs []ProductUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

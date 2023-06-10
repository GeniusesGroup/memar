/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountGroup indicate the domain record data fields.
type DiscountGroup interface {
	DiscountID() DiscountUUID       //
	GroupID() GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountGroup_StorageServices interface {
	Save(dm DiscountGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

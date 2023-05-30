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
	Save(dg DiscountGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dg DiscountGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID [16]byte, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

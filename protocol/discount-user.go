/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DiscountUser indicate the domain record data fields.
type DiscountUser interface {
	DiscountID() DiscountUUID       //
	UserID() up.UserUUID            //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountUser_StorageServices interface {
	Save(dm DiscountUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountUser, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_UserID(userID up.UserUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

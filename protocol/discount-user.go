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
	Save(ds DiscountUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (ds DiscountUser, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID up.UserUUID, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

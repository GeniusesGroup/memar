/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
	up "org/modules/user/protocol"
)

// DiscountUserType indicate the domain record data fields.
type DiscountUserType interface {
	DiscountID() DiscountUUID       //
	UserType() protocol.UserType    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountUserType_StorageServices interface {
	Save(dm DiscountUserType) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID DiscountUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID DiscountUUID, vo protocol.VersionOffset) (dm DiscountUserType, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_DiscountIDs_BY_UserType(userType up.UserUUID, offset, limit uint64) (discountIDs []DiscountUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

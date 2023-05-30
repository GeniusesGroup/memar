/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// DiscountUserType indicate the domain record data fields.
type DiscountUserType interface {
	DiscountID() DiscountUUID       //
	UserType() protocol.UserType    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type DiscountUserType_StorageServices interface {
	Save(dut DiscountUserType) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(discountID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(discountID [16]byte, vo protocol.VersionOffset) (dut DiscountUserType, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUserType(userType protocol.UserType, offset, limit uint64) (discountIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

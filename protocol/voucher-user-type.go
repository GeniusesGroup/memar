/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherUserType indicate the domain record data fields.
// Use to restrict the voucher usage by specific user type.
type VoucherUserType interface {
	VoucherID() VoucherUUID         //
	UserType() protocol.UserType    //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherUserType_StorageServices interface {
	Save(vut VoucherUserType) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vut VoucherUserType, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByUserType(userType protocol.UserType, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

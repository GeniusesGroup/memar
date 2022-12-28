/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherUserType indicate the domain record data fields.
// Use to restrict the voucher usage by specific user type.
type VoucherUserType interface {
	VoucherID() [16]byte         // voucher domain
	UserType() protocol.UserType //
	Time() protocol.Time         // save time
	RequestID() UserRequestUUID  // user-request domain
}

type VoucherUserType_StorageServices interface {
	Save(vut VoucherUserType) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vut VoucherUserType, nv protocol.NumberOfVersion, err protocol.Error)

	FilterByUserType(userType protocol.UserType, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

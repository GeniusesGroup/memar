/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherUser indicate the domain record data fields.
// Use to restrict the voucher usage by specific users.
type VoucherUser interface {
	VoucherID() VoucherUUID         //
	UserID() UserUUID               //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherUser_StorageServices interface {
	Save(vu VoucherUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vu VoucherUser, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID UserUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

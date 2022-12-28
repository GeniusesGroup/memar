/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherUser indicate the domain record data fields.
// Use to restrict the voucher usage by specific users.
type VoucherUser interface {
	VoucherID() [16]byte        // voucher domain
	UserID() protocol.UserID    // user domain.
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherUser_StorageServices interface {
	Save(vu VoucherUser) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vu VoucherUser, nv protocol.NumberOfVersion, err protocol.Error)

	FindByUser(userID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

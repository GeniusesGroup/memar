/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherGroup indicate the domain record data fields.
type VoucherGroup interface {
	VoucherID() [16]byte        // voucher domain
	GroupID() [16]byte          // group domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherGroup_StorageServices interface {
	Save(vg VoucherGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vg VoucherGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

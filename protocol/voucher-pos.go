/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// VoucherPOS indicate the domain record data fields.
type VoucherPOS interface {
	VoucherID() [16]byte        // voucher domain
	PosID() [16]byte            // pos domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherPOS_StorageServices interface {
	Save(vp VoucherPOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vp VoucherPOS, nv protocol.NumberOfVersion, err protocol.Error)

	FindByPOS(posID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

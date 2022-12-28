/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherCategory indicate the domain record data fields.
// Use to restrict the voucher on specific category.
type VoucherCategory interface {
	VoucherID() [16]byte        // voucher domain
	Each() uint8                // Each time use
	CategoryID() [16]byte       // category domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherCategory_StorageServices interface {
	Save(vc VoucherCategory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vc VoucherCategory, nv protocol.NumberOfVersion, err protocol.Error)
}

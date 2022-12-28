/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherProduct restrict use voucher on specific product
type VoucherProduct interface {
	VoucherID() [16]byte        // voucher domain
	Each() uint8                // Each time use
	ProductID() [16]byte        // product domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherProduct_StorageServices interface {
	Save(vp VoucherProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vp VoucherProduct, nv protocol.NumberOfVersion, err protocol.Error)

	FindByProduct(productID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

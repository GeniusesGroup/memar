/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherArea indicate the domain record data fields.
// VoucherArea is proper or appropriate location indicate specific area not specific location
// It's rule depend on products in invoices e.g. source or destination of taxi as a service(product).
type VoucherArea interface {
	VoucherID() [16]byte        // voucher domain
	AreaID() [16]byte           // area domain
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherArea_StorageServices interface {
	Save(va VoucherArea) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (va VoucherArea, nv protocol.NumberOfVersion, err protocol.Error)

	FindByArea(AreaID [16]byte, offset, limit uint64) (voucherIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

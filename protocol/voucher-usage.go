/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherUsage indicate the domain record data fields.
type VoucherUsage interface {
	VoucherID() [16]byte        // product domain
	MaximumInvoice() uint64     //
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherUsage_StorageServices interface {
	Save(vu VoucherUsage) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vu VoucherUsage, nv protocol.NumberOfVersion, err protocol.Error)
}

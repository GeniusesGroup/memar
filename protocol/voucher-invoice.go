/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// VoucherInvoice indicate the domain record data fields.
type VoucherInvoice interface {
	VoucherID() [16]byte        // voucher domain
	Each() uint8                // Each time use
	MinPrice() int64            // Minimum invoice price
	MinAmount() uint64          // Minimum invoice product numbers
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type VoucherInvoice_StorageServices interface {
	Save(vi VoucherInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vi VoucherInvoice, nv protocol.NumberOfVersion, err protocol.Error)
}

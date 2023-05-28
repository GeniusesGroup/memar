/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherInvoice indicate the domain record data fields.
type VoucherInvoice interface {
	VoucherID() VoucherUUID         //
	Each() uint8                    // Each time use
	MinPrice() int64                // Minimum invoice price
	MinAmount() uint64              // Minimum invoice product numbers
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherInvoice_StorageServices interface {
	Save(vi VoucherInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vi VoucherInvoice, nv protocol.NumberOfVersion, err protocol.Error)
}

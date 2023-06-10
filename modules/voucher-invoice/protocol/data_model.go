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
	Save(dm VoucherInvoice) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID, each uint8) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, each uint8 ,vo protocol.VersionOffset) (dm VoucherInvoice, nv protocol.NumberOfVersion, err protocol.Error)
}

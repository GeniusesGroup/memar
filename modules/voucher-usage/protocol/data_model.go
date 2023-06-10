/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherUsage indicate the domain record data fields.
type VoucherUsage interface {
	VoucherID() VoucherUUID         //
	MaximumInvoice() uint64         //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherUsage_StorageServices interface {
	Save(dm VoucherUsage) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm VoucherUsage, nv protocol.NumberOfVersion, err protocol.Error)
}

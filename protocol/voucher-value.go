/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// VoucherValue indicate the domain record data fields.
type VoucherValue interface {
	VoucherID() [16]byte            // voucher domain
	Each() uint8                    // Each time use
	Percentage() protocol.PerMyriad // Max discount percentage per use
	Price() protocol.MoneyAmount    // Max discount price per use
	Time() protocol.Time            // save time
	RequestID() UserRequestUUID     // user-request domain
}

type VoucherValue_StorageServices interface {
	Save(vv VoucherValue) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID [16]byte, vo protocol.VersionOffset) (vv VoucherValue, nv protocol.NumberOfVersion, err protocol.Error)
}

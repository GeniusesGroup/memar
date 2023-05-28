/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherValue indicate the domain record data fields.
type VoucherValue interface {
	VoucherID() VoucherUUID         //
	Each() uint8                    // Each time use
	Percentage() protocol.PerMyriad // Max discount percentage per use
	Price() protocol.MoneyAmount    // Max discount price per use
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherValue_StorageServices interface {
	Save(vv VoucherValue) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vv VoucherValue, nv protocol.NumberOfVersion, err protocol.Error)
}

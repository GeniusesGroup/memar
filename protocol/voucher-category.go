/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherCategory indicate the domain record data fields.
// Use to restrict the voucher on specific category.
type VoucherCategory interface {
	VoucherID() VoucherUUID         //
	Each() uint8                    // Each time use
	CategoryID() CategoryUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherCategory_StorageServices interface {
	Save(vc VoucherCategory) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vc VoucherCategory, nv protocol.NumberOfVersion, err protocol.Error)
}

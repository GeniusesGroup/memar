/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherProduct restrict use voucher on specific product
type VoucherProduct interface {
	VoucherID() VoucherUUID         //
	Each() uint8                    // Each time use
	ProductID() []ProductUUID       //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherProduct_StorageServices interface {
	Save(dm VoucherProduct) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID, each uint8) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, each uint8, vo protocol.VersionOffset) (dm VoucherProduct, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

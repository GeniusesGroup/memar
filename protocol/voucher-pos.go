/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherPOS indicate the domain record data fields.
type VoucherPOS interface {
	VoucherID() VoucherUUID         //
	PosID() PosUUID                 //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherPOS_StorageServices interface {
	Save(vp VoucherPOS) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vp VoucherPOS, nv protocol.NumberOfVersion, err protocol.Error)

	FindByPOS(posID PosUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

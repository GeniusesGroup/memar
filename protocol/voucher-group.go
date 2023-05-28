/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherGroup indicate the domain record data fields.
type VoucherGroup interface {
	VoucherID() VoucherUUID         //
	GroupID() GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherGroup_StorageServices interface {
	Save(vg VoucherGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (vg VoucherGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FindByGroup(groupID GroupUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// VoucherGroup indicate the domain record data fields.
type VoucherGroup interface {
	VoucherID() VoucherUUID         //
	GroupID() []GroupUUID             //
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type VoucherGroup_StorageServices interface {
	Save(dm VoucherGroup) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID VoucherUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID VoucherUUID, vo protocol.VersionOffset) (dm VoucherGroup, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_GroupID(groupID GroupUUID, offset, limit uint64) (voucherIDs []VoucherUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

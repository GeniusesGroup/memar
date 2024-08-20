/* For license and copyright information please see the LEGAL file in the code repository */

package vgp

import (
	"memar/protocol"

	gp "org/modules/group/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID) (dm DataModel, err protocol.Error)

	FIND_VoucherIDs_BY_GroupID(groupID gp.GroupUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

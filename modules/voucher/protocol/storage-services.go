/* For license and copyright information please see the LEGAL file in the code repository */

package vp

import (
	"memar/protocol"

	sp "org/modules/storage/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID VoucherUUID) (dm DataModel, err protocol.Error)

	FIND_VoucherIDs_BY_Type(t Type, offset, limit uint64) (voucherIDs []VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

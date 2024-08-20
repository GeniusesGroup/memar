/* For license and copyright information please see the LEGAL file in the code repository */

package vcp

import (
	"memar/protocol"

	cp "org/modules/category/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID, Each uint8) (dm DataModel, err protocol.Error)

	LIST_VoucherIDs_By_CategoryID(categoryID cp.CategoryUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

/* For license and copyright information please see the LEGAL file in the code repository */

package vpp

import (
	"memar/protocol"

	pp "org/modules/product/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID, each uint8) (dm DataModel, err protocol.Error)

	FIND_VoucherIDs_BY_ProductID(productID pp.ProductUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

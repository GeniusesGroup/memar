/* For license and copyright information please see the LEGAL file in the code repository */

package vutp

import (
	"memar/protocol"

	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID) (dm DataModel, err protocol.Error)

	FILTER_VoucherIDs_BY_Type(userType protocol.UserType, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

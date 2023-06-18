/* For license and copyright information please see the LEGAL file in the code repository */

package vip

import (
	"libgo/protocol"

	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(voucherID vp.VoucherUUID, each uint8) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(voucherID vp.VoucherUUID, each uint8, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)
}

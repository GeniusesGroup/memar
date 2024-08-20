/* For license and copyright information please see the LEGAL file in the code repository */

package vvp

import (
	"memar/protocol"

	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID, each uint8) (dm DataModel, err protocol.Error)
}

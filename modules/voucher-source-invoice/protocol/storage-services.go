/* For license and copyright information please see the LEGAL file in the code repository */

package vsip

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	sp "org/modules/storage/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (err protocol.Error)

	Get(voucherID vp.VoucherUUID) (dm DataModel, err protocol.Error)

	FIND_VoucherIDs_BY_InvoiceID(invoiceID ip.InvoiceUUID, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)

	FIND_VoucherIDs_BY_Type(t Type, offset, limit uint64) (voucherIDs []vp.VoucherUUID, num sp.NumberOfVersion, err protocol.Error)
}

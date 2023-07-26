/* For license and copyright information please see the LEGAL file in the code repository */

package ivp

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	vp "org/modules/voucher/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID ip.InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID ip.InvoiceUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_VoucherID(voucherID vp.VoucherUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)

	// protocol.EventTarget
}

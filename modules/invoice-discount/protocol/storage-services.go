/* For license and copyright information please see the LEGAL file in the code repository */

package idp

import (
	"memar/protocol"

	dp "org/modules/discount/protocol"
	ip "org/modules/invoice/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID ip.InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID ip.InvoiceUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_DiscountID(discountID dp.DiscountUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// TODO::: discount status???

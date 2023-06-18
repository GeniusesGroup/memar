/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	"libgo/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID ip.InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID ip.InvoiceUUID, vo protocol.VersionOffset) (dm DataModel, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_IngredientID(IngredientID pp.ProductUUID, offset, limit uint64) (invoiceIDs []ip.InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

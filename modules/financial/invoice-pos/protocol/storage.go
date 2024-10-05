/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	error_p "memar/error/protocol"

	pp "org/modules/business/pos/protocol"
	ip "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Get(invoiceID ip.UUID) (dm DataModel, err error_p.Error)

	FIND_InvoiceIDs_BY_PosID(posID pp.PosUUID, offset, limit uint64) (invoiceIDs []ip.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}

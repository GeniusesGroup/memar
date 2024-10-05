/* For license and copyright information please see the LEGAL file in the code repository */

package iip

import (
	error_p "memar/error/protocol"

	pp "org/modules/business/product/protocol"
	ip "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Count(invoiceID ip.UUID) (nv storage_p.NumberOfVersion, err error_p.Error)
	Get(invoiceID ip.UUID, vo storage_p.VersionOffset) (dm DataModel, err error_p.Error)

	FIND_InvoiceIDs_BY_ProductID(productID pp.UUID, offset, limit uint64) (invoiceIDs []ip.UUID, nv storage_p.NumberOfVersion, err error_p.Error)
}

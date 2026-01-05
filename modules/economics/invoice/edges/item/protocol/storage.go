/* For license and copyright information please see the LEGAL file in the code repository */

package item_p

import (
	error_p "memar/error/protocol"

	product_p "org/modules/business/product/protocol"
	invoice_p "org/modules/financial/invoice/protocol"
	storage_p "org/modules/storage/primitive/protocol"
)

type StorageServices interface {
	Save(dm DataModel) (nv storage_p.NumberOfVersion, err error_p.Error)

	Get(invoiceID invoice_p.UUID, productID product_p.UUID) (dm DataModel, err error_p.Error)

	FIND_ProductIDs_BY_InvoiceID(invoiceID invoice_p.UUID, offset, limit uint64) (productIDs []product_p.UUID, err error_p.Error)
	FIND_InvoiceIDs_BY_ProductID(productID product_p.UUID, offset, limit uint64) (invoiceIDs []invoice_p.UUID, err error_p.Error)
}

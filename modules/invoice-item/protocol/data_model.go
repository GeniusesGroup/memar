/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceItem indicate the domain record data fields.
// each InvoiceItem is immutable record and so use version mechanism to chain InvoiceItem in InvoiceID group.
// Ship service can add as an item to invoice
// Each item must check for reserve validity and make action in end of validity
type InvoiceItem interface {
	InvoiceID() InvoiceUUID         //
	ProductID() ProductUUID         //
	Quantity() uint64               // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Time() protocol.Time            // save time
	RequestID() urp.UserRequestUUID //
}

type InvoiceItem_StorageServices interface {
	Save(dm InvoiceItem) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceItem, err protocol.Error)

	FIND_InvoiceIDs_BY_ProductID(productID ProductUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

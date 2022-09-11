/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"github.com/GeniusesGroup/libgo/protocol"
)

// InvoiceItem indicate the domain record data fields.
// each InvoiceItem is immutable record and so use version mechanism to chain InvoiceItem in InvoiceID group.
// Ship service can add as an item to invoice
// Each item must check for reserve validity and make action in end of validity
type InvoiceItem interface {
	InvoiceID() [16]byte        // invoice domain
	ProductID() [16]byte        // product domain
	Quantity() uint64           // decimal >> 1.5 >> 1.2 >> 10 >> 0
	Time() protocol.Time        // save time
	RequestID() UserRequestUUID // user-request domain
}

type InvoiceItem_StorageServices interface {
	Save(ii InvoiceItem) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (ii InvoiceItem, err protocol.Error)

	FindByProductID(productID uint64, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

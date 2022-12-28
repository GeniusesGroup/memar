/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InvoiceDiscount indicate the domain record data fields.
type InvoiceDiscount interface {
	InvoiceID() [16]byte              // invoice domain
	DiscountID() [16]byte             // discount domain
	Discounted() protocol.MoneyAmount //
	Time() protocol.Time              // save time
	RequestID() UserRequestUUID       // user-request domain
}

type InvoiceDiscount_StorageServices interface {
	Save(iv InvoiceDiscount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iv InvoiceDiscount, nv protocol.NumberOfVersion, err protocol.Error)

	FindByDiscountID(discountID [16]byte, offset, limit uint64) (invoiceIDs [][16]byte, nv protocol.NumberOfVersion, err protocol.Error)
}

// TODO::: discount status???

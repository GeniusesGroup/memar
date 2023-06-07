/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"

	urp "org/modules/user-request/protocol"
)

// InvoiceDiscount indicate the domain record data fields.
type InvoiceDiscount interface {
	InvoiceID() InvoiceUUID           //
	DiscountID() DiscountUUID         //
	Discounted() protocol.MoneyAmount //
	Time() protocol.Time              // save time
	RequestID() urp.UserRequestUUID   //
}

type InvoiceDiscount_StorageServices interface {
	Save(dm InvoiceDiscount) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID InvoiceUUID) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID InvoiceUUID, vo protocol.VersionOffset) (dm InvoiceDiscount, nv protocol.NumberOfVersion, err protocol.Error)

	FIND_InvoiceIDs_BY_DiscountID(discountID DiscountUUID, offset, limit uint64) (invoiceIDs []InvoiceUUID, nv protocol.NumberOfVersion, err protocol.Error)
}

// TODO::: discount status???

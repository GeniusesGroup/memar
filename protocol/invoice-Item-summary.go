/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InvoiceItemSummary indicate the domain record data fields.
type InvoiceItemSummary interface {
	InvoiceID() InvoiceUUID                //
	ProductID() ProductUUID                //
	SuggestedPrice() protocol.MoneyAmount  // Total should pay before any discount or auction
	DiscountedPrice() protocol.MoneyAmount // user profit from this product purchase by auctions
	PayablePrice() protocol.MoneyAmount    // Total price user pay to organization
	VAT() protocol.MoneyAmount             // Total VAT user pay to its country government
	Time() protocol.Time                   // save time
}

type InvoiceItemSummary_StorageServices interface {
	Save(iis InvoiceItemSummary) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (iis InvoiceItemSummary, err protocol.Error)
}

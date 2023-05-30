/* For license and copyright information please see the LEGAL file in the code repository */

package org

import (
	"libgo/protocol"
)

// InvoiceSummary indicate the domain record data fields.
// InvoiceSummary is summary data that calculated to reduce fetch and calculate on each client device.
type InvoiceSummary interface {
	InvoiceID() InvoiceUUID                //
	ItemCount() uint64                     // Total item count
	Quantity() uint64                      // Total product count
	SuggestedPrice() protocol.MoneyAmount  // Total should pay before any discount or auction
	DiscountedPrice() protocol.MoneyAmount // user profit from this purchase by vouchers+auctions
	VoucherPrice() protocol.MoneyAmount    // the sum of all vouchers apply for this invoice
	PayablePrice() protocol.MoneyAmount    // Total price user pay to organization
	VAT() protocol.MoneyAmount             // Total VAT user pay to its country government
	Time() protocol.Time                   // save time
}

type InvoiceSummary_StorageServices interface {
	Save(is InvoiceSummary) (nv protocol.NumberOfVersion, err protocol.Error)

	Count(invoiceID [16]byte) (nv protocol.NumberOfVersion, err protocol.Error)
	Get(invoiceID [16]byte, vo protocol.VersionOffset) (is InvoiceSummary, nv protocol.NumberOfVersion, err protocol.Error)
}

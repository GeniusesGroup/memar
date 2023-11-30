/* For license and copyright information please see the LEGAL file in the code repository */

package isp

import (
	"memar/protocol"

	// arp "org/modules/app-request/protocol"
	ip "org/modules/invoice/protocol"
)

// DataModel indicate the domain record data fields.
// DataModel is summary data that calculated to reduce fetch and calculate on each client device.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ItemCount() uint64                     // Total item count
	Quantity() uint64                      // Total product count
	SuggestedPrice() protocol.MoneyAmount  // Total should pay before any discount or auction
	DiscountedPrice() protocol.MoneyAmount // user profit from this purchase by vouchers+auctions
	VoucherPrice() protocol.MoneyAmount    // the sum of all vouchers apply for this invoice
	PayablePrice() protocol.MoneyAmount    // Total price user pay to organization
	VAT() protocol.MoneyAmount             // Total VAT user pay to its country government

	// arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

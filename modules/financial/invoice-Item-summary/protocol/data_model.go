/* For license and copyright information please see the LEGAL file in the code repository */

package iisp

import (
	"memar/protocol"

	// arp "org/modules/app-request/protocol"
	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ProductID() pp.ProductUUID
	SuggestedPrice() protocol.MoneyAmount  // Total should pay before any discount or auction
	DiscountedPrice() protocol.MoneyAmount // user profit from this product purchase by auctions
	PayablePrice() protocol.MoneyAmount    // Total price user pay to organization
	VAT() protocol.MoneyAmount             // Total VAT user pay to its country government

	// arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

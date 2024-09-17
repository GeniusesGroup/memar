/* For license and copyright information please see the LEGAL file in the code repository */

package idp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/discount/protocol"
	ip "org/modules/invoice/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	DiscountID() dp.DiscountUUID
	Discounted() protocol.MoneyAmount

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

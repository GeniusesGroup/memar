/* For license and copyright information please see the LEGAL file in the code repository */

package omp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	dp "org/modules/deal/protocol"
	ip "org/modules/invoice/protocol"
)

// DataModel indicate the domain record data fields. each order is immutable record.
type DataModel interface {
	DealID() dp.DealUUID
	InvoiceID() ip.InvoiceUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

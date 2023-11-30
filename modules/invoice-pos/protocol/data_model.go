/* For license and copyright information please see the LEGAL file in the code repository */

package ip

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	ip "org/modules/invoice/protocol"
	pp "org/modules/pos/protocol"
	sp "org/modules/staff/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	// InvoiceNumber() uint16      // TODO::: do we need auto increment number? Why not QR code?
	PosID() pp.PosUUID
	StaffID() sp.StaffUUID // OrdererID that is creator of the invoice e.g. restaurant, drug prescription, sales agent,

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

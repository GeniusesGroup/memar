/* For license and copyright information please see the LEGAL file in the code repository */

package iiip

import (
	"memar/protocol"

	ip "org/modules/invoice/protocol"
	pp "org/modules/product/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	InvoiceID() ip.InvoiceUUID
	ProductID() pp.ProductUUID
	Type() Type
	ActionTime() protocol.Time

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

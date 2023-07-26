/* For license and copyright information please see the LEGAL file in the code repository */

package brip

import (
	"memar/protocol"

	bp "org/modules/budget/protocol"
	ip "org/modules/invoice/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	BudgetID() bp.BudgetUUID
	InvoiceID() ip.InvoiceUUID
	Type() Type
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

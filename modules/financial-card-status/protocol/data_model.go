/* For license and copyright information please see the LEGAL file in the code repository */

package fcsp

import (
	"memar/protocol"

	fcp "org/modules/financial-card/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	FinancialCardID() fcp.FinancialCardUUID
	Status()

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

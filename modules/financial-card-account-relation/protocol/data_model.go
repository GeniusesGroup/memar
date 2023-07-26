/* For license and copyright information please see the LEGAL file in the code repository */

package fcarp

import (
	"memar/protocol"

	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-card/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	CardID() fcp.FinancialCardUUID
	AccountID() fap.FinancialAccountUUID
	Priority() uint64
	Status() Status

	protocol.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

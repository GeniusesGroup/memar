/* For license and copyright information please see the LEGAL file in the code repository */

package pfap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
	pp "org/modules/pos/protocol"
)

// DataModel or pos operator is to supply a particular service.
type DataModel interface {
	PosID() pp.PosUUID
	AccountID() fap.FinancialAccountUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

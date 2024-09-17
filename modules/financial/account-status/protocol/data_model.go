/* For license and copyright information please see the LEGAL file in the code repository */

package fasp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	Status() Status

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

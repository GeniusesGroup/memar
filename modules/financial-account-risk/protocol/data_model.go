/* For license and copyright information please see the LEGAL file in the code repository */

// use in risk assessment
package farap

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
)

// DataModel
// Store user risk to prevent or detect frauds
type DataModel interface {
	AccountID() fap.FinancialAccountUUID
	Score() int64

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

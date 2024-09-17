/* For license and copyright information please see the LEGAL file in the code repository */

package fcsp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fcp "org/modules/financial-card/protocol"
)

// store users bank account to distinguish user balances in desire indexes
type DataModel interface {
	FinancialCardID() fcp.FinancialCardUUID
	CardHexSHA1() CardHexSHA1

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}

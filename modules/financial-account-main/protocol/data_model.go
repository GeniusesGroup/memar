/* For license and copyright information please see the LEGAL file in the code repository */

package famp

import (
	"memar/protocol"

	arp "org/modules/app-request/protocol"
	fap "org/modules/financial-account/protocol"
	fcp "org/modules/financial-currency/protocol"
	up "org/modules/user/protocol"
)

// DataModel indicate the domain record data fields.
type DataModel interface {
	UserID() up.UserUUID
	Currency() fcp.FinancialCurrencyUUID
	AccountID() fap.FinancialAccountUUID

	arp.AuditLogging
	protocol.Storage_Versioned
	protocol.Storage_SaveTime
}
